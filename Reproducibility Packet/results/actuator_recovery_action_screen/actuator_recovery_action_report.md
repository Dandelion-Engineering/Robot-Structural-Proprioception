# Actuator Recovery Action Screen

**Decision:** `BLOCK_ACTUATOR_ACTION_FAMILY_AT_SOURCE_SPECIFIC_GATE`

## Question and evidence boundary

At the bounded task's selected 0.25 remaining-gain condition, can a bounded inverse-gain action recover tracking source-specifically rather than merely improve any arm that is authorized to act? This is a development action-mechanism screen. It is not calibrated authorization, a C1-versus-S control result, validation-sized evidence, or a frozen config.

Three tuning seeds choose from the predeclared cap/floor family using both fault recovery and the same diagnosis falsely authorized on healthy. Four disjoint assessment seeds then evaluate the tuning-selected profile with oracle severity and the already-recorded C1/S held-out severity estimates. The 95% interval resamples only four physical seeds, so it is a sign-stability guard rather than a confirmatory uncertainty statement.

## Tuning-only cap/floor family

| candidate | cap | floor | oracle m | fault reduction | healthy false-auth benefit | source-specific margin | gates |
|---|---:|---:|---:|---:|---:|---:|---|
| cap2_floor0p25 | 2.00 | 0.25 | 2.000 | 10.852% (min 10.770%) | 6.177% | 4.675 pp (min 4.376) | BLOCK |
| cap3_floor0p25 | 3.00 | 0.25 | 3.000 | 16.657% (min 16.508%) | 8.174% | 8.483 pp (min 8.340) | BLOCK |
| cap4_floor0p25 | 4.00 | 0.25 | 4.000 | 19.711% (min 19.596%) | 9.987% | 9.723 pp (min 6.701) | BLOCK |
| cap5_floor0p25 | 5.00 | 0.25 | 4.000 | 19.711% (min 19.596%) | 9.987% | 9.723 pp (min 6.701) | BLOCK |
| cap5_floor0p20 | 5.00 | 0.20 | 4.000 | 19.711% (min 19.596%) | 9.987% | 9.723 pp (min 6.701) | BLOCK |

Tuning selected **`cap3_floor0p25`** by source-specific margin among tracking-capable, lifecycle-safe candidates; assessment was not read during selection.

## Disjoint assessment

| profile | diagnosis | multiplier range | fault reduction | healthy false-auth benefit | source-specific margin (95% paired bootstrap) | gate |
|---|---|---:|---:|---:|---:|---|
| cap3_floor0p25 | C1 | 3.000–3.000 | 16.576% (min 16.489%) | 8.322% | 8.254 pp [8.093, 8.532] | BLOCK |
| cap3_floor0p25 | S | 3.000–3.000 | 16.576% (min 16.489%) | 8.322% | 8.254 pp [8.093, 8.532] | BLOCK |
| cap3_floor0p25 | oracle | 3.000–3.000 | 16.576% (min 16.489%) | 8.322% | 8.254 pp [8.093, 8.532] | BLOCK |
| cap5_floor0p20 | C1 | 3.763–4.020 | 19.503% (min 19.051%) | 10.026% | 9.477 pp [9.112, 9.781] | BLOCK |
| cap5_floor0p20 | S | 3.732–3.969 | 19.440% (min 19.090%) | 9.261% | 10.179 pp [9.677, 10.633] | BLOCK |
| cap5_floor0p25 | C1 | 3.763–4.000 | 19.497% (min 19.051%) | 10.032% | 9.465 pp [9.102, 9.779] | BLOCK |
| cap5_floor0p25 | S | 3.732–3.969 | 19.440% (min 19.090%) | 9.261% | 10.179 pp [9.677, 10.633] | BLOCK |

## Interpretation

No candidate clears the development source-specific gate through disjoint assessment. The action family therefore remains blocked; larger raw fault recovery is not promoted when the same authorization also improves or harms a healthy arm enough to consume the margin, or when the candidate violates the lifecycle/safety contract.

The cap-5 profiles are sensitivity arms, not extra selected candidates. Comparing `cap5_floor0p25` with `cap5_floor0p20` isolates whether lowering the floor lets recorded severity underestimates command above exact restoration. Any effect is reported in tracking units rather than inferred from multiplier differences.

All arms use one held decision, no pre-decision recovery, and exact within-source pre-decision CRN matching. Reference arms retain zero A1 incidents, zero saturation, and commanded-versus-applied multiplier identity. Candidate violations remain visible as scientific block evidence: 19 candidate arms with A1 incidents, 0 with saturation, and 0 with multiplier mismatch. Assessment references reproduce the approved severity screen's committed no-action J5 values.

## Selected-profile assessment detail

- **C1 severity:** fault reduction 16.576%; healthy false-authorization benefit 8.322%; source-specific margin 8.254 pp.
- **S severity:** fault reduction 16.576%; healthy false-authorization benefit 8.322%; source-specific margin 8.254 pp.
- **oracle severity:** fault reduction 16.576%; healthy false-authorization benefit 8.322%; source-specific margin 8.254 pp.
