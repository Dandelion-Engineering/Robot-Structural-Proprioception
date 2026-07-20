# Noisy Healthy-Reference Coefficient Pilot

**Decision: NO SETTING CLEARS THE DEPLOYABLE PILOT SCREEN.** No suite-S cell simultaneously cleared safety, held-out false alarms, the minimum per-fault detection rate, and the full-cycle feature gate.

Development pilot only. Every score below comes from noisy deployable `ObservedRecord` data. The healthy reference and the three fault-shape centroids use calibration sensor seeds; false alarms, detection, and prototype attribution use disjoint held-out seeds. No privileged fault-minus-healthy trace is a detector input, and no config value is frozen.

## Reference and alignment convention tested

- Phase-locked scheduled probe: the one-cycle 0.8 Hz burst resets phase at the declared fault/probe onset.
- The estimator decision is the first global stride-grid decision at or after the probe ends. The healthy reference is conditioned on task/probe setting, W, and that decision lag; it is a calibration model, not a matched counterfactual run.
- Detection uses the dimension-normalized, healthy-standardized Euclidean distance between the live cosine/sine coefficient vector and the healthy mean. The threshold is the 99th-percentile (higher method) leave-one-out healthy calibration score.
- Attribution is nearest fault-shape centroid in the same standardized coefficient space. It is a pilot instrument, not the learned headline attribution model.
- Reproduction seed: base 1000; calibration uses [1000, 1007] and held-out evaluation uses [1008, 1019].

## What blocked, and what survived

The closest cell was task 0.500, probe 0.050 N, W=640, stride=8. Suite S's worst per-fault detection rate across the tested alignments was 100.0%, and its prototype attribution was 100.0% in the worst alignment. The matched C1 minimum fault-detection rate was only 8.3%.

The block was false alarms: suite S produced a pooled/mean held-out healthy false-alarm rate of 8.3% and a worst-alignment rate of 16.7%, above the 5.0% development screen. With 8 healthy calibration seeds, the nominal 99th-percentile higher-method threshold is the maximum leave-one-out calibration score whenever fewer than 100 values are available. The current sample did not resolve the requested tail. This pilot therefore supports the coefficient/reference signal path but blocks the threshold as not validation-ready. The next threshold choice must use a larger healthy calibration set or a separately predeclared conservative rule; it must not be tuned on these held-out rows.

## Best cell per candidate (suite S)

| Task | Probe | W | Stride | Mean / max false alarm | Min fault detect | Min attribution |
|---:|---:|---:|---:|---:|---:|---:|
| 0.400 | 0.025 N | 640 | 16 | 27.8% / 50.0% | 33.3% | 97.2% |
| 0.400 | 0.050 N | 640 | 4 | 5.6% / 8.3% | 83.3% | 97.2% |
| 0.500 | 0.025 N | 640 | 16 | 2.8% / 8.3% | 50.0% | 100.0% |
| 0.500 | 0.050 N | 640 | 8 | 8.3% / 16.7% | 100.0% | 100.0% |

## Required negative control

W=512 is shorter than one 0.8 Hz period. Under the current estimator contract its synchronous cosine/sine entries remain zero; it is retained in the CSV/JSON as the inert-window negative control rather than silently dropped.

## Boundaries

- This is not the confirmatory C1-vs-S experiment, does not set the Claim-Sheet effect bars, and does not train the matched temporal-attribution or RMA models.
- Reference conditioning assumes a scheduled, phase-reset diagnostic probe. Unscheduled phase drift and probe-band thermal interference remain open tests.
- The current non-load-bearing sensor constants and fixed development severities remain provisional. Optional-contact cases are still blocked on endpoint-contact extraction.
- This BLOCK still settles a usable scheduled-reference convention for owner review, but the threshold must be re-calibrated prospectively before any setting can advance. Nothing here is a config freeze.
