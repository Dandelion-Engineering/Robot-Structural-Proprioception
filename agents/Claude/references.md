# Claude — References Ledger

Running source ledger for the **Robot Structural Proprioception** project, per the Dandelion references-file standard. Every entry: what the source covers · how it informed the project · a verified link/DOI (obtained from a real Phase 0 search — nothing cited from memory) · a citation transferable into the Technical Report bibliography.

**Status:** Phase 0 complete on Claude's side (Session 1, 2026-07-16). This is the full ledger backing my `Literature Foundation.md`. Load-bearing canonical anchors and all recent/high-risk sources were independently re-verified by me; the remainder were verified by the Phase-0 search agents (link/DOI fetched, paywalled numbers flagged). At Phase 1 start, this reconciles with Codex's ledger into the Technical Report bibliography.

Clusters: (1) self-modeling & body schema · (2) morphological intelligence · (3) adaptive/fault-tolerant control & damage recovery · (4) online system ID & fast adaptation · (5) SHM & distributed strain/fiber sensing · (6) soft-robot & tactile proprioception, artificial skin · (7) sensor-fault detection/isolation/diagnosis · (8) simulation tooling & datasets (licensed).

---

## 1. Robot self-modeling & body-schema learning

**Bongard, J., Zykov, V. & Lipson, H. 2006 — "Resilient Machines Through Continuous Self-Modeling." *Science* 314(5802):1118–1121.** https://doi.org/10.1126/science.1133687
A 4-legged robot infers its own morphology from actuation–sensation via active learning, synthesizes a gait, and re-infers the model to recover after limb damage. *Informs:* the founding template for a revisable, physically-grounded self-model that adapts to mechanical change — but uses sparse motion sensing, not distributed structural signals; the baseline the project extends.

**Kwiatkowski, R. & Lipson, H. 2019 — "Task-agnostic self-modeling machines." *Science Robotics* 4(26):eaau9354.** https://doi.org/10.1126/scirobotics.aau9354
A 4-DoF arm learns a deep self-model from ~1,000 babbling trajectories (<35 h), ~4 cm accuracy, 100% closed-loop pick-and-place; detects a 3D-printed deformation and re-trains. *Informs:* concrete damage-detection metrics and training-cost baseline for a structural-sensing self-model to beat.

**Chen, B., Kwiatkowski, R., Vondrick, C. & Lipson, H. 2022 — "Full-body visual self-modeling of robot morphologies." *Science Robotics* 7(68):eabn1944.** https://doi.org/10.1126/scirobotics.abn1944 · arXiv:2111.06389
Continuous, differentiable, query-driven visual self-model (~1% of workspace accuracy) supporting planning, damage detection/localization, and recovery. *Informs:* shows value of differentiable self-models and damage *localization*, while exposing the reliance on external vision that structural sensing would replace.

**Hu, J., Chen, B. & Lipson, H. 2025 — "Egocentric visual self-modeling for autonomous robot dynamics prediction and adaptation." *npj Robotics*.** https://doi.org/10.1038/s44182-025-00031-6 · arXiv:2207.03386
A 12-DoF legged robot learns a dynamics self-model from a single first-person camera; detects a broken leg via prediction–reality discrepancy and recovers after ~30 min of babbling; visual input cuts prediction error vs action/IMU-only. *Informs:* its action/IMU-vs-visual error comparison is a direct model for the project's "advantage beyond a conventional suite" experiment.

**Li, S., Zhang, A., Chen, B., Matusik, W., Liu, C., Rus, D. & Sitzmann, V. 2025 — "Controlling diverse robots by inferring Jacobian fields with deep networks." *Nature* (25 Jun 2025).** https://doi.org/10.1038/s41586-025-09170-0 · arXiv:2407.08722 · code https://github.com/sizhe-li/neural-jacobian-field
Self-supervised vision-to-Jacobian-field model controls diverse robots (incl. a $220 arm, soft/multi-material robots) from one camera, with no assumptions about materials/actuation and tolerance to changing material properties. *Informs:* state of the art in morphology-/material-agnostic self-models; the "works as materials change" claim is what a structural self-model should also deliver, minus the camera.

**Hoffmann, M., Marques, H., Hernandez Arieta, A., Sumioka, H., Lungarella, M. & Pfeifer, R. 2010 — "Body Schema in Robotics: A Review." *IEEE Trans. Autonomous Mental Development* 2(4):304–324.** https://doi.org/10.1109/TAMD.2010.2086454
Canonical survey bridging neuroscience body-schema/peripersonal-space concepts and robot self-representation learning from multimodal sensorimotor data. *Informs:* situates the project in the body-schema tradition and supplies the biological framing of a plastic, revisable, multimodal self-representation.

**Kawaharazuka, K., Okada, K. & Inaba, M. 2024 — "GeMuCo: Generalized Multisensory Correlational Model for Body Schema Learning." *IEEE Robotics & Automation Magazine* 32(2):80–98.** https://doi.org/10.1109/MRA.2024.3106223 · arXiv:2409.06427
Learns a sensor–actuator body schema from self-experience (including network structure), updates it online, and does state estimation, control, anomaly detection, and simulation; demoed on tool-use, a musculoskeletal robot, a low-rigidity humanoid. *Informs:* the closest prior art to a *revisable, online-updated, anomaly-detecting* body model — but proprioceptive-from-actuation, not distributed-structural; strong methodological template.

**"High-Degrees-of-Freedom Dynamic Neural Fields for Robot Self-Modeling and Motion Planning." 2023 — preprint, arXiv:2310.03624.** https://arxiv.org/abs/2310.03624
Learns a 7-DoF robot's kinematics as a neural-implicit self-model from 2D images + configs; geometry to Chamfer-L2 ≈ 2% of workspace. *Informs:* a differentiable neural-field self-model with a clean geometric-accuracy metric; vision-based, highlighting the structural-sensing gap. *(Un-refereed preprint; cited for title/ID/self-reported number only.)*

**Hu, K., Yu, P. & Tan, N. 2025 — "Learning High-Fidelity Robot Self-Model with Articulated 3D Gaussian Splatting." preprint, arXiv:2503.05398.** https://arxiv.org/abs/2503.05398
Articulated 3D Gaussian splatting for higher-fidelity visual robot self-models, evaluated in sim vs neural-field baselines. *Informs:* marks the current frontier of *visual* self-model fidelity, reinforcing that structural/proprioceptive self-modeling is the unaddressed axis. *(Un-refereed preprint.)*

## 2. Embodied / morphological intelligence

**Pfeifer, R. & Bongard, J. 2006 — *How the Body Shapes the Way We Think: A New View of Intelligence.* MIT Press.** https://mitpress.mit.edu/9780262162395/how-the-body-shapes-the-way-we-think/
Foundational monograph: body morphology and material properties actively participate in control and cognition ("morphological computation"). *Informs:* the theoretical justification for treating structural/material state as control-relevant information, not noise.

**Müller, V.C. & Hoffmann, M. 2017 — "What Is Morphological Computation? On How the Body Contributes to Cognition and Control." *Artificial Life* 23(1):1–24.** https://doi.org/10.1162/ARTL_a_00219 · open https://philarchive.org/rec/MLLWIM
Argues most cited cases are morphology *facilitating* control/perception, not genuine computation off-loaded to the body. *Informs:* keeps the framing honest — the contribution is richer *information* from structural sensing, not the body "computing"; guards against over-claiming.

## 3. Adaptive & fault-tolerant control; damage recovery

**Cully, A., Clune, J., Tarapore, D. & Mouret, J-B. 2015 — "Robots that can adapt like animals." *Nature* 521(7553):503–507.** https://doi.org/10.1038/nature14422 · arXiv:1407.3501 · code https://github.com/resibots/cully_2015_nature
Intelligent Trial-and-Error: a precomputed MAP-Elites behavior–performance map (~13,000 behaviors) + Bayesian optimization recovers a working gait in <2 min after damage, without self-diagnosis. *Informs:* the canonical *fast damage recovery* baseline that deliberately ignores the cause — sharpens the project's question of whether *diagnosing* the change beats behavior-space search.

**Nagabandi, A., Clavera, I., Liu, S., Fearing, R.S., Abbeel, P., Levine, S. & Finn, C. 2019 — "Learning to Adapt in Dynamic, Real-World Environments Through Meta-Reinforcement Learning." *ICLR 2019*.** https://arxiv.org/abs/1803.11347
Meta-learns a dynamics-model prior (GrBAL/ReBAL) that adapts online from recent data to changing dynamics (e.g., a crippled leg). *Informs:* the meta-learning route to fast dynamics adaptation; a strong learning-based baseline that adapts *dynamics* without accounting for body-vs-sensor cause.

**Kumar, A., Fu, Z., Pathak, D. & Malik, J. 2021 — "RMA: Rapid Motor Adaptation for Legged Robots." *RSS 2021*.** https://arxiv.org/abs/2107.04034
Base policy + adaptation module regresses an 8-D "extrinsics" latent from 0.5 s of proprioceptive history; adapts to payload/terrain/wear in a fraction of a second; sim-trained, deployed on A1 without fine-tuning. Sim success 73.5% vs 76.2% privileged / 62.4% domain-randomization / 56.5% system-ID. *Informs:* the dominant modern adaptation paradigm from a *conventional* proprioceptive suite — the competitor the structural-sensing hypothesis must beat or complement; also the exemplar of latent *conflation* (no source attribution).

**Quamar, M.M. & Nasir, A. 2024 — "Review on Fault Diagnosis and Fault-Tolerant Control Scheme for Robotic Manipulators: Recent Advances in AI, ML, and Digital Twin." preprint, arXiv:2402.02980.** https://arxiv.org/abs/2402.02980
Surveys model-based, signal-based, and AI/ML fault detection–isolation–recovery for manipulators. *Informs:* frames the FDIR vocabulary the project must connect online sysID to in order to attribute a change's source.

**Ben Brahim, A., Dhahri, S., Ben Hmida, F. & Sellami, A. 2017 — "Sliding Mode Observers Based Simultaneous Actuator and Sensor Faults Estimation for Linear Parameter Varying Systems." *Math. Problems in Engineering* 2017:1747095.** https://doi.org/10.1155/2017/1747095
Sliding-mode observers that simultaneously reconstruct actuator and sensor faults for LPV systems via augmented-state/coordinate-transform decoupling. *Informs:* evidence that separating actuator- from sensor-originated change is possible *only* under structural decoupling or added redundancy — the barrier distributed structural sensing is hypothesized to lower.

**Stewart-Height, A., Jahagirdar, S. & Matni, N. 2026 — "Learning-Based Fault Detection for Legged Robots in Remote Dynamic Environments." preprint, arXiv:2604.03397.** https://arxiv.org/abs/2604.03397
Offline-learned detector identifies single-limb damage from quadruped proprioception to trigger tripedal gait reconfiguration. *Informs:* recent robotics example of recognizing a *body change* and adapting — but at limb granularity, motivating finer distributed sensing.

## 4. Online system identification & fast adaptation

**Wensing, P.M., Niemeyer, G. & Slotine, J-J.E. 2024 — "A geometric characterization of observability in inertial parameter identification." *Int. J. Robotics Research* 43(12).** https://doi.org/10.1177/02783649241258215 · arXiv:1711.03896
An O(N) algorithm (RPNA) exactly classifies which inertial parameters/combinations are identifiable; unidentifiable changes = "inertial transfers" across joints that leave joint-space dynamics unchanged. *Informs:* the theoretical backbone for *why* distributed structural sensing could help — joint-space data leaves an identifiability nullspace that extra sensing could observe. **Load-bearing for Slot 3.**

**Guo, K. & Pan, Y. 2023 — "Composite adaptation and learning for robot control: A survey." *Annual Reviews in Control* 55:279–290.** https://doi.org/10.1016/j.arcontrol.2022.10.002
Surveys composite adaptation / concurrent learning / memory-regressor-extension, centering the persistent-excitation problem and how modern methods relax it to finite excitation. *Informs:* the authoritative map of the adaptive-control lineage and the PE limitation the project's experiments must design around (excitation vs. safety on a damaged body).

**Nguyen-Tuong, D., Seeger, M. & Peters, J. 2009 — "Model Learning with Local Gaussian Process Regression." *Advanced Robotics* 23(15):2015–2034.** https://doi.org/10.1163/016918609X12529286896877
Local-GP inverse-dynamics learning combining GP accuracy with real-time speed; online updates improve tracking on a Barrett WAM. *Informs:* foundational online non-parametric model-learning with *calibrated uncertainty* — a candidate substrate for a body model that carries uncertainty about its own dynamics.

**Chebbi, A., Franchek, M.A. & Grigoriadis, K. 2025 — "Simultaneous State and Parameter Estimation Methods Based on Kalman Filters and Luenberger Observers: A Tutorial & Review." *Sensors* 25(22):7043.** https://doi.org/10.3390/s25227043
Clean taxonomy of *joint* (augmented-state) vs *dual* (parallel-filter) estimation across EKF/UKF/CKF/EnKF, with the PE requirement stated explicitly. *Informs:* the reference architecture for joint state+parameter estimation the project can build on.

**O'Connell, M., Shi, G., Shi, X., Azizzadenesheli, K., Anandkumar, A., Yue, Y. & Chung, S-J. 2022 — "Neural-Fly enables rapid learning for agile flight in strong winds." *Science Robotics* 7(66):eabm6597.** https://doi.org/10.1126/scirobotics.abm6597 · arXiv:2205.06908
Meta-learns a wind-invariant DNN basis (12 min data) and adapts only a 12-D linear coefficient vector online at 50 Hz (~3 ms update), cutting tracking error 35–66% vs strong baselines. *Informs:* the "fixed basis + tiny online linear adapter" pattern with hard tracking numbers; a baseline the structural approach must justify against.

**Rakelly, K., Zhou, A., Quillen, D., Finn, C. & Levine, S. 2019 — "Efficient Off-Policy Meta-RL via Probabilistic Context Variables (PEARL)." *ICML 2019*.** https://arxiv.org/abs/1903.08254 · code https://github.com/katerakelly/oyster
Adapts by online posterior inference over a latent context variable; 20–100× more meta-training-sample-efficient than prior meta-RL. *Informs:* the nearest existing thing to a *probabilistic posterior over dynamics* — a concrete starting point to extend toward a posterior over the *source* of change.

**Lee, K., Seo, Y., Lee, S., Lee, H. & Shin, J. 2020 — "Context-aware Dynamics Model for Generalization in Model-Based RL (CaDM)." *ICML 2020*.** https://arxiv.org/abs/2005.06800
A context encoder infers a latent from 5–10 past transitions to condition a forward dynamics model; large OOD gains and bounded error under mass/length changes. *Informs:* targets *changed dynamics* via an inferred latent; single conflated latent underscores the missing source-attribution structure.

**Mei, Y., Zhou, ..., Tan, X. 2025 — "Fast Online Adaptive Neural MPC via Meta-Learning." preprint, arXiv:2504.16369.** https://arxiv.org/abs/2504.16369 · code https://github.com/yu-mei/MetaResidual-MPC
MAML-trained neural *residual* dynamics fine-tuned online (20–50 samples, ~2 Hz) under a 45–50 Hz loop; cuts prediction RMSE 49→61%, lifts cart-pole stabilization 0→100%. *Informs:* concrete recipe and the realistic adaptation-rate-vs-control-rate constraint.

**Chakrabarty, A., Wichern, G., Deshpande, V., Vinod, A.P., Berntorp, K. & Laughman, C. 2025 — "Meta-Learning for Physically-Constrained Neural System Identification." (MERL TR2025-159; *Neurocomputing*).** https://arxiv.org/abs/2501.06167
Gradient-based meta-learning adapts physically-constrained neural state-space models to a new system from few data/iterations (Bouc-Wen hysteresis; real case studies). *Informs:* bridges meta-learning and *structured* sysID — a route to keep fast adaptation physically interpretable. *(Adaptation counts stated qualitatively in source; treat as qualitative.)*

**Zhang, X., Liu, S., Huang, Y., Han, ..., Zhao, D. 2024 — "Dynamics as Prompts: In-Context Learning for Sim-to-Real System Identification (CAPTURE)." *IEEE RA-L*.** https://arxiv.org/abs/2410.20357
A causal transformer predicts next simulator parameters from interaction history (no gradient updates), improving parameter estimation 42–80% and reaching ≥70% real scooping success in ~7 iterations. *Informs:* state-of-the-art *explicit* run-time dynamics-parameter estimation; a strong interpretable-ID comparison point.

**Baek, D., et al. 2024 — "Online Learning-Based Inertial Parameter Identification of Unknown Object for Model-Based Control of Wheeled Humanoids." *IEEE RA-L*.** https://arxiv.org/abs/2309.09810
Proprioception-only learned estimator returns a full inertial set in ~0.1 s (no long excitation); NMAE mass 0.63 / Izz 0.94; 36% (manipulation) and 65% (locomotion) tracking gains on SATYRR. *Informs:* real-robot evidence that internal measurements drive fast structural-parameter estimation and improve control.

## 5. Structural health monitoring (SHM) & distributed strain/fiber sensing

**Farrar, C.R. & Worden, K. 2007 — "An introduction to structural health monitoring." *Phil. Trans. R. Soc. A* 365(1851):303–315.** https://doi.org/10.1098/rsta.2006.1928
Foundational: SHM as statistical pattern recognition; damage = change to material/geometric properties or boundary conditions; the operational-evaluation → feature → statistical-model pipeline; damage detection requires comparison of two states. *Informs:* the vocabulary and physically-grounded notion of "structural change" the project borrows — and the boundary (SHM stops before control) the project crosses.

**Worden, K., Farrar, C.R., Manson, G. & Park, G. 2007 — "The fundamental axioms of structural health monitoring." *Proc. R. Soc. A* 463(2082):1639–1664.** https://doi.org/10.1098/rspa.2007.1834
States the field's axioms (damage assessment requires comparison; sensors don't measure damage directly; feature extraction/normalization is central). *Informs:* constraints any credible self-sensing scheme must respect — especially the baseline-comparison requirement driving the EOV/false-alarm problem.

**Mitra, M. & Gopalakrishnan, S. 2016 — "Guided wave based structural health monitoring: A review." *Smart Mater. Struct.* 25(5):053001.** https://doi.org/10.1088/0964-1726/25/5/053001
State-of-the-art review of guided-wave generation/sensing/imaging and dispersion/multi-mode challenges. *Informs:* scopes what an embedded PZT/guided-wave layer could detect (small local defects) and its cost (dense networks, hard localization).

**Capineri, L., Taddei, L. & Marino Merlo, E. 2024 — "Detection of a Submillimeter Notch-Type Defect at Multiple Orientations by a Lamb Wave A0 Mode at 550 kHz." *Sensors* 24(6):1926.** https://doi.org/10.3390/s24061926
Detects a 100 µm-wide × 3 mm-deep notch in a 4.1 mm Al plate with A0 @550 kHz over 0.35–0.7 m. *Informs:* concrete sensitivity/range numbers to bound a simulated guided-wave modality.

**Azimi, M., Eslamlou, A.D. & Pekcan, G. 2020 — "Data-Driven SHM and Damage Detection through Deep Learning: State-of-the-Art Review." *Sensors* 20(10):2778.** https://doi.org/10.3390/s20102778
Surveys CNN/RNN/autoencoder/GAN SHM (e.g., 99.46% loose-bolt) and flags the absence of standard datasets and poor field generalization. *Informs:* justifies a simulation-first, label-rich approach and warns about baseline/EOV brittleness in learned detectors.

**Na, W.S. & Baek, J. 2018 — "A Review of the Piezoelectric Electromechanical Impedance-Based SHM Technique for Engineering Structures." *Sensors* 18(5):1307.** https://doi.org/10.3390/s18051307
EMI operates ~30–400 kHz (RMSD/MAPD/CC indices), detects incipient/local damage, but is temperature-sensitive and localization-limited. *Informs:* characterizes a high-frequency, very-local self-sensing option and its false-alarm/temperature limits.

**Barrias, A., Casas, J.R. & Villalba, S. 2016 — "A Review of Distributed Optical Fiber Sensors for Civil Engineering Applications." *Sensors* 16(5):748.** https://doi.org/10.3390/s16050748
Tabulates DOFS trade-offs: OFDR/Rayleigh ~1 mm res (50–70 m); BOTDR 5 µε, ~1 m, 20–50 km; BOTDA 2 cm–2 m over 150–200 km; detectability scales with sensor density, damage size, load. *Informs:* the primary quantitative basis for credible distributed-strain resolution/range in the simulation, and the "many channels cross-check" analytical-redundancy idea.

**Silveira, M.L., et al. 2021 — "An Optimized Self-Compensated Solution for Temperature and Strain Cross-Sensitivity in FBG Interrogators Based on Edge Filter." *Sensors* 21(17):5828.** https://doi.org/10.3390/s21175828
FBG strain sensitivity 1.2 pm/µε, temperature 12 pm/°C (⇒ ~10 µε/°C cross-sensitivity). *Informs:* canonical FBG numbers and the temperature cross-sensitivity the simulation must include rather than idealize away.

**Galloway, K.C., et al. 2019 — "Fiber Optic Shape Sensing for Soft Robotics." *Soft Robotics* 6(5):671–684.** https://doi.org/10.1089/soro.2018.0131
OFDR multicore fiber inside a soft actuator: strain every 0.8 mm, up to 250 Hz, sub-mm/sub-degree shape reconstruction; open-loop only. *Informs:* the closest existing "distributed strain → body state" system in robotics; evidence that closed-loop use of it is still open.

**Johnson, E.A., Lam, H.F., Katafygiotis, L.S. & Beck, J.L. 2004 — "Phase I IASC-ASCE Structural Health Monitoring Benchmark Problem Using Simulated Data." *J. Eng. Mech.* 130(1):3–15.** https://doi.org/10.1061/(ASCE)0733-9399(2004)130:1(3)
Defines the shared 4-story steel-frame benchmark (12-DOF and 120-DOF models, damage patterns, sensor/noise specs). *Informs:* a standard structural testbed and damage-scenario template a simulation can emulate for comparability.

**Peeters, B. & De Roeck, G. 2001 — "One-year monitoring of the Z24-Bridge: environmental effects versus damage events." *Earthquake Eng. Struct. Dyn.* 30(2):149–171.** https://doi.org/10.1002/1096-9845(200102)30:2<149::AID-EQE1>3.0.CO;2-Z
Year-long modal data; bilinear temperature–frequency dependence; environmental swings (first mode ~10%) rival/exceed damage signatures. *Informs:* the quantitative anchor for the temperature-masks-damage confound the self-recognition system must overcome — inject Z24-scale drift so the problem is realistically hard.

**Figueiredo, E., Park, G., Figueiras, J., Farrar, C. & Worden, K. 2009 — "Structural Health Monitoring Algorithm Comparisons Using Standard Data Sets." LANL report LA-14393** (companion: *Structural Health Monitoring* 10(6), 2011, https://doi.org/10.1177/1475921710388971). https://www.osti.gov/biblio/961604
The open Los Alamos three-story-structure dataset (4-DOF frame, bumper-induced nonlinear "damage," 5 channels @322.58 Hz) + 4 ML baselines under EOV. *Informs:* a downloadable damage/EOV dataset and ready ML baselines for benchmarking a detector.

## 6. Soft-robot & tactile proprioception; artificial skin

**Wang, T., Xie, ..., Laschi, C. 2024 — "Sensing expectation enables simultaneous proprioception and contact detection in an intelligent soft continuum robot." *Nature Communications* 15:9978.** https://doi.org/10.1038/s41467-024-54327-6
Predicts expected shape from internal sensing and flags the prediction–measurement *residual* as external contact: 1.4% shape error, <0.4 s contact detection, <10° direction error, vision-free. *Informs:* the single closest published mechanism to the project's idea — a self-model residual doing double duty; directly adaptable from "external contact" to "internal fault/change." **Load-bearing.**

**Han, ..., Bruder, D. 2025 — "An Enhanced Proprioceptive Method for Soft Robots Integrating Bend Sensors and IMUs." preprint, arXiv:2511.01165.** https://arxiv.org/abs/2511.01165
Kalman fusion of bend sensors + IMUs: 16.96 mm (2.91%) RMSE, 56% better than IMU-only, stable over 45 min by mutually cancelling drift. *Informs:* a template for complementary multi-modal fusion that fights drift — the confound the project must manage to separate drift from structural change.

**Yoo, ..., Ichnowski, J. 2025 — "KineSoft: Learning Proprioceptive Manipulation Policies with Soft Robot Hands." preprint, arXiv:2503.01078.** https://arxiv.org/abs/2503.01078
Internal strain array gives occlusion-free shape estimation feeding a shape-conditioned diffusion policy; beats imitation baselines. *Informs:* internal proprioceptive sensing directly driving a control policy — evidence for the "adaptive-control advantage of internal sensing" hypothesis.

**Baaij, T., Della Santina, C., et al. 2023 — "Learning 3D shape proprioception for continuum soft robots with multiple magnetic sensors." *Soft Matter* 19(1):44–56.** https://doi.org/10.1039/D2SM00914E · code https://github.com/tud-phi/promasens
Magnet + 3 magnetoresistive sensors + kinematic-prior net; ~4.5% mean relative shape error, data-efficient. *Informs:* a compact, drift-resistant modality and a physics-informed-learning recipe for sparse sensing. *(4.5% figure as-reported via search index.)*

**Feliu-Talegon, D., Adamu, Y.A., Mathew, A.T., Alkayas, A.Y. & Renda, F. 2025 — "Advancing Soft Robot Proprioception Through 6D Strain Sensors Embedding." *Soft Robotics*.** https://doi.org/10.1089/soro.2024.0017
Embeds distributed 6D strain sensors (bending, torsion, shear, elongation) and reconstructs configuration via a Cosserat/strain-parameterized model. *Informs:* the most complete distributed structural-modality set in the soft-robot camp — a menu of the measurements the project proposes and a modeling backbone. *(Publisher blocked fetch; cited for method, no numeric claim asserted.)*

**Kushawaha, S., et al. 2025 — "Adaptive Drift Compensation for Soft Sensorized Finger Using Continual Learning." preprint, arXiv:2503.16540.** https://arxiv.org/abs/2503.16540
Quantifies sensor drift (baseline RMSE 1.67–17.79°) and cuts it to 2.07–6.43° with continual learning (R²>0.90). *Informs:* the best quantitative handle on drift and a candidate online compensator — central to distinguishing sensor degradation from true structural change.

**Monet, F., et al. 2020/2021 — "High-Resolution Optical Fiber Shape Sensing of Continuum Robots: A Comparative Study."** https://pmc.ncbi.nlm.nih.gov/articles/PMC8375516/
Benchmarks FBG vs OFDR/ROGUE fiber shape sensing: FBG tip error 0.83/0.80/2.27 mm (free/obstacle/S-bend); OFDR ~2× better. *Informs:* sets the accuracy ceiling (and cost/stiffness price) for optical structural sensing on a rigid-ish body.

**Van Meerbeek, I.M., De Sa, C.M. & Shepherd, R.F. 2018 — "Soft optoelectronic sensory foams with proprioception." *Science Robotics* 3(24):eaau2489.** https://doi.org/10.1126/scirobotics.aau2489
Internally illuminated elastomer foam + ML classifies deformation type at 100% and predicts magnitude at 0.06° MAE. *Informs:* proof that *distributed internal structural sensing* can drive an accurate learned model of body deformation — the sensing paradigm the project extends into self-modeling.

**Thuruthel, T.G., Shih, B., Laschi, C. & Tolley, M.T. 2019 — "Soft robot perception using embedded soft sensors and recurrent neural networks." *Science Robotics* 4(26):eaav1488.** https://doi.org/10.1126/scirobotics.aav1488
Embedded soft sensors + RNN infer configuration and external load for a soft robot. *Informs:* foundational embedded-sensor + temporal-learning recipe for proprioception from distributed internal signals.

**Marques Monteiro, R., Shi, J., Wurdemann, H., Iida, F. & George Thuruthel, T. 2024 — "Visuo-dynamic self-modelling of soft robotic systems." *Frontiers in Robotics and AI*.** https://doi.org/10.3389/frobt.2024.1403733
End-to-end LSTM+VAE self-model of a 2-segment pneumatic soft robot from 90 min babbling; validation MSE ≈ 0.02; struggles with high-frequency dynamics. *Informs:* demonstrates self-modeling of a *deformable* body and quantifies its limits.

**Yuan, W., Dong, S. & Adelson, E.H. 2017 — "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force." *Sensors* 17(12):2762.** https://doi.org/10.3390/s17122762
Camera-over-elastomer sensor: ~1–2 µm lateral resolution, 18×14 mm area, <0.05 N sensitivity. *Informs:* the canonical *external* high-resolution tactile modality — the contrast case for internal structural proprioception.

**Lambeta, M., Chou, P-W., Tian, S., et al. 2020 — "DIGIT: A Novel Design for a Low-Cost Compact High-Resolution Tactile Sensor with Application to In-Hand Manipulation." *IEEE RA-L* 5(3):3838–3845.** https://doi.org/10.1109/LRA.2020.2977257 · arXiv:2005.14679
Low-cost open-source fingertip visuotactile sensor; open hardware + software ecosystem. *Informs:* reference open-hardware tactile platform anchoring the TACTO/Taxim sim stack; the external-contact toolchain the project contrasts against.

**Wang, S., Lambeta, M., Chou, P-W. & Calandra, R. 2022 — "TACTO: A Fast, Flexible, and Open-Source Simulator for High-Resolution Vision-Based Tactile Sensors." *IEEE RA-L* 7(2):3930–3937.** https://doi.org/10.1109/LRA.2022.3146945 · code https://github.com/facebookresearch/tacto (**MIT**)
Renders DIGIT/OmniTact at 200 fps; cylinder pose sim-to-real 4.56→0.52 mm with augmentation + real data. *Informs:* benchmark for the tactile sim-to-real gap and a model for the *kind* of shared simulator internal-proprioception currently lacks.

**Si, Z. & Yuan, W. 2022 — "Taxim: An Example-Based Simulation Model for GelSight Tactile Sensors." *IEEE RA-L* 7(2):2361–2368.** https://doi.org/10.1109/LRA.2022.3141221 · code https://github.com/CMURoboTouch/Taxim (**MIT**)
Example-based optical + marker simulation calibrated from <100 real points. *Informs:* data-efficient calibration idea transferable to calibrating internal structural-sensor models.

**Mittendorfer, P. & Cheng, G. 2015 — "Realizing whole-body tactile interactions with a self-organizing, multi-modal artificial skin on a humanoid robot." *Advanced Robotics* 29(1):51–63.** https://doi.org/10.1080/01691864.2014.952493
HEX-o-SKIN: multimodal hexagonal cells (temperature, 3-axis accel, proximity, force), 1 kHz local processing, mesh networking that slashes wiring. *Informs:* the reference architecture for scaling distributed sensing over a whole body, and the wiring/networking constraints a distributed structural suite faces.

**Ozaki, K., et al. 2025 — "Self-rerouting sensor network for electronic skin resilient to severe damage." *Nature Communications*.** https://pmc.ncbi.nlm.nih.gov/articles/PMC11782484/
Distributed nodes autonomously reroute readout after cuts; demoed on 64-node grids and a 96-node 3D structure. *Informs:* closest tactile-side fault tolerance — but preserves *external* readout, not structural self-knowledge; sharpens where the project's internal-diagnosis contribution differs.

## 7. Sensor-fault detection, isolation & diagnosis (FDI/FDD)

**Hwang, I., Kim, S., Kim, Y. & Seah, C.E. 2010 — "A Survey of Fault Detection, Isolation, and Reconfiguration Methods." *IEEE Trans. Control Systems Technology* 18(3):636–653.** https://doi.org/10.1109/TCST.2009.2026285
The canonical FDIR survey: model-based FDI (observers, parity space, parameter estimation) + controller reconfiguration. *Informs:* the taxonomy and vocabulary for positioning the project and its conventional-sensor baseline.

**Gao, Z., Cecati, C. & Ding, S.X. 2015 — "A Survey of Fault Diagnosis and Fault-Tolerant Techniques—Part I: Model-Based and Signal-Based Approaches." *IEEE Trans. Industrial Electronics* 62(6):3757–3767.** https://doi.org/10.1109/TIE.2015.2417501
Comprehensive review splitting diagnosis into model-based and signal-based branches. *Informs:* broad reference for method selection and contrasting model-based residuals with data-driven diagnosis.

**Patton, R.J. & Chen, J. 1994 — "Review of parity space approaches to fault diagnosis for aerospace systems." *J. Guidance, Control, and Dynamics* 17(2):278–285.** https://doi.org/10.2514/3.21194
Tutorial establishing parity-space residual generation and its robustness/isolation problems. *Informs:* the analytical-redundancy formalism the project would extend to distributed structural channels.

**Marzat, J., Piet-Lahanier, H., Damongeot, F. & Walter, E. 2012 — "Model-based fault diagnosis for aerospace systems: a survey." *Proc. IMechE Part G* 226(10):1329–1360.** https://doi.org/10.1177/0954410011421717 · open https://hal.science/hal-00615617
Observer/parity/parameter-estimation FDI with strong emphasis on robustness to model uncertainty/disturbance. *Informs:* directly addresses distinguishing faults from modeling error/disturbance — the sensor-vs-plant ambiguity.

**Paviglianiti, G., Pierri, F., Caccavale, F. & Mattei, M. 2010 — "Robust fault detection and isolation for proprioceptive sensors of robot manipulators." *Mechatronics* 20(1):162–170.** https://doi.org/10.1016/j.mechatronics.2009.09.003
Observer-bank analytical-redundancy scheme (extended H∞ + RBF compensation) detecting/isolating position- and velocity-encoder faults. *Informs:* the closest classical baseline — proprioceptive-sensor FDI on a robot — that the distributed-structural approach must outperform.

**D'Amato, E., Nardi, V.A., Notaro, I. & Scordamaglia, V. 2021 — "A Particle Filtering Approach for Fault Detection and Isolation of UAV IMU Sensors." *Sensors* 21(9):3066.** https://doi.org/10.3390/s21093066
Particle-filter residual FDI for UAV IMUs: 99.50% correct / 0.00% wrong detection, 0.27 s detection on abrupt bias, across five fault modes; 68 ms on a Raspberry Pi 3B. *Informs:* a quantitative baseline for IMU fault detection and a template for the fault-mode battery (bias, drift, stuck, oscillation, random walk).

**Sravani, V. & Venkata, S.K. 2023 — "Detection of Sensor Faults with or without Disturbance Using Analytical Redundancy Methods." *Sensors* 23(14):6633.** https://doi.org/10.3390/s23146633
LPV-observer FDI tested with and without a real process disturbance; <0.5 s detection for open/short faults, 5.2–20 s for drift; adaptive 10–15% thresholds to cut false alarms. *Informs:* the clearest worked example of separating a sensor fault from a genuine plant disturbance — the core disambiguation problem.

**Deng, Z., Zhang, Z., Ding, Z. & Liu, B. 2025 — "Multi-Source, Fault-Tolerant, and Robust Navigation Method for Tightly Coupled GNSS/5G/IMU System." *Sensors* 25(3):965.** https://doi.org/10.3390/s25030965
Robust adaptive Kalman fusion with full-source fault detection/exclusion: 0.83 m (1σ), 28.3%/53.1% improvement over EKF/multi-rate KF. *Informs:* fault-tolerant multi-sensor fusion quantifying the estimation benefit of an FDE layer.

**Li, Z., Zhao, Y., Ma, J., Ai, J. & Dong, Y. 2022 — "Fault Detection and Classification of Aerospace Sensors using a VGG16-based Deep Neural Network." preprint, arXiv:2207.13267.** https://arxiv.org/abs/2207.13267
Image-stacked CNN classifier: 98.90% sensor-fault classification across 4 aircraft × 5 flight conditions, ~26 ms inference. *Informs:* a data-driven upper-bound reference for multi-mode sensor-fault classification.

**Haldimann, D., Guerriero, M., Maret, Y., Bonavita, N., Ciarlo, G. & Sabbadin, M. 2019 — "A scalable algorithm for identifying multiple sensor faults using disentangled RNNs." preprint, arXiv:1909.02449.** https://arxiv.org/abs/1909.02449
Isolates multiple simultaneously-faulty sensors, mitigating "smearing-out," with complexity linear in sensor count. *Informs:* the algorithmic primitive for using many distributed channels as mutual cross-checks and localizing which changed.

**Zhou, T., Droguett, E.L., Mosleh, A. & Chan, F.T.S. 2021/2023 — "An Uncertainty-Informed Framework for Trustworthy Fault Diagnosis in Safety-Critical Applications." preprint arXiv:2111.00874; *Reliability Eng. & System Safety* 229:108865.** https://arxiv.org/abs/2111.00874
Bayesian CNN separating epistemic vs aleatoric uncertainty and flagging OOD inputs; tested on unknown-fault and four common sensor-fault OOD scenarios. *Informs:* state of the art for representing uncertainty about *whether/what* fault occurred — the basis to extend toward *source* attribution (structure vs actuator vs sensor). **Load-bearing for Slot 3.**

**Hendriks, J., Dumond, P. & Knox, D.A. 2022 — "Towards better benchmarking using the CWRU bearing fault dataset." *Mechanical Systems and Signal Processing* 169:108732.** https://doi.org/10.1016/j.ymssp.2021.108732
Shows the standard CWRU train/test protocol reuses the same physical bearings, so it is not a true domain shift and inflates reported accuracy (honest evaluation collapses to ~30–45%). *Informs:* methodological warning to design honest, leakage-free evaluation and treat published data-driven FDD accuracies skeptically.

## 8. Simulation environments, tooling & datasets (licensed)

*All licenses verified from the official repo/site during Phase 0. This project runs in simulation on one Windows 11 desktop (Ryzen 7 8700F, RTX 5060 Ti 16 GB, 32 GB RAM, Python 3.12). The realistic architecture is **hybrid**: a fast rigid-body engine supplies joint torques / contact forces / body accelerations, which drive a reduced-order structural model (analytical modal beam, PyElastica Cosserat rods, or a precomputed FEM reduced basis) to synthesize distributed strain/curvature/vibration; full FEM is reserved for offline ground-truth and validation.*

**Physics / RL engines (rigid-body):**
- **MuJoCo** — Apache-2.0 — https://github.com/google-deepmind/mujoco — native-Windows, rich native sensor suite (touch, force-torque, IMU, joint pos/vel), flex deformables. *Primary engine candidate.*
- **MJX (MuJoCo-XLA)** — Apache-2.0 — https://mujoco.readthedocs.io/en/stable/mjx.html — GPU/JAX batched, differentiable; GPU needs WSL2 on this box.
- **MuJoCo Playground** — Apache-2.0 — https://github.com/google-deepmind/mujoco_playground — 50+ GPU RL envs; WSL2 for GPU.
- **MuJoCo Menagerie** — Apache-2.0 (per-model licenses) — https://github.com/google-deepmind/mujoco_menagerie — curated robot models to instrument.
- **dm_control** — Apache-2.0 — https://github.com/google-deepmind/dm_control — standard continuous-control tasks.
- **Gymnasium / Gymnasium-Robotics** — MIT — https://github.com/Farama-Foundation/Gymnasium — RL API + baseline envs.
- **PyBullet / Bullet3** — zlib — https://github.com/bulletphysics/bullet3 — native-Windows, contact/joint readouts.
- **Isaac Sim** — mixed (OSS app + NVIDIA license on some materials — verify before commercial reliance) — https://github.com/isaac-sim/IsaacSim — native-Windows GPU, PhysX FEM deformables; RTX 5060 Ti = 16 GB VRAM floor.
- **Isaac Lab** — BSD-3-Clause — https://github.com/isaac-sim/IsaacLab — current NVIDIA RL stack (Isaac Gym Preview is EOL).
- **Genesis** — Apache-2.0 — https://github.com/Genesis-Embodied-AI/Genesis — multi-physics (rigid+FEM+MPM+…); Linux-favored, partial Windows.
- **Brax** — Apache-2.0 — https://github.com/google/brax — JAX differentiable, massively parallel; GPU via WSL2.
- **Drake** — BSD-3-Clause — https://drake.mit.edu — model-based dynamics/control; Windows via WSL only.
- **DART** — BSD-2-Clause — https://github.com/dartsim/dart — white-box Featherstone dynamics.
- **Gazebo (gz-sim)** — Apache-2.0 — https://github.com/gazebosim/gz-sim — ROS-ecosystem; partial Windows.

**Deformable / FEM / structural (for credible strain/curvature/vibration):**
- **PyElastica** — MIT — https://github.com/GazzolaLab/PyElastica — Cosserat rods → curvature/bend/twist/shear strain + vibration on slender links; native-Windows, CPU-cheap. *Best-fit reduced-order structural model.*
- **SOFA** — LGPL-2.1-or-later — https://github.com/sofa-framework/sofa — real-time FEM soft bodies; Linux-favored; offline ground-truth.
- **FEniCSx (DOLFINx)** — LGPL-3.0-or-later — https://fenicsproject.org — general FEM → strain fields; Linux/WSL-favored.
- **NVIDIA Warp** — Apache-2.0 — https://github.com/NVIDIA/warp — GPU differentiable Python sim kernels; native-Windows + CUDA.
- **Taichi / DiffTaichi** — Apache-2.0 — https://github.com/taichi-dev/taichi ; https://github.com/taichi-dev/difftaichi — parallel/differentiable physics DSL; native-Windows + CUDA.

**Newbury, R., Collins, J., et al. 2024 — "A Review of Differentiable Simulators." *IEEE Access*.** https://doi.org/10.1109/ACCESS.2024.3425448
Documents that contact gradients are discontinuous at impact and zero when separated. *Informs:* grounds the honest assessment that end-to-end differentiability through contact/deformation is immature — not a foundation to depend on.

**Datasets:**
- **LUMO** — CC-BY-3.0 — https://data.uni-hannover.de/dataset/lumo — real lattice tower: strain gauges + accelerometers + temperature + reversible damage states + companion FE model. *Best openly-licensed real distributed-structural dataset; validation/calibration + sensor-model reference.*
- **IASC-ASCE / LANL SHM benchmarks** — openly available (verify per-dataset terms) — https://www.osti.gov/biblio/961604 — standard structural-response data under damage (see Johnson 2004, Figueiredo 2009 above).
- **Z24 Bridge (SIMCES)** — research-open (KU Leuven) — the temperature-vs-damage reference dataset (see Peeters & De Roeck 2001 above).
- **CWRU Bearing Data Center** — **no formal license** (publicly downloadable; commercial terms unclear — caveat) — https://engineering.case.edu/bearingdatacenter — bearing-fault vibration benchmark. Use with the Hendriks 2022 leakage caveat.

---

*Living-bibliography pointer:* `github.com/linchangyi1/Awesome-Touch` — curated, maintained index of tactile sensors/datasets/simulators (surfaced during Phase 0; useful for Phase 1 tactile scoping).

---

## Phase 1 — Claim Sheet companion artifacts (Session 3)

*Sources used while writing the Accessible Claim Sheet and Study Guide Pass 1. The evaluation/stats tool docs below are logged now (per the "cite when fresh" standard) because they are both reader-facing concept explainers in those artifacts and the implementations the Slot-7 metrics will use; their canonical software-paper citations (scikit-learn: Pedregosa et al., JMLR 2011; SciPy: Virtanen et al., Nature Methods 2020) are the bibliography targets, to be finalized at the Phase-2 references reconciliation. Doc-page URLs below were fetched/verified this session.*

**Traub, J., Bungert, T. J., Lüth, C. T., Baumgartner, M., Maier-Hein, K. H., Maier-Hein, L. & Jaeger, P. F. 2024 — "Overcoming common flaws in the evaluation of selective classification systems." *NeurIPS 37*.** https://papers.nips.cc/paper_files/paper/2024/hash/047c84ec50bd8ea29349b996fc64af4b-Abstract-Conference.html
Separates probability calibration from selective-classification evaluation, formalizes risk/coverage working points, and shows a single aggregate rejection metric can hide the accepted-error-vs-coverage trade (proposes AUGRC). *Informs:* my angle here is director-facing framing — it grounded how I explained, in both the Accessible Claim Sheet (Slot 7) and Study Guide Pass 1, *why* calibration, selective prediction, and unknown detection are reported as three separate things and why known-class abstention is scored as an error in the headline macro-F1. (Codex's ledger holds the same source from the contract-editing angle; the divergence is intended.) Title/authors independently re-verified this session via the NeurIPS page.

**scikit-learn — `f1_score` / macro-averaging documentation.** https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html
Precise, runnable definition of F1 (harmonic mean of precision and recall) and macro-averaging (unweighted mean across classes, so rare classes count equally). *Informs:* the verified plain-language explainer link for the headline diagnosis metric (four-way macro-F1) in both companion artifacts; the implementation the Slot-7 diagnosis layer will use. Bibliography target: Pedregosa et al. 2011 (confirm at reconciliation).

**scikit-learn — probability calibration / reliability diagrams documentation.** https://scikit-learn.org/stable/modules/calibration.html
Defines calibration operationally (a well-calibrated classifier's stated confidence matches its empirical accuracy) and reliability diagrams. *Informs:* the verified explainer for the calibration metrics (Brier/NLL/ECE + reliability diagrams) in Slot 7; the tooling reference for that metric family.

**SciPy — `scipy.stats.bootstrap` documentation.** https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
Bootstrap confidence intervals (percentile / basic / BCa), one- and two-sided. *Informs:* the verified explainer for the paired hierarchical-bootstrap 95% intervals the confirmatory analysis relies on (Slot 7 / Slot 11); the implementation reference for the "interval excludes zero" success criterion. Bibliography target: Virtanen et al. 2020 (confirm at reconciliation).

---

## Phase 2 — Sensor-realism + fault-injection model (Session 6)

*No new sources this session; the sensor model was built from sources already in this ledger. Recording the source-to-implementation mapping now, while it is fresh, so the Technical Report's sensor-model methods section can cite the justification for each pathology rather than reconstruct it later. Implementation: `Reproducibility Packet/scripts/utils/sensor_model.py`.*

- **Thermal apparent strain (~10 µε/°C).** Implemented as `gauge_obs += thermal_coeff · (temperature_true − T_ref)`, `thermal_microstrain_per_c = 10.0`. Justified by **Silveira et al. 2021** (FBG 1.2 pm/µε, 12 pm/°C ⇒ ~10 µε/°C cross-sensitivity; §5 above). This is the load-bearing confound — idealizing it away would manufacture S's advantage, so it is a default-on pathology, not optional.
- **Gauge noise floor (~1 µε).** Additive Gaussian at `gauge_noise_microstrain = 1.0`. Justified by **Barrias et al. 2016** (distributed optical-fiber strain resolution figures; §5) and consistent with the FBG resolution scale the Claim Sheet's credibility floor uses.
- **Random-walk drift.** Gauge/bias drift modeled as a variance-linear-in-time random walk (step std `rate·√dt`). Grounded in **Kushawaha et al. 2025** (quantified soft-sensor drift and continual-learning compensation; §6) and the **Peeters & De Roeck 2001 / Z24** environmental-drift-rivals-damage evidence (§5) — the drift-vs-true-change confound the estimator must overcome.
- **Encoder fault battery (bias / drift / dropout), observation-path only.** The `FaultSpec` sensor subtypes and their relational signature (encoder lies; gauge/IMU physical history untouched) follow **D'Amato et al. 2021** (IMU/encoder fault-mode battery: bias, drift, stuck, oscillation, random walk; §7) and **Paviglianiti et al. 2010** (proprioceptive-sensor FDI as analytical redundancy; §7). The relational-signature design is the schema's Slot-9 statement of analytical redundancy in miniature.
- **Hysteresis as first-order lag — simplification, flagged.** Gauge hysteresis/creep is modeled as a causal first-order IIR (`first_order_lag`), a deliberate reduction of the full rate-dependent hysteresis loop. **Chakrabarty et al. 2025** (physically-constrained neural sysID on **Bouc-Wen** hysteresis; §4) is the reference for the richer model; the first-order lag is the smallest-sufficient stand-in for now (Efficiency standard) and is a candidate to revisit if hysteresis proves to matter for attribution. Noted as a modeling simplification, not a claim that gauge hysteresis is first-order.
- **Common random numbers.** The paired-comparison variance-reduction technique (matched exogenous draws across the C1/S pair) is standard simulation practice; its role for the paired hierarchical bootstrap is anchored by the **SciPy bootstrap** entry above (Slot 7). Implementation: independent per-`(sensor_seed, pair_id, channel, stream)` generators in `utils/rng.py`.
