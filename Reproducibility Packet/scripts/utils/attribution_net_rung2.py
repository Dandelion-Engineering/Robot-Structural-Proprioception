"""Gate-4 rung 2: the recurrent-plus-attention attribution network.

This is the architecture half of `protocol/rung2-escalation-v0.1.md`, which both
agents approved at Git blob `404c9f1fc1b0112e5ed8164853b261e97d510662`. That
approval authorizes **this module and its tests and nothing else** — no executable,
no plan, no fit, no checkpoint, no analyzer, no capacity choice and no threshold.

Where this sits
---------------
Slot 9's model-capacity ladder has three rungs. Rung 1 (`attribution_net.
TemporalAttributionNet`, 39,594 parameters) is built, fitted and closed. This module
is the smallest thing that constitutes climbing to rung 2: **one named
recurrent-plus-attention architecture**, exactly capacity-matched between suites C1
and S, consuming exactly the `[B, 2D, T]` tensor `attribution_net.window_to_input`
produces and returning exactly the approved `AttributionHeads` dataclass. It is
deliberately not a within-rung sweep — design §4.6 gives the measured reason.

```text
input [B, 36, T]
  -> input_proj   Conv1d(2D -> C, kernel 1)
  -> stem         4 residual causal dilated blocks, dilations 1, 2, 4, 8
  -> stem_norm    per-timestep channel LayerNorm
  -> gru          nn.GRU(C -> H, 2 layers, unidirectional)
  -> attention    one query from the FINAL GRU output, keys/values from every step
  -> fuse         Linear(2H -> H) over [final, context] -> GELU
  -> heads        class(4) / unknown(1) / location(3) / severity(2)
```

What this module deliberately does **not** contain
--------------------------------------------------
* **No training loop, no fitting, no persistence.** The fitting loop, its factory
  seam and the equivalence gate that proves the copied loop equals the approved one
  live in the separate `rung2_escalation.py` executable, which is step 3 of the
  design's sequencing and is not authorized by this module's existence.
* **No enforcement bypass.** `RecurrentAttentionAttributionNet.__init__` takes no
  argument that can disable the band check (design invariant R5), and the tests get
  their speed from short windows rather than from a de-banded network.
* **No re-definition of the causal padding rule.** `_CausalDilatedBlock` and
  `_PerStepChannelNorm` are imported from the approved rung-1 module. Two definitions
  of one rule with nothing comparing them is finding AP's defect class, and this
  project has paid for it before. The import crosses a module boundary to reach two
  underscore-private names inside the same `utils` package; that is design decision
  D1, ruled and accepted, and a test pins that this module defines no causal block of
  its own.

Four disclosed limitations, each pinned by a test rather than repaired
---------------------------------------------------------------------
All four have the same cause, which is design decision D4: `attribution_net.py` is
one of the eight entries of `dev_fit_trainer.training_code_identity()` and
`capacity_sweep.py` is an entry of `sweep_code_identity()`. Editing either changes a
**recorded identity**, and the entry-by-entry check would then refuse every future
run that reads the approved rung-1 anchors. A one-word edit to a comment-level field
would cost the project its ability to re-verify its own fitted record.

1. `attribution_net.CAPACITY_LADDER`'s rung-2 entry still reads `built=False`, and
   stays that way. The ladder tuple is documentation inside an identity-bearing file.
2. `TemporalAttributionEstimator`'s type annotation says `TemporalAttributionNet`
   while its behaviour is rung-agnostic — measured, not assumed: it accepts a rung-2
   network, produces a validating unfitted output and preserves `self.net`'s identity.
3. `capacity_sweep.score_arm` carries the same narrower annotation and the same
   rung-agnostic runtime contract.
4. This class exposes `stem_receptive_field` and **deliberately no**
   `receptive_field`. Rung 1's property names the number of past samples its final
   feature can depend on; here the GRU and the attention pool each span the whole
   window, so a `receptive_field` of 31 would be a false name for a true number.

Determinism and the RNG order
-----------------------------
Construction inherits rung 1's RNG isolation and **the order is part of the
specification**: the fork is entered first and `torch.random.manual_seed(seed)` is
called *inside* it, matching `attribution_net.py:317-318`. Seeding before the fork
builds the identical 219,018 parameters and still leaves the caller's global CPU RNG
state mutated — so the parameter count, the invariant a reader checks first, cannot
tell the two orders apart. The test that can is the one asserting the caller's CPU
RNG state is unchanged across a construction (design invariant R13).
"""

from __future__ import annotations

import math

import numpy as np
import torch
from torch import nn

from utils.attribution_net import (
    AttributionHeads,
    N_INPUT_STREAMS,
    N_LOCATION_LOGITS,
    RUNG1_MAX_PARAMETERS,
    _CausalDilatedBlock,
    _PerStepChannelNorm,
)
from utils.estimator import N_SOURCE_CLASSES
from utils.schema_types import observed_registry_width

# The rung's name, used verbatim by `attribution_net.CAPACITY_LADDER`'s rung-2 entry
# and by every artifact the executable will later persist.
RUNG2_NAME = "rung2_recurrent_plus_attention"

# Slot 9 declares no parameter band for rung 2; this one is design decision D2. The
# lower bound is **derived from the approved rung-1 constant, never retyped**, so the
# two size bands are contiguous and disjoint by construction and no parameter count
# has both size-band answers available. Note what this does and does not do: an
# admitted rung-2 instance cannot lie in rung 1's size band, but a parameter count
# does not by itself identify the architecture rung. An 82,778-parameter
# recurrent-plus-attention candidate is an *undersized rung-2 candidate*, not a
# rung-1 network.
RUNG2_MIN_PARAMETERS = RUNG1_MAX_PARAMETERS + 1
RUNG2_MAX_PARAMETERS = 1_000_000

# The selected configuration, and the only one the approved design proposes. The
# selection rule was declared before the numbers were used for anything: the smallest
# measured grid point that is inside the band with margin, carries more than one
# recurrent layer so "deeper" is true of the recurrent path rather than only of the
# parameter count, and carries multi-head attention.
RUNG2_CHANNELS = 64
RUNG2_STEM_BLOCKS = 4
RUNG2_HIDDEN_SIZE = 96
RUNG2_GRU_LAYERS = 2
RUNG2_ATTENTION_HEADS = 4
RUNG2_KERNEL_SIZE = 3

# The declared parameter count of that configuration. The tests recompute this from a
# constructed network rather than trusting the constant, and the executable will
# refuse a network whose count does not equal it (design invariant R4). It is a
# ledger entry, not an input: nothing in this module sizes anything from it.
RUNG2_DECLARED_PARAMETERS = 219_018


class RecurrentAttentionAttributionNet(nn.Module):
    """Rung 2: causal conv stem -> unidirectional GRU -> single-query attention.

    Consumes the `[B, 2D, T]` values-and-mask tensor rung 1 consumes, and emits the
    same `AttributionHeads`. Shape and parameter count depend on `registry_width`,
    never on the sensor suite: a channel a suite lacks arrives as a zero value column
    and a `False` validity column, so "exactly capacity-matched between C1 and S" is a
    property of the construction rather than a promise.

    The recurrent layer is unidirectional because a bidirectional one would read the
    window's future into its past and destroy rung 1's design commitment 2 — the same
    weights must remain valid in a streaming setting. The attention is a **single
    query built from the final GRU output**, not causal self-attention at every
    timestep: only the final step is read by the heads, so per-timestep self-attention
    would compute `T` times more attention than the decision uses, at `O(T^2)` cost on
    CPU for no measured benefit. What that preserves is the property that matters —
    the pooled read at time `T` is a function of inputs at times `<= T` only.

    The three attention projections are written out rather than delegated to
    `nn.MultiheadAttention`, which would silently add an `H -> H` output projection
    and build 228,330 parameters instead of 219,018. Both counts lie inside the
    declared band, so the band check cannot tell them apart; only the exact-count
    assertion can.
    """

    def __init__(
        self,
        *,
        registry_width: int | None = None,
        channels: int = RUNG2_CHANNELS,
        n_stem_blocks: int = RUNG2_STEM_BLOCKS,
        hidden_size: int = RUNG2_HIDDEN_SIZE,
        n_gru_layers: int = RUNG2_GRU_LAYERS,
        n_heads: int = RUNG2_ATTENTION_HEADS,
        kernel_size: int = RUNG2_KERNEL_SIZE,
        seed: int = 0,
    ) -> None:
        """Build the rung-2 encoder and heads deterministically from `seed`.

        Inputs: the registry width (defaulting to the schema's fixed observed width),
        the architecture's six size parameters, and the construction seed. Output: a
        constructed module whose parameter count has been checked against the rung-2
        band. Purpose: design section 4.2's named architecture, with the band check as
        the unconditional last statement so climbing the ladder cannot happen by edit.

        There is deliberately no argument that disables the band check. Where a test
        needs something that is not a rung-2 network it uses a stub; where it needs
        speed it uses a short window.
        """

        super().__init__()
        if registry_width is None:
            registry_width = observed_registry_width()
        if registry_width <= 0:
            raise ValueError("registry_width must be positive")
        if channels <= 0:
            raise ValueError("channels must be positive")
        if n_stem_blocks <= 0:
            raise ValueError("n_stem_blocks must be positive")
        if hidden_size <= 0:
            raise ValueError("hidden_size must be positive")
        if n_gru_layers <= 0:
            raise ValueError("n_gru_layers must be positive")
        if n_heads <= 0:
            raise ValueError("n_heads must be positive")
        if hidden_size % n_heads != 0:
            raise ValueError(
                f"hidden_size {hidden_size} is not divisible by n_heads {n_heads}; "
                "each attention head must carry an equal share of the hidden width"
            )
        if kernel_size < 1:
            raise ValueError("kernel_size must be >= 1")
        if not isinstance(seed, (int, np.integer)) or int(seed) < 0:
            raise ValueError("seed must be a non-negative integer")

        self.registry_width = int(registry_width)
        self.channels = int(channels)
        self.n_stem_blocks = int(n_stem_blocks)
        self.hidden_size = int(hidden_size)
        self.n_gru_layers = int(n_gru_layers)
        self.n_heads = int(n_heads)
        self.kernel_size = int(kernel_size)
        self.seed = int(seed)
        self.rung = RUNG2_NAME

        # Enter the fork FIRST and seed INSIDE it, exactly as rung 1 does. Seeding
        # before the fork constructs the identical parameters while mutating the
        # caller's global CPU RNG state, and no parameter-count check can see the
        # difference.
        with torch.random.fork_rng(devices=[], enabled=True):
            torch.random.manual_seed(int(seed))
            self.input_proj = nn.Conv1d(
                N_INPUT_STREAMS * self.registry_width, self.channels, 1
            )
            self.stem = nn.ModuleList(
                [
                    _CausalDilatedBlock(self.channels, self.kernel_size, 2**index)
                    for index in range(self.n_stem_blocks)
                ]
            )
            self.stem_norm = _PerStepChannelNorm(self.channels)
            self.gru = nn.GRU(
                input_size=self.channels,
                hidden_size=self.hidden_size,
                num_layers=self.n_gru_layers,
                bias=True,
                batch_first=True,
                dropout=0.0,
                bidirectional=False,
            )
            self.q_proj = nn.Linear(self.hidden_size, self.hidden_size)
            self.k_proj = nn.Linear(self.hidden_size, self.hidden_size)
            self.v_proj = nn.Linear(self.hidden_size, self.hidden_size)
            self.fuse = nn.Linear(2 * self.hidden_size, self.hidden_size)
            self.fuse_act = nn.GELU()
            self.class_head = nn.Linear(self.hidden_size, N_SOURCE_CLASSES)
            self.unknown_head = nn.Linear(self.hidden_size, 1)
            self.location_head = nn.Linear(self.hidden_size, N_LOCATION_LOGITS)
            self.severity_head = nn.Linear(self.hidden_size, 2)

        total = self.n_parameters
        if not RUNG2_MIN_PARAMETERS <= total <= RUNG2_MAX_PARAMETERS:
            raise ValueError(
                f"configuration has {total} parameters, outside the rung-2 band "
                f"[{RUNG2_MIN_PARAMETERS}, {RUNG2_MAX_PARAMETERS}]; the rung a network "
                "belongs to is a recorded decision, not a constructor argument"
            )

    @property
    def n_parameters(self) -> int:
        """Total number of trainable parameters."""

        return sum(int(p.numel()) for p in self.parameters() if p.requires_grad)

    @property
    def head_dim(self) -> int:
        """Hidden width carried by each attention head."""

        return self.hidden_size // self.n_heads

    @property
    def stem_receptive_field(self) -> int:
        """Past samples the **stem's** feature at one timestep can depend on.

        This is a property of the convolutional stem alone. It is deliberately not
        called `receptive_field`: the GRU and the attention pool each span the whole
        window, so the pooled read the heads consume depends on every earlier sample
        of the window regardless of this number.
        """

        return 1 + (self.kernel_size - 1) * (2**self.n_stem_blocks - 1)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """Return the `[B, T, H]` per-timestep recurrent features for `[B, 2D, T]`.

        Inputs: the stacked values-and-mask tensor. Output: the GRU's output at every
        timestep. Purpose: the causal sequence representation the pooled read is built
        from. Every returned step is a function of input steps at or before it — the
        stem is left-padded and right-trimmed and the GRU is unidirectional — which is
        measured by perturbation in the tests rather than asserted from the diagram.
        """

        if x.dim() != 3:
            raise ValueError(f"input must be [B, 2D, T], got {tuple(x.shape)}")
        expected = N_INPUT_STREAMS * self.registry_width
        if x.shape[1] != expected:
            raise ValueError(
                f"input must carry {expected} streams (values then mask), got {x.shape[1]}"
            )
        h = self.input_proj(x)
        for block in self.stem:
            h = block(h)
        h = self.stem_norm(h)
        sequence, _ = self.gru(h.transpose(1, 2))
        return sequence

    def attend(self, sequence: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Return the `[B, H]` attention context and its `[B, n_heads, T]` weights.

        Inputs: the `[B, T, H]` sequence from `encode`. Outputs: the concatenated
        per-head context vectors, and the attention weights that produced them.
        Purpose: the single-query multi-head pool of design section 4.2 — one query
        built from the final step, keys and values from every step, scores divided by
        `sqrt(H / n_heads)`, softmax over the time axis, no output projection and no
        dropout.

        The weights are returned rather than discarded so a test can measure that the
        pool actually reads the window instead of inferring it from the code.
        """

        if sequence.dim() != 3:
            raise ValueError(f"sequence must be [B, T, H], got {tuple(sequence.shape)}")
        if sequence.shape[2] != self.hidden_size:
            raise ValueError(
                f"sequence must carry {self.hidden_size} hidden units, got {sequence.shape[2]}"
            )
        batch, steps, hidden = sequence.shape
        head_dim = self.head_dim
        final = sequence[:, -1, :]
        query = self.q_proj(final).view(batch, self.n_heads, 1, head_dim)
        keys = self.k_proj(sequence).view(batch, steps, self.n_heads, head_dim).transpose(1, 2)
        values = self.v_proj(sequence).view(batch, steps, self.n_heads, head_dim).transpose(1, 2)
        scores = torch.matmul(query, keys.transpose(-2, -1)) / math.sqrt(head_dim)
        weights = torch.softmax(scores, dim=-1)
        context = torch.matmul(weights, values).reshape(batch, hidden)
        return context, weights.reshape(batch, self.n_heads, steps)

    def pool(self, sequence: torch.Tensor) -> torch.Tensor:
        """Return the `[B, H]` fused representation the heads are read from.

        Inputs: the `[B, T, H]` sequence from `encode`. Output: the GELU of the one
        fusion projection applied to the final recurrent state concatenated with the
        attention context. Purpose: the single decision vector, so that the fusion has
        one definition and `forward` cannot grow a second one.
        """

        context, _ = self.attend(sequence)
        final = sequence[:, -1, :]
        return self.fuse_act(self.fuse(torch.cat([final, context], dim=-1)))

    def forward(self, x: torch.Tensor) -> AttributionHeads:
        """Return the raw heads read off the pooled representation of the window."""

        pooled = self.pool(self.encode(x))
        severity = self.severity_head(pooled)
        return AttributionHeads(
            class_logits=self.class_head(pooled),
            unknown_logit=self.unknown_head(pooled).squeeze(-1),
            location_logits=self.location_head(pooled),
            severity_value=severity[:, 0],
            severity_log_scale=severity[:, 1],
        )
