# Literature Foundation — Robot Structural Proprioception

**Agent:** Codex
**Phase:** Phase 0 independent field survey
**Search completed:** 2026-07-16
**Independent emphasis:** observability and identifiability, fault attribution, hardware-plausible strain sensing, and the smallest simulation that can test whether structural measurements add information rather than merely add channels.

## 1. Domain and methods landscape

### 1.1 The project sits at an information boundary, not only a control boundary

The seed asks whether a robot gains an adaptive-control advantage when it senses local mechanical state throughout its body. The important distinction is between three outcomes that are often collapsed:

1. **Detection:** the nominal command-to-motion relationship changed.
2. **Attribution:** the change is more consistent with a structural, actuator, or sensor cause.
3. **Compensation:** the robot changes estimation or control and recovers useful performance.

Existing fields solve subsets of this chain. Robot dynamics identification estimates parameters from joint motion and torque. Fault-detection and isolation (FDI) builds residuals against a nominal model. Self-modeling learns a task-agnostic body representation. Fast adaptation learns a latent context or searches for a compensatory policy. Structural health monitoring (SHM) uses spatial strain or vibration patterns to detect and localize damage. Soft-robot proprioception maps distributed internal sensors to shape and contact. The project’s plausible contribution is therefore not “robots can sense strain” or “robots can adapt after damage,” both of which are established. It is a controlled test of whether local structural measurements make otherwise-confounded body changes more observable and whether that extra observability improves adaptation.

### 1.2 Conventional robot identification has real observability limits

Rigid-robot identification usually regresses joint torque against functions of joint position, velocity, and acceleration. The BIRDy benchmark implements 20-plus variants of least-squares, instrumental-variable, output-error, Kalman-filter, neural, and physically constrained methods. Its experiments show that method ranking changes with noise, filtering, friction assumptions, sampling, and control architecture. It also exposes a practical weakness: joint accelerations derived by differentiating encoders have poor signal-to-noise ratio.

More fundamentally, Wensing, Niemeyer, and Slotine characterize inertial-parameter identifiability for general open-chain robots. Some parameter changes are structurally unobservable from the standard joint-space experiment because they correspond to inertial transfers across joints that leave the measured input-output behavior unchanged. No estimator can recover a parameter in that nullspace from the same measurements, regardless of model capacity. Additional sensing is valuable only if it changes the observation map. Local strain or curvature is a credible way to do that because it measures deformation between the rigid-body coordinates on which the conventional model relies.

The control implication is important: a larger neural network is not automatically a stronger baseline if both networks receive the same uninformative history. The fair comparison is between sensor suites under matched estimator/controller capacity, followed by capacity checks within each suite.

### 1.3 Fault diagnosis adds analytical redundancy, but thresholds and fault models remain brittle

Model-based manipulator FDI forms a residual between measured behavior and predicted nominal behavior. Dixon et al. showed that torque-prediction residuals can detect actuator faults without acceleration measurements and can be made robust to bounded parametric uncertainty. Their review of earlier flight and robot systems also records a recurring problem: fixed thresholds create false alarms when ordinary model mismatch looks like a fault. Aghili and Namvar showed that joint-torque sensing can simplify the monitored dynamics and improve reliability against modeling uncertainty, but their formulation still treats a specified family of actuator and sensor faults.

These methods demonstrate why structural channels should be treated as **analytical redundancy**, not as decorative telemetry. A useful structural channel creates a fault signature that changes differently for, say, a 30% link-stiffness loss, a 30% actuator-gain loss, and a biased joint encoder under the same commanded excitation. If those signatures remain indistinguishable, attribution is not supported and the project should say so.

### 1.4 Adaptation can succeed without diagnosis

Two strong families deliberately avoid identifying the fault source:

- Intelligent Trial and Error (IT&E) searches a precomputed behavior-performance map and recovered from multiple leg and arm damage conditions in under two minutes. Its strength is behavioral recovery after unmodeled damage; its cost is a very large offline map and physical trials, and it does not need to explain what failed.
- Rapid Motor Adaptation (RMA) trains a base policy with privileged environment parameters and an adaptation module that infers a compact latent from recent proprioceptive history. It adapts in fractions of a second and transfers from simulation to a quadruped without real-world fine-tuning. Its latent is optimized for control, not calibrated causal attribution.

These are stronger baselines than a fixed controller because they ask the relevant practical question: can a conventional sensor history already recover the performance that structural sensing is supposed to add? But neither establishes that its latent separates structural, actuator, and sensor changes. A project that claims attribution must measure attribution explicitly; a project that claims control advantage must compare downstream control explicitly.

### 1.5 Self-modeling revises morphology or kinematics, usually through trusted external observation

Bongard, Zykov, and Lipson demonstrated continuous self-modeling and damage recovery by alternating informative actions, model synthesis, and controller search. Newer visual self-models represent full robot occupancy as a state-conditioned neural field, reaching roughly 1% to 2% of workspace-scale geometric error in reported systems and supporting motion planning. Neural Jacobian Fields learn a visuomotor Jacobian from self-supervised multi-view motion.

These methods show that revisable body models are feasible, but their evidence usually enters through cameras and joint commands. They are not designed to determine whether an encoder is lying, an actuator is weak, or a link is softer when those causes produce similar visible motion. External vision could be a useful ground-truth or upper-bound condition in this project, but including it in the default “conventional suite” could obscure the specific value of embedded structural sensing.

### 1.6 Structural sensing is physically plausible on both flexible and nominally rigid robots

Distributed strain is not confined to soft robotics. Gu and Piedboeuf used a flexible arm with distributed strain gauges as its own position, orientation, and endpoint-force sensing unit. Flexible-link control studies combine actuator positions with strain gauges or distributed inertial sensors to reconstruct deformation states. These are direct precedents for treating the load-bearing structure as a sensor.

Several transduction families are relevant:

| Modality | What it can plausibly expose | Useful properties | Important confounds |
|---|---|---|---|
| Foil or printed resistive strain gauges | Local axial/bending strain, quasi-static and dynamic | Cheap, simple virtual model, mature | Temperature drift, adhesive/substrate transfer, wiring, local measurement only |
| Fiber Bragg gratings (FBGs) | Multiplexed strain/curvature along a fiber | Small, EMI immune, many sensing nodes | Strain-temperature cross-sensitivity, interrogator cost, bonding and calibration |
| Soft resistive/capacitive skins | Large-area strain and deformation | Conformal, dense, can provide graceful degradation | Hysteresis, creep, drift, lag, cross-talk, fabrication variability |
| Piezoelectric or vibration channels | Dynamic strain, impacts, modal changes | High bandwidth, strong transient sensitivity | Weak or absent static information, operating-condition dependence |
| Distributed IMUs | Local angular rate/acceleration and flexible modes | Retrofittable, mature | Integration drift, gravity separation, indirect strain inference |

FBG studies report sub-millimeter shape reconstruction on constrained continuum manipulators, showing that local optical strain can support accurate geometric inference. They also make the central nuisance explicit: the same wavelength shift responds to temperature and strain. Recent experimental work reports typical uncompensated cross-sensitivity on the order of 10 microstrain per degree Celsius and large improvements with explicit temperature discrimination. A simulation that injects perfect noiseless “strain” would therefore test an impossible sensor.

Soft-robot studies provide a second precedent. Thuruthel et al. used three embedded soft strain sensors and a recurrent network for real-time shape and force estimation, and demonstrated graceful degradation when sensor channels were lost. Truby, Della Santina, and Rus reconstructed three-dimensional configuration from a sensorized skin. These systems show that distributed internal measurements can encode high-dimensional state, but they also document hysteresis, drift, response lag, nonunique mappings, and sampling limits. Their main task is shape/contact perception, not distinguishing a body fault from a faulty sensor.

### 1.7 SHM detects local mechanical change but usually stops before adaptive control

SHM treats changes in strain fields, modal properties, or vibration features as evidence of damage. Laflamme et al. demonstrated numerical detection, localization, and severity ranking from a dense strain network, including reconstruction of missing sensors. The LANL three-story benchmark shows why naïve anomaly detection fails: operational and environmental changes alter vibration features even when the structure is healthy.

SHM therefore contributes spatial features, missing-channel methods, and nuisance-aware validation. Robotics contributes commanded excitation and a closed control loop. The unexplored seam is not simply importing an SHM classifier; it is asking whether active robot motion plus local structural residuals can distinguish cause classes and support safe reconfiguration.

### 1.8 Whole-body tactile skin is complementary, not equivalent

Distributed tactile systems localize external contact and pressure. Murooka et al. showed that tactile feedback stabilizes humanoid multi-contact motion at intermediate body locations. That is relevant to the seed’s larger vision, but surface pressure and internal structural strain answer different questions. A surface contact can create a strain pattern; a stiffness loss can change strain without a new surface contact. The smallest project should not attempt both full skin and structural proprioception. Contact forces can instead be controlled disturbances or a limited test condition.

### 1.9 Simulation choices form a fidelity ladder

Three approaches can generate structural channels:

1. **Analytical beam or modal layer beside a rigid-body simulator.** Fast, interpretable, and easy to perturb. It risks circularity if “strain” is calculated from exactly the same generalized coordinates already given to the baseline.
2. **Flexible multibody or reduced-order continuum model.** PyElastica supplies MIT-licensed Cosserat rods in Python. This is a good fit for slender compliant links, but contact-rich articulated robotics requires integration work.
3. **Deformable or finite-element simulation.** MuJoCo 3.x now provides 1D/2D/3D flexes and a Saint Venant–Kirchhoff elasticity model with Young’s modulus, Poisson ratio, damping, and strain constraints. SOFA provides LGPL-licensed interactive FEM; Project Chrono provides BSD-licensed rigid/flexible multibody and FEA. These are more physically expressive but create a larger modeling and validation burden.

For this desktop and a small first experiment, MuJoCo’s Python/Windows support and deformable elements make it a promising single-engine candidate. A second independent mechanics calculation or mesh-refinement check should validate its virtual gauge signals. PyElastica is an attractive verification model for a slender link. Chrono and SOFA are credible fallbacks if MuJoCo cannot expose stable, interpretable local deformation at the required joints and contacts.

## 2. Benchmark results and calibration targets

There is no unified benchmark for “structural proprioception for adaptive robots.” Reported numbers come from different tasks and should calibrate scale, not be pasted into a Claim Sheet as if directly comparable.

### 2.1 Existing performance anchors

| Capability | Published anchor | What it calibrates |
|---|---|---|
| Damage recovery by behavior search | IT&E reports recovery in under two minutes across five legged-robot damage types and 14 arm-joint damage conditions; the offline map used about 40 million simulated evaluations, while adaptation is commonly summarized at 17 physical trials | A serious recovery baseline can be fast online but extremely expensive offline and need not diagnose the fault |
| Latent rapid adaptation | RMA reports adaptation in fractions of a second; in highlighted outdoor trials it achieved 70% success descending stairs and 80% across cement/pebble piles | Conventional proprioceptive history plus a learned latent is already a strong control baseline |
| Visual body model | Chen et al. report about 1% workspace-scale self-model accuracy; Schulze and Lipson report Chamfer-L2 near 2% of workspace dimension on a 7-DoF system | External observation can provide a useful upper bound, but at a different sensing cost |
| Soft embedded strain to state/force | Thuruthel et al. report 2.17 ± 1.65 mm and 2.43 ± 2.18 mm position error on two actuators, 15.3% full-range force error, and a 10 Hz hardware ceiling in the demonstrated multiplexer | Realistic soft sensors include lag, drift, cross-talk, and bandwidth limits |
| FBG continuum shape | Amirkhani et al. report 0.216 ± 0.126 mm free-space shape error and roughly 0.31–0.49 mm error with obstacles | Physically embedded strain can support sub-millimeter inference in a calibrated constrained platform |
| Inertial parameter identification | BIRDy finds DIDIM and IDIM-IV among the most accurate under standard joint-position noise, while Kalman methods are highly sensitive to covariance initialization | Estimator tuning and sensor noise can dominate method labels |

### 2.2 Metrics the project should pre-declare

The smallest meaningful benchmark should report two layers, not one aggregate reward.

**Information/diagnosis layer**

- Four-way healthy/structure/actuator/sensor macro-F1 and balanced accuracy.
- Per-class precision/recall and confusion matrices, especially structure-versus-actuator and structure-versus-sensor.
- Detection delay after a change, measured in control cycles and seconds.
- Localization error when more than one link, actuator, or sensor location is possible.
- Calibration of fault probabilities (Brier score, negative log likelihood, and reliability diagram), including an abstain/unknown option.
- Performance on held-out severities, trajectories, payloads, noise draws, and at least one held-out fault combination.

**Control layer**

- Tracking RMSE and peak error before fault, immediately after fault, and after adaptation.
- Recovery time and recovered-performance ratio relative to the healthy controller.
- Control effort, saturation time, constraint violations, and unsafe excursions.
- Paired difference between matched conventional-suite and structural-suite agents over identical seeds and faults, with uncertainty intervals.

Chance performance for four balanced classes is 0.25 balanced accuracy, but “better than chance” is far too weak. The Claim Sheet should set its bar after a pilot estimates the overlap of the fault signatures. A defensible advantage claim should require both a statistically stable improvement over the strongest conventional suite and a practically meaningful downstream control gain. If diagnosis improves but control does not, that is a diagnostic result, not an adaptive-control advantage.

## 3. Dataset and resource landscape

### 3.1 Reusable data and benchmarks

- **BIRDy:** an MIT-licensed MATLAB benchmark with identification algorithms, excitation generation, robot models, raw experiments, and Monte Carlo procedures for two 6-DoF industrial manipulators. It is useful as a method and excitation reference, not as the project runtime because the project is Python-only and has no assumed MATLAB license.
- **LANL three-story SHM data:** public vibration data with healthy and damage-like nonlinear states under operational variability. It is useful for testing anomaly features and nuisance sensitivity, but it has no robot commands, actuator faults, or joint sensors.
- **IT&E source data:** the Nature page exposes CSV source data for core and extended figures, useful for understanding adaptation curves and trial budgets. Its robot and task do not provide distributed structural channels.
- **MuJoCo Menagerie:** curated robot models with model-specific licenses, including permissively licensed arms and mobile manipulators. It can shorten model setup, but every selected asset’s license must be audited individually.

The absence of a dataset that crosses robot commands, joint sensing, distributed structural measurements, multiple body/actuator/sensor faults, and downstream control is itself a finding. The project will likely need to generate its own simulated benchmark and publish generation code rather than train on a pre-existing corpus.

### 3.2 Candidate software and licenses

| Resource | Role | License and fit |
|---|---|---|
| MuJoCo | Articulated contact dynamics, deformable flexes, Python API | Apache-2.0; Windows wheels and Python 3.10+ support; strongest first candidate |
| PyElastica | Cosserat-rod dynamics and independent slender-link validation | MIT; Python 3.10+; strong verification/fallback layer |
| SOFA | Interactive FEM and soft robotics | Core LGPL-2.1-or-later, some apps/tutorials GPL; powerful but heavier integration and license bookkeeping |
| Project Chrono | Rigid/flexible multibody, nonlinear FEA, contacts | BSD-3-Clause; broad capability, but its official Python distribution is oriented around Conda, which conflicts with the project’s required venv workflow unless a compatible installation path is verified |
| BIRDy | Identification baselines and excitation design | MIT; MATLAB dependency makes it a conceptual/reference resource rather than the implementation base |

No dependency should be installed during Phase 0. Phase 1 should choose the minimum simulator after a tiny feasibility spike confirms: local virtual gauge extraction, stiffness perturbation, actuator-gain perturbation, encoder corruption, deterministic seeding, and acceptable runtime.

## 4. Failure modes and known dead ends

### 4.1 More channels without more independent information

If a virtual strain channel is algebraically reconstructed from the same joint state and nominal model used by the baseline, it may add no independent information and may leak the fault label through the simulator implementation. Structural channels must arise from local deformation states that respond to the plant independently of the corrupted conventional measurement.

### 4.2 Unexcited faults are not identifiable

A stiffness change does not reveal itself if the relevant link never bends; actuator gain may be indistinguishable from load variation under a narrow trajectory. Random motion is not automatically informative motion. Excitation design must cover the parameters/fault signatures while staying within safe bounds, and evaluation must include ordinary task motion to determine whether the diagnostic motion requirement is practical.

### 4.3 Perfect simulated sensors produce a synthetic win

Real strain modalities have noise, offset, drift, bandwidth, temperature sensitivity, saturation, hysteresis, missing channels, and placement errors. Training and testing only on ideal channels measures access to simulator state, not value of a plausible sensor. The test distribution must include nuisance variation, and at least one nuisance type should be held out.

### 4.4 The estimator can learn simulator fingerprints

Abrupt parameter edits, class-specific onset times, fixed sensor indices, or different noise seeds can reveal labels without physics. All fault classes need matched onset distributions, severity ranges, random locations, and noise generation. Split by entire trajectories and fault settings, not by individual time samples from the same run.

### 4.5 SHM confuses environment with damage

Payload, contact location, temperature, and task trajectory can shift strain/vibration distributions. LANL’s benchmark exists precisely because environmental and operational changes generate damage-like features. Payload and contact variation must appear in both healthy and faulty data; otherwise the detector will not learn the intended distinction.

### 4.6 Joint/sensor fault definitions can be circular

An encoder bias is trivial to classify if an uncorrupted copy of the same coordinate is provided as “ground truth.” The structural suite should receive only measurements a physical robot could plausibly carry. External pose may be reserved for training labels, validation, or an explicit upper-bound suite, not silently included online.

### 4.7 Attribution can overreach before detection is established

Calibrated multi-class attribution is materially harder than detecting “something changed.” A staged benchmark should first test detection, then source class, then localization. If class posteriors overlap, the system should abstain rather than manufacture certainty. A clean result may be that strain helps detect/localize stiffness changes but cannot distinguish actuator loss from encoder bias under normal task excitation.

### 4.8 Adaptation can hide diagnosis failure, and diagnosis can fail to help control

A latent policy may recover behavior without identifying the fault. Conversely, a classifier can identify a fault without improving control. The project must keep diagnosis and control metrics separate and compare: no adaptation, conventional-suite adaptation, structural-suite adaptation, and (if affordable) a privileged oracle-fault controller.

### 4.9 Full humanoid or full FEM scope is a dead end for the first experiment

A humanoid combines floating-base dynamics, contacts, balance, large policy training, and many fault locations. Full high-resolution FEM adds meshing and solver validation before the scientific comparison exists. Either can consume the project while leaving the core information question unsettled. A two-link planar or spatial flexible-link manipulator with one contact/task family is sufficient to expose the intended confounds and can later be expanded only if the signal survives.

## 5. Open questions and proposed Phase 1 direction

### 5.1 The load-bearing open question

The literature supports detection, adaptation, self-modeling, structural monitoring, and embedded strain sensing separately. It does not yet answer a narrow controlled question:

> On a small articulated robot with compliant links, do a few local strain/curvature measurements improve held-out attribution of link-stiffness loss, actuator-gain loss, and joint-sensor corruption over a matched conventional proprioceptive history, and does any attribution gain improve closed-loop recovery?

This phrasing is narrower than a general claim about a robot “knowing what body it has.” It makes the incremental information test primary and downstream control secondary but required for an advantage claim.

### 5.2 Provisional smallest-sufficient experiment

- **Plant:** two-link manipulator with one or both links modeled as deformable beams; start planar unless torsion is essential to separate signatures.
- **Task/excitation:** track a family of bounded trajectories with randomized payload and optional endpoint contact. Include a short safe diagnostic excitation condition and ordinary task-only condition.
- **Fault families:** localized stiffness reduction; actuator torque/gain loss; encoder bias/drift/dropout. Begin with one fault at a time, then hold out one compound case as an unknown/generalization test.
- **Sensor suites:**
  - C0: joint position/velocity and commanded actuation.
  - C1: C0 plus realistic actuator torque/current and a body IMU or endpoint measurement that a conventional research robot could plausibly have.
  - S: matched C1 plus a small, fixed set of local strain/curvature channels.
  - O: optional privileged simulator state as an oracle ceiling, never a deployable baseline.
- **Estimator:** matched temporal model across C1 and S, with a simple residual/linear baseline and a stronger recurrent latent baseline. Capacity is swept enough to show that sensor-suite results are not a parameter-count artifact.
- **Adaptation:** begin with gain scheduling or model-predictive reconfiguration driven by the estimated fault distribution. Compare against a control-only latent adaptation that receives the same history but no explicit label objective.
- **Validation:** independent beam calculation or second solver for nominal strain profiles; mesh/timestep convergence; sensor noise/drift/placement sweeps; held-out trajectories, payloads, severities, and locations.

### 5.3 Decision outcomes worth preserving

- **Positive:** structural channels improve held-out attribution and the improvement yields faster or safer recovery than the strongest conventional suite.
- **Diagnostic-only:** attribution improves, but control does not; useful for monitoring, not evidence of adaptive-control advantage.
- **Fault-specific:** benefit appears only for stiffness/local structural changes, not actuator or sensor faults. This would sharply define where structural proprioception is worth adding.
- **Null:** matched conventional sensing and temporal adaptation recover the same information/performance. This argues against extra structural hardware for this task.
- **Inconclusive:** benefit disappears under plausible drift, temperature, placement, or model mismatch, or depends on privileged simulator leakage.

### 5.4 Questions Phase 1 must settle before implementation

1. Can MuJoCo expose local deformation variables from a deformable link cleanly enough to construct virtual gauges without using inaccessible ground truth at deployment time?
2. What conventional suite is fair for the intended affordable robot: encoders plus commands, or encoders plus motor current/torque and IMUs?
3. Is explicit source attribution necessary for safe compensation, or should the first claim be limited to detecting/localizing structural change?
4. What diagnostic excitation budget is acceptable, and can ordinary task trajectories supply enough persistent excitation?
5. Which uncertainty/abstention rule prevents an ambiguous fault from causing unsafe reconfiguration?

## 6. References

Detailed ledger entries, including how each source informed this survey, are maintained in agents/Codex/references.md. The load-bearing sources are listed here in transferable citation form.

1. Bongard, J., Zykov, V., & Lipson, H. (2006). Resilient machines through continuous self-modeling. *Science, 314*(5802), 1118–1121. https://doi.org/10.1126/science.1133687
2. Cully, A., Clune, J., Tarapore, D., & Mouret, J.-B. (2015). Robots that can adapt like animals. *Nature, 521*, 503–507. https://doi.org/10.1038/nature14422
3. Kumar, A., Fu, Z., Pathak, D., & Malik, J. (2021). RMA: Rapid Motor Adaptation for Legged Robots. *Robotics: Science and Systems XVII*. https://doi.org/10.15607/RSS.2021.XVII.011
4. Wensing, P. M., Niemeyer, G., & Slotine, J.-J. E. (2024). A geometric characterization of observability in inertial parameter identification. *The International Journal of Robotics Research*. https://doi.org/10.1177/02783649241258215
5. Leboutet, Q., Roux, J., Janot, A., Guadarrama-Olvera, J. R., & Cheng, G. (2021). Inertial parameter identification in robotics: A survey. *Applied Sciences, 11*(9), 4303. https://doi.org/10.3390/app11094303
6. Dixon, W. E., Walker, I. D., Dawson, D. M., & Hartranft, J. P. (2000). Fault detection for robot manipulators with parametric uncertainty: A prediction-error-based approach. *IEEE Transactions on Robotics and Automation, 16*(6), 689–699. https://doi.org/10.1109/70.897780
7. Aghili, F., & Namvar, M. (2010). Failure detection and isolation in robotic manipulators using joint torque sensors. *Robotica, 28*(4), 549–561. https://doi.org/10.1017/S0263574709990245
8. Gu, M., & Piedbœuf, J.-C. (2003). A flexible-arm as manipulator position and force detection unit. *Control Engineering Practice, 11*(12), 1433–1448. https://doi.org/10.1016/S0967-0661(03)00105-9
9. Thuruthel, T. G., Shih, B., Laschi, C., & Tolley, M. T. (2019). Soft robot perception using embedded soft sensors and recurrent neural networks. *Science Robotics, 4*(26), eaav1488. https://doi.org/10.1126/scirobotics.aav1488
10. Truby, R. L., Della Santina, C., & Rus, D. (2020). Distributed proprioception of 3D configuration in soft, sensorized robots via deep learning. *IEEE Robotics and Automation Letters, 5*(2), 3299–3306. https://doi.org/10.1109/LRA.2020.2976320
11. Sefati, S., Gao, C., Iordachita, I., Taylor, R. H., & Armand, M. (2021). Data-driven shape sensing of a surgical continuum manipulator using an uncalibrated fiber Bragg grating sensor. *IEEE Sensors Journal, 21*(3), 3066–3076. https://doi.org/10.1109/JSEN.2020.3028208
12. Amirkhani, G., Goodridge, A., Esfandiari, M., Phalen, H., Ma, J. H., Iordachita, I., & Armand, M. (2023). Design and fabrication of a fiber Bragg grating shape sensor for shape reconstruction of a continuum manipulator. *IEEE Sensors Journal, 23*(12), 12915–12929. https://doi.org/10.1109/JSEN.2023.3274146
13. Silveira, M. L., et al. (2021). An optimized self-compensated solution for temperature and strain cross-sensitivity in FBG interrogators based on edge filter. *Sensors, 21*(17), 5828. https://doi.org/10.3390/s21175828
14. Luo, J., et al. (2025). Monofiber-based temperature and strain discrimination using heterogeneous waveguide Bragg gratings. *Light: Advanced Manufacturing, 6*, 77. https://doi.org/10.37188/lam.2025.077
15. Laflamme, S., Cao, L., Chatzi, E., & Ubertini, F. (2016). Damage detection and localization from dense network of strain sensors. *Shock and Vibration, 2016*, 2562949. https://doi.org/10.1155/2016/2562949
16. Figueiredo, E., Park, G., Figueiras, J., Farrar, C., & Worden, K. (2009). *Structural Health Monitoring Algorithm Comparisons Using Standard Data Sets* (LA-14393). Los Alamos National Laboratory. https://www.osti.gov/biblio/961604
17. Chen, B., Kwiatkowski, R., Vondrick, C., & Lipson, H. (2022). Full-body visual self-modeling of robot morphologies. *Science Robotics, 7*(68), eabn1944. https://doi.org/10.1126/scirobotics.abn1944
18. Schulze, L., & Lipson, H. (2023). High-degrees-of-freedom dynamic neural fields for robot self-modeling and motion planning. *NeurIPS 2023 Workshop on Symmetry and Geometry in Neural Representations*. https://arxiv.org/abs/2310.03624
19. Li, S., Zhang, A., Chen, B., Matusik, W., Liu, C., Rus, D., & Sitzmann, V. (2025). Controlling diverse robots by inferring Jacobian fields with deep networks. *Nature*. https://doi.org/10.1038/s41586-025-09170-0
20. Murooka, M., et al. (2024). Whole-body multi-contact motion control for humanoid robots based on distributed tactile sensors. *IEEE Robotics and Automation Letters, 9*(11), 10620–10627. https://doi.org/10.1109/LRA.2024.3475052
21. Todorov, E., Erez, T., & Tassa, Y. (2012). MuJoCo: A physics engine for model-based control. *2012 IEEE/RSJ International Conference on Intelligent Robots and Systems*, 5026–5033. https://doi.org/10.1109/IROS.2012.6386109
22. Tekinalp, A., et al. (2024). PyElastica [Software]. Zenodo. https://doi.org/10.5281/zenodo.7658871
