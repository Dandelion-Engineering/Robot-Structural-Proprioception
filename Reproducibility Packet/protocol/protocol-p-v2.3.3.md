# Protocol P — v2.3.3

**A pre-registered screen for whether the delivered diagnostic probe can make a
structural stiffness-loss fault detectable above the healthy run-to-run null.**

| | |
|---|---|
| Version | v2.3.3 (= v2.3.2 + the Session-43 identifier-binding corrections; no scientific change) |
| Author | Claude |
| Reviewer | Codex (owns `scripts/utils/assignment_generator.py`) |
| Status | **PENDING REVIEWER APPROVAL — NOTHING IN THIS PROTOCOL HAS BEEN RUN** |
| Phase | 2 (Execution) |
| Contract | `Claim Sheet.md`, schema v1.0 + Amendment A1 |

**Supersedes v2.3.2** (canonical sha256
`9d25701796a039d55fcff02b68e2c665a0e492888850dd20bb1e31cf738ba6e5`, 50,169 bytes),
which was approved by Claude and **blocked by Codex** on 2026-07-29 17:22 PDT under
`BLOCK_PROTOCOL_P_V2_3_2_PENDING_STAGE0_IDENTITY_PAYLOAD_BINDING`. Codex confirmed in
the same review that all four Session-41 findings are corrected in v2.3.2 and
independently reproduced every byte measurement in §0 and §7; the block was on one new
defect, corrected here as Correction 8.

Neither v2.3.1 nor v2.3.2 was ever executed — no identity generated, no statistic
computed, no artifact written — so nothing is bound to either digest. Each survives as
a prior revision of this file in git history (v2.3.1 committed `Claude Session 41`,
v2.3.2 committed `Claude Session 42`) and neither needs a separate archive copy. The
version number is bumped and the file renamed rather than edited in place, so that the
transcript's approve/block record refers to exactly one byte-state per version name.

## 0. Status, scope, and what this document is for

This file is the complete operative state of Protocol P. It exists because a
pre-registration that lives only in a chat transcript cannot be hashed, cannot be
reviewed as an object, and — as Session 41 demonstrated — can silently disagree with
the prototype that was supposed to implement it. The v2.3 text named a `FaultSpec`
construction that omitted `onset_index`; the S40 prototype passed `onset_index=500`
explicitly. Both were internally consistent and they contradicted each other. The
executable text is what a reader who did not write it would run, so the text was the
defect.

Two hard scope statements:

- **Nothing here has been executed.** No Protocol-P identity has been generated, no
  Protocol-P statistic computed, no dataset-role artifact written.
- **Every artifact this protocol produces is a `dev-` screen artifact** and is
  permanently ineligible for confirmatory analysis. Protocol P cannot establish the
  project's hypothesis. It decides whether a structural fault is *measurable at all*
  at the delivered excitation, which determines whether the confirmatory design has a
  testable structural stratum.

### Terms used in this file

This file is standalone: it must be executable by a reader who has seen none of the
discussion that produced it. Every abbreviation it uses is therefore defined here.

```text
EI            flexural rigidity (elastic modulus x second moment of area), the
              stiffness quantity a link-softening fault reduces
remEI v       "remaining EI" — the structural fault's severity expressed as the
              FRACTION of nominal flexural rigidity that survives. remEI 0.35 is a
              severe fault; remEI 0.90 is mild. This is exactly
              CableModelConfig.structural_ei_remaining, and exactly FaultSpec.severity
              for a structural fault.
D(v,c)        the operative statistic (§8): the L2 norm of the matched fault-minus-
              healthy 0.8 Hz harmonic coefficient difference across four gauges, for
              ladder value v in context cell c. 8 entries.
Q95_c         the operative per-cell null (§8, Stage C): the 0.95 quantile,
              method="higher", of the 28 within-cell healthy pairwise distances.
Q95_c^gauge   the gauge-only fixed-trace redraw of that null (§9). A no-authority
              descriptive secondary; it gates nothing and sets no threshold.
OOD           out-of-distribution — the reserved compound/held-out settings at
              remEI 0.45/0.55, carrying ood_flag=true and excluded from four-way
              known-class macro-F1 (§9, "OOD role pinned").
CRN           common random numbers — matching the sensor RNG identity across two
              rollouts so the sensor term cancels in their difference.
```

**Two retired abbreviations are named so they cannot be silently reintroduced.**
`T1` was a candidate Stage-A amplitude cutoff from an earlier draft; **it is retired and
this protocol has no such cutoff** (§8, Stage A selection). `M2` was transcript
shorthand that at different times meant two incompatible things — a descriptive
fixed-trace gauge-only check *and* the operative mechanics rule. **Neither token denotes
anything in this file.** Each appears only here and in Corrections 4–5, which are about
their retirement; every object they once stood for is now named in full at every
occurrence.

### Two hash domains — text and binary are not interchangeable

This protocol pins files of two different kinds, and applying the wrong helper to
either one breaks it. The domains are disjoint and each file belongs to exactly one:

```text
canonical_text_sha256(path)        DOMAIN: tracked text
  raw = path.read_bytes()
  if raw.startswith(b"\xef\xbb\xbf"): raw = raw[3:]     # strip UTF-8 BOM
  return sha256(raw.replace(b"\r\n", b"\n")).hexdigest()  # fold CRLF -> LF

  applies to exactly:
    protocol/protocol-p-v2.3.3.md              (this file)
    config/proposed-gate3-assignment-v0.1.json

raw_file_sha256(path)              DOMAIN: binary artifacts
  return sha256(path.read_bytes()).hexdigest()          # NO transformation

  applies to exactly:
    the two retained .npz replay references (§7)
```

**Why the split is load-bearing, measured rather than argued.** A `.npz` is a ZIP
archive of NumPy buffers. Byte pairs equal to `0d 0a` occur inside that payload as
data, not as line endings, so folding them corrupts the file's identity. The two
retained references contain **18** and **1** such pairs respectively, and folding
changes both digests:

```text
plant reference          3,176,122 bytes   18 CRLF pairs
  raw          ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45   <- pinned
  text-folded  638e384f3a75c4cefb360e7b7815e7a1b9f5dcd2e01c2cbb718410db9964c575

S observation reference    929,068 bytes    1 CRLF pair
  raw          cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83   <- pinned
  text-folded  0051ea132a783264c47a370184f0d328e2ae4c3a95ad227b3cf9c181c599435e
```

Both agents computed all four values independently and they agree. §7's pins are the
**raw** digests, so routing the references through the text helper would fail I1
deterministically before the replay ever ran.

For the text domain, folding in memory makes the digest invariant to the checkout
convention: this repository is developed on Windows with `core.autocrlf=true`, and an
unpinned text file materializes as CRLF in a fresh clone. Both text files are
additionally pinned `text eol=lf` in the root `.gitattributes` as defence in depth, but
the fold is what makes the digest portable. `.gitattributes` has **no** role for the
binary references — they are git-ignored local artifacts.

This document cannot contain its own hash. The implementation reads this file,
computes its canonical text digest at run time, and records it in every artifact
identity below.

### Provenance scope — which identity each artifact carries

`config_hash` is a stored field of the `ObservedRecord` that `SensorModel.observe`
writes, so *what is stamped changes the artifact's bytes*. That makes the scope
below a correctness requirement, not a convention:

```text
replay gate (§7)                  overrides=None, stamps the BASE config hash.
                                  Ephemeral; never persisted as a screen artifact.
                                  It MUST stamp base: the retained reference row was
                                  generated under the base hash, so stamping anything
                                  else changes the observation's config_hash field and
                                  I2's 38-entry npz equality fails by construction.

Stage A / B / C rollouts (§8)     active overrides, so each stamps its own
                                  per-rollout base-distinct dev-<64 hex> provenance
                                  (Correction 2).

Stage 0 (§8)                      no rollout and no reservation, so no per-rollout
                                  payload exists. Its written artifact still carries
                                  one explicit artifact-level dev-<64 hex> identity
                                  (Correction 6). No fake plant reservation is invented.
```

The v2.3.1 sentence "every rollout stamps a provenance digest that binds this
document" was false for the replay rollout and undefined for Stage 0. It is replaced by
the table above.

## 1. Correction history

**Every correction on this list is an executability fix. Across v2.3 → v2.3.1 → v2.3.2
→ v2.3.3 no universe, statistic, threshold, stage, branch, secondary, or success
criterion has changed.** Corrections 1–3 landed in v2.3.1 and their substance is
approved by both agents; Corrections 4–7 landed in v2.3.2 and answer Codex's four
Session-41 findings, all four of which Codex re-verified as corrected. Correction 8 is
new in v2.3.3 and answers Codex's single Session-42 finding. The list is kept rather
than compressed because each entry records a measurement or a source fact that
justifies a pin the body of this file now depends on.

### Correction 1 — the structural override must activate at the declared onset

`FaultSpec.onset_index` defaults to `-1` (`utils/schema_types.py:77`) and the plant's
rule is `onset = max(int(fault.onset_index), 0)` (`utils/cable_plant.py:183`). A
`FaultSpec` built without an explicit onset therefore softens the body **at step 0**,
not at the declared 1.0 s trajectory onset (step 500 at `control_dt_s = 0.002`). The
committed generator's ordinary path derives the onset properly in `_fault_components`
(`assignment_generator.py:390`); the v2.3 screen text did not.

Every structural override is now built by a helper that derives the onset exactly as
the committed path does, and the healthy condition is the empty tuple:

```python
SCREEN_CONDITIONS = ("healthy", "structural")   # closed vocabulary; nothing else is legal

def screen_physical_faults(condition, trajectory, *, severity=None, control_dt_s):
    if condition not in SCREEN_CONDITIONS:
        raise ProtocolPError(
            f"unknown screen condition {condition!r}; expected one of {SCREEN_CONDITIONS}")
    if condition == "healthy":
        if severity is not None:
            raise ProtocolPError("healthy condition must not carry a severity")
        return ()
    if severity is None:
        raise ProtocolPError("structural condition requires an explicit severity")
    v = float(severity)
    if not math.isfinite(v) or not (0.0 < v <= 1.0):
        raise ProtocolPError(f"remEI severity must be finite in (0, 1]; got {severity!r}")
    onset_index = _step_index(float(trajectory["onset_time_s"]), control_dt_s)
    return (
        FaultSpec(
            source_class="structure",
            subtype="link_stiffness_loss",
            location=1,
            severity=v,
            onset_index=onset_index,
            compound_flag=False,
            ood_flag=False,
        ),
    )
```

Three properties of this signature are deliberate and are what Correction 7 checks.
The condition vocabulary is a **closed set**, so a misspelling raises instead of being
treated as structural. `severity` is **keyword-only with default `None`**, so "severity
is absent" is an expressible and checkable state rather than an unused positional
argument. The `(0, 1]` bound matches the plant's own structural validator
(`cable_plant.py:124-125`), so an out-of-range severity fails at construction rather
than deeper in MuJoCo.

The empty tuple is **not** `None`, so a healthy screen row is still an *active*
override and still requires a provenance hash. Every override guard tests
`is not None`, never truthiness — an empty tuple is falsy, and a truthiness test would
silently fall through to the reservation's derived fault list.

**Measured consequence of the defect (Session 41, 4 rollouts).** The Stage-A safety
gates would **not** have caught this. At both remEI 0.75 and remEI 0.35, the step-0
and step-500 constructions are both fully admissible, with every gate passing by a
wide margin and a peak `|gauge_true|` ratio of 1.035 and 0.999 respectively:

```text
remEI 0.75  step 0    gauge   5.76 ue   qd 0.686   q 0.396   flags 0   sat 0   ADMISSIBLE
remEI 0.75  step 500  gauge   5.56 ue   qd 0.773   q 0.396   flags 0   sat 0   ADMISSIBLE
remEI 0.35  step 0    gauge   5.58 ue   qd 0.752   q 0.396   flags 0   sat 0   ADMISSIBLE
remEI 0.35  step 500  gauge   5.59 ue   qd 0.720   q 0.396   flags 0   sat 0   ADMISSIBLE
```

So the defect had no route to a spurious safety failure, and no route to being
misclassified as a physical limit. It had the quieter route: all 169 rollouts would
have completed, and `D` would have been measured on a body soft from step 0 with no
healthy pre-change segment, with nothing in the protocol flagging it. **A safety gate
passing with 70x margin is evidence about safety, not about construction.** This is
why the onset is now an explicit asserted invariant (§10, I13) rather than something
the gates are trusted to notice. The `|gauge|` values above are whole-run peak
statistics on the privileged path and bear on nothing else in this protocol — in
particular they are not `D` and say nothing about separability.

### Correction 2 — the provenance identity must be lifecycle-valid and base-distinct

v2.3's guard tested only that a provenance hash was non-empty, so
`provenance_hash=config_hash` was accepted and the claim that an overridden run cannot
carry the base hash was false. The proposed value `dev-protocolp-v2.3-<32 hex>` also
failed the packet's own validator: `_valid_config_hash` strips exactly `dev-` and then
requires one full 64-character lowercase SHA-256 (`storage_contract.py:103-109, 364-367`).
The value was never storable, and it described a 128-bit truncation as a SHA-256.

The seam now validates inside `_generate_reservation` — not only in the caller —
requiring all four of:

```text
provenance is a non-empty string
provenance starts with "dev-"                     (screen artifacts stay ineligible)
the remainder is exactly 64 lowercase hex digits  (passes _valid_config_hash)
provenance != the supplied base config hash
```

and the derived value uses the full digest:

```python
# CANONICAL_JSON — the single serialization rule for every identity payload in this
# protocol. Matches the packet precedent in config_contract.canonical_json_bytes:89.
def canonical_json(payload) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,      # a NaN or Infinity in an identity payload must raise
    )

rollout_canonical = canonical_json(rollout_identity_payload)
screen_provenance_hash = (
    "dev-" + hashlib.sha256(rollout_canonical.encode("utf-8")).hexdigest())
```

`allow_nan=False` is not decoration. Plain `json.dumps` defaults emit the non-standard
tokens `NaN` / `Infinity` rather than raising, so a corrupted float reaching an identity
payload would produce a *valid-looking* digest over an unparseable document. The packet
already made this choice for the config hash; this protocol uses the same rule for
every payload it digests.

`rollout_identity_payload` contains: `base_config_hash`, `assignment_canonical_sha256`,
`assignment_hash`, `protocol_spec_sha256` (this file, §0), `stage`, `cell`,
`condition`, `overrides` (all four values), and `reservation`
(`scenario_spec_id`, `base_pair_id`, `sensor_seed`). The results JSON records the full
`rollout_canonical` string per rollout, not only the digest.

**Both identity payloads in this protocol carry distinct, explicit names** — this one
and Stage 0's (Correction 6) — because a generic `payload` in one operative expression
is precisely what let the other bind to the wrong object (Correction 8). The only
`payload` remaining in this file is `canonical_json`'s own formal parameter, which is
locally bound by definition.

### Correction 3 — the assignment byte pin must be portable

v2.3 pinned the assignment file by raw bytes. That file is pure LF in the development
working tree and hashes to
`76255a8089f3e27d893b26d981cbf50e808bd75ba518c44b55c4635ec83514ae`, but its CRLF
rendering hashes to
`00dacaf6277d6b274e3690ab3d3f68607eb61a22fe0df75ea8688fe4c7d4f87f`. The exposure is
not hypothetical: `draft-config-v0.1.json`, in the same directory, is **already CRLF**
in this working tree.

Both pinned **text** files — this document and the assignment JSON, and only those two
(Correction 4) — are hashed through the folding helper, so the digest is portable by
construction rather than by depending on `.gitattributes` being present and correct:

```python
def canonical_text_sha256(path):          # TEXT DOMAIN ONLY — never a .npz
    raw = Path(path).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
```

The helper is named for its domain rather than for files in general, because v2.3.1's
domain-neutral name (`canonical_file_sha256`) is what invited applying it to the binary
replay references.

The canonical assignment digest equals the raw digest in an LF checkout, so
`76255a80...514ae` remains the operative value; it simply can no longer break in a
CRLF clone. The document-derived `assignment_hash`
(`dev-eec59ec8a296a9a4ff4909f8e7f1de91a0a8f4bf289ae1533a427d1a87bc33f1`) is retained
alongside it: the canonical digest is EOL-immune, the raw-byte digest catches
whitespace or key-order changes that canonicalization would hide, and the two
cross-check each other.

### Correction 4 — the text canonicalizer must not touch the binary references

v2.3.1 generalized Correction 3's folding helper to *every* pinned file, including the
two retained `.npz` replay references in §7. That was wrong, and it was a hard-stop
defect rather than a cosmetic one: §7's pinned values are raw digests, the references
contain 18 and 1 embedded `0d 0a` payload byte pairs, and folding changes both digests,
so **the operative instruction guaranteed that I1 would fail before the replay could
run**. The protocol as written could not start.

The fix is the two-domain split now stated in §0: `canonical_text_sha256` for the two
tracked text files, `raw_file_sha256` with no transformation for the two binary
references, each file belonging to exactly one domain. I1 is rewritten to name the
domain per file (§10).

**Scope check performed, not assumed.** Every byte pin in this protocol was enumerated
and assigned a domain: this file (text), the assignment JSON (text), the two `.npz`
references (binary). `draft-config-v0.1.json` is deliberately **not** byte-pinned — its
`config_hash` is computed over `canonical_json_bytes(document)` and is therefore already
EOL-immune — and no other file is hashed anywhere in this protocol. Exactly one domain
error existed and it is corrected.

**A distinction the split makes visible.** The replay gate now guards its *input* by
exact binary identity and its *output* by array equality (20 privileged fields, 38 npz
entries). These are different checks answering different questions: "is the retained
artifact the one we pinned?" and "does regeneration reproduce its contents?" A `.npz` is
a ZIP container, so byte-identity of a *regenerated* archive is not a property this
protocol claims or needs; array equality is the reproduction claim.

### Correction 5 — no undefined or overloaded abbreviations

v2.3.1 used `M2` four times without ever defining it, and the four uses split into
**two incompatible objects**: at Stage 0 and in the secondaries it meant a descriptive
fixed-trace gauge-only check, while in the Case A/B/C conditions it meant the operative
per-cell mechanics verdict. That is not a wording blemish. The gauge-only secondary is
declared in §9 to set no threshold and gate nothing, so a reader who resolved `M2` that
way in the Case conditions would have gated the protocol's terminal outcome on an object
the same file says has no authority — **the document would have contradicted itself in a
verdict-bearing sentence.**

`M2` is removed entirely; each occurrence now names the object it meant. Auditing the
whole file for that defect class found two further instances, both fixed: `T1` (used
twice, never defined — a retired cutoff from an earlier draft) and `remEI` / `EI` (used
throughout, never expanded). §0 now carries a terms block covering every abbreviation in
the file, and names `T1` and `M2` as retired so neither can be reintroduced silently.

### Correction 6 — provenance scope stated per artifact class

§0 claimed every rollout stamps a protocol-derived provenance digest. §3 correctly says
an `overrides=None` call stamps the base config hash, and §7 requires exactly that
all-None path for the replay. The replay rollout therefore could not satisfy §0, and
Stage 0 — which runs no rollout and holds no reservation — had no defined identity at
all while §0 simultaneously declared every produced artifact a `dev-` screen artifact.

§0's provenance-scope table replaces the false universal claim, and it records the
*mechanism*: `config_hash` is a stored `ObservedRecord` field, so the replay must stamp
base or I2's byte comparison fails by construction.

**Stage 0's artifact-level identity**, pinned now because it is the one artifact this
protocol writes without a rollout. One digest for the whole file, not per sample, over
`CANONICAL_JSON` (Correction 2) — no plant reservation is invented:

```text
stage_0_identity_payload = {
  "stage":                       "0",
  "base_config_hash":            config.config_hash,
  "assignment_canonical_sha256": canonical_text_sha256(assignment path),
  "assignment_hash":             document-derived dev-eec59ec8...bc33f1,
  "protocol_spec_sha256":        canonical_text_sha256(this file),
  "cli": { "window": 768, "f_ctrl_hz": 500.0, "diagnostic_hz": 0.8,
           "thermal_ramp_c": 3.0, "pairs": 100, "seed": 0, "pair_id": 1 },
  "output_schema":               sorted top-level keys the script writes,
}
stage_0_canonical = canonical_json(stage_0_identity_payload)
stage_0_identity  = "dev-" + hashlib.sha256(
                        stage_0_canonical.encode("utf-8")).hexdigest()
```

`sensor_only_difference_null.json` records **both** `stage_0_identity` and the exact
`stage_0_canonical` string it was hashed from — the *same* object, not a second call
that ought to agree — so the digest is independently recomputable from the artifact
alone. The same `dev-` prefix keeps it permanently ineligible for confirmatory
analysis, and the same base-distinctness requirement in I8 applies to it.

### Correction 7 — the construction check and the behavioural test are two different objects

v2.3.1's I13 conflated them, and each half was defective on its own.

**The runtime half was incomplete.** I13 checked the onset step, the empty-tuple healthy
case, and the `is not None` guard style — but not that the constructed fault *is the
requested fault*. Combined with a helper that treated every non-`"healthy"` string as
structural and silently ignored `severity` when healthy, a misspelled condition or a
condition/severity mismatch could produce a clean, fully admissible result **for the
wrong body**. Correction 1's closed vocabulary and keyword-only `severity` close the
helper side; I13a (§10) now compares the complete constructed object field by field
against the exact expected object, and raises before the rollout.

**The behavioural half was not implementable where it was placed.** I13 required
verifying that the softened model is inactive before the onset step and active at or
after it — as a *per-rollout runtime invariant*. It cannot be one.
`_generate_reservation` returns
`(control_pair_id, PrivilegedRecord, observations, label_payload, safety_count,
contact_count)`; the `CablePlant` instance is constructed inside the call and never
returned, so `_softened` history is unreachable from the production loop's return value.
Verified by reading the return statement, not inferred.

That check therefore becomes **I13b**, a focused implementation test that instantiates
`CablePlant` directly and asserts the step-499/step-500 boundary once. It is a
precondition on the protocol running at all, not a per-rollout assertion.

**Where it lives, and why (decided by Codex, Session 42).** It is a **permanent packet
test** at `Reproducibility Packet/tests/test_cable_plant_softening_boundary.py`, not a
Protocol-P-scoped precondition sitting beside the screen script. The activation
boundary is a property of the **plant contract** — `CablePlant`'s
`_activate_structural_fault_if_needed` against `FaultSpec.onset_index` — not of this
screen's measurement, so every future consumer of the plant should keep the regression
guard after Protocol P is over. It also would have caught the Session-41 onset defect
on its own, before any protocol existed to be blocked.

**The physical-limit label now requires both.** §9's `NO_ADMISSIBLE_PROBE` second branch
may label a Stage-A failure a newly observed physical limit only when I13a has been
asserted for that rollout **and** I13b is in a passing state. Session 41 measured that
the safety gates pass with ~70x margin under both the correct and the defective onset,
so a gate outcome carries physical meaning only once the construction has been
established separately — by both halves, since either one alone leaves a route from a
build mistake to a reported discovery.

### Correction 8 — every identity expression must name the object it hashes

v2.3.2's Correction 6 defined `stage_0_identity_payload` and then, in the very next
line, hashed `canonical_json(payload)`. The name `payload` is not that object. Worse
than an undefined name: `payload` had already been established 122 lines earlier, in
Correction 2, as the **per-rollout** identity payload. A reader resolving the Stage-0
expression literally either hits an undefined name or binds it to the wrong payload, so
the one artifact this protocol writes without a rollout would not have been bound to
the object its own specification declares.

This is Correction 5's defect class — a token whose meaning lives outside the
expression that uses it — relocated from prose into an **executable identity
expression**, where the consequence is a wrong digest rather than a wrong reading.
Correction 5 retired two ambiguous *abbreviations*; it did not audit *variable names*,
which is why this survived it.

**Class audit performed rather than the single instance fixed.** Every identifier
appearing in an operative expression in this file was checked for a binding, and every
binding checked against the object the surrounding text defines. The protocol generates
exactly two identity digests — the per-rollout provenance hash (Correction 2) and the
Stage-0 artifact identity (Correction 6); the replay rollout stamps base by requirement
and generates none (§0, I8). Both are now bound to explicitly and distinctly named
payloads, and each names the canonical string it hashes. Three further in-class
instances were found and corrected, none of them able to change a result:

```text
Correction 2   the call site read canonical_json(payload) with `payload` bound only by
               the prose beneath it. That generic name is the affordance the Stage-0
               defect took. Now rollout_identity_payload / rollout_canonical.
§6             P_SEED_BASE = 150000 was defined and then never used; both seed
               expressions repeated the literal. A constant that looks authoritative
               and drives nothing is the same trap as a name that points at the wrong
               object. The expressions now use it. Every seed value is unchanged.
§10 I13a       the onset expression read _step_index(onset_time_s, dt); `dt` is bound
               nowhere in this file. Correction 1 writes the same call as
               _step_index(..., control_dt_s). Now spelled the same way in both.
```

No universe, statistic, threshold, stage, branch, secondary, invariant, or success
criterion is touched by any of the four. Nothing in this protocol had been executed
when the defect was found, so no digest, artifact, or result is affected.

## 2. Universe

`trajectory_dev_diagnostic_b` (`t01`) only. Context cells 4/5/6/7 = replicates
r00..r03, a balanced half-fraction over payload x environment x contact:

```text
cell 4 = r00   payload 0.000 kg   iso25c   contact brief
cell 5 = r01   payload 0.000 kg   warm2c   contact none
cell 6 = r02   payload 0.050 kg   iso25c   contact none
cell 7 = r03   payload 0.050 kg   warm2c   contact brief
```

The ordinary trajectory `t00` stays probe-free and is the pre-registered negative
control. Only `t01` carries a probe.

## 3. The seam — the code change this protocol requires

Three additions to `Reproducibility Packet/scripts/utils/assignment_generator.py`, all
keyword-only, all defaulting to current behaviour. The file is Codex's. Claude owns the
implementation; **the applied working-tree diff plus its focused tests are posted for
review before anything runs** — the patch is applied to the working tree first so that
what Codex reviews is the exact bytes that will execute, not a description of them. No
replay and no Protocol-P stage may run before that review closes.

```python
@dataclass(frozen=True)
class ScreenOverrides:
    probe_peak_force_n: float | None = None
    probe_ramp_fraction_of_duration: float | None = None
    physical_faults: tuple[FaultSpec, ...] | None = None
    realized_pair_id: str | None = None
    provenance_hash: str | None = None

    def is_active(self) -> bool:
        return any(v is not None for v in (
            self.probe_peak_force_n, self.probe_ramp_fraction_of_duration,
            self.physical_faults, self.realized_pair_id))


def screen_pair_id(reservation, overrides) -> str:
    if overrides is not None and overrides.realized_pair_id is not None:
        return str(overrides.realized_pair_id)
    return f"{reservation.base_pair_id}_dataset0"
```

`_physical_config(..., *, control_dt_s, overrides=None)` — inside the
`probe is not None` branch only, `peak_n` and `ramp_s` become locals with
`ramp_s = duration / 2.0` as the default. A peak override must be finite and `> 0`; a
ramp fraction must be finite and in `(0, 0.5]`, else raise. In the `probe is None`
branch, a probe override **raises** rather than being silently discarded.

`_generate_reservation(..., overrides=None)` — active overrides are validated per
Correction 2; `stamped_hash` is the provenance hash when active and the base
`config_hash` otherwise, and **`stamped_hash`, not `config_hash`, is passed to the
`OnlineSensorSession` and to every `SensorModel.observe`**. A `physical_faults`
override replaces the derived list (raising if `sensor_fault is not None`), and
`control_pair_id = screen_pair_id(reservation, overrides)`.

**Why the ramp override is a forced code change, not a preference.**
`_physical_config:338` computes `ramp_s = duration / 2.0` from `cycles` and
`frequency_hz`. Every possible assignment-document input therefore yields exactly
fraction 0.5. Fraction 0.125 — the value every pre-dataset screen used — is reachable
by no route at all. Peak force and fault severity *are* reachable without touching
Codex's file, by mutating the in-memory assignment document, but that is rejected on
provenance grounds: it would leave no typed record of what was altered.

**Known and deliberately unpatched.** When `physical_faults` is overridden,
`_fault_components` still returns the *source reservation's* label, so a screen run on
a healthy reservation describes itself as healthy while its plant carries a structural
fault. Protocol P never persists or reads a screen label, so this is out of scope here.
It is non-blocking only under the three conditions in §9. The first future consumer
that persists an overridden run must make the label and run identity describe the
override before persistence is authorized.

## 4. Construction path

Every plant-bearing rollout is built through `_generate_reservation` via the seam:

```text
config     = load_config("config/draft-config-v0.1.json", "schema/schema.json")
assignment = load_assignment("config/proposed-gate3-assignment-v0.1.json")
binding    = validate_approved_assignment_binding(config, expected_assignment=assignment)
runtime    = _runtime_parameters(binding)   # dt 0.002, f_ctrl 500, sim_dt 1e-4, points 17
history    = config.document["values"]["timing"]["window_steps"]   # 768
_generate_reservation(binding.assignment, config.config_hash, ("S",), None,
                      history, runtime, screen_reservation,
                      overrides=ScreenOverrides(...))
```

The closed loop is driven by the **C0** session; S is produced afterwards by
`SensorModel().observe(result.plant, "S", ...)` at the **same realized identity**. This
is the verified construction path (S39 Finding K). **No online-S variant is
authorized** — an online-S construction is a different, untested instrument.

## 5. Screen reservation

Copy the delivered dev `t01` reservation for the target context cell (r00..r03 — that
is what fixes payload, environment, and contact) and replace **exactly two fields**,
`sensor_seed` and `base_pair_id`, asserting every other field equal to the source.
`fault_setting_id` stays the dev **healthy** setting (`fault_dev_healthy`, f000) so
`_fault_components` returns no physical and no sensor fault; the ladder fault enters
only through `overrides.physical_faults`. The assignment catalog is never mutated.

## 6. Realized identity table

`CablePlant` contains no RNG, so a rollout's identity is exactly
`(sensor_seed, realized pair_id)`. Realized identities are suffix-free by override.

```text
P_SEED_BASE = 150000 ; cell c in {4,5,6,7} ; r = c - 4

Stage A + B   sensor_seed = P_SEED_BASE + 10*r + 2   -> 150002 150012 150022 150032
              pair_id     = "basepair_protocolp_stageAB_c{c}"
Stage C k=0   reuse the Stage-A healthy rollout of the SELECTED candidate
      k>=1    sensor_seed = P_SEED_BASE + 10*r + 1000*k + 2
              pair_id     = "basepair_protocolp_stageC_c{c}_k{k}"
Stage C gauge-only secondary (0 rollouts)  the k=0 trace redrawn at k=1..7
Stage 0 (no plant)                          pair_id = 1, sensor_seed = 0..199
```

The band `[150002, 157032]` cannot collide with dev `[110000, 111514)` and sits far
below pilot's 210000. Two **tested** leak tripwires protect the dataset: the
`_dataset0` suffix assertion at `assignment_generator.py:241-242` and the approved-set
comparison at `:244-245`. Both have been fed the exact state they were written to
catch and both raise.

Sensor RNG is keyed on `(sensor_seed, pair_id, channel, stream)` jointly
(`utils/rng.py:76-78`). A `pair_id` change alone moves `gauge_obs` by up to 6.50 µε,
against `D` values of order 0.1–0.5 — which is why any protocol, audit, join, or leak
guard that names "pair_id" must say **which one**, base or realized.

## 7. Replay gate — a stop-or-go precondition (1 rollout)

Hash both pinned references with **`raw_file_sha256` — exact bytes, no BOM strip, no
CRLF fold** (§0, Correction 4). These are ZIP/NumPy binaries; the text canonicalizer
must never be applied to them. **Absent or changed ⇒ raise and stop** — never fall back
to whatever is on disk. Then rebuild `scenario_dev_t01_f000_r00` with `overrides=None`
(which stamps the base config hash — see §0's provenance scope; anything else changes
the observation's stored `config_hash` and fails the comparison below by construction)
and require all 20 privileged array fields and all 38 npz payload entries equal.
**Failure ⇒ Stage A does not start.**

The input is guarded by exact binary identity; the output is guarded by array equality.
Byte-identity of a *regenerated* `.npz` is not claimed.

```text
data/gate3-base-dev-pilot-val-c1-s/   (git-ignored, local only; retained development
                                       data, NOT committed payload)

plant/scenario_dev_t01_f000_r00_S_dataset0.npz
  ed5b1f39f4ba535c60eb3e1b8587c7b03f59a5c3f9c1189b55635f0d49b65e45
observations/S/scenario_dev_t01_f000_r00_S_dataset0.npz
  cdde17f6d32c5d648249f4a9b343ec3f997b04c83cadacbf9d2c5f1186bb4c83
```

Both hashes were computed independently by both agents and agree. The 38 npz keys are
30 per-channel arrays (5 dicts x 6 channels) plus 8 metadata entries
(`schema_version, suite, run_id, pair_id, config_hash, split, channel_names,
suite_available_mask`).

**Achieved replay scope is ONE ROW, EXACT.** The 472-reservation / 944-pair dataset was
never regenerated. No dataset-wide reproduction claim is made anywhere in this
protocol or in any artifact derived from it.

## 8. Window, statistic, and stages

### Window origin (S38 Finding J)

```text
w0 = round((onset_time_s + diagnostic_probe.start_offset_s) / control_dt_s)  # raise if off-grid
w1 = w0 + 768                                                               # raise if w1 > n_steps

split   trajectory                     onset  offset   w0    window        steps
dev     trajectory_dev_diagnostic_b     1.00   1.00    1000  [1000,1768)   3000
pilot   trajectory_pilot_diagnostic_d   1.10   1.20    1150  [1150,1918)   3050
val     trajectory_val_diagnostic_f     1.15   0.90    1025  [1025,1793)   3075
test    trajectory_test_diagnostic_h    1.25   1.10    1175  [1175,1943)   3125
```

Every split is 625 probe steps plus 143 ringdown steps. Stage 0 is exempt (no plant,
so no origin). Nothing in the codebase fixes the window origin — `window_tensor`
refuses a full run and right-aligns, so the caller owns the origin. This pin is
therefore effectively the pipeline's pre-registration, and the Gate-7 evaluation
driver must reuse it.

The empirical peak origin (1208 / 2.092897106, +11.2897% over the probe-start origin's
1.880585474) is **disclosed and rejected**: it is response-selected and favours S. The
probe-start origin is retained on purely prospective grounds — it is config-derived,
contains the whole declared burst, and was fixed before any response was seen.

### Statistic

```text
D = || concat_{g=0..3} ( b_g(fault) - b_g(healthy) ) ||_2        8 entries

tm = record.measurement_time_s["gauge_obs"]
if   tm.ndim == 1:                       t_g = tm
elif tm.ndim == 2 and tm.shape[1] == 1:  t_g = tm[:, 0]   # legacy; currently unreachable
else:                                    raise ProtocolPError("must be [T] or [T,1]")
if not (t_g.shape[0] == gauge_obs.shape[0] == gauge_valid.shape[0]):
    raise ProtocolPError(...)

b_g = harmonic_coefficients(gauge_obs[w0:w1, g], gauge_valid[w0:w1, g], t_g[w0:w1], 0.8)
```

Observed path only. Matched on `sensor_seed` **and** realized `pair_id` in Stages A
and B. `harmonic_coefficients` fits with an intercept and a centred linear trend, so a
linear-in-time thermal ramp contributes exactly zero in exact arithmetic; quantization
is what breaks that. `gauge_obs` for S contains NaNs from dropout and latency, so all
statistics are NaN-aware. Requires at least 5 finite valid samples.

### Stage 0 — sensor-only difference null (0 rollouts)

Adds `timing.diagnostic_probe.ramp_fraction_of_duration`; candidates
`{0.125, 0.25, 0.5}` map to ramps `0.15625 / 0.3125 / 0.625 s` at duration 1.25 s. At
`cycles = 1`, fraction-of-duration is identical to fraction-of-period.
`cable_mechanics.diagnostic_tip_load_envelope` (`:444-454`) admits `(0, 0.5]`.

New packet script `scripts/analyze_synchronous_difference_null.py` writes
`results/protocol_p/sensor_only_difference_null.json`, reusing the gauge-window helper
lifted into `utils/`.

```powershell
Set-Location "Reproducibility Packet"
..\venv\Scripts\python.exe scripts\analyze_synchronous_difference_null.py --window 768 --f-ctrl-hz 500.0 --diagnostic-hz 0.8 --thermal-ramp-c 3.0 --pairs 100 --seed 0 --pair-id 1
```

Single line. A backtick is the only permitted continuation; `^` is a cmd.exe token, not
a PowerShell one.

**One sample is one PAIR of four-gauge windows reduced to one scalar. 100 samples — not
200, and emphatically not 800.** The 800-sample figure in
`analyze_synchronous_detection_floor.py` arises because lines 241-242 append per gauge
per realization; that is how `0.4053` became an 800-sample per-gauge number. There is no
amplitude cutoff in this protocol (the earlier `T1` cutoff is retired; see §0).

Stage 0 has no plant, so it is a purely synthetic sensor-path null. **Its one existing
real-plant corroboration is the prior fixed-trace gauge-only check** — one delivered
healthy trace per cell held exactly fixed and redrawn at 8 sensor identities, giving
per-cell 0.95 quantiles of `0.3176 / 0.3555 / 0.3854 / 0.4251 µε` across cells 6/4/7/5.
Stage 0's synthetic value of roughly `0.39` falls inside that measured real-plant range,
which is the sense — and the only sense — in which Stage 0 is corroborated. That check is
a **conditional healthy-null diagnostic**: it is not this protocol's operative null, it
sets no threshold, and it gates nothing. The operative null is Stage C's `Q95_c`.

The written artifact carries the Stage-0 artifact-level identity and the canonical string
it was derived from (Correction 6), so its provenance is recomputable from the file alone.

### Stage A — admissibility and selection (108 rollouts, after the replay gate)

Declared candidate grid: peak `{0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40}` N x
ramp fraction `{0.125, 0.25, 0.5}` = 24 candidates (restated from the v2.3 turn). The
approved **inclusive** torque gate

```text
F_peak * 2 * link_length_m <= 0.60 * torque_abs_limit[0]
```

excludes 15 before any simulation, admitting 9: peak `{0.05, 0.10, 0.15}` N x ramp
fraction `{0.125, 0.25, 0.5}`. At 0.15 N the left side is `0.15 * 2 * 0.40 = 0.12` and
the right side is `0.60 * 0.20 = 0.12`, so **`<=` rather than `<` is load-bearing** and
0.15 N is admitted by exact equality.

9 candidates x 4 cells x 3 conditions `{healthy, remEI 0.75, remEI 0.35}` = 108
rollouts. Hard gates apply to every cell and condition and are **all computed from the
returned `PrivilegedRecord`**: zero `safety_flag` across all 7 A1 flags;
`max|qd_true| <= 8.0`; `max|q_true| <= 2.5`; `max|gauge_true| <= 400 µε`; the torque
gate; and no increase in saturated steps against zero probe amplitude (baseline 0). A
failing candidate is dropped, its remaining cells skipped, and the drop count logged.

**Selection: maximise worst-cell `D` at remEI 0.75.** No amplitude cutoff of any kind
enters selection. Ties within 1% resolve to the smallest amplitude, then the largest
ramp fraction.

### Stage B — the ladder (32 new rollouts)

The selected candidate at all ten reserved remaining-EI values
`{0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.75, 0.85, 0.90}` x 4 cells. The values
0.75 and 0.35 are reused from Stage A at matched identity, so 32 rollouts are new.
Every rollout re-asserts the hard gates.

### Stage C — the operative null (28 new rollouts)

8 healthy replicates per cell (k=0 reused from the selected Stage-A healthy rollout),
and all `C(8,2) = 28` within-cell pairs.

```text
Q95_c   = np.quantile(within_cell_distances, 0.95, method="higher")
pass(v) iff D(v,c) >= 2.0 * Q95_c   for EVERY screened cell c
```

The scalar form `min_c D >= 2 * max_c Q95_c` is strictly stricter and is a
pre-declared sensitivity, **not** a second route to success. `Q95_c >= 0.30 µε`
triggers a diagnostic pause only. Carried limitation: 28 distances from 8 runs is a
U-statistic, and `method="higher"` places `Q95_c` at the 27th of 28 order statistics.

## 9. Outcome, cases, and terminal branches

One row per ladder value: `D(v,c)` for all four cells, `Q95_c`, `2*Q95_c`,
`Q95_c^gauge`, the seven `D_unmatched`, a per-cell verdict, and a value verdict.

**Aggregation is the conjunction over all four cells:** testable iff
`min_c [ D(v,c) - 2*Q95_c ] >= 0`. No mean, median, or pooled quantity enters any
verdict.

```text
Case A   all ten ladder values pass
Case B   a proper subset passes
Case C   none passes, after all ten ladder values have a SAFE, VALID per-cell
         mechanics verdict under the operative D(v,c) >= 2*Q95_c rule
         -> Slot-12 method failure + Slot-13 excitation-bounded non-transfer

           "safe"  = not excluded by UNSAFE_LADDER_VALUE
           "valid" = the statistic was computable in every cell: I9 window on-grid,
                     I10 measurement-time shape, I11 >= 5 finite valid samples
```

**`TESTABLE` is necessary, not sufficient.** Stage A/B signal is seed-matched so the
sensor term cancels, while the Stage-C null is not matched. The asymmetry favours S.

### Two secondaries, neither with authority

- **Stage C gauge-only decomposition** (0 rollouts). The k=0 trace held fixed and
  redrawn at k=1..7, all 28 distances, same rule, giving `Q95_c^gauge`. This is a
  **conditional healthy-null diagnostic only**: it may report whether `Q95_c` exceeds
  the fixed-trace redraw term and by how much, conditional on that trace. One fixed
  trace identifies no population decomposition, and components can interact or
  partially cancel, so there is **no mechanism attribution**. It sets no threshold and
  gates nothing. **The identical narrowing applies to the prior fixed-trace gauge-only
  check referenced in §8 (Stage 0).** Neither object has authority over any verdict;
  only Stage C's `Q95_c` does.
- **Unmatched secondary** (0 rollouts).
  `D_unmatched(v,c,k) = ||b(fault at v, identity_AB) - b(healthy_k, identity_k)||`,
  k=1..7. Seven **dependent** distances sharing one fixed fault-side identity, with no
  fault-side replication. **No quantile, gate, route, or bound.** Conditional
  descriptive sensitivity only.

### `NO_ADMISSIBLE_PROBE` — terminal, and pins nothing

`config.json` stays absent and no regeneration is triggered. Slot-12 method failure
plus Slot-13 excitation-bounded non-transfer. Scoped strictly to the one measured
candidate:

```text
0.05 N / ramp 0.5 fails healthy or remEI 0.75
   -> contradicts its delivered-row pass; implementation-integrity failure requiring
      diagnosis before further execution        (NO defect-localization claim)
that candidate passes those but fails remEI 0.35
   -> newly observed physical safety/method limit
any other candidate's failure
   -> recorded normally; classifies nothing by itself
```

**A precondition on the second branch (v2.3.1, tightened in v2.3.2).** No Stage-A
failure may be labelled a newly observed physical limit unless **both** construction
checks are in a passing state: **I13a** asserted for that specific rollout (the
constructed fault object equals the requested one, field by field) **and I13b** passing
(the step-499/step-500 softening boundary implementation test). Session 41 measured that
the safety gates are insensitive to a construction defect that changes which body is
being measured — they passed with ~70x margin under both the correct and the defective
onset. A gate outcome carries physical meaning only once the construction has been
established separately, and either half alone leaves a route from a build mistake to a
reported discovery: I13a without I13b never checks that the softened model actually
switches at the onset, and I13b without I13a never checks that *this* rollout requested
the body it got.

### `UNSAFE_LADDER_VALUE`

Labels a value `v` unsafe, excludes it with a reason, does **not** reopen selection,
and is neither TESTABLE nor SUB-THRESHOLD. Cases A, B, and C all require all ten ladder
values to have a safe, valid per-cell mechanics verdict under the operative
`D(v,c) >= 2*Q95_c` rule, in the exact sense defined under Case C above; otherwise the
outcome is terminal.

### Role coverage — pre-declared, read before the ladder

Count known-class testable structural settings per split and report the count 0/1/2.
OOD at 0.45/0.55 never counts.

```text
zero dev    -> no testable structural training support
zero val    -> structural model selection / calibration unsupported
zero test   -> four-way testable-stratum confirmatory metric undefined
```

Any of those three zeroes yields a named **role-coverage-bounded non-transfer
outcome**: the S/C1 secondary remains reportable, and it establishes neither success
nor hypothesis failure. Count 1 is a thin single-severity role and opens no new
terminal branch. Zero pilot relabels nothing but disables data-driven downsizing, so
the prospectively allowed maximum test replication is retained and the limitation
named.

**OOD role pinned.** Labels at 0.45/0.55 characterize mechanics testability only.
Those rows keep `ood_flag=true`, stay excluded from four-way known-class macro-F1 under
`ood_known_metric_rule`, and remain in the pre-registered OOD metrics.

### Label-stamp scope condition

The stale returned label (§3) is non-blocking for Protocol P only if the
implementation: persists no screen `ObservedRecord`, label payload, manifest, or role
index; keys every result from the explicit Protocol-P condition rather than the
returned assignment label; and tests that the results-only path writes no
dataset-role artifact.

## 10. Fail-loud invariants

Every decision-bearing invariant raises `ProtocolPError`. **Never `assert`** — `python -O`
removes assertions. `assert` appears only in `tests/`.

```text
I1   every pinned digest present and unchanged, EACH THROUGH ITS OWN DOMAIN (§0):
       canonical_text_sha256  this file; proposed-gate3-assignment-v0.1.json
       raw_file_sha256        both retained .npz replay references (exact bytes)
     Applying the text helper to a .npz, or the raw helper to either text file, is
     itself an I1 failure.
I2   array equality on replay: 20 privileged fields + 38 npz entries
I3   screen reservation differs from source in exactly {sensor_seed, base_pair_id}
I4   realized pair_id carries no _dataset0 suffix
I5   all eight Stage-C identities unique within a cell
I6   Stage-C k=0 identity == the selected Stage-A healthy identity
I7   Stage-A/B fault and healthy share one identity (deliberate; asserted, not assumed)
I8   every generated identity is dev-<64 lowercase hex> and differs from the base
     config hash, in both classes that exist:
       Stage A/B/C rollouts  active overrides carry a per-rollout provenance hash, and
                             the stamped hash reaches the OnlineSensorSession and every
                             SensorModel.observe
       Stage 0               the written artifact carries one artifact-level identity
                             plus the exact canonical_json string it was derived from
     The replay rollout is explicitly OUT of scope: it stamps the base config hash by
     requirement (§0, §7), and any implementation that gives it a dev- provenance has
     broken I2.
I9   window origin on-grid and w1 <= n_steps
I10  measurement-time rank / width / length, via explicit if / elif / else
I11  harmonic fit has >= 5 finite valid samples
I12  every hard safety gate, per cell and per condition
I13a [RUNTIME, per rollout] the constructed physical_faults tuple equals the requested
     condition EXACTLY. Unknown conditions raise (closed vocabulary, Correction 1).
       condition "healthy"     -> severity is None AND physical_faults == ()
       condition "structural"  -> exactly one FaultSpec, and every field equal:
                                  source_class  == "structure"
                                  subtype       == "link_stiffness_loss"
                                  location      == 1
                                  severity      == float(requested remEI value)
                                  onset_index   == _step_index(onset_time_s, control_dt_s)
                                  compound_flag == False
                                  ood_flag      == False
     Raised before the rollout starts. Checks the CONSTRUCTION, never a downstream
     consequence of it.
I13b [PERMANENT PACKET TEST, once — tests/test_cable_plant_softening_boundary.py]
     instantiate CablePlant directly and assert
     the softened model is inactive at step 499 and active at step 500 for the derived
     onset. This CANNOT be a per-rollout runtime invariant: _generate_reservation
     returns (pair_id, PrivilegedRecord, observations, label_payload, safety_count,
     contact_count) and the CablePlant instance is never returned, so `_softened`
     history is unreachable from the production loop. Must be passing before any stage
     runs; it is a precondition on the protocol, not an assertion inside it.
```

I13a and I13b are separate because they fail for different reasons and neither implies
the other. The `NO_ADMISSIBLE_PROBE` physical-limit label requires both (§9).

## 11. Cost

```text
replay gate      1 rollout
Stage 0          0 rollouts (no plant)
Stage A        108 rollouts
Stage B         32 rollouts
Stage C         28 rollouts
               ---
total          169 rollouts   ~76 min at the 26.4-27.5 s/rollout measured in S40/S41
```

Run as a background job. **Poll the results JSON, not the log** — Python buffers stdout
when redirected.

## 12. What this protocol cannot establish

- It cannot establish the project's hypothesis. Every artifact carries a `dev-` hash
  and is ineligible for confirmatory analysis.
- `TESTABLE` means a fault is measurable above a matched-signal / unmatched-null
  comparison that favours S. It is necessary, not sufficient.
- No mechanism attribution follows from either secondary.
- The replay gate demonstrates one-row exact reproduction, not dataset-wide
  reproduction.
- The honest prior going in: remEI 0.75 is expected to fail in every cell by a wide
  margin, and remEI 0.50 clears the binding cell by only about 1.11x on a projection
  computed with an inflated signal against a deflated bar — both errors favouring the
  hypothesis. Case B and Case C are roughly comparable in likelihood. Stage C settles
  it.
