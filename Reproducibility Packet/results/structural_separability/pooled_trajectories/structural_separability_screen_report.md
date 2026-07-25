# Development structural separability screen

- Generated: 2026-07-25T02:32:11Z
- Dataset root: `C:\Users\cresp\Documents\Dandelion Engineering\Robot Structural Proprioception\data\gate3-base-dev-pilot-val-c1-s`
- Config hash: `dev-712abf27c3f8f3c331ae9b76e3f22c48857334cc15a81e819718165e47753e56`
- Split screened: `dev` (the script refuses any other split)
- Trajectory filter: `all`
- Window W = 768 steps, stride 64, [28] post-onset windows per run
- Context cells (folds): 8; runs per contrast arm: 8

Every contrast is context-matched: the healthy run and the fault run in a
fold share trajectory, payload, environment and contact profile, and differ
only in the fault and the sensor seed. Folds hold out a whole cell.

## Run-level AUROC (held-out, leave-one-cell-out)

| contrast | suite | interpretable rung | learned probe (best over C grid) | learned permutation p |
|---|---|---|---|---|
| structure_rem_ei_0.75 | C1 | 0.453 | 0.250 | 0.914 |
| structure_rem_ei_0.75 | S | 0.469 | 0.172 | 0.945 |
| structure_rem_ei_0.50 | C1 | 0.469 | 0.750 | not run |
| structure_rem_ei_0.50 | S | 0.578 | 0.703 | not run |
| actuator_rem_gain_0.50 | C1 | 0.594 | 0.891 | not run |
| actuator_rem_gain_0.50 | S | 0.500 | 0.859 | not run |

## Paired per-cell sign tests (exact, two-sided)

| contrast | suite | rung | cells with fault > healthy | p |
|---|---|---|---|---|
| structure_rem_ei_0.75 | C1 | interpretable | 2/8 | 0.2891 |
| structure_rem_ei_0.75 | C1 | learned | 2/8 | 0.2891 |
| structure_rem_ei_0.75 | S | interpretable | 3/8 | 0.7266 |
| structure_rem_ei_0.75 | S | learned | 1/8 | 0.0703 |
| structure_rem_ei_0.50 | C1 | interpretable | 2/8 | 0.2891 |
| structure_rem_ei_0.50 | C1 | learned | 6/8 | 0.2891 |
| structure_rem_ei_0.50 | S | interpretable | 6/8 | 0.2891 |
| structure_rem_ei_0.50 | S | learned | 7/8 | 0.0703 |
| actuator_rem_gain_0.50 | C1 | interpretable | 4/8 | 1.0000 |
| actuator_rem_gain_0.50 | C1 | learned | 6/8 | 0.2891 |
| actuator_rem_gain_0.50 | S | interpretable | 4/8 | 1.0000 |
| actuator_rem_gain_0.50 | S | learned | 6/8 | 0.2891 |

## Interpretable rung score scale

| contrast | suite | healthy mean | fault mean | median paired ratio |
|---|---|---|---|---|
| structure_rem_ei_0.75 | C1 | 1.0323 | 1.0111 | 0.988 |
| structure_rem_ei_0.75 | S | 1.0343 | 1.0265 | 0.992 |
| structure_rem_ei_0.50 | C1 | 1.0323 | 1.0165 | 0.980 |
| structure_rem_ei_0.50 | S | 1.0343 | 1.0852 | 1.055 |
| actuator_rem_gain_0.50 | C1 | 1.0323 | 1.1981 | 1.143 |
| actuator_rem_gain_0.50 | S | 1.0343 | 1.1351 | 1.092 |

## Per-channel paired attribution (suite S, all 18 registry columns)

Columns whose paired sign test clears p <= 0.05 are listed; the exact 8-cell floor is p = 0.0078. `S-excl` marks the four gauge columns S alone carries.

| contrast | column | S-excl | median rel. change | effect / healthy spread | sign p |
|---|---|---|---|---|---|
| structure_rem_ei_0.75 | `imu_obs[2]` | no | -12.34% | 0.223 | 0.0078 |
| structure_rem_ei_0.50 | `imu_obs[0]` | no | -9.37% | 0.597 | 0.0078 |
| structure_rem_ei_0.50 | `imu_obs[2]` | no | -29.34% | 0.502 | 0.0078 |
| actuator_rem_gain_0.50 | `q_obs[0]` | no | -7.01% | 0.345 | 0.0078 |
| actuator_rem_gain_0.50 | `tau_cmd[0]` | no | -13.19% | 1.829 | 0.0078 |
| actuator_rem_gain_0.50 | `tau_cmd[1]` | no | 62.82% | 6.027 | 0.0078 |
| actuator_rem_gain_0.50 | `current_proxy_obs[1]` | no | 55.12% | 7.430 | 0.0078 |
| actuator_rem_gain_0.50 | `imu_obs[0]` | no | -30.52% | 1.775 | 0.0078 |
| actuator_rem_gain_0.50 | `imu_obs[2]` | no | -34.69% | 0.573 | 0.0078 |

Largest S-exclusive gauge effect per contrast, whether or not significant:

| contrast | best gauge column | effect / healthy spread | sign p |
|---|---|---|---|
| structure_rem_ei_0.75 | `gauge_obs[1]` | 0.134 | 0.2891 |
| structure_rem_ei_0.50 | `gauge_obs[0]` | 0.111 | 0.2891 |
| actuator_rem_gain_0.50 | `gauge_obs[2]` | 0.099 | 0.7266 |

## Reading this screen

The learned AUROC is a maximum over a regularisation grid and is therefore
an optimistic bound on what this probe class can do at this sample size.
The permutation null applies the same maximisation, so the selection is
inside the null and the p-value remains interpretable. A positive control
(actuator_rem_gain_0.50) is included so an all-null table can be told apart
from a broken pipeline.
