# Deep Analysis PRO - Unified Agent Operating Manual

> **Version:** 2.0
> **Date:** 2026-07-30
> **Language:** English (canonical agent rules)
> **Purpose:** Provider-independent and phase-independent rules for how any AI agent or human engineer must investigate, change, verify, secure, and report work in LogicaMath.
>
> This manual governs **how work is performed**. The user request, maintained design rules, and an applicable approved plan or specification govern **what must be built**.

---

# Part I - Mandatory Operational Core

## 0. Mandatory execution contract

These rules apply to every provider, model, phase, module, environment, and task.

1. **No evidence, no completion.** A file, checkbox, comment, counter, or plausible implementation is not proof of behavior.
2. **Unavailable verification is not a pass.** Record it as `UNVERIFIED` or `BLOCKED`; never declare the affected requirement complete.
3. **Observe before changing.** Reproduce or confirm the real terrain: UI, endpoint, DB, generated artifact, log, diff, or user flow.
4. **Fix the root and its contract.** Trace producer and consumer; do not patch only the visible symptom.
5. **Use one source of truth.** Prompt, data, formula, answer, explanation, visual, API, and UI must not derive independently when they represent the same fact.
6. **Re-run the revealing check.** The same observation that exposed the defect must become green after the change.
7. **Verify collateral behavior.** At least one sibling, error path, role, or adjacent flow must remain correct for every non-trivial change.
8. **Compile and integrate before advancing.** Broken imports, types, builds, contracts, or startup stop the change.
9. **Never hide missing content.** No-scroll UI must prove that content fits; `overflow: hidden` is not proof.
10. **Never weaken safety to make a change work.** Auth, authorization, sanitization, CORS, secrets, privacy, and data isolation remain fail-closed.
11. **Improve before removing.** A working capability is removed only after its replacement is connected and verified.
12. **Keep claims honest.** Separate what was already good, what changed, what remains unverified, and what changes observable behavior.
13. **Preserve handoff state.** A model or session change must carry reproducible evidence, not only a conversational summary.
14. **Stop on unresolved contradictions or destructive uncertainty.** Ask the user when product semantics, live data, security, or scope cannot be resolved from terrain.

### 0.1 Required execution sequence

```text
SCOPE
  -> TERRAIN
  -> QUANTIFY AND TRACE
  -> INVARIANTS AND BLAST RADIUS
  -> MINIMAL IMPLEMENTATION
  -> STATIC GATE
  -> DYNAMIC GATE
  -> PERCEPTUAL / USER GATE
  -> COLLATERAL AND SECURITY CLOSE
  -> HONEST REPORT AND HANDOFF
```

Skipping an applicable gate makes the result incomplete.

### 0.2 Proportional path

For a trivial documentation or obvious one-line change, the record may be brief:

- requested outcome;
- exact diff;
- one revealing check;
- applicable collateral;
- remaining uncertainty.

Use the full sequence for behavior changes, generated content, UI, data, auth, security, migrations, refactors, phase work, or multi-file changes.

---

## 1. Authority, scope, and applicable context

### 1.1 Source precedence

Use this order unless a higher-level platform instruction overrides it:

1. Safety, privacy, legal, and platform restrictions.
2. The user's current request and explicit decisions.
3. This canonical manual for **how to work**.
4. Maintained project design rules for the affected subsystem.
5. The approved plan/specification explicitly applicable to the current task.
6. Observed runtime and stored-data terrain.
7. Historical documents, comments, names, and prior reports as context only.

Code and data can reveal that a plan is stale. That is a contradiction to surface, not permission to silently change product intent.

### 1.2 How a plan becomes applicable

A task-specific plan or specification is authoritative only when at least one is true:

- the user names it for the current task;
- the active OpenSpec change links it;
- the task entrypoint requires it;
- a maintained documentation index identifies it as current for the affected subsystem.

Do **not** load a historical plan merely because it mentions the same phase number or has a familiar filename. Do not apply a Phase N plan to another phase.

If no dedicated plan applies, follow the user request, maintained design rules, this manual, and observed terrain. Never substitute an unrelated plan.

### 1.3 Provider adapters

Provider-specific files may describe:

- available capabilities and tool mappings;
- filesystem/network permissions;
- approval boundaries;
- environment-specific limitations.

They must not:

- redefine this behavior contract;
- weaken safety or evidence gates;
- embed credentials or secrets;
- assume tool names exist for every provider;
- make a historical phase plan globally mandatory.

Required outcomes are capability-based: search files, inspect diffs, run commands, query data, render UI, or request approval using whatever safe mechanism the provider supplies.

### 1.4 Startup routing

Every agent must read:

1. this Part I operational core;
2. the functional reference sections routed by the task;
3. applicable design rules and approved task plan;
4. local entrypoint instructions nearest the files being changed.

| Task | Required reference |
|---|---|
| Bug, audit, or inconsistency | §6 Investigation + §7 Verification |
| Frontend or fixed viewport | §8.1-§8.3 |
| Generated math/content/SVG | §8.4-§8.8 |
| Auth, admin, sessions, child data | §9 Security |
| DB, seed, migration, clear, sync | §10 Data and environments |
| Large redesign or OpenSpec | §11 Change programs |
| Production/deploy | §10.8 plus deployment source of truth |
| Review another agent/model | §6.6, §7, §12 |

### 1.5 When to stop and ask

Ask before implementing when:

- two applicable authorities conflict;
- user intent conflicts with safety, privacy, data integrity, or non-regression;
- two valid designs change product semantics;
- scope ambiguity would produce materially different systems;
- a destructive operation may touch live or unknown data;
- observed reality contradicts a product-owned requirement;
- a convenience request would weaken security;
- the approved change grows beyond its agreed root or blast radius.

Do not ask about facts you can verify safely in code, data, docs, or runtime.

---

## 2. Terrain-first execution

### 2.1 Define success before editing

Translate the request into measurable acceptance conditions:

- observable behavior;
- invariants to preserve;
- affected roles, phases, modules, routes, tables, and viewports;
- explicit non-goals;
- rollback or recovery requirement;
- proof that would fail a plausible-but-wrong implementation.

### 2.2 Observe real terrain

At least one ground observation must support every important claim.

- "Code says X" is not "X happens."
- "The test exists" is not "the test passed."
- "No scroll" is not "all content is visible."
- "The seed ran" is not "served data changed."
- "The component renders" is not "the student can finish the flow."
- "The report says fixed" is not evidence.

Useful terrain:

- real DB rows and distributions;
- actual endpoint request/response;
- import, startup, or build result;
- browser flow and target viewport;
- generated PNG/SVG opened and inspected;
- `git diff`, status, log, and call sites;
- progress changing through a real answer flow.

### 2.3 Quantify and trace both directions

Quantify affected cases before designing a fix:

- number of phases/modules/levels/templates/users/rows;
- distributions, NULLs, duplicates, extremes;
- reachable call sites and consumers;
- maximum-content and boundary cases.

Trace in both directions:

```text
user symptom -> renderer -> API -> service/router -> DB/seed/generator
source datum -> writer -> storage/contract -> consumer -> rendered behavior
```

Frontier contradictions are common. A correct producer connected to a stale consumer is still a broken system.

### 2.4 Blast radius

Complete this before non-trivial edits:

| Surface | Touched? | What can break? | How it will be verified |
|---|---:|---|---|
| User flow | | | |
| Sibling phase/module | | | |
| API/schema/frontend contract | | | |
| Generator/seed/DB | | | |
| Progress/unlock/scoring | | | |
| Auth/roles/admin | | | |
| UI/layout/accessibility | | | |
| Storage/MinIO/URLs | | | |
| Existing user data | | | |
| Logs/secrets/child privacy | | | |

If a risk has no verification method, there is no valid close plan.

### 2.5 Plan and invariant record

```markdown
## Plan before edit
- Request and scope:
- Applicable design rules / plan:
- Terrain before:
- Root-cause hypothesis:
- Affected producer and consumers:
- Functional invariant:
- Pedagogical invariant:
- Security/data invariant:
- Blast radius:
- Plausible-but-wrong solution the test must reject:
- Verification gates:
- Non-goals:
- Contradictions / approvals:
```

This is a concise decision record, not private chain-of-thought.

---

## 3. Implementation discipline

### 3.1 Improve first

Order of operations:

1. Keep current working behavior reachable.
2. Add or repair the improved root path.
3. Connect every real caller and consumer.
4. Verify original and collateral behavior.
5. Remove the old path only after it is proven dead or fully superseded.

Removal requires one of:

- no real call sites and unreachable behavior proven;
- all callers migrated and former flows verified;
- active security emergency with documented mitigation;
- explicit user request with understood impact.

Never delete pedagogy, auth, sanitization, auditability, or a working path merely to simplify implementation.

### 3.2 Root fixes and single source of truth

- Fix generator/contract/renderer causes, not hundreds of stored symptoms.
- Extract shared non-trivial logic before new features depend on duplicated copies.
- Prompt, formula, answer, explanation, and visual must derive from the same structured result.
- API fields read by the frontend must be verified against the real response.
- Do not trust folder names for `fase_id`.
- Do not apply a sibling fix until local structure is proven equivalent.
- Prefer additive compatible fields before breaking renames.
- Make reseeds and migrations idempotent where required.

### 3.3 Code and architecture quality

- Use existing architecture and helpers.
- Keep routers thin; business/pedagogy logic belongs in services/composers.
- Keep UI separate from business logic.
- Frontend never talks directly to PostgreSQL.
- Use structured parsers/APIs for structured data.
- Write readable names and small cohesive functions.
- Add comments only where logic is not self-explanatory.
- Never use a bare `except`, empty catch, or silent failure; preserve traceback/context server-side.
- Do not add dependencies for trivial native functionality.
- Prefer maintained dependencies and check material security risk.
- Define deterministic tests first for non-trivial scoring, progression, algorithms, and generated-content invariants when practical.
- Public backend functions/classes require useful docstrings.
- Keep docs accurate when behavior changes.

### 3.4 Scope control

- One change should have one root cause or one vertical feature slice.
- A vertical slice includes implementation and its acceptance evidence.
- If the diff grows beyond the approved footprint, pause and remap blast radius.
- Do not mix phase renumbering, auth changes, unrelated cleanup, and content redesign.
- Record out-of-scope findings; do not silently lose them.
- Active security exposure is reported immediately.

### 3.5 Compile gate before continuing

After each coherent implementation step:

- import affected backend modules;
- compile/type-check touched surfaces;
- validate schemas/contracts;
- start the relevant service or isolated harness when practical.

Do not continue stacking changes on a broken integration base.

---

## 4. Evidence ledger and closure

### 4.1 Persistent evidence ledger

Every non-trivial change needs an evidence record in the change artifact, task file, or final report:

| Requirement | Before terrain | Change | Verification command/artifact | Result | Limits |
|---|---|---|---|---|---|
| | | | | PASS / FAIL / UNVERIFIED / N/A | |

Rules:

- A checked task without evidence is not complete.
- Raw output may be summarized in chat, but command/query/artifact identity must be reproducible.
- Harness evidence is labeled as harness evidence.
- A sample cannot prove an exhaustive invariant unless the sampling argument is explicit.
- Failure or unavailable terrain remains visible.

### 4.2 Three verification passes

**Pass A - Static**

- `git diff` contains every claimed change and no accidental scope;
- references/call sites/imports are valid;
- types, schemas, and contracts align;
- compile/build/type-check exits 0;
- no stale identifiers, unresolved placeholders, secrets, or debug bypasses.

**Pass B - Dynamic**

- targeted test reproduces the former failure and now passes;
- relevant full or subsystem suite passes;
- real endpoint, DB, seed, generator, progress, or startup behavior is exercised;
- error path behaves correctly;
- test data is cleaned.

**Pass C - Perceptual / user**

- real user flow is played;
- target viewport and maximum-content states are inspected;
- interactions, navigation, feedback, and role behavior are correct;
- images/SVGs are fetched/generated and looked at;
- required content is visible, legible, and not contradictory.

Mark a pass `N/A` only with a concrete reason.

### 4.3 Minimum non-regression matrix

| Path | Required observation |
|---|---|
| Original defect | same revealing check green |
| Sibling/neighbor | representative adjacent path green |
| Error path | wrong/invalid input gives expected safe result |
| Student role | no admin or other-student access |
| Admin role, if touched | authenticated and authorized |
| Data integrity | non-target rows/users/phases unchanged |
| Compile/startup | clean exit/start |
| User completion | flow can reach intended terminal state |

### 4.4 Fail-closed close decision

Do not close when any applicable answer is NO:

| Question | If NO |
|---|---|
| Original terrain is green? | Continue investigation |
| Diff matches the report? | Correct report or diff |
| Affected surface compiles/starts? | Stop |
| At least one collateral is verified? | Stop, except trivial docs |
| Required static/dynamic/user passes complete? | Mark unverified |
| Correct phase/user/data scope proven? | Stop |
| Security remains fail-closed? | Stop |
| Working capability replacement proven before removal? | Restore or complete replacement |
| Behavior/data change disclosed? | Do not close |
| Contradictions and approvals resolved? | Ask user |

### 4.5 Definition of Done

- [ ] Scope and applicable authorities recorded
- [ ] Terrain reproduced or confirmed
- [ ] Impact quantified and producer/consumer traced
- [ ] Root cause and invariants recorded
- [ ] Blast radius and rollback/recovery considered
- [ ] Minimal change implemented
- [ ] Static gate passed
- [ ] Dynamic gate passed where applicable
- [ ] Perceptual/user gate passed where applicable
- [ ] Same revealing check is green
- [ ] Sibling and error path checked
- [ ] Security/data/privacy close passed
- [ ] Generated pool/artifact integrity checked where applicable
- [ ] Real served/reseeded data checked where applicable
- [ ] Diff and report agree
- [ ] Existing behavior/data changes disclosed
- [ ] Unverified items and residual risks listed
- [ ] Handoff evidence recorded if work crosses sessions/models

---

## 5. Reporting and cross-model handoff

### 5.1 Honest completion report

Always separate:

1. What was already correct.
2. What this agent changed.
3. What was verified and with which terrain.
4. What remains unverified or blocked.
5. Observable behavior/data changes.
6. Residual risks and follow-ups.

```markdown
## Honest summary
- User request:
- Applicable plan/design rules:
- Files actually modified:
- Terrain before -> after:
- Static verification:
- Dynamic verification:
- Perceptual/user verification:
- Collaterals and roles:
- Security/data findings:
- Behavior/data changes:
- Unverified/blockers:
- Residual risks:
```

Reject reports that cite tests not run, endpoints not called, UI not opened, nonexistent files, or fixes absent from the diff.

### 5.2 Model/session handoff

When work moves because of token limits, provider changes, interruption, or a new session, record:

- exact objective and non-goals;
- applicable rules/plan;
- branch, commit, status, and relevant diff;
- files changed and why;
- evidence already collected;
- failed and unverified checks;
- running services/sessions;
- data mutations and recovery state;
- contradictions/decisions;
- exact next action.

The receiving agent must inspect terrain and diff; it must not trust the handoff summary as proof.

### 5.3 Independent and adversarial review

For destructive, security-sensitive, cross-phase, unusually large, or generated-content changes:

- use another agent/model when available, or a fresh-context review;
- ask the reviewer to falsify the result;
- inspect interfaces and consumers, not only touched files;
- replay acceptance checks;
- compare task checkboxes with evidence;
- challenge samples, stale caches, and optimistic summaries.

Self-review is useful but is not independent certification.

---

# Part II - Functional Reference Library

## 6. Investigation and bug hunting

### 6.1 Core hunting techniques (legacy §7-§11)

1. Interrogate data, not only code.
2. Cross-check claims: image mention vs image data, numeric type vs numeric answer, option count vs stored alternatives.
3. Render artifacts and inspect them.
4. Trace the full producer-to-user flow.
5. Find UI features whose activating data never occurs.
6. Compare with a working sibling, then verify local equivalence.
7. Play the app end to end or call real endpoint functions with real sessions.
8. Hunt answer leaks in data and renderer.
9. Measure structural variety, not name-only variation.
10. Distrust comments, names, and old reports.
11. Search every discovered bug pattern across siblings.
12. Use indirect signals: zero progress, zero attempts with traffic, impossible counts.
13. Enumerate value-dependent edge cases: equality, zero, symmetry, boundaries.
14. If one link is fixed but E2E still fails, hunt the next independent cause.

### 6.2 Data and security frontiers (legacy §5 and §9)

```text
pedagogy: generator -> seed/DB -> router/API -> frontend -> user eye
security: browser -> CORS/TLS -> authn -> authz -> validation
          -> business -> DB -> storage -> logs -> admin
```

At each frontier ask:

- Can this datum be NULL, stale, duplicated, differently named, or differently typed?
- Does the next layer actually consume the field?
- Does identity come from verified session or client input?
- Can a role or user cross ownership boundaries?
- Does the visual contradict or reveal the answer?

### 6.3 Bug archetypes A-Z (legacy §10)

| ID | Archetype | Detection signal |
|---|---|---|
| A | Broken relational mapping | NULL key, wrong join, wrong phase |
| B | Hidden zero-child rows | INNER JOIN hides missing alternatives |
| C | Dead feature | UI exists, activating data never occurs |
| D | Answer leak | correct answer visible/countable in prompt or SVG |
| E | Empty pedagogy after fix | leak removed but visual becomes useless |
| F | Type/contract mismatch | numeric UI receives text or stale field |
| G | Blind sibling patch | local control flow differs |
| H | Duplicate source of truth | maps/formulas drift |
| I | Fake variety | names change, structure does not |
| J | RNG degeneration | zero/equal/symmetric values break invariant |
| K | Seed not applied | code changed, stored/served data stale |
| L | Wrong-scope clear | another phase/user deleted |
| M | Progress dead end | phantom level or impossible unlock |
| N | Missing authn | protected route accepts no identity |
| O | Missing authz/IDOR | student reaches another resource |
| P | Secret exposure | diff/log/error contains credentials |
| Q | XSS/raw HTML | unsanitized dynamic HTML |
| R | Weak session lifecycle | insecure storage/logout/cookie flags |
| S | Bad CORS/CSRF | wildcard with credentials, missing protection |
| T | Unsafe upload/storage | no type/size validation, public bucket |
| U | Dependency risk | unnecessary or vulnerable package |
| V | Sensitive reporting | child PII or exploit details exposed |
| W | Unverified removal | working path deleted before replacement |
| X | False completion | checkbox/report without terrain |
| Y | Broken integration | touched unit passes, import/startup fails |
| Z | Collateral regression | sibling/role/data path damaged |

### 6.4 Report and diff probes

| Claim | Probe |
|---|---|
| "I modified this file" | `git diff` and status |
| "This fix is mine" | diff, blame/log when needed |
| "Bug is in this function" | real call site and reachable path |
| "Fixed" | same check plus consumer flow |
| "Compiles" | real type/import/build exit 0 |
| "Endpoint works" | real request/response |
| "UI is correct" | render and inspect |
| "Pool is valid" | query/validator over stored or generated pool |

One probe can lie. Verify that the probe observes the correct layer.

---

## 7. Verification recipes

### 7.1 Multiple-choice integrity (legacy §12.1)

Use `LEFT JOIN` when checking child cardinality so zero-child parents remain visible.

```sql
SELECT p.id
FROM preguntas p
LEFT JOIN alternativas a ON a.pregunta_id = p.id
WHERE p.fase_id = :fase_id
  AND p.tipo_pregunta = 'MULTIPLE_OPCION'
GROUP BY p.id
HAVING count(a.id) <> 4
    OR count(*) FILTER (WHERE a.es_correcta) <> 1
    OR count(a.id) <> count(DISTINCT a.texto);
```

Expected result: zero rows.

### 7.2 Variety and family coverage (legacy §12.2-§12.3)

```sql
SELECT seccion,
       count(*) AS filas,
       count(DISTINCT enunciado) AS enunciados,
       count(DISTINCT estructura_padre_id) AS familias
FROM preguntas
WHERE fase_id = :fase_id
GROUP BY seccion
ORDER BY seccion;
```

Interpret against the approved structural invariant. Non-NULL is not sufficient.

### 7.3 Numeric-answer contract (legacy §12.4)

```sql
SELECT id, respuesta_correcta
FROM preguntas
WHERE fase_id = :fase_id
  AND tipo_pregunta = 'RESPUESTA_NUMERICA'
  AND respuesta_correcta !~ '^-?[0-9]+([.,][0-9]+)?$';
```

Expected result: zero rows unless the type is intentionally changed and all consumers support it.

### 7.4 Image cross-check (legacy §12.5 and §12.8)

- Prompt mentions an image -> URL or inline SVG exists.
- Image exists -> prompt or interaction actually uses it.
- Fetch storage URL -> HTTP 200 and correct media type.
- Open the actual artifact.
- Confirm it does not reveal, contradict, crop, or hide required information.

### 7.5 Real endpoint and progression (legacy §12.7)

Use a real test student/session where safe:

1. request actual content;
2. submit correct and incorrect answers;
3. verify feedback and attempt records;
4. verify progress/unlock changes numerically;
5. reach the intended terminal state;
6. delete test attempts/progress in `finally`.

### 7.6 Authz smoke (legacy §12.10)

For protected/admin resources:

- no identity -> 401/403;
- student -> denied from admin;
- admin -> allowed;
- student A -> denied from student B data.

### 7.7 XSS, secrets, and session surface (legacy §12.11)

Search changed scope for:

- `dangerouslySetInnerHTML`, `innerHTML`, `eval`, raw markdown;
- project sanitizer usage;
- passwords, keys, tokens, connection strings, `.env`;
- auth tokens in `localStorage`;
- relaxed CORS, headers, or feature flags.

Every dynamic HTML sink needs the project sanitizer and visual re-check.

### 7.8 Post-clear/reseed integrity (legacy §12.12)

Before and after:

```sql
SELECT fase_id, count(*) FROM preguntas GROUP BY fase_id ORDER BY fase_id;
SELECT count(*) FROM users;
SELECT count(*) FROM alumnos;
```

Also compare progress, attempts, theory/config, and storage objects in the affected scope. Non-target counts must remain unchanged.

---

## 8. Pedagogy, generated content, and frontend UX

### 8.1 Pedagogical integrity

- Every exercise must be answerable from the information shown.
- Language, units, values, formula, answer, explanation, and visual must agree.
- Distractors must model plausible errors, not random noise.
- Do not reveal the answer through text, highlighting, counts, SVG labels, or geometry.
- Removing a leak must not leave an empty or meaningless visual.
- Measure structural variety and family coverage.
- Preserve approved terminology, difficulty, progression, and feedback.
- Logical consistency matters beyond arithmetic: expenses cannot exceed available money when asking "how much remains" unless debt is explicitly taught.

### 8.2 Fixed viewport and zero-scroll gate

No-scroll means all required content is visible and usable.

For every affected card type:

1. identify maximum-content cases;
2. render at every required viewport, especially the minimum supported viewport;
3. assert the content region has no unintended overflow:
   `scrollHeight <= clientHeight` and `scrollWidth <= clientWidth`;
4. confirm expected terms/steps/items equal visible rendered items;
5. inspect screenshots for clipping, overlap, tiny text, hidden controls, and broken navigation;
6. navigate first, middle, last, back, and completion states.

When content does not fit:

- split into pedagogically coherent steps;
- compact redundant labels and decoration;
- preserve readable typography;
- never hide content, introduce forbidden scroll, or reduce text below the design standard.

### 8.3 Frontend interaction gate

- Stable dimensions prevent layout shifts.
- Text fits buttons, cards, headers, and tiles.
- Controls remain reachable with keyboard/pointer as required.
- Loading, empty, error, success, back, next, and completion states work.
- API errors produce friendly messages without leaking internals.
- The visible phase/module/level identity matches the real route and data.

### 8.4 Generated mathematical content contract (legacy §25.4)

Every generated item should have one structured composition result:

```text
scenario + template + operands + formula + units
    -> prompt
    -> correct answer
    -> explanation
    -> anticipated errors/distractors
    -> visual data
```

The seed and UI consume that result; they do not recalculate independent answers.

### 8.5 Generator validation

Fail generation/seed, do not warn and continue, when:

- required fields are missing;
- placeholders remain unresolved;
- operands violate range or precision rules;
- formula cannot be evaluated independently;
- answer differs from independent recomputation;
- units or magnitude are incompatible;
- explanation uses different values;
- distractors duplicate or include multiple correct options;
- content exceeds an approved budget;
- forbidden vocabulary or out-of-scope concepts appear;
- visual reveals or contradicts the answer;
- family/variety constraints fail.

### 8.6 Coverage strategy

For finite template spaces:

- validate every template class;
- validate every compatible scenario class;
- cover min/max, zero, equality, rounding, carry/borrow, conversion direction, and precision boundaries;
- prove incompatible pairs fail closed.

For very large/random spaces:

- use deterministic seeded tests;
- enumerate equivalence classes and boundaries;
- add property/invariant tests;
- measure stored output distributions after seed;
- inspect representative artifacts from every family.

One random snapshot cannot certify a generator.

### 8.7 Core Guardrails for Natural Narrative Generation & Verification Across Phases

For creating or modifying any question-generation engine (Phase 4 and future phases):

1. **Root-Cause Resolution vs. Cosmetic String Patching**: Never attempt to resolve collisions, broken placeholders, or awkward text combinations using surface regex replacements on output strings if the pattern originates from a template or generator function. Always trace and fix the generator function or source dataset.
2. **Mandatory Perceptual Inspection of Real Generated Output**: Never mark a generator change complete based solely on JSON structure or source code inspection. Always instantiate the composer (`CompositorFaseX`), generate real output text with resolved data, and perceptually read a representative sample.
3. **Narrative Referent Invariant**: When a template shares or inherits a pool of alternative frames, verify template by template that every entity/referent mentioned in the question (e.g., "el primer paquete", "el total", "la diferencia") is explicitly present in ALL alternative frames in that pool.
4. **Direction-Aware Scaling and Filtering**: When filtering scenarios or templates for scale conversions or unit changes, matching criteria must strictly enforce the exact origin unit and conversion direction, not just a broad magnitude category.
5. **Physical & Domain Plausibility**: Value generation logic must enforce domain-specific physical constraints. For clinical/medical magnitudes (e.g., body temperature), values must stay within realistic biological boundaries (e.g. 36.5°C to 40.0°C), rather than generic mathematical ranges (e.g. 0.1°C to 2.0°C).
6. **Universal Container Terms**: In dynamic templates where the object is variable (`{objetos_0}`, `{objeto_medible}`), use container words that apply universally across item types (e.g. bolsas, cajas, paquetes, moldes, recipientes, frascos, lotes, porciones), avoiding hyper-specific containers (e.g. hormas, pallets, mallas) that produce unnatural pairings.
7. **Mandatory Dual Verification Suite**: Before declaring work complete on any generation engine:
   - Run the static and dynamic narrative audit script (`python scripts/audit_fase4_narrativas.py --muestras 80` or phase equivalent).
   - Run the full automated test suite for the module (`pytest tests/test_faseX_*.py`).

### 8.8 SVG and image rules

- Generate from structured data, not answer text.
- No hidden answer in `<text>`, labels, colors, counts, or geometry.
- Stable viewBox/aspect ratio and readable text.
- No decorative frame that consumes needed learning space unless design requires it.
- Use consistent text color and adequate contrast.
- Validate XML/SVG and inspect rendered pixels.
- External storage URLs must resolve.

### 8.9 Content budgets

Every budget must be countable: characters, lines, steps, labels, options, cards, or visible height.

Budget validation belongs at generation/seed time and at render time. Character limits alone cannot prove that a card fits because typography, line wrapping, tables, and viewports vary.

---

## 9. Security and privacy

### 9.1 Non-negotiable rules (legacy §6 and §14)

1. Frontend never connects directly to PostgreSQL.
2. Sensitive identity comes from verified server session, not request body.
3. Every user-owned query filters by verified user/student identity.
4. Admin routes require explicit server-side ADMIN authorization.
5. Passwords use approved slow hashes (bcrypt under current project policy); password policy remains at least 8 characters with upper, lower, and digit unless the maintained auth design changes it; reset tokens use cryptographic randomness.
6. Secrets stay in protected environment configuration, never code, docs, logs, screenshots, or client bundles.
7. Cookies/sessions use `httpOnly`, `secure` in production, an approved `sameSite` policy, server verification, and real logout invalidation.
8. CORS uses exact origins; never wildcard with credentials.
9. Dynamic HTML is sanitized through the project helper.
10. Uploads validate type, size, ownership, and storage visibility.
11. Errors keep context server-side without leaking SQL, stack, env, tokens, or child data.
12. Dependencies are necessary, maintained, and checked for material vulnerabilities.
13. Security remains fail-closed when configuration is missing.
14. CSP, anti-clickjacking, and other security headers are preserved unless a reviewed replacement is provided.
15. Public reports use safe local/staging proof and avoid exploitable production detail.

### 9.2 Security pre-flight

- Which roles and identities are affected?
- Is any client-supplied identity/grade/progress trusted?
- Is raw HTML or markdown introduced?
- Are new endpoints protected?
- Does the change widen CORS, cookies, storage, logs, or uploads?
- Does a risky auth/session change need a reversible feature flag?
- Can student A access student B?
- Can a missing config enable a dangerous path?
- Can errors expose secrets or child PII?

### 9.3 Security close

- [ ] No credentials -> protected route denied
- [ ] Student -> admin denied
- [ ] Cross-student access denied
- [ ] Logout/session behavior intact
- [ ] Dynamic HTML sanitized and visually intact
- [ ] No secrets or unnecessary PII in diff/logs/responses
- [ ] CORS/headers/cookies not weakened
- [ ] Upload/storage scope not widened
- [ ] No unknown vulnerable dependency introduced
- [ ] Destructive actions unreachable by unauthorized users

---

## 10. Data, database, environments, and production

### 10.1 Database ownership and async behavior (legacy hard Rules 01-03)

- Backend owns PostgreSQL access.
- I/O in request paths is async; use `async`/`await`, `asyncio.sleep`, and an async HTTP client rather than `time.sleep` or blocking requests.
- Long-running request work moves to the existing background-task or queue mechanism.
- Routers validate, delegate, and respond; services own business logic.
- Queries use bound parameters/ORM expressions, not string-built SQL.
- User data is scoped by verified identity.

### 10.2 Query and schema hygiene (legacy §15)

- Inspect actual schema/model names before querying.
- Confirm canonical phase IDs from data, not filenames.
- Use `LEFT JOIN` for missing-child audits.
- Validate NULL, duplicates, cardinality, types, and ownership.
- Prefer existing models over schema churn when they can express the requirement.
- Migrations include forward, backward/recovery, data impact, and verification.

### 10.3 Seeds and clears

- Clear only the canonical target scope.
- Snapshot non-target counts before destructive local work.
- Reseed twice when idempotency is required.
- Confirm seed version/state and served data.
- A generator validation failure aborts the seed.
- Never claim code data changes until DB/served data reflects them.

### 10.4 Test data

- Use synthetic users/data.
- Do not expose real child data.
- Delete attempts/progress/resources created by tests in `finally`.
- Keep test database/environment isolated.

### 10.5 Environment isolation (legacy hard Rule 13)

- Local, development, and production databases are separate.
- Local agent work never points at production by default.
- Protected environment files remain unmodified unless explicitly authorized and safe.
- Scripts that can clear/seed must refuse production connection strings unless operating through the approved production workflow.
- Resolve current environment topology from maintained docs/configuration; do not embed credentials in agent rules.

### 10.6 Destructive local/dev operations (legacy §25.3)

Before delete, clear, reseed, migration, or bulk rewrite:

1. identify exact environment and target;
2. show resolved IDs/paths/tables;
3. snapshot counts or create recoverable backup as proportional;
4. prove exclusion of non-target phases/users;
5. request approval when user data or broad state is involved;
6. execute the narrow operation;
7. compare post-state;
8. report recoverability.

### 10.7 REST and error consistency (legacy hard Rules 08 and 11)

Use conventional resource methods and paths:

- GET list/detail;
- POST create;
- PATCH update;
- PUT replace;
- DELETE remove with appropriate status.

Return stable, client-safe error shapes with code, message, field when relevant, and request ID when available. Keep traceback/context server-side.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "field": "field_name",
    "request_id": "req_..."
  }
}
```

### 10.8 Production discipline (legacy §16)

Production work requires:

- explicit authorization;
- current deployment source of truth;
- backup or tested recovery;
- exact target/environment confirmation;
- minimal scoped change;
- health/startup/log checks;
- proof new code/data is actually running;
- user/progress integrity checks;
- rollback decision if critical gates fail.

Never infer deployment success from `git push`.

---

## 11. Large changes, OpenSpec, and change programs

### 11.1 Diagnose before proposing (legacy §17)

- Read the affected subsystem and consumers.
- Translate complaints into concrete terrain and root causes.
- Use a cheap mockup/harness for uncertain UX or architecture.
- Obtain user decision where product semantics differ.
- Prefer existing models and helpers.
- Delete temporary harnesses after verification.

### 11.2 OpenSpec usage (legacy §25.1)

Use OpenSpec for:

- multi-file behavior changes;
- new capabilities;
- migrations/refactors;
- changes with important acceptance criteria or dependencies.

A change is a vertical slice, not a batch. It must be independently implementable and verifiable.

Artifacts:

- proposal: why and scope;
- spec: testable requirements;
- design: decisions and trade-offs;
- tasks: executable steps;
- evidence: reproducible proof for completed tasks.

Checking a task without evidence does not satisfy this manual.

### 11.3 Programs of changes (legacy §25.2)

- Map dependency graph before implementation.
- Keep irreversible work behind reversible foundations and proof.
- Finish static/dynamic/user gates for one change before advancing.
- Integrate after each slice; do not postpone all integration to the end.
- Reassess scope when cumulative diff becomes difficult to review.
- Preserve user data and rollback strategy across the program.

### 11.4 Git and documentation hygiene (legacy hard Rules 12 and 14)

- Do not commit/push unless authorized by current project/user rules.
- Conventional commit when requested: `<type>(<scope>): <description>`.
- Keep first line concise; body explains what and why.
- Never version secrets, `.env`, dumps, or generated test debris.
- Documentation changes with behavior.
- Git is history; do not leave large commented-out dead blocks.

---

## 12. Review playbooks and templates

### 12.1 Audit another agent

1. Read request/spec, not only summary.
2. Inspect status, diff, and real call sites.
3. Compare every completed task to evidence.
4. Import/build/start affected surfaces.
5. Replay central acceptance behavior.
6. Inspect DB/API/UI consumers.
7. Try boundary and plausible-wrong cases.
8. Verify collateral roles/phases/data.
9. Separate pre-existing, changed, unverified, and behavior changes.

### 12.2 Guided scenarios (legacy §22)

**Progress never advances**

- Inspect real progress rows and unlock metadata.
- Trace answer -> attempt -> progress -> unlock.
- Search phantom levels/duplicate maps.
- Answer correctly through the real endpoint and watch the number change.

**Richer theory or visual content**

- Sanitize dynamic HTML.
- Render maximum content at target viewport.
- Verify no clipping, no answer leak, and navigation completion.

**Apply a sibling fix**

- Compare control flow and local data shape first.
- If structure differs, derive a local fix.
- Verify both sibling and target afterward.

**Reseed a phase**

- Confirm environment and canonical phase ID.
- Snapshot counts and user/progress scope.
- Validate generator, run seed, verify idempotency and served data.

**Another agent reports many fixes**

- Recount from diff and terrain.
- Reject nonexistent or unexecuted evidence.
- Re-run critical behavior independently.

**User asks to remove a guard or working helper**

- Explain the safety/capability impact.
- Add and verify the replacement first.
- Remove only after proof.

### 12.3 Close template

```markdown
## Close
- Objective:
- Files in real diff:
- Terrain before -> after:
- Static gate:
- Dynamic gate:
- Perceptual/user gate:
- Collaterals/roles:
- Security/data close:
- Behavior/data changes:
- Unverified/blockers:
- Residual risks:
- Evidence location:
```

### 12.4 Quick route (successor to legacy §24)

```text
READ CORE -> RESOLVE APPLICABLE PLAN -> OBSERVE TERRAIN
-> TRACE PRODUCER/CONSUMERS -> DEFINE INVARIANTS/BLAST RADIUS
-> IMPLEMENT MINIMALLY -> STATIC -> DYNAMIC -> USER/PERCEPTUAL
-> COLLATERAL/SECURITY -> HONEST REPORT/HANDOFF

NEVER:
- pass without evidence
- close unavailable checks
- trust names/comments/reports over behavior
- equate hidden overflow with visible content
- derive prompt and answer independently
- apply sibling changes blind
- reseed/clear the wrong phase/environment
- weaken auth/sanitization/CORS
- expose secrets or child data
- remove working capability before verified replacement
- load an unrelated historical phase plan
```

---

## 13. Legacy reference map

This map preserves discoverability for active scripts and documents that cite Version 1 section numbers.

| Legacy reference | Version 2 location |
|---|---|
| §1-§2 Mission/core behavior | §0-§3 |
| §3 Improve-first | §3.1 |
| §4 Contradictions | §1.5 |
| §5 Architecture/frontiers | §2.3, §3.3, §6.2 |
| §6 14 hard rules | §3.3, §9, §10, §11.4 |
| §7 Deep reasoning | §0, §2.2 |
| §8 PRO loop/blast radius | §0.1, §2, §4 |
| §9 Data/security frontiers | §6.2, §9, §10 |
| §10 Archetypes A-Z | §6.3 |
| §11 Detection/report probes | §6.1, §6.4 |
| §12 Verification recipes | §7 |
| §13 Robust fix | §3 |
| §14 Security protocols | §9 |
| §15 Database discipline | §10.1-§10.5 |
| §16 Production | §10.8 |
| §17 Large changes | §3.4, §11.1 |
| §18 Testing/DoD | §4 |
| §19 Report integrity | §5 |
| §20 Anti-patterns | §0, §12.4 |
| §21 Close matrix | §4.4 |
| §22 Scenarios | §12.2 |
| §23 Templates | §2.5, §4.1, §5.1, §12.3 |
| §24 Cheat sheet | §12.4 |
| §25.1 OpenSpec | §11.2 |
| §25.2 Programs | §11.3 |
| §25.3 Destructive local ops | §10.6 |
| §25.4 Generated content | §8.4-§8.8 |

Historical documents can retain old citations. New and actively maintained documentation should cite Version 2 functional sections.

---

## 14. One-sentence doctrine

> Do not trust what code, names, reports, or checkboxes claim: observe real terrain, trace producer and consumer, fix one root safely, prove the same failure gone through static, dynamic, and user-facing evidence, preserve neighboring behavior and child safety, and report every uncertainty honestly.
