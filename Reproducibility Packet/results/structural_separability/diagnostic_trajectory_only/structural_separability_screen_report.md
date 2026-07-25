# Development structural separability screen

- Generated: 2026-07-25T02:34:42Z
- Dataset root: `C:\Users\cresp\Documents\Dandelion Engineering\Robot Structural Proprioception\data\gate3-base-dev-pilot-val-c1-s`
- Config hash: `dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`
- Split screened: `dev` (the script refuses any other split)
- Trajectory filter: `diagnostic`
- Window W = 768 steps, stride 64, [28] post-onset windows per run
- Context cells (folds): 4; runs per contrast arm: 4

Every contrast is context-matched: the healthy run and the fault run in a
fold share trajectory, payload, environment and contact profile, and differ
only in the fault and the sensor seed. Folds hold out a whole cell.

## Run-level AUROC (held-out, leave-one-cell-out)

| contrast | suite | interpretable rung | learned probe (best over C grid) | learned permutation p |
|---|---|---|---|---|
| structure_rem_ei_0.75 | C1 | 0.375 | 0.000 | 1.000 |
| structure_rem_ei_0.75 | S | 0.500 | 0.000 | 1.000 |
| structure_rem_ei_0.50 | C1 | 0.375 | 0.375 | not run |
| structure_rem_ei_0.50 | S | 0.625 | 0.500 | not run |
| actuator_rem_gain_0.50 | C1 | 0.875 | 0.875 | not run |
| actuator_rem_gain_0.50 | S | 0.875 | 0.750 | not run |

## Paired per-cell sign tests (exact, two-sided)

| contrast | suite | rung | cells with fault > healthy | p |
|---|---|---|---|---|
| structure_rem_ei_0.75 | C1 | interpretable | 1/4 | 0.6250 |
| structure_rem_ei_0.75 | C1 | learned | 0/4 | 0.1250 |
| structure_rem_ei_0.75 | S | interpretable | 2/4 | 1.0000 |
| structure_rem_ei_0.75 | S | learned | 0/4 | 0.1250 |
| structure_rem_ei_0.50 | C1 | interpretable | 1/4 | 0.6250 |
| structure_rem_ei_0.50 | C1 | learned | 2/4 | 1.0000 |
| structure_rem_ei_0.50 | S | interpretable | 3/4 | 0.6250 |
| structure_rem_ei_0.50 | S | learned | 2/4 | 1.0000 |
| actuator_rem_gain_0.50 | C1 | interpretable | 4/4 | 0.1250 |
| actuator_rem_gain_0.50 | C1 | learned | 3/4 | 0.6250 |
| actuator_rem_gain_0.50 | S | interpretable | 4/4 | 0.1250 |
| actuator_rem_gain_0.50 | S | learned | 3/4 | 0.6250 |

## Interpretable rung score scale

| contrast | suite | healthy mean | fault mean | median paired ratio |
|---|---|---|---|---|
| structure_rem_ei_0.75 | C1 | 1.0907 | 1.0505 | 0.979 |
| structure_rem_ei_0.75 | S | 1.0827 | 1.0555 | 0.992 |
| structure_rem_ei_0.50 | C1 | 1.0907 | 1.0599 | 0.972 |
| structure_rem_ei_0.50 | S | 1.0827 | 1.1287 | 1.045 |
| actuator_rem_gain_0.50 | C1 | 1.0907 | 1.7864 | 1.626 |
| actuator_rem_gain_0.50 | S | 1.0827 | 1.6729 | 1.539 |

## Per-channel paired attribution (suite S, all 18 registry columns)

Columns whose paired sign test clears p <= 0.05 are listed; the exact 4-cell floor is p = 0.1250. `S-excl` marks the four gauge columns S alone carries.

**No column can reach p <= 0.05 at 4 paired cells.** The exact two-sided sign test bottoms out at 0.1250 here, so an empty table below is forced by the cell count and is not evidence that the columns carry no effect. Read the pooled-trajectory screen for the attribution question.

| contrast | column | S-excl | median rel. change | effect / healthy spread | sign p |
|---|---|---|---|---|---|
| structure_rem_ei_0.75 | *(no column reaches p <= 0.05)* | | | | |
| structure_rem_ei_0.50 | *(no column reaches p <= 0.05)* | | | | |
| actuator_rem_gain_0.50 | *(no column reaches p <= 0.05)* | | | | |

Largest S-exclusive gauge effect per contrast, whether or not significant:

| contrast | best gauge column | effect / healthy spread | sign p |
|---|---|---|---|
| structure_rem_ei_0.75 | `gauge_obs[1]` | 0.174 | 1.0000 |
| structure_rem_ei_0.50 | `gauge_obs[1]` | 0.122 | 1.0000 |
| actuator_rem_gain_0.50 | `gauge_obs[2]` | 0.120 | 1.0000 |

## Reading this screen

The learned AUROC is a maximum over a regularisation grid and is therefore
an optimistic bound on what this probe class can do at this sample size.
The permutation null applies the same maximisation, so the selection is
inside the null and the p-value remains interpretable. A positive control
(actuator_rem_gain_0.50) is included so an all-null table can be told apart
from a broken pipeline.
