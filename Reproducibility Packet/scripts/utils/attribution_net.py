"""Gate-4 rung 1: the matched learned temporal-attribution head (`TemporalAttributionNet`).

This is Claude's estimator lane (Claim Sheet Slots 5/9; schema §D). It builds the
first rung of Slot 9's **model-capacity ladder** — "a compact recurrent/temporal-
convolutional estimator (~10^4-10^5 parameters)" — as the concrete realization of the
rung `utils.estimator` has carried as *specified, not built* since Session 9.

Where this sits
---------------
`utils.estimator.WindowFeatureExtractor.window_tensor` produces a fixed `[W, D]`
values/valid pair over the whole channel registry for **every** suite. This module
consumes exactly that pair and nothing else, and emits the schema-§D
`EstimatorOutput` contract through the same `DiagnosisEstimator` interface the
interpretable rungs implement. The recovery controller and the evaluation driver
therefore stay agnostic to which rung is installed (Slot 5's matched ablation).

Four design commitments, each pinned by a test in
`tests/test_attribution_net.py`, because each is a way the matched ablation could be
silently broken:

1. **Suite-agnostic by construction.** The network's shape *and its parameter count*
   are identical for C0, C1 and S. The suite enters only through the mask channels:
   a channel a suite lacks arrives as a zero value column and a `False` validity
   column. If the architecture could shrink with the suite, a measured S-over-C1
   advantage would be confounded with model capacity, which is the exact failure
   Slot 5 holds the algorithm fixed to avoid.

2. **Strictly causal, including the normalization.** Every convolution is left-padded
   and right-trimmed, so the feature at time *i* cannot depend on an input at any
   *j > i*. Normalization is per-timestep over the channel axis for the same reason:
   a `GroupNorm`/`BatchNorm` over `(channel, time)` would mix a window's later
   samples into its earlier features and quietly make an "online" estimator
   non-causal. The window front-end is already past-only (schema §D); this keeps the
   *encoder* past-only too, so the same weights are valid in a streaming setting.

3. **An untrained network is not allowed to answer.** A freshly constructed
   `TemporalAttributionEstimator` is *unfitted*: it abstains on every decision,
   splits `p_class` uniformly, reports `location_out = -1`,
   `severity_uncertainty = +inf`, and never flags a detection. Weights become usable
   only through `attach_trained_weights`, which requires a non-empty training
   provenance string. Reading an attribution off randomly initialized weights is
   fabrication, and the honest default is the one that refuses.

4. **Thresholds are validation-owned, not model-owned.** `abstain_threshold` and
   `detect_threshold` default to `None`, which means *always abstain* and *never
   flag*. Gate 5 (calibration/abstention/OOD) sets them from a validation-sized
   healthy calibration set. The same discipline `WindowNoveltyDetector` already
   applies to its own threshold: a pilot may not hand a rung its operating point.

What this module deliberately does **not** contain
--------------------------------------------------
* **No training loop and no fitting.** Building the architecture is Gate 4's first
  step; training runs against generated data are a separate step under their own
  explicit authorization, and Amendment A2 (2026-08-04) authorizes no data
  generation, regeneration, or confirmatory work (A2.9).
* **No calibration.** `severity_uncertainty` must be a *bias-inclusive predictive
  error scale*, never an in-sample residual dispersion (measured Session 24: the
  in-sample scale understates the true predictive error by 5.72x for suite S). The
  network emits a raw log-scale head; turning it into a reported uncertainty is
  Gate 5's job, and until then this module reports `+inf`.
* **No ladder rungs 2 and 3.** Slot 9's rung 2 (larger recurrent-plus-attention) and
  rung 3 (probabilistic/ensemble head) are escalations, taken only when there is
  partial signal worth strengthening or a stated reason a larger model could capture
  one this rung cannot. Building them now would buy capacity the project cannot yet
  use, against the efficiency standard.

Determinism
-----------
Construction is seeded explicitly (`seed=`), so five independent training seeds are
five explicitly named integers rather than whatever global RNG state happens to hold.
Two `TemporalAttributionNet`s built at the same seed have bit-identical parameters
and bit-identical forward outputs on the same input and device.
"""

from __future__ import annotations

import contextlib
import copy
from dataclasses import dataclass

import numpy as np
import torch
from torch import nn

from utils.estimator import (
    DiagnosisEstimator,
    EstimatorOutput,
    HEALTHY_INDEX,
    N_SOURCE_CLASSES,
    WindowFeatureExtractor,
)
from utils.schema_types import N_JOINTS, ObservedRecord, observed_registry_width

# The network reads the registry twice: the value column and its validity column.
# Keeping the mask as an explicit input (rather than imputing) is schema §C [C4] —
# a learned model is never handed a filled value without being told it was filled.
N_INPUT_STREAMS = 2

# `location_out` is a joint index or -1 ("not localized"). The head therefore has one
# logit per joint plus one for the not-localized outcome, and index 0 of the head is
# the not-localized class so a zero-initialized head is honest by default.
NOT_LOCALIZED_INDEX = 0
N_LOCATION_LOGITS = N_JOINTS + 1

# Slot 9's rung-1 parameter band. `TemporalAttributionNet.__init__` refuses a
# configuration outside it rather than letting the ladder drift a rung without anyone
# writing down that it climbed.
RUNG1_MIN_PARAMETERS = 10_000
RUNG1_MAX_PARAMETERS = 100_000

_EPS = 1.0e-12


@contextlib.contextmanager
def deterministic_conv_precision():
    """Run convolutions at full float32 instead of cuDNN's TF32 default.

    **Measured on the project GPU (RTX 5060 Ti, sm_120, torch 2.11.0+cu128), Session
    77**, over four seeds of this architecture on a 768-step window, comparing the CPU
    and CUDA class simplex for the same weights and the same input:

    ```text
    torch.backends.cudnn.allow_tf32 = True   (PyTorch's default)  max |dp| 8.842e-05
    torch.backends.cudnn.allow_tf32 = False                       max |dp| 5.960e-08
    ```

    Eight parts in 10^5 is three orders below Slot 11's 0.05 absolute macro-F1 bar, so
    the default would not have changed a headline. It would have made two things false
    that this project relies on being true: that a persisted result reproduces on
    another machine, and that a paired C1-vs-S difference is a difference in *sensing*
    rather than partly in which device or backend flag each arm happened to run under.
    Turning TF32 off costs nothing measurable at ~4x10^4 parameters.

    The flag is global, so this restores the previous value on exit rather than
    setting it at import time and silently changing the numerics of every other
    convolution in the process. It is deliberately public: the later trainer and the
    evaluation driver must use this same context rather than each re-deciding.
    """

    previous = torch.backends.cudnn.allow_tf32
    torch.backends.cudnn.allow_tf32 = False
    try:
        yield
    finally:
        torch.backends.cudnn.allow_tf32 = previous


@dataclass(frozen=True)
class LadderRung:
    """One rung of the Slot-9 model-capacity ladder, with its escalation condition."""

    name: str
    built: bool
    description: str
    escalate_when: str


# The ladder, recorded here so "which rung are we on" has one answer in the code
# rather than three answers in three documents. Only rung 1 is built.
CAPACITY_LADDER: tuple[LadderRung, ...] = (
    LadderRung(
        name="rung1_compact_temporal_conv",
        built=True,
        description=(
            "Compact causal dilated temporal-convolutional encoder over the [W, D] "
            "window plus its validity mask, with class / unknown / location / severity "
            "heads. ~10^4-10^5 parameters."
        ),
        escalate_when=(
            "Partial signal worth strengthening, or no signal yet where a larger model "
            "could plausibly capture one this rung cannot (Slot 9 (a)/(b))."
        ),
    ),
    LadderRung(
        name="rung2_recurrent_plus_attention",
        built=False,
        description="Larger/deeper recurrent-plus-attention estimator (Slot 9 rung 2).",
        escalate_when="Rung 1's result is partial or capacity-limited, per Slot 9 (a)/(b).",
    ),
    LadderRung(
        name="rung3_probabilistic_ensemble_head",
        built=False,
        description=(
            "Probabilistic/ensemble head (deep ensembles or evidential output) for "
            "calibrated attribution and honest abstention (Slot 9 rung 3)."
        ),
        escalate_when="Calibrated attribution is needed beyond what rung 2 supports.",
    ),
)


class _PerStepChannelNorm(nn.Module):
    """LayerNorm over the channel axis at each timestep — never across time.

    A `GroupNorm` or `BatchNorm1d` on a `[B, C, T]` activation normalizes over the
    time axis and therefore lets a window's later samples influence its earlier
    features. That is invisible in a batched offline forward pass and fatal to the
    causality claim, so the normalization used here is explicitly per-timestep.
    """

    def __init__(self, channels: int) -> None:
        """Normalize `[B, C, T]` activations over `C` independently at each `T`."""

        super().__init__()
        self.norm = nn.LayerNorm(channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return the per-timestep channel-normalized activation, same shape as `x`."""

        return self.norm(x.transpose(1, 2)).transpose(1, 2)


class _CausalDilatedBlock(nn.Module):
    """One residual block: causal dilated conv -> per-step norm -> GELU -> pointwise.

    The dilated convolution is left-padded by `(kernel_size - 1) * dilation` and the
    right overhang is trimmed, which is what makes it causal: output index `i` reads
    input indices `i - (kernel_size - 1) * dilation .. i` and nothing later.
    """

    def __init__(self, channels: int, kernel_size: int, dilation: int) -> None:
        """Build a residual causal block at the given channel count and dilation."""

        super().__init__()
        if kernel_size < 1:
            raise ValueError("kernel_size must be >= 1")
        if dilation < 1:
            raise ValueError("dilation must be >= 1")
        self.left_pad = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(channels, channels, kernel_size, dilation=dilation)
        self.norm = _PerStepChannelNorm(channels)
        self.act = nn.GELU()
        self.pointwise = nn.Conv1d(channels, channels, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return `x + f(x)` for `[B, C, T]` input, preserving `T` and causality."""

        padded = nn.functional.pad(x, (self.left_pad, 0))
        h = self.conv(padded)
        h = self.act(self.norm(h))
        return x + self.pointwise(h)


@dataclass(frozen=True)
class AttributionHeads:
    """The raw head outputs of one forward pass, before any calibration.

    `class_logits` are the four known source classes in
    `utils.estimator.SOURCE_CLASS_ORDER`; `unknown_logit` is a single higher-is-more-
    out-of-distribution score; `location_logits` index `[not-localized, joint 0, ...]`;
    `severity_value` and `severity_log_scale` are the point estimate and the raw
    predictive log-scale. None of these are calibrated — Gate 5 owns that step.
    """

    class_logits: torch.Tensor
    unknown_logit: torch.Tensor
    location_logits: torch.Tensor
    severity_value: torch.Tensor
    severity_log_scale: torch.Tensor


class TemporalAttributionNet(nn.Module):
    """Compact causal dilated temporal-convolutional attribution network (rung 1).

    Consumes the `[W, D]` values/valid pair from
    `utils.estimator.WindowFeatureExtractor.window_tensor`, stacked as `2 * D` input
    streams, and emits class / unknown / location / severity heads from the encoder
    feature at the window's **final** timestep — the only timestep whose feature is a
    function of the whole window under a causal encoder.

    Shape and parameter count depend on `registry_width`, never on the sensor suite.
    """

    def __init__(
        self,
        *,
        registry_width: int | None = None,
        channels: int = 32,
        n_blocks: int = 9,
        kernel_size: int = 3,
        seed: int = 0,
        enforce_rung1_band: bool = True,
    ) -> None:
        """Build the rung-1 encoder and heads deterministically from `seed`.

        `registry_width` defaults to the schema's fixed observed-registry width.
        `n_blocks` dilations double from 1, so the receptive field is
        `1 + 2 * (2 ** n_blocks - 1)` samples; the default 9 blocks reach 1023
        samples, covering the proposed `W = 768` window whole.
        `enforce_rung1_band` refuses a configuration whose parameter count leaves
        Slot 9's rung-1 band, so climbing the ladder cannot happen by edit.
        """

        super().__init__()
        if registry_width is None:
            registry_width = observed_registry_width()
        if registry_width <= 0:
            raise ValueError("registry_width must be positive")
        if channels <= 0:
            raise ValueError("channels must be positive")
        if n_blocks <= 0:
            raise ValueError("n_blocks must be positive")
        if kernel_size < 1:
            raise ValueError("kernel_size must be >= 1")
        if not isinstance(seed, (int, np.integer)) or int(seed) < 0:
            raise ValueError("seed must be a non-negative integer")

        self.registry_width = int(registry_width)
        self.channels = int(channels)
        self.n_blocks = int(n_blocks)
        self.kernel_size = int(kernel_size)
        self.seed = int(seed)

        # Fork the global RNG rather than consuming it, so constructing a network
        # never perturbs anything else's draw sequence and two nets at the same seed
        # are bit-identical however their constructions were interleaved.
        with torch.random.fork_rng(devices=[], enabled=True):
            torch.random.manual_seed(int(seed))
            self.input_proj = nn.Conv1d(N_INPUT_STREAMS * self.registry_width, self.channels, 1)
            self.blocks = nn.ModuleList(
                [
                    _CausalDilatedBlock(self.channels, self.kernel_size, 2**index)
                    for index in range(self.n_blocks)
                ]
            )
            self.encoder_norm = _PerStepChannelNorm(self.channels)
            self.class_head = nn.Linear(self.channels, N_SOURCE_CLASSES)
            self.unknown_head = nn.Linear(self.channels, 1)
            self.location_head = nn.Linear(self.channels, N_LOCATION_LOGITS)
            self.severity_head = nn.Linear(self.channels, 2)

        if enforce_rung1_band:
            total = self.n_parameters
            if not RUNG1_MIN_PARAMETERS <= total <= RUNG1_MAX_PARAMETERS:
                raise ValueError(
                    f"configuration has {total} parameters, outside Slot 9's rung-1 band "
                    f"[{RUNG1_MIN_PARAMETERS}, {RUNG1_MAX_PARAMETERS}]; escalating the "
                    "capacity ladder is a recorded decision, not a constructor argument"
                )

    @property
    def n_parameters(self) -> int:
        """Total number of trainable parameters."""

        return sum(int(p.numel()) for p in self.parameters() if p.requires_grad)

    @property
    def receptive_field(self) -> int:
        """Number of past samples the final-timestep feature can depend on."""

        return 1 + (self.kernel_size - 1) * (2**self.n_blocks - 1)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """Return the `[B, C, T]` causal encoder features for `[B, 2D, T]` input."""

        if x.dim() != 3:
            raise ValueError(f"input must be [B, 2D, T], got {tuple(x.shape)}")
        expected = N_INPUT_STREAMS * self.registry_width
        if x.shape[1] != expected:
            raise ValueError(
                f"input must carry {expected} streams (values then mask), got {x.shape[1]}"
            )
        h = self.input_proj(x)
        for block in self.blocks:
            h = block(h)
        return self.encoder_norm(h)

    def forward(self, x: torch.Tensor) -> AttributionHeads:
        """Return the raw heads read off the final timestep of the causal encoding."""

        features = self.encode(x)[:, :, -1]
        severity = self.severity_head(features)
        return AttributionHeads(
            class_logits=self.class_head(features),
            unknown_logit=self.unknown_head(features).squeeze(-1),
            location_logits=self.location_head(features),
            severity_value=severity[:, 0],
            severity_log_scale=severity[:, 1],
        )


def window_to_input(
    values: np.ndarray, valid: np.ndarray, *, device: torch.device | str = "cpu"
) -> torch.Tensor:
    """Stack a `window_tensor` pair into the `[1, 2D, W]` batch the network reads.

    `values` and `valid` are the `[W, D]` arrays returned by
    `WindowFeatureExtractor.window_tensor`. The mask is carried as an explicit float
    stream so a filled entry is always accompanied by the fact that it was filled.
    Fails loudly on shape disagreement rather than broadcasting a wrong window into a
    plausible-looking tensor.
    """

    values_array = np.asarray(values, dtype=float)
    valid_array = np.asarray(valid)
    if values_array.ndim != 2:
        raise ValueError(f"values must be [W, D], got {values_array.shape}")
    if valid_array.shape != values_array.shape:
        raise ValueError(
            f"values/valid must share shape, got {values_array.shape}/{valid_array.shape}"
        )
    if not np.all(np.isfinite(values_array)):
        raise ValueError("window values must be finite (window_tensor fills invalid entries)")
    stacked = np.concatenate(
        [values_array.T, valid_array.T.astype(float)], axis=0
    )  # [2D, W]
    return torch.as_tensor(stacked, dtype=torch.float32, device=device).unsqueeze(0)


class TemporalAttributionEstimator(DiagnosisEstimator):
    """The §D estimator wrapping `TemporalAttributionNet` (Gate-4 rung 1).

    Until `attach_trained_weights` has been called this estimator is **unfitted** and
    answers honestly: uniform `p_class`, `abstain_decision=True`, `location_out=-1`,
    `severity_uncertainty=+inf`, no detection. Randomly initialized weights carry no
    information about a fault, and reporting an argmax over them would be fabrication.

    Once fitted, the operating points still belong to validation: with
    `abstain_threshold=None` the estimator reports the network's `p_class` but
    continues to abstain, and with `detect_threshold=None` it never flags a detection.
    Gate 5 supplies both from a healthy calibration set.
    """

    def __init__(
        self,
        net: TemporalAttributionNet | None = None,
        extractor: WindowFeatureExtractor | None = None,
        *,
        abstain_threshold: float | None = None,
        detect_threshold: float | None = None,
        device: torch.device | str = "cpu",
    ) -> None:
        """Wrap a *copy* of a network and a window front-end; thresholds default honest.

        The network is deep-copied rather than adopted. `nn.Module.to` relocates in
        place, so adopting the caller's module would move it — and two estimators
        built from one network on two devices would alias each other, which is exactly
        the matched C1-vs-S and multi-seed usage this rung exists for. Owning a copy
        also means `attach_trained_weights` cannot reach back into the caller's object.
        """

        if abstain_threshold is not None and not 0.0 < float(abstain_threshold) <= 1.0:
            raise ValueError("abstain_threshold must lie in (0, 1] when supplied")
        if detect_threshold is not None and not 0.0 < float(detect_threshold) <= 1.0:
            raise ValueError("detect_threshold must lie in (0, 1] when supplied")
        self.device = torch.device(device)
        source = net if net is not None else TemporalAttributionNet()
        self.net = copy.deepcopy(source).to(self.device)
        self.net.eval()
        self.extractor = extractor if extractor is not None else WindowFeatureExtractor()
        if self.net.registry_width != self.extractor.registry_width:
            raise ValueError(
                f"net registry_width {self.net.registry_width} does not match extractor "
                f"{self.extractor.registry_width}"
            )
        self.abstain_threshold = None if abstain_threshold is None else float(abstain_threshold)
        self.detect_threshold = None if detect_threshold is None else float(detect_threshold)
        self.training_provenance: str | None = None
        self._detection_time_s = float("nan")

    @property
    def fitted(self) -> bool:
        """Whether trained weights with a recorded provenance have been attached."""

        return self.training_provenance is not None

    def attach_trained_weights(
        self, state_dict: dict[str, torch.Tensor], *, training_provenance: str
    ) -> None:
        """Load trained weights transactionally and record where they came from.

        `training_provenance` must be a non-empty description a reader can trace — the
        training run's identity, its data root, its seed. It is required rather than
        optional because an estimator that cannot say where its weights came from
        cannot be audited, and the alternative default (trusting whatever tensor
        arrived) is exactly the silent failure the standards forbid.

        Loading happens on a candidate copy. PyTorch may copy every compatible tensor
        before reporting a missing or mismatched key, so loading directly into the live
        network could leave partially replaced weights carrying the previous run's
        provenance after an exception. The candidate is installed only after the whole
        state dictionary and device transfer succeed.

        The install writes the validated tensors *into* `self.net` rather than rebinding
        the attribute to the candidate, so `self.net` is the same object before and after
        a call. A caller that captured `estimator.net` earlier — an optimizer built over
        `estimator.net.parameters()` before a checkpoint was resumed is the case this
        rung will meet — would otherwise be left driving an orphaned module while the
        estimator answered from a different one, with no error and a falling loss. The
        second load cannot itself fail partway: `candidate` is a deep copy of `self.net`
        and a strict load neither adds keys nor changes shapes, so the two state
        dictionaries agree by construction.
        """

        if not isinstance(training_provenance, str) or not training_provenance.strip():
            raise ValueError("training_provenance must be a non-empty string")
        candidate = copy.deepcopy(self.net)
        candidate.load_state_dict(state_dict)
        candidate.to(self.device)
        candidate.eval()
        self.net.load_state_dict(candidate.state_dict())
        self.net.to(self.device)
        self.net.eval()
        self.training_provenance = training_provenance.strip()

    def reset(self) -> None:
        """Clear per-rollout state (the first-detection latch) before a new run."""

        self._detection_time_s = float("nan")

    def _unfitted_output(self, step_index: int, decision_time_s: float) -> EstimatorOutput:
        """Return the honest no-information output of an unfitted or empty decision."""

        return EstimatorOutput(
            step=int(step_index),
            decision_time_s=float(decision_time_s),
            p_class=np.full(N_SOURCE_CLASSES, 1.0 / N_SOURCE_CLASSES, dtype=float),
            unknown_score=1.0,
            abstain_decision=True,
            location_out=-1,
            severity_out=0.0,
            severity_uncertainty=float("inf"),
            detection_time_s=float("nan"),
        )

    def update(
        self, step_index: int, decision_time_s: float, window: ObservedRecord | None
    ) -> EstimatorOutput:
        """Consume one past-only window and return a validated §D output."""

        if window is None or not self.fitted:
            output = self._unfitted_output(step_index, decision_time_s)
            output.validate()
            return output

        values, valid = self.extractor.window_tensor(window)
        batch = window_to_input(values, valid, device=self.device)
        with torch.no_grad(), deterministic_conv_precision():
            heads = self.net(batch)
            probs = torch.softmax(heads.class_logits, dim=-1)[0].cpu().numpy().astype(float)
            unknown = float(torch.sigmoid(heads.unknown_logit)[0].item())
            location_index = int(torch.argmax(heads.location_logits, dim=-1)[0].item())
            severity_value = float(heads.severity_value[0].item())
            severity_scale = float(torch.exp(heads.severity_log_scale)[0].item())

        # Renormalize defensively: softmax already sums to 1, but float32 -> float64
        # can leave the §D simplex check a few ULP short, and a validated contract
        # should not depend on which dtype the head happened to run in.
        probs = probs / max(float(probs.sum()), _EPS)

        healthy_probability = float(probs[HEALTHY_INDEX])
        if self.detect_threshold is not None and not np.isfinite(self._detection_time_s):
            if healthy_probability < self.detect_threshold:
                self._detection_time_s = float(decision_time_s)

        if self.abstain_threshold is None:
            abstain = True
        else:
            abstain = bool(float(probs.max()) < self.abstain_threshold)

        location_out = (
            -1 if location_index == NOT_LOCALIZED_INDEX else location_index - 1
        )

        output = EstimatorOutput(
            step=int(step_index),
            decision_time_s=float(decision_time_s),
            p_class=probs,
            unknown_score=unknown,
            abstain_decision=abstain,
            location_out=location_out,
            # Gate 5 owns the calibrated, bias-inclusive predictive scale. The raw head
            # scale is an in-model quantity and reporting it as `severity_uncertainty`
            # would repeat the Session-24 error (in-sample dispersion understates the
            # true predictive error by 5.72x for suite S), so it stays +inf here.
            severity_out=severity_value,
            severity_uncertainty=float("inf"),
            detection_time_s=self._detection_time_s,
        )
        output.validate()
        return output

    def raw_severity_scale(self, window: ObservedRecord) -> float:
        """Return the network's uncalibrated severity scale for this window.

        Exposed separately, and named `raw_`, so Gate 5 can calibrate it without any
        code path being tempted to report it as `severity_uncertainty` first.
        """

        if not self.fitted:
            raise ValueError("raw_severity_scale requires attached trained weights")
        values, valid = self.extractor.window_tensor(window)
        batch = window_to_input(values, valid, device=self.device)
        with torch.no_grad(), deterministic_conv_precision():
            heads = self.net(batch)
            return float(torch.exp(heads.severity_log_scale)[0].item())
