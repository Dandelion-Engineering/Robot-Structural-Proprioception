# Noisy Healthy-Reference Coefficient Pilot

**Decision: ADVANCE SETTING FOR REFERENCE-RUNG IMPLEMENTATION REVIEW.** This suite-S setting cleared the predeclared development false-alarm and per-fault detection screens across every tested onset alignment and ranked highest on worst-alignment prototype attribution. It remains a pilot choice, not a frozen configuration or headline result.

Development pilot only. Every score below comes from noisy deployable `ObservedRecord` data. The healthy reference and the three fault-shape centroids use calibration sensor seeds; false alarms, detection, and prototype attribution use disjoint held-out seeds. No privileged fault-minus-healthy trace is a detector input, and no config value is frozen.

## Reference and alignment convention tested

- Phase-locked scheduled probe: the one-cycle 0.8 Hz burst resets phase at the declared fault/probe onset.
- The estimator decision is the first global stride-grid decision at or after the probe ends. The healthy reference is conditioned on task/probe setting, W, and that decision lag; it is a calibration model, not a matched counterfactual run.
- Detection uses the dimension-normalized, healthy-standardized Euclidean distance between the live cosine/sine coefficient vector and the healthy mean. The threshold is the 99th-percentile (higher method) leave-one-out healthy calibration score.
- Attribution is nearest fault-shape centroid in the same standardized coefficient space. It is a pilot instrument, not the learned headline attribution model.

## What cleared, and what remains provisional

The selected cell was task 0.500, probe 0.050 N, W=768, stride=16. Suite S's worst per-fault detection rate across the tested alignments was 97.9%, and its prototype attribution was 100.0% in the worst alignment. The matched C1 minimum fault-detection rate was only 0.0%.

Suite S's pooled/mean held-out healthy false-alarm rate was 0.7% and the worst tested alignment was 2.1%, while the minimum per-fault detection rate remained 97.9%. This advances the scheduled-reference convention for estimator-owner review only. The threshold, sensor constants, severities, and W/stride values remain development choices until validation and config freeze.

## Best cell per candidate (suite S)

| Task | Probe | W | Stride | Mean / max false alarm | Min fault detect | Min attribution |
|---:|---:|---:|---:|---:|---:|---:|
| 0.500 | 0.050 N | 768 | 16 | 0.7% / 2.1% | 97.9% | 100.0% |

## Required negative control

W=512 is shorter than one 0.8 Hz period. Under the current estimator contract its synchronous cosine/sine entries remain zero; it is retained in the CSV/JSON as the inert-window negative control rather than silently dropped.

## Boundaries

- This is not the confirmatory C1-vs-S experiment, does not set the Claim-Sheet effect bars, and does not train the matched temporal-attribution or RMA models.
- Reference conditioning assumes a scheduled, phase-reset diagnostic probe. Unscheduled phase drift and probe-band thermal interference remain open tests.
- The current non-load-bearing sensor constants and fixed development severities remain provisional. Optional-contact cases are still blocked on endpoint-contact extraction.
- The advance is only to estimator-owner review and the next pilot increment; it is not a research result or a config freeze.
