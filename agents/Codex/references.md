# Codex Reference Ledger

This ledger records sources that informed Codex’s work on Robot Structural Proprioception. Entries are written when the source is used and include the project decision or question each source shaped.

## Phase 0 — Literature Foundation

### Bongard, Zykov, and Lipson (2006) — continuous self-modeling

Demonstrates a robot that selects informative actions, synthesizes competing self-models, and uses the selected model to recover locomotion after physical change. It establishes that a robot can revise a body model without a pre-enumerated damage diagnosis.

*How it informed the project:* establishes the historical self-modeling baseline and clarifies that behavioral recovery does not by itself establish source attribution among structure, actuator, and sensor changes.

Link: https://doi.org/10.1126/science.1133687

Citation: Bongard, J., Zykov, V., & Lipson, H. (2006). Resilient machines through continuous self-modeling. *Science, 314*(5802), 1118–1121. https://doi.org/10.1126/science.1133687

### Cully et al. (2015) — Intelligent Trial and Error

Introduces a behavior-performance map plus Bayesian search that recovers useful behavior after several unanticipated damage conditions. The paper reports adaptation in under two minutes and exposes source data for its figures.

*How it informed the project:* sets a strong control-recovery baseline that needs no explicit diagnosis, supplies an online trial-budget anchor, and warns that fast online recovery can hide very large offline computation (about 40 million evaluations for the reported map).

Link: https://doi.org/10.1038/nature14422

Citation: Cully, A., Clune, J., Tarapore, D., & Mouret, J.-B. (2015). Robots that can adapt like animals. *Nature, 521*, 503–507. https://doi.org/10.1038/nature14422

### Kumar et al. (2021) — Rapid Motor Adaptation

Presents a base locomotion policy and an adaptation module that estimates a compact environment/body latent from recent proprioceptive history. The same policy transfers from simulation to an A1 quadruped and adapts in fractions of a second.

*How it informed the project:* motivates a strong history-based conventional-sensor baseline and the distinction between a latent sufficient for control and a calibrated explanation of what changed.

Link: https://doi.org/10.15607/RSS.2021.XVII.011

Citation: Kumar, A., Fu, Z., Pathak, D., & Malik, J. (2021). RMA: Rapid Motor Adaptation for Legged Robots. *Robotics: Science and Systems XVII*. https://doi.org/10.15607/RSS.2021.XVII.011

### Wensing, Niemeyer, and Slotine (2024) — inertial-parameter observability

Provides a provably correct geometric characterization of identifiable inertial parameters for open-chain articulated robots. Undetectable parameter changes can be represented as inertial transfers across joints.

*How it informed the project:* supplies the formal reason that estimator capacity cannot repair an uninformative observation map and motivates testing whether local structural measurements shrink the conventional joint-space nullspace.

Link: https://doi.org/10.1177/02783649241258215

Citation: Wensing, P. M., Niemeyer, G., & Slotine, J.-J. E. (2024). A geometric characterization of observability in inertial parameter identification. *The International Journal of Robotics Research*. https://doi.org/10.1177/02783649241258215

### Leboutet et al. (2021) — BIRDy and robot dynamics identification

Surveys and benchmarks more than 20 inertial-parameter identification variants across least-squares, instrumental-variable, output-error, Kalman, neural, and physically consistent formulations. It documents noise, differentiation, filtering, tuning, and excitation issues on simulated and physical 6-DoF robots.

*How it informed the project:* grounds the conventional identification landscape, makes excitation design a first-class requirement, and supports simple/residual and strong/history-based estimator tiers rather than a single neural comparator.

Link: https://doi.org/10.3390/app11094303

Citation: Leboutet, Q., Roux, J., Janot, A., Guadarrama-Olvera, J. R., & Cheng, G. (2021). Inertial parameter identification in robotics: A survey. *Applied Sciences, 11*(9), 4303. https://doi.org/10.3390/app11094303

### TUM-ICS BIRDy repository and experiment data

The MIT-licensed repository contains robot models, excitation-trajectory generation, simulated experiment generation, and identification implementations; the paper also links raw data and results on Zenodo.

*How it informed the project:* identifies reusable ideas and public comparison data, while also showing why BIRDy is a reference rather than this project’s runtime base: it requires MATLAB and some physically constrained methods use CVX/MOSEK.

Links: https://github.com/TUM-ICS/BIRDy and https://doi.org/10.5281/zenodo.4728085

Citation: TUM Institute for Cognitive Systems. (2021). *BIRDy: Benchmark for Identification of Robot Dynamics* [Software]. https://github.com/TUM-ICS/BIRDy

### Dixon et al. (2000) — robust residual-based actuator fault detection

Develops a filtered torque-prediction-error method that avoids acceleration measurements, handles bounded parametric uncertainty, and detects actuator fault signatures on a two-joint manipulator.

*How it informed the project:* anchors analytical-redundancy baselines and documents how model uncertainty and threshold selection can cause slow detection or false alarms.

Link: https://doi.org/10.1109/70.897780

Citation: Dixon, W. E., Walker, I. D., Dawson, D. M., & Hartranft, J. P. (2000). Fault detection for robot manipulators with parametric uncertainty: A prediction-error-based approach. *IEEE Transactions on Robotics and Automation, 16*(6), 689–699. https://doi.org/10.1109/70.897780

### Aghili and Namvar (2010) — FDI with joint-torque sensing

Shows that joint-torque sensing can simplify the dynamics used by an FDI monitor and improve robustness to poorly identifiable link dynamics, friction, backlash, and flexibility. It studies actuator faults plus torque- and position-sensor noise/bias in simulation.

*How it informed the project:* provides a strong “conventional plus torque sensor” comparator and supports treating added sensing as analytical redundancy whose value must be tested under noise and bias.

Link: https://doi.org/10.1017/S0263574709990245

Citation: Aghili, F., & Namvar, M. (2010). Failure detection and isolation in robotic manipulators using joint torque sensors. *Robotica, 28*(4), 549–561. https://doi.org/10.1017/S0263574709990245

### Gu and Piedbœuf (2003) — a flexible arm as its own sensor

Uses distributed strain gauges on a flexible robot arm to estimate structural deformation, endpoint position/orientation, and endpoint contact force.

*How it informed the project:* directly establishes that structural strain sensing on a robot link can provide control-relevant state beyond joint coordinates; it is the closest conceptual precedent for a small flexible-link simulation.

Link: https://doi.org/10.1016/S0967-0661(03)00105-9

Citation: Gu, M., & Piedbœuf, J.-C. (2003). A flexible-arm as manipulator position and force detection unit. *Control Engineering Practice, 11*(12), 1433–1448. https://doi.org/10.1016/S0967-0661(03)00105-9

### Thuruthel et al. (2019) — embedded soft sensors and recurrent perception

Uses three embedded cPDMS strain sensors plus command history and an LSTM to estimate soft-finger kinematics and contact force. The paper reports millimeter-scale position errors, 15.3% full-range force error, graceful degradation under sensor loss, and practical 10 Hz, drift, lag, and cross-talk limitations.

*How it informed the project:* supplies realistic sensor-error modes and quantitative anchors; shows why a temporally informed model is fair, but also why ideal simulator-state channels would be an invalid proxy for physical sensors.

Link: https://doi.org/10.1126/scirobotics.aav1488

Citation: Thuruthel, T. G., Shih, B., Laschi, C., & Tolley, M. T. (2019). Soft robot perception using embedded soft sensors and recurrent neural networks. *Science Robotics, 4*(26), eaav1488. https://doi.org/10.1126/scirobotics.aav1488

### Truby, Della Santina, and Rus (2020) — distributed 3D soft-robot proprioception

Presents a sensorized skin and deep model for estimating a soft robot’s three-dimensional configuration from distributed internal measurements.

*How it informed the project:* supports the premise that distributed strain-like channels can encode high-dimensional body state, while delimiting the current task: shape estimation is not the same as fault-source attribution.

Link: https://doi.org/10.1109/LRA.2020.2976320

Citation: Truby, R. L., Della Santina, C., & Rus, D. (2020). Distributed proprioception of 3D configuration in soft, sensorized robots via deep learning. *IEEE Robotics and Automation Letters, 5*(2), 3299–3306. https://doi.org/10.1109/LRA.2020.2976320

### Sefati et al. (2021) — data-driven FBG shape sensing

Compares linear, deep, temporal, and conventional model-dependent shape estimation from an uncalibrated FBG sensor on a continuum manipulator, including instrument and obstacle disturbances.

*How it informed the project:* provides realistic FBG inference accuracy and shows that sensor-to-state calibration can be learned, but also that validation must include disturbances absent from nominal calibration.

Link: https://doi.org/10.1109/JSEN.2020.3028208

Citation: Sefati, S., Gao, C., Iordachita, I., Taylor, R. H., & Armand, M. (2021). Data-driven shape sensing of a surgical continuum manipulator using an uncalibrated fiber Bragg grating sensor. *IEEE Sensors Journal, 21*(3), 3066–3076. https://doi.org/10.1109/JSEN.2020.3028208

### Amirkhani et al. (2023) — embedded FBG shape reconstruction

Designs a two-fiber, six-node FBG shape sensor for a continuum manipulator and reports 0.216 ± 0.126 mm free-space shape error and about 0.31–0.49 mm error in obstacle-constrained bends.

*How it informed the project:* calibrates the physical plausibility and accuracy of multiplexed local strain/curvature sensing without implying that those numbers transfer directly to a different robot.

Link: https://doi.org/10.1109/JSEN.2023.3274146

Citation: Amirkhani, G., Goodridge, A., Esfandiari, M., Phalen, H., Ma, J. H., Iordachita, I., & Armand, M. (2023). Design and fabrication of a fiber Bragg grating shape sensor for shape reconstruction of a continuum manipulator. *IEEE Sensors Journal, 23*(12), 12915–12929. https://doi.org/10.1109/JSEN.2023.3274146

### Silveira et al. (2021) — FBG temperature/strain cross-sensitivity

Characterizes a self-compensated FBG interrogation design and reports typical FBG sensitivities of about 1.2 pm per microstrain and 12 pm per degree Celsius, equivalent to roughly 10 microstrain per degree Celsius if temperature is not separated.

*How it informed the project:* supplies the quantitative basis for treating temperature as a first-order confound in virtual strain channels instead of adding generic independent noise.

Link: https://doi.org/10.3390/s21175828

Citation: Silveira, M. L., et al. (2021). An optimized self-compensated solution for temperature and strain cross-sensitivity in FBG interrogators based on edge filter. *Sensors, 21*(17), 5828. https://doi.org/10.3390/s21175828

### Luo et al. (2025) — FBG temperature/strain discrimination

Demonstrates a single-fiber pair of heterogeneous Bragg gratings whose different thermo-optic responses separate temperature from strain; the paper reports stable average strain sensitivity across a wide temperature range.

*How it informed the project:* makes temperature-strain cross-sensitivity an explicit simulation nuisance and supports treating temperature compensation as an additional measurement/design requirement rather than assuming pure strain.

Link: https://doi.org/10.37188/lam.2025.077

Citation: Luo, J., Liu, H., Ding, H., Zhang, Z., Chen, Z., & Xu, F. (2025). Monofiber-based temperature and strain discrimination using heterogeneous waveguide Bragg gratings. *Light: Advanced Manufacturing, 6*, 77. https://doi.org/10.37188/lam.2025.077

### Laflamme et al. (2016) — dense strain networks for SHM

Uses dense capacitive strain measurements to detect, localize, and rank damage in a simulated wind-turbine blade, including reconstruction with missing or malfunctioning sensors.

*How it informed the project:* contributes spatial residual and missing-channel ideas, and shows that dense strain can localize stiffness change; the gap is closing the loop from structural diagnosis to robot adaptation.

Link: https://doi.org/10.1155/2016/2562949

Citation: Laflamme, S., Cao, L., Chatzi, E., & Ubertini, F. (2016). Damage detection and localization from dense network of strain sensors. *Shock and Vibration, 2016*, 2562949. https://doi.org/10.1155/2016/2562949

### Figueiredo et al. (2009) — LANL SHM benchmark

Compares SHM algorithms on a three-story laboratory structure where damage-like nonlinearity must be detected amid operational and environmental variation; the underlying data were released publicly.

*How it informed the project:* makes payload, task, contact, and environmental shifts mandatory healthy controls so the project does not mistake domain shift for structural change.

Link: https://www.osti.gov/biblio/961604

Citation: Figueiredo, E., Park, G., Figueiras, J., Farrar, C., & Worden, K. (2009). *Structural Health Monitoring Algorithm Comparisons Using Standard Data Sets* (LA-14393). Los Alamos National Laboratory. https://www.osti.gov/biblio/961604

### Chen et al. (2022) — full-body visual self-modeling

Learns a state-conditioned implicit representation of robot occupancy from images and uses it for planning; the reported physical system reaches about 1% of workspace-scale accuracy.

*How it informed the project:* supplies an external-observation upper bound and demonstrates task-agnostic body-model revision, while highlighting that cameras and trusted joint state answer a different observability question from embedded structural sensing.

Link: https://doi.org/10.1126/scirobotics.abn1944

Citation: Chen, B., Kwiatkowski, R., Vondrick, C., & Lipson, H. (2022). Full-body visual self-modeling of robot morphologies. *Science Robotics, 7*(68), eabn1944. https://doi.org/10.1126/scirobotics.abn1944

### Schulze and Lipson (2023) — high-DoF neural-field self-modeling

Learns a kinematic neural field from posed two-dimensional images and reports Chamfer-L2 error of about 2% of workspace dimension on a 7-DoF robot.

*How it informed the project:* provides a second modern body-model accuracy anchor and reinforces the need to separate geometry learning from diagnosis of mechanical and sensor changes.

Link: https://arxiv.org/abs/2310.03624

Citation: Schulze, L., & Lipson, H. (2023). High-degrees-of-freedom dynamic neural fields for robot self-modeling and motion planning. *NeurIPS 2023 Workshop on Symmetry and Geometry in Neural Representations*. https://arxiv.org/abs/2310.03624

### Li et al. (2025) — Neural Jacobian Fields

Learns a self-supervised visuomotor Jacobian field from robot motion observed by cameras and applies the representation to closed-loop control across diverse robot morphologies.

*How it informed the project:* demonstrates that a controller can learn body response without a hand-built kinematic model; external vision remains an optional oracle/upper-bound suite rather than the default comparator for embedded sensing.

Link: https://doi.org/10.1038/s41586-025-09170-0

Citation: Li, S., Zhang, A., Chen, B., Matusik, W., Liu, C., Rus, D., & Sitzmann, V. (2025). Controlling diverse robots by inferring Jacobian fields with deep networks. *Nature*. https://doi.org/10.1038/s41586-025-09170-0

### Murooka et al. (2024) — whole-body tactile feedback

Uses deformable distributed tactile sheets on humanoid limbs and integrates them into feedback control for intermediate-body multi-contact motion in simulation and hardware.

*How it informed the project:* establishes surface tactile sensing as a complementary channel for external contact, not a substitute for internal structural state; supports keeping full-body skin outside the smallest first experiment.

Link: https://doi.org/10.1109/LRA.2024.3475052

Citation: Murooka, M., Fukumitsu, K., Hamze, M., Morisawa, M., Kaminaga, H., Kanehiro, F., & Yoshida, E. (2024). Whole-body multi-contact motion control for humanoid robots based on distributed tactile sensors. *IEEE Robotics and Automation Letters, 9*(11), 10620–10627. https://doi.org/10.1109/LRA.2024.3475052

### MuJoCo paper, repository, and deformable-object documentation

MuJoCo is an Apache-2.0 articulated dynamics engine with maintained Windows/Python releases. Current documentation distinguishes generic 1D flexes (stretchable line elements with edge stiffness) from the cable/elastic-rod route for bending and twisting, while 3D flexes support Saint Venant–Kirchhoff solid elasticity for large displacement and small strain. The documentation does not make a generic 1D flex synonymous with a bending beam or a built-in strain sensor.

*How it informed the project:* makes a bounded single-engine articulated/deformable spike plausible, but corrected the Claim Sheet's implementation assumption: the spike must test cable/rod mechanics and, if needed, a slender 3D flex rather than assume any native flex is a beam. Virtual gauges must be derived from the simulator's independent deformation coordinates and validated against a beam/Cosserat calculation.

Links: https://github.com/google-deepmind/mujoco, https://mujoco.readthedocs.io/en/stable/modeling.html#deformable-objects, and https://mujoco.readthedocs.io/en/latest/XMLreference.html#deformable-flex-elasticity

Citation: Todorov, E., Erez, T., & Tassa, Y. (2012). MuJoCo: A physics engine for model-based control. *2012 IEEE/RSJ International Conference on Intelligent Robots and Systems*, 5026–5033. https://doi.org/10.1109/IROS.2012.6386109

### PyElastica

PyElastica is an MIT-licensed Python implementation of Cosserat-rod mechanics for assemblies of slender one-dimensional structures, supports Python 3.10+, and publishes a Zenodo software record.

*How it informed the project:* supplies a lightweight reduced-order mechanics option and an independent verification path for strain/curvature on a slender link.

Links: https://github.com/GazzolaLab/PyElastica and https://doi.org/10.5281/zenodo.7658871

Citation: Tekinalp, A., et al. (2024). *PyElastica* [Software]. Zenodo. https://doi.org/10.5281/zenodo.7658871

### SOFA framework

SOFA is an open-source interactive multiphysics/FEM framework used in biomechanics and robotics. The core is LGPL-2.1-or-later, while some applications and tutorials carry GPL terms.

*How it informed the project:* establishes a high-fidelity FEM fallback and the need for file-level license auditing if SOFA components are redistributed.

Link: https://github.com/sofa-framework/sofa

Citation: SOFA Consortium. (2026). *SOFA: Simulation Open Framework Architecture* [Software]. https://github.com/sofa-framework/sofa

### Project Chrono

Project Chrono is a BSD-3-Clause multiphysics engine supporting rigid and flexible multibody dynamics, nonlinear FEA, contacts, and a Python wrapper.

*How it informed the project:* establishes a permissively licensed combined rigid/flexible fallback. Its official Python installation path is oriented around Conda, so compatibility with the project-mandated root venv must be verified before selection.

Link: https://github.com/projectchrono/chrono

Citation: Project Chrono. (2026). *Project Chrono* [Software]. https://github.com/projectchrono/chrono

### MuJoCo Menagerie

The Menagerie is a curated collection of MuJoCo robot models with licenses recorded per model.

*How it informed the project:* may shorten articulated model setup, but reinforces that selecting a repository does not settle asset licensing; the exact chosen model must be audited.

Link: https://github.com/google-deepmind/mujoco_menagerie

Citation: Google DeepMind. (2026). *MuJoCo Menagerie* [Model collection]. https://github.com/google-deepmind/mujoco_menagerie

## Phase 1 — Claim Sheet review

### Traub et al. (2024) — evaluation of selective classifiers

Separates ordinary probability calibration from selective-classification evaluation and formalizes risk/coverage working points; it also documents why a single aggregate rejection metric can hide the trade between accepted-case error and coverage.

*How it informed the project:* tightened Slot 7 so abstention cannot inflate the primary four-way score. The Claim Sheet now scores abstentions as errors in the known-class headline metric and separately reports risk-coverage behavior, fixed working points, false abstention on known cases, and held-out-compound unknown detection.

Link: https://papers.nips.cc/paper_files/paper/2024/hash/047c84ec50bd8ea29349b996fc64af4b-Abstract-Conference.html

Citation: Traub, J., Bungert, T. J., Lüth, C. T., Baumgartner, M., Maier-Hein, K. H., Maier-Hein, L., & Jaeger, P. F. (2024). Overcoming common flaws in the evaluation of selective classification systems. *Advances in Neural Information Processing Systems 37*.

## Phase 1 — Companion-artifact review

### MuJoCo elasticity extension documentation — 1-D cable mechanics

The current first-party extension documentation distinguishes MuJoCo's one-dimensional cable elasticity model from generic flex topology. It states that the cable model captures large deformation while separating twisting and bending strains.

*How it informed the project:* replaced an indirect repository link in both companion artifacts with the documentation that directly supports the bending-capable candidate, while preserving the feasibility spike rather than implying that the candidate is already validated for this plant.

Link: https://mujoco.readthedocs.io/en/stable/programming/extension.html#elasticity

Citation: Google DeepMind. (2026). *MuJoCo documentation: Extensions — elasticity*. https://mujoco.readthedocs.io/en/stable/programming/extension.html#elasticity

### SciPy bootstrap documentation — primitive, not hierarchical design

Documents SciPy's bootstrap confidence-interval routine and its supported interval methods. It does not define this project's two-level resampling of training seeds and whole scenario/trajectory units.

*How it informed the project:* corrected the Accessible Claim Sheet and Study Guide so they no longer imply that SciPy provides the paired hierarchical design automatically. The project must implement and test that nesting explicitly while using SciPy only as a confidence-interval primitive where appropriate.

Link: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html

Citation: SciPy Developers. (2026). *scipy.stats.bootstrap documentation*. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html

### U.S. Food and Drug Administration (2016) — non-inferiority margins

Official guidance explains the purpose of non-inferiority designs, the role of a pre-specified margin, and how the corresponding hypothesis is tested.

*How it informed the project:* supplies a verified director-facing explainer for the borrowed term "non-inferiority." The project's −0.02 per-source recall guard is an engineering design constraint, not a clinical-trial claim; the citation explains the statistical analogy only.

Link: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/non-inferiority-clinical-trials

Citation: U.S. Food and Drug Administration. (2016). *Non-Inferiority Clinical Trials to Establish Effectiveness: Guidance for Industry*. https://www.fda.gov/regulatory-information/search-fda-guidance-documents/non-inferiority-clinical-trials
