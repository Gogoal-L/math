# Frontier V: finite-bank goal-tolerance repair, source-inspired but independently derived

**Date:** 2026-10-10. **Upstream version:** `openai/math` [`fd4aeeb2`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). **Scientific authority:** independent algebraic result and synthetic executable, not a claim that S09 native dynamics satisfy any new hypothesis. The DPT controller remains owner of the legitimate preparation set, known command conditions, scorer, model identity and acquisition decisions.

## The sharper question

Existing DPT-R1 results distinguish a source tangent nullspace, fixed-Q one/two-row behavior at different preparation radii, one-Newton versus full/affine goal adequacy, a valid local Eth lift and command-order contrasts. The unresolved practical question is not just *whether* a missing direction exists. It is **which collection of actual affordable pretarget readouts would remove every materially goal-distinct but observation-indistinguishable pair across a declared command family**. No differentiability is required for a finite, possibly nonsmooth bank.

This is a mathematically exact *finite-bank, fixed-candidate-library* question. It does **not** establish a globally minimal physical state, an autonomous update, or an upper bound on the entire reachable preparation family. A known-answer bank contains only the specified same-law, physically legal histories if the controller establishes that fact; the tool does not.

## Proposition A: interval minimax equals the largest compatible goal-interval diameter

Let `H={h_1,...,h_N}` be a finite set of legal histories in a **single model/source and matched reference**, and let `C` be a finite family of fixed, available future commands or command words. Existing retained observations are `O_i in R^m`; candidate scalar features are `P_ij`, `j=1,...,p`. The true readout of each component may lie in **the independent coordinate interval** `[O_ir-sigmaO_r,O_ir+sigmaO_r]` or `[P_ij-sigmaP_j,P_ij+sigmaP_j]`. Here 'independent coordinate interval' is a Cartesian-product uncertainty set, **not a probability/independence claim**. Per history and command, the true scalar future goal may lie in `[g_ic-eta_ic,g_ic+eta_ic]`. All radii are nonnegative and the same declared goal units apply within each command.

For a fixed nonadaptive feature subset `S`, call `i,j` *compatible* if their retained observation intervals and all chosen feature intervals overlap componentwise. For `i != j`, this is equivalent to

```
all_r abs(O_ir - O_jr) <= 2*sigmaO_r
and all_s_in_S abs(P_is - P_js) <= 2*sigmaP_s.
```

Equality is compatibility (closed intervals touch), **not separation**. All histories are self-compatible. The optimum worst-case deterministic scalar-goal prediction error when the decoder knows the command `c` is exactly

\[
R_c(S)=\max\left\{\max_i\eta_{ic},\quad
\frac12\max_{i<j:\,i\sim_S j}(|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc})\right\},
\]

where the second maximum is omitted if no distinct compatible pair exists. The overall command-coordinatewise tolerance requirement is `R_c(S) <= tau_c` for **every** `c`. Each command may use a different decoder, but **the same feature subset** is retained before the target; no future goal is an input. This theorem presumes simultaneous Cartesian worst-case uncertainty across histories and intervals; no stochastic noise law, confidence level, or source correlations are inferred.

**Proof.** Every possible readout `y` determines a set `H_y` of compatible histories. For that `y` and command `c`, all feasible true goals form a union of intervals; the midpoint between its smallest possible value and largest possible value minimizes worst-case absolute error with radius half their span. Across all `y`, any pair of compatible histories has a common readout `y`, giving the lower bound. Conversely the maximal span of any `H_y` is bounded by the largest pairwise upper-endpoint/lower-endpoint difference among its histories, with self intervals included. Taking maxima across `y` gives the formula. A single history with `eta_ic > tau_c` cannot be repaired by *any* more precise measurement of its identity.

**Important quantifier.** This is a minimax over **arbitrary deterministic decoders** on the finite bank, stronger than checking a particular linear or neural decoder fit. It is **not** an achieved error of the current DPT decoder and cannot rescue poor approximation architecture by itself.

## Proposition B: minimum-cost robust measurement repair is an exact hitting-set problem

Suppose all `eta_ic <= tau_c`. First form the **base-ambiguous and goal-conflicting pair universe**

\[
\mathcal U=\left\{\{i,j\}: i<j,\;|O_{ir}-O_{jr}|\le2\sigma^O_r\ \forall r,\;
\exists c\in C:\ |g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}>2\tau_c\right\}.
\]

Candidate feature `s` resolves the conflicts

\[
E_s=\{\{i,j\}\in\mathcal U:|P_{is}-P_{js}|>2\sigma_s^P\}.
\]

Then `R_c(S)<=tau_c` for every command `c` **if and only if** `union_{s in S} E_s = U`. Proof: Proposition A says exactly those conflicting pairs must become incompatible, and a Cartesian coordinate product makes a pair incompatible precisely when at least one selected scalar coordinate is separated. With positive additive declared costs `w_s`, the minimum feasible total cost is the weighted set-cover optimum. When a conflict lies in no `E_s`, the supplied feature library cannot meet the goal contract; output the failing same-law history pair and its command.

For `p<=18` by default, [`goal_repair_cover.py`](../dpt_tools/goal_repair_cover.py) finds the exact minimum-cost subset using branch-and-bound; larger libraries use weighted-greedy and label the minimum cost **unproven**. For M nonempty conflicts, ordinary weighted greedy has the classical harmonic approximation factor `H_M`, conditional on cost additivity, fixed cover sets, and feasibility. This is not an application of F175's special constant-factor expectation-threshold comparison theorem.

### A hand-checkable obstruction and a relaxation gap

Construct six histories forming three isolated matched base-observation pairs: `(0,1)`, `(2,3)`, `(4,5)`. The members of each pair have fixed future goal values 0 and 4, so each pair is a conflict at `tau=1`. Three candidate features have separation sets

```
A covers pairs 0 and 1;
B covers pairs 1 and 2;
C covers pairs 0 and 2.
```

All three unit-cost integer sensor choices require at least two features, and any two work. A **fractional** relaxation assigning `x_A=x_B=x_C=1/2` satisfies all constraints at cost `3/2`; summing the three pair constraints shows this is the fractional optimum. The integral optimum is 2; **integrality gap 4/3**. F175 does not erase this gap: its setting is a monotone family of subsets, random Bernoulli event-costs `p^|S|`, and a threshold rescaling, not arbitrary acquisition-price hitting set.

**Noise counterexample.** For two candidate readings whose pairwise gaps are both 0.8 and interval radii both 0.5, neither alone nor both together separates the pair in our coordinatewise-box model. A *different* model with a joint Euclidean-radius-0.5 ball would separate them jointly because `sqrt(0.8^2+0.8^2)>1`; the set-cover reduction **does not apply without modification** under Euclidean joint noise. Do not silently reuse the old `goal_ambiguity_audit.py` Euclidean observation-radius formula.

**Sub-picocost numeric counterexample.** A pruning rule with an arbitrary `1e-12` cost tolerance can falsely claim cost optimality for candidate prices on the order of `1e-15`. The tool uses strict positive-price comparisons and reports a *numerical exact search on supplied float costs*, not a symbolic real-arithmetic proof.

## Source-critical OpenAI Math research: new families, real and failed transfers

The original source manuscripts below are pinned to `fd4aeeb2`. The examined surface is named; no claim of exhaustive PDF page-by-page visual verification or independent proof of the source headline is made. The cited Lean descriptions are *selected statement scopes*, not separate transfer proofs.

| Family and inspected primary sections | Strongest source-grounded contribution | Constructive transfer, strongest obstruction, and decision |
|---|---|---|
| **F175**, [Integral and fractional expectation thresholds](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Integral-and-fractional-expectation-thresholds-are-equivalent-September-23-2026/build/source/sections), inspected all four included section files' theorem/proof mechanisms including multiscale selector and rounding (see `selector.tex` and `rounding.tex`) | For a nonempty proper increasing finite set family, defines integral and fractional **Bernoulli-price expectation thresholds** and shows `q_f <=25*512^4*q`. The rounding constructs a multiscale mass capture and uses a random-color expectation contradiction. [Lean selected scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/175.md). | **TRANSFER AS PROOF DISCIPLINE ONLY.** First define exact cover semantics and price; a fractional surrogate may be cheaper and require honest integrality analysis. Its numeric theorem **does not** give a universal fixed-cost DPT sensor-rounding factor. |
| **F125**, [Single-exponential k-median recovery](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Single-Exponential-Recovery-and-Bounded-Price-Strictness-for-Metric-k-Median-September-24-2026/build/sections), inspected introduction/recovery theorem and stability-dichotomy/final assembly proof | Supplied anchor with accurate *distinct* proxies for all but `O(log N)` comparison clusters allows exact-budget recovery in normalized integral metrics. A dichotomy distinguishes a flat `opt_k` curve from a cardinality sensitivity jump. [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/125.md). | **WATCH, high pilot value.** Inspect whether most reachable history fibers share one low-information decoder and a small *predeclared* exceptional domain needs a different feature. Selecting excluded histories after seeing failure is invalid. Neither metric k-median's `1+2/e` nor its cluster-complexity guarantee transfers to DPT. |
| **F139**, [Subpolynomial query complexity for log-concave sampling](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections), inspected main theorem/model, proof overview, Gaussian block-Krylov lower construction | Exact value+gradient oracle, minimizer known, `I<=D2V<=2I`, arbitrary computation between calls: `Q(d)<=C_eps*d^eps` and `Q(d)>=c log d` for fixed total-variation accuracy. The lower bound uses hidden random rotations and a Gaussian statistic. [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/139.md). | **PARK** for immediate DPT. Crucial lesson is *oracle-call count is not total compute, physical data acquisition, or measurement count*. Do not use this headline to claim two native LTspice runs suffice or GPU cost vanishes. |
| **F327**, [Nontrivial Markov type forces superreflexivity](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nontrivial-Markov-Type-Forces-Superreflexivity-September-23-2026/build/main.tex), inspected stationary/reversible finite-Markov definition and main theorem; [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/327.md) | Under stationary reversible finite-Markov walks, Markov-type bounds control expected powered displacement in a Banach target; the paper characterizes superreflexivity via nontrivial Markov type. | **PARK** until genuinely stochastic stage uncertainty is measured. Deterministic LTspice discretization/branch bias is not an unbiased reversible Markov error. A separate martingale RMS identity may be useful with measured zero-mean/orthogonality conditions, independently of F327's theorem. |
| **F110**, [squared-log randomized k-server](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Squared-logarithmic-randomized-k-server-on-arbitrary-metrics-September-24-2026/build/source/main.tex), inspected model statement and complete manuscript chapter map; [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/110.md) | One policy obtains an online movement-cost guarantee against all *oblivious* request sequences, given a k-server metric and initial configuration. | **PARK**: request servicing/movement cost and online adversary are not equal to adaptive choice of LTspice switching command, whose value is discrimination rather than servicing a metric request. |
| **F331**, [reflexive midpoint / diamond distortion](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Asymptotic-midpoint-uniform-convexity-and-unbounded-diamond-distortion-in-a-reflexive-tree-space-September-27-2026/build/main.tex), inspected statement and formalization scope; [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/331.md) | Reflexive Banach example with asymptotic midpoint uniform convexity but diamond-depth `k` distortion at least `sqrt(1+k/12)`. | **WATCH** as a warning against extrapolating local midpoint or tangent regularity into globally stable multi-word charts. No claim that the actual DPT preparation metric is the constructed Banach metric. |

### Closest-prior subtraction (not an originality claim about set cover)

- [Healy and Leo (2026), *Which experiments test a model?*](https://doi.org/10.1016/j.jet.2026.106191) explicitly uses pairwise separation and integer set cover to select minimal classification/testing experiments in a deterministic preference-model setting. Our pair-cover reduction is not a novel abstract algorithm or generic combinatorial theorem.
- [Krause, McMahan, Guestrin, Gupta (2008), *Robust Submodular Observation Selection*](https://www.jmlr.org/papers/v9/krause08b.html) studies robust observation choice under specific submodularity assumptions. The present goal-diameter design is not automatically the same objective or a Gaussian/Bayesian information gain.
- [Willems (1986), *From time series to linear system*](https://doi.org/10.1016/0005-1098(86)90066-X) places trajectory families and state equivalence before representation. Even if the finite feature set predicts a designated list of goals, autonomous state updates must satisfy a stronger **future-word closure**. The current tool does not claim behavioral realization.

**Potential DPT residual contribution:** not hitting set itself. Rather: same-law physical reachable history selection, pulse/command-specific true goal-tolerance boundaries, correct interval/numeric/model error accounting, pretarget feature availability and acquisition-versus-retention cost, and prospective discrimination versus strong ordinary/one-Newton. A successful native generalization across fresh histories is needed before treating it as a scientific method result.

## Adversarial simulated roundtable (public ideas reconstructed; NOT actual statements)

**Question:** Does cheap predictive sufficiency mean low-dimensional physical dynamics, few actual sensors, or a low-cost finite-table decoder?

**Willems lens (behavioral system):** The equivalence relation must persist under future concatenation, or a current-goal code will fail after an unseen command. Response: specify the command language and horizon; distinguish bank goal prediction from right-congruence and autonomous `T_a`.

**Talagrand/F175 lens (covering certificates):** A fractional feasibility certificate is not automatically an implementable integer collection of sensors; check the underlying probabilistic cost. Response: our criterion uses fixed-price hitting set with an observed `4/3` gap in a three-conflict example, not the F175 constant-factor theorem.

**Krause lens (sensor utility):** A small feature count is not the same as minimized measurement cost or robust utility. Response: costs and goal-coordinatewise radii are explicit; *joint correlated noise* and physical sensor qualification remain outside the mathematical oracle.

**Moderator's live crux:** the scientifically decisive information is **which admissible history pairs remain inseparable under a legitimately obtainable pretarget feature**, not the number of parameters in a simulator or how many PDFs were read. An apparent cheap state is meaningless if its features are only posttarget outputs or hidden internal states at deployment.

## Material candidate portfolio, after hostile pruning

| Hypothesis / move | Observable discriminator | Disposition |
|---|---|---|
| H1. A small pretarget feature set controls goal ambiguity for all currently relevant commands | Construct same-law, source-reachable bank; run minimal cover against fixed tau; recheck on new legal histories | **PURSUE: executable independent candidate** |
| H2. One fixed-Q row fails only on a few physically definable preparation regimes | Compare a domain-qualified exception set selected **before** goal scoring with both ordinary full state and low-Q decoder on same-law examples | **CONDITIONAL pilot**, inspired by F125's few bad clusters but not guaranteed by it |
| H3. Low feature count implies low autonomous state dimension | Compare single-command goals versus same histories after `AB`/`BA` future words and legitimate Eth lift | **REJECT as stated**: can predict immediate goals yet fail future-update closure |
| H4. An LP fractional sensor weighting certifies that many fewer actual sensors suffice | On three conflict pairs, fractional cost=1.5 versus discrete=2 | **REJECT** in generic fixed-cost cover; no transfer of F175 constant loss |
| H5. Stochastic aggregation can improve linear-stage defect budget from sum to RMS | Verify martingale differences and stage covariance rather than infer from numerical tolerance | **PARK** until actual noise process exists |
| H6. Few exact solver calls imply cheap physical measurement | Compare F139 oracle assumptions with actual input/circuit/CPU costs | **REJECT**: exact value-gradient oracle / unbounded between-call work is not LTspice cost |

### Stronger next questions, not new simulator authorization

1. **Existing-data pilot:** on one *physically legal* bank of 150/600 V histories, construct aligned `[histories x commands]` scalar goal matrix for full, affine and one-Newton under the same declared scoring operator, but do **not** mix rival goal predictions into a single ground-truth bank. Separately construct `O`, the available candidate `P`, measurement uncertainty and per-command tolerance. Does the two-row fixed-Q feature set eliminate conflicts one row misses? What is the actual extra RAW/storage/acquisition cost?
2. **Command extension:** does the winning subset remain sufficient on a predeclared new future command word (including event readout and target normalization)? If not, record the shortest and largest material pair witness; upgrade the library only with legitimate pretarget features.
3. **Continuous-domain check:** check whether finite witness direction agrees with source-null and nonlinear fiber-curvature auditors. A bank positive gives no all-reachable upper bound; a bank failure gives a valid lower bound only when histories themselves are accepted as physically reachable.
4. **Stage update test:** if feature set predicts endpoint goals but fails a stage-right-congruence check, do not call it an autonomous predictive state. Check Sol9 Eth transition with real guard and lift, then estimate added information or resort to direct command-to-goal decoders.

## Reproducible contract and results (synthetic only)

CLI: `python goal_repair_cover.py matched_history_bank.npz --output repair_report.json`. Required NPZ keys: `observations (N,m)`, `goals (N,K)`, `candidates (N,p)`, `observation_radii (m,)`, `candidate_radii (p,)`, `goal_tolerances (K,)`, `candidate_costs (p,)`; optional `goal_uncertainty (N,K)`, `candidate_names (p,)`, `command_names (K,)`. All numeric inputs finite; radii/tolerances nonnegative and costs strictly positive. `N>=1`, `K>=1`; columns may be zero. With equal goal rows the same bank may support several matched fixed commands. No assumption about normalized relative RMS versus absolute goal units is made by the software.

Outputs include baseline and selected exact finite-bank minimax errors per command, chosen feature indices/labels and price, source conflict count, or an unrepairable-pair witness. `NO_REPAIR_NEEDED`, `INTRINSIC_GOAL_UNCERTAINTY`, `NO_LIBRARY_REPAIR`, `EXACT_MIN_COST_REPAIR`, and `GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM` are separate statuses. An exact cost solver is enabled up to 18 candidate features by default; larger inputs return a feasible weighted-greedy upper bound and the classical `H_M` set-cover factor, not a proven optimal price.

Direct focused test evidence: 14 tests, including 80 random independent weighted-set-cover brute-force checks, 65 general random noise/goal-interval full-subset checks, analytic hand cases, impossible regimes, exact-touching thresholds, Euclidean-versus-box counterexample, sub-picocost guard, and end-to-end NPZ CLI. **These tests are mathematical/synthetic only**. The library doesn't access private S09 data, update frozen predictions or trigger LTspice.

**Exit condition:** deliver to the controller only after input ancestry and pretarget provenance are known; if source history bank cannot be aligned without outcome leakage, classify this as an OPEN data contract, not a model failure. A negative finding can rationally favor direct command-to-goal prediction over adding hidden state.
