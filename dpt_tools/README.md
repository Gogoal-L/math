# DPT mechanical audit tools

These scripts turn tangent information, bounded-noise goal ambiguity, finite command congruence and original-expression definedness checks into reproducible numerical artifacts. They are deliberately conservative: a PASS never upgrades a numerical linearization into a native theorem. They require Python 3.10+ and NumPy (`pip install -r requirements.txt`).

The controller's entry remains [DPT_MATH_RESEARCH_MAP.md](../DPT_MATH_RESEARCH_MAP.md).
The [core literature bundle](../literature/README.md) provides stable PDF names and
statement-level Lean correspondence. No S09 archive adapter is required to read
or run these tools. Before native replay, record history/command identity,
units and time convention, reference/query, information budget and provenance
alongside the input; array compatibility alone does not validate that contract.

## `predictive_state_audit.py`

Input is an `.npz` file with:

- `DO`: observation Jacobian, shape `(m_obs, n_state)`;
- `DG`: stacked future-goal Jacobian, shape `(m_goal, n_state)`;
- optional `DP`: candidate measurement Jacobian, shape `(m_meas, n_state)`;
- optional `DP_candidates`: one scalar candidate measurement per row;
- optional `candidate_labels`: labels aligned with `DP_candidates`;
- optional `DO_scales`, `DG_scales`, `DP_scales`: scale-indexed Jacobians;
- optional `radii`, `remainder_observation_coeff`, `remainder_goal_coeff`, `remainder_measurement_coeff` for the full-direction conditional Taylor bound;
- optional `observation_noise_radii`, `measurement_noise_radii` for independent measurement-error envelopes.

Run:

```bash
python predictive_state_audit.py audit_input.npz --output audit_report.json
```

The center report computes:

- `K = ker(DO)`;
- `r_G = rank(DG|_K) = dim(K/N)` where `N = K intersect ker(DG)`;
- the scalar-measurement lower bound `k >= r_G`;
- whether `ker(DP|_K) subseteq ker(DG|_K)` numerically;
- the minimum-norm linear factor from measurement perturbations to goal perturbations and its 2-norm gain;
- exact-small-subset and greedy candidate selection when `DP_candidates` is supplied.

The multiscale block repeats the tangent audit at each supplied scale. The previous formula
`||Delta G - A Delta P|| <= (C_G + ||A|| C_P) r^2` was **not valid
for arbitrary state perturbations**: it omitted existing observations.
For example, O(x,y)=x, P(x,y)=y and G(x,y)=x+y are all linear, yet A=1
on ker(DO) cannot predict a change in x from Delta P alone.

The updated conditional block factors `DG = B DO + A DP + E`. For
`||delta h||_2 <= r`, separately valid (and independently justified)
Taylor remainders `||R_O||<=C_O r^2`, `||R_P||<=C_P r^2`,
`||R_G||<=C_G r^2`, and noise radii `sigma_O, sigma_P`, it gives:

```text
||Delta G - B Delta O - A Delta P||
  <= ||E|| r + (C_G + ||B|| C_O + ||A|| C_P) r^2
     + ||B|| sigma_O + ||A|| sigma_P
```

The noise term applies when Delta O / Delta P are replaced by noisy
measurements; without supplied noise arrays the program assumes zero.
Missing observation, goal or measurement remainder means **no quadratic
bound is emitted**. The output is a conditional algebraic estimate, not
a verified native-model certificate. Rank thresholds, channel units and
the validity domain remain independent audit requirements.

Rank and pseudoinverse now use the same strict singular cutoff
`s > max(atol, rtol*s_max)`. The reported factor is the minimum-norm factor
on the retained singular directions; discarded goal components stay in `E`.
For the analytic example `O=0, P=eps*y, G=y`, retaining `eps` gives gain
`1/abs(eps)` and noise error `sigma_P/abs(eps)`. Discarding `eps` gives
`E=DG` and the state-ball bound `r`, rather than an exact-recovery report
using a direction rejected by the rank audit. This is numerical truncation,
not proof of physical unobservability. Fix units/whitening before interpreting
the cutoff and compare plausible thresholds near weak singular values.


## `command_domain_audit.py`

This audits every `inv` node in the original sampled expression tree. It does not simplify the expression before checking definedness.

Expression nodes support `const`, `var`, `eye`, `neg`, `add`, `sub`, elementwise `mul`, `matmul`, and `inv`. Each inverse can carry a `label`.

Example:

```json
{
  "op": "matmul",
  "args": [
    {
      "op": "inv",
      "label": "I-A",
      "arg": {
        "op": "sub",
        "args": [{"op": "eye", "n": 2}, {"op": "var", "name": "A"}]
      }
    },
    {"op": "var", "name": "B"}
  ]
}
```

Samples are a JSON list:

```json
[
  {"id": "S09-center", "vars": {"A": [[0.1, 0.0], [0.0, 0.2]], "B": [[1.0, 0.0], [0.0, 1.0]]}}
]
```

Run:

```bash
python command_domain_audit.py expression.json samples.json --output domain_report.json
```

The auditor now creates a static inventory of every original inverse node by unique AST path (even if evaluation stops at an earlier undefined inverse). It reports `inverse_coverage_by_sample`, `inverse_summary_by_path`, and `all_original_inverse_occurrences_evaluated`. Reused display labels remain allowed but the path is the unique occurrence ID.

A sampled PASS means only that all original inverse occurrences have been evaluated and are numerically defined at those samples. A continuous command-domain certificate still requires an analytic, interval, or optimization lower bound on each inverse singular margin.


## `goal_ambiguity_audit.py` (independent finite-bank scalar minimax)

Input NPZ arrays `observations` (N,m), `goals` (N,) and optional
`candidates` (N,p), `candidate_names`. Run:

```bash
python goal_ambiguity_audit.py finite_history_bank.npz --observation-noise-radius 0.1 --candidate-noise-radius 0.05
```

The supplied deterministic Euclidean noise balls have radii `sigma_O`
and `sigma_P` in **already-whitened and compatible units**. An observation
pair is indistinguishable when its centers are within `2*sigma_O` and,
if one candidate is added, that scalar feature's gap is within
`2*sigma_P`. On the enumerated finite bank the exact minimax scalar-goal
error equals one-half the largest goal gap among indistinguishable pairs.
For a larger operational history class, this is only a lower bound.
The tool also reports the exact empirical pairwise Lipschitz gain on the
finite bank, with `INF_GOAL_COLLISION` for identical observations and
different scalar goals. It is **not** a whole-class stability guarantee.
Readout-from-archive and genuinely fresh physical acquisitions must be
identified separately in the scientific record.

### Additional two-history Gaussian repeatability diagnostic

The separate **--gaussian-repeat-goal** option in goal_ambiguity_audit.py is NOT the deterministic Euclidean-ball bank audit above. Its exact inputs describe just **two legally repeatable histories**: pretarget sensor means and known scalar future goals for one fixed command, within-campaign independent Gaussian noise, and one unknown Gaussian calibration offset **shared across all repetitions**. All inputs must refer to the same source/reference and a qualified sensor/noise protocol. Goals, tolerances, sensor means, and sensor noise are different physical quantities and may have different units.

NPZ fields: observed_means(2,), future_goals(2,), scalar goal_tolerance, independent_sigma, shared_sigma, failure_probability in (0,0.5). Run:

```bash
python goal_ambiguity_audit.py two_legal_histories.npz --gaussian-repeat-goal --output repeat_budget.json
```

For future goal gap <= twice the goal tolerance, the constant-goal ordinary needs zero acquisitions. For separated goals, repeated measurements with identical pretarget laws cannot help. Under the stated common Gaussian model, the sample mean has variance shared_sigma² + independent_sigma²/m and the **exact minimax** per-history misclassification/error rate is Phi(-sensor_mean_gap/(2*sqrt(variance))). A shared calibration component imposes a nonzero asymptotic error floor, potentially making the requested success probability unattainable for every finite m.

The mathematical synthetic regression has **three sensors with identical one-shot noise variance 1.04** but distinct time-correlation structure: 12 acquisitions, 20 acquisitions, and impossible, respectively, for the same stated pretarget mean gap and future-goal tolerance. This demonstrates why a per-waveform oscilloscope noise specification cannot by itself qualify a repeat-based sensor acquisition. Repeatability of the preparation, sensor bandwidth/skew, physically calibrated noise covariance, complete recorded-command ordinary and held-out future goals are mandatory for native use.

[Complete conditional theorem P23–P26 and source-critical OpenAI F122/F115/F373/F139 audit](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md). F122's deletion-channel superpolynomial complete-string reconstruction claim is *not* used to infer DPT sample complexity.

### Separate marginal-only sensor-dependence / future-goal fusion audit

**--marginal-only-fusion** extends the two-history goal question to p simultaneously legal **pretarget sensor channels** with finite categorical readout histograms. It requires *no independence assumption* between sensors. It is different from both the deterministic Euclidean-ball model and the repeated Gaussian-with-common-drift model above. Its exact object is the **Fréchet class of joint observation distributions with specified separate per-sensor marginals**, without any other dependence or physical support constraints.

Required NPZ: marginal_probabilities(2,p,k), with each [history,sensor] vector a finite nonnegative PMF summing to one; future_goals(2,), scalar goal_tolerance. Every sensor uses k named categorical bins (unused bins may be zero-padded), but the labels must have consistent meaning **across the two histories** for that sensor. Optional sensor_names(p) Unicode strings, and optionally **complete** joint_probabilities(2,k,...,k) (p factors of k) *only when independently qualified*. The matrix sizes grow exponentially for a complete joint PMF, but the marginal-only worst-case theorem and its **factorized attaining witness** do not enumerate k^p states.

```bash
python goal_ambiguity_audit.py two_histories_sensor_marginals.npz --marginal-only-fusion --output dependence.json
python -m unittest -v test_goal_ceiling_tools.py
```

Under two **separated fixed future scalar goals**, the lowest total-variation distinction among *all possible compatible cross-sensor joint laws* is **exactly the largest single-sensor total variation**. Therefore the best guaranteed **equal-prior average** goal-testing error is (1-best_single_tv)/2. The tool returns a constructive attaining mixture-of-products coupling plus a feasible single-sensor likelihood decision rule, with its TWO **per-history conditional error rates**. The equal-prior average error is not necessarily the minimax *worst-history* error, and is **not** a 95%-per-history safety guarantee. If the two goal tolerance intervals overlap, a constant forecast needs no sensor.

When joint_probabilities are supplied, the tool checks they match the stated marginals and separately reports **supplied joint-TV advantage**. It does NOT assert that this PMF or the available histogram calibration is physical: mismatched source reference, incomplete digitally recorded commands, untested legal preparation, sample size, missing joint dependence, bin choice, hysteresis and capture timing can make this number misleading. With two perfectly uniform Bernoulli marginals under both hypotheses, a qualified parity-dependent **joint law** can give joint TV=1, yet the unrestricted marginal-only TV guarantee is zero. Conversely, under **independent** qualified three-channel observations with individual 0.8-versus-0.2 Bernoulli probabilities, marginal TV=0.6 while actual joint TV=0.792. These are strictly **synthetic analytical cases**, not SiC evidence.

**Primary-source discipline:** OpenAI F115-A samples integer tables uniformly at fixed margins; companion F115-B handles bounded cells and structural zeros. Neither automatically specifies a semiconductor sensor noise prior. F373 supplies a special Coulomb non-Monge counterexample, not a Gaussian/SiC transport theorem. F122 supplies the general statistical testing logic. The sharp Fréchet sensor-TV theorem and witness are proved **independently** in [P27–P30](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md). A real positive result needs same-shot paired port calibration and a frozen held-out future-goal scorer, compared against **complete recorded-command** and strongest-one-sensor ordinaries.

#### Optional source-qualified joint-support / bounded-leakage repair (two sensors)

Without changing --marginal-only-fusion, add the **optional** NPZ arrays allowed_joint_supports(2,k,k) (0/1 mask for each history, with 1 indicating a possible joint bin) and support_leakage_bounds(2,) (each in [0,1], default **zero**). This optional submode accepts exactly **two** sensor channels, at most **14 bins** each; the general marginal-only TV result works for more sensors without these masks.

A bounded exhaustive **weighted Hall/min-cut** calculation checks, for *each history independently*, the minimum possible mass outside the declared support while satisfying both categorical sensor marginals:

```math
\ell_h^{\min}=\max_{I}
\left[\sum_{i\in I}P_h(Y_1=i)-
\sum_{j\in N_h(I)}P_h(Y_2=j)\right]_+.
```

If a claimed support-leakage upper bound is below this mathematical minimum, the tool rejects the input with a violating row subset: the **joint support contract is inconsistent with its own marginals**. A hard-zero mask is therefore checked for feasibility, not blindly assumed. If two history-specific high-probability support masks are disjoint, a simple joint-bin membership decision has **per-history** error no greater than that history's declared support-leakage bound; joint-TV is at least the maximum of best-single-sensor TV and 1−(sum of leakage bounds). This is a positive **conditional** repair even when all single-sensor marginals match.

These masks and leakage bounds must come from a legal same-shot physical source/noise model or independent hardware qualification. The code cannot infer physically impossible port-bin pairs, accept Gaussian noise as bounded without justification, or turn binned empirical measurements into error-free PMFs. A supplied joint_probabilities input is checked against the stated masks/leakage, but a numerically consistent table is not hardware evidence. The bounded-flow viewpoint is related to the **F115-B** original table/flow construction, while the sharp two-dimensional Hall deficiency is classical network-flow duality, independently proved in [P31–P32](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md).

## `command_word_audit.py` (finite partial command model)

Input JSON structure:

```json
{
  "commands": ["A", "B"],
  "states": {
    "h0": {"observation": "same", "goal": 0, "transitions": {"A": "h1"},
           "transition_outputs": {"A": {"vds_peak_exceeded": false}}},
    "h1": {"observation": "other", "goal": 1, "transitions": {"B": "h1"}}
  }
}
```

Run `python command_word_audit.py finite_commands.json`. The program
refines state partitions by current goal, command definedness, optional
within-command output and all future command words. It returns a finite
goal-predictive right congruence and shortest word witnesses distinguishing
currently observation-aliased states. A missing output is **not reconstructed**
from a waveform, and a finite symbolic command model is not a claim about
native LTspice switching. For a whole-pulse peak, compute it explicitly from
trace data before adding it to `transition_outputs`.

## `measurement_factor_audit.py` and `expression_domain_inventory.py`

The former is a callable array-level helper producing full `B,A,E`
factorization and conditional Taylor bound. The latter enumerates all
inverse AST nodes and classifies sampled occurrence coverage as
`DEFINED`, `SINGULAR`, `NUMERICALLY_ILL_CONDITIONED`, or
`NOT_REACHED_DEPENDENCY`. Both have separate synthetic regression tests.

## Tests

```bash
python -m unittest discover -v -p 'test_*.py'
```

## `mixed_interaction_audit.py` (S09 scalar four-corner mixed query)

Given an already-fixed scalar readout (for example a frozen overshoot or Eoff functional),
estimate the **central** mixed derivative using a matched 2x2 response table.
The program reports the raw mixed contrast, the conditional central coefficient interval,
and an amplitude-grid choice minimizing a worst-case bound. It does not fit the
unknown remainder/noise coefficients or claim they have been validated.

Minimal JSON input:

```json
{
  "alpha": 0.3,
  "beta": 0.2,
  "samples": {"f00": 0, "fa0": 0.1, "f0b": 0.2, "fab": 0.6},
  "mixed_derivative_variation": {"alpha": 0.4, "beta": 0.6},
  "absolute_readout_error": {"f00": 0.001, "fa0": 0.001, "f0b": 0.001, "fab": 0.001},
  "candidate_amplitudes": {"alpha": [0.1, 0.2, 0.3], "beta": [0.1, 0.2, 0.3]}
}
```

```bash
python mixed_interaction_audit.py s09_query.json --output s09_mixed_report.json
python -m unittest -v test_mixed_interaction_audit.py
```

The bound assumes that all four anchors share reference conditions and the
same normalized alpha/beta coordinates, the mixed derivative is C2 on each
entire query rectangle, and its variation is bounded by
`M_alpha*|u| + M_beta*|v|`. Every readout error is an externally
justified absolute bound (numerical/model/measurement uncertainty as applicable).
Unconstrained analytic amplitude optima can be outside the physical domain;
candidate amplitudes are accepted only when the corresponding archived axis
anchors and derivative/noise envelopes are valid. Multiple waveform time samples
at one query do not identify independently varying cubic-interaction waveforms.

## `goal_word_quotient.py` (all-word linear goal state)

For a **fixed linear switched model in one common state chart** `x' = A_command @ x`,
this tool computes the smallest right-invariant row space containing the specified
goal matrix `C`. It stops when the row-space rank saturates, so it does **not**
enumerate every command word. It reports the minimal *autonomous goal-only
linear-state dimension* and the number of extra freely designed linear
measurement rows beyond `O`. It also returns an explicit orthonormal goal
quotient, induced command matrices and numerical closure residuals.

NPZ schema: `updates (n_commands,n,n)`, `command_names (n_commands,)`,
`observation (m,n)`, `goal (q,n)`; float matrices must use common physical
coordinates and pre-established scales.

```bash
python goal_word_quotient.py fixed_linear_model.npz --output all_word_quotient.json
```

This is a conditional *exact-model* result; rank under floating tolerances
is a numerical diagnostic. Actual nonlinear stage Jacobians depend on the
prefix and may change chart through Eth/guard. Do not label one local
linearization an all-word native certificate. The algorithm complements
`command_word_audit.py` (finite partial symbolic transition model) and
`predictive_state_audit.py` (single-domain goal Jacobians).

## `implicit_goal_certificate.py` (same-law cheap-solver goal bound)

Evaluate a **full-law implicit residual at an already frozen cheap prediction**
(eg. one-Newton). The tool solves the adjoint to compute signed goal correction
`-lambda.T @ F(yhat)` and a conditional Newton--Kantorovich quadratic remainder.
The bounds are not inferred from a passed test or measured output: inverse norm,
Newton step, Jacobian Lipschitz constant, goal Hessian and branch-ball radius
must each be independently established.

Minimal scalar-goal JSON for `F(y)=y+y²-0.09` at `yhat=0`:

```json
{
  "residual": [-0.09],
  "jacobian": [[1.0]],
  "goal_gradient": [1.0],
  "inverse_norm_upper": 1.0,
  "newton_step_upper": 0.09,
  "jacobian_lipschitz_upper": 2.0,
  "goal_hessian_upper": 0.0,
  "domain_radius": 0.2
}
```

```bash
python implicit_goal_certificate.py bound_input.json --output goal_bound.json
python -m unittest -v test_goal_ceiling_tools.py
```

The tool returns `INCONCLUSIVE_CURVATURE` or `INCONCLUSIVE_DOMAIN` when it
cannot establish the conditional ball, rather than claiming that the cheap
solver is inadequate. A stacked all-stage residual can be used only after
the actual-law Eth lift, previous-state terms and moving-event derivatives
have been incorporated into one smooth square system. Nonsmooth event/peak
targets require separate analysis; an exact full-law root is not hardware truth.

See the [full derivations and scientific claim boundary](../dpt_research/20261010_goal_information_solver_fidelity.md).

## `goal_defect_transport.py` (finite ordered-stage goal error)

Companion to `goal_word_quotient.py` and `implicit_goal_certificate.py`. For
a **supplied, fixed, common-chart linear stage sequence**, calculate the exact
finite-horizon worst-case scalar goal deviation when the initial state is
unobservable under an *exact* preparation observation and independent
Euclidean-bounded defects can enter at each stage:

```math
\delta x_{j+1}=A_j\delta x_j+\xi_j,\quad
O\delta x_0=0,\quad \|\delta x_0\|_2\le\rho,\quad \|\xi_j\|_2\le\epsilon_j.
```

The backward goal row for each endpoint supplies an **information radius**
(initial observation nullspace), a **defect radius** (sum of stage disturbance
sensitivities) and their total. Unlike multiplying whole-state operator norms,
this is sharp for the independent product-of-balls linear model and respects
the literal A/B command order. The output contains a directly replayable
maximizing witness plus numeric rank/spectral diagnostics.

**NPZ input fields:**
- `updates`: finite float `(H,n,n)` array of sequential stage maps,
  already expressed in the *same* physically meaningful/scaled state coordinates;
- `observation`: finite float `(m,n)`; an empty `(0,n)` matrix is allowed;
- `goal`: one row `(n,)` repeated at all stage endpoints, or `(H+1,n)`
  distinct scalar readout gradients;
- `initial_radius`: nonnegative scalar; the Euclidean root-state radius
  **inside ker(observation)**, not a measurement-noise estimate;
- `defect_radii`: nonnegative finite `(H,)`; independently justified
  *stage-state error* upper radii after each commanded update.

```bash
python goal_defect_transport.py ordered_stage_bound.npz --output ordered_goal_report.json
python -m unittest -v test_goal_defect_transport.py
```

When the inputs are local Jacobians or point residuals from nonlinear LTspice
rather than fully certified linear error envelopes, report only a
**SENSITIVITY diagnostic**, not a guaranteed native waveform/error bound.
Nonlinear branch/guard errors, the qualified Eth lift, correlated disturbances,
a tied/nonsmooth peak, noisy observation equality and unqualified units
each require further modeling. A stable per-stage eigenvalue does **not**
exclude transient goal error amplification. The maximizing witness is for the
mathematical uncertainty balls and may be physically unreachable.

**Source and proof audit:** [living goal-stability / ordered-defect derivation](../dpt_research/20261010_goal_stability_compositional_closure.md)
(deep reads of OpenAI Math F325/F251/F289/F129/F363/F151, exact linear
support-function proof, counterexamples, transfer ceiling and DPT replay gate).

## `fiber_curvature_audit.py` — second-order observation-fiber goal ambiguity

Input JSON fields: `observation_jacobian` (m,n), `goal_gradient` (n), `observation_hessians` (m,n,n), `goal_hessian` (n,n). The auditor checks full-row-rank `DO` and the numerical first-order factor `DG = b DO`, then restricts `D2G - sum(b_i D2O_i)` to `ker(DO)` to locate an extremal curvature and a matching local level-set second derivative. A nonzero result yields a **conditional asymptotic same-observation goal-distinct witness**, not a finite-radius/native guarantee.

```bash
python fiber_curvature_audit.py nonlinear_chart.json --output fiber_report.json
python -m unittest -v test_fiber_curvature_audit.py
```

`NEAR_FIRST_ORDER_FACTOR` prevents a tiny but nonzero linear goal leak from silently being treated as quadratic. `QUADRATIC_ZERO_NOT_SUFFICIENCY` explicitly allows cubic and higher leakage. Derivatives must come from the same physical reachable preparation chart, future command and scalar goal. C2 smoothness, Eth/guard branch and units are independent assumptions.

## `stage_box_reachability.py` — finite-stage affine box inclusion

NPZ: `updates` (H,n,n), `offsets` (H,n), `initial_lower`, `initial_upper` (n), `admissible_lower`, `admissible_upper` (H+1,n), `remainder_radii` (H,n). For the **actual** stage law written `x_next = A_k x + b_k + r_k(x)` on the entire supplied stage box, use independently validated componentwise `|r_k|<=eps_k`; the program computes a conservative interval hull and checks inclusion in the next valid stage box.

```bash
python stage_box_reachability.py stage_envelopes.npz --output tube_report.json
python -m unittest -v test_stage_box_reachability.py
```

`CONDITIONAL_AFFINE_BOX_CHAIN` is conditional on all supplied map/guard/remainder assumptions, not a native or hardware certificate. A failed box check can be caused by neglected physical correlations; it is `INCONCLUSIVE_BOX_CONTAINMENT`, not a falsified SiC law. The `roundoff_margin_warning` field identifies stage guards too close to the computed hull for casual floating-point assurance; formal certification requires outward interval arithmetic. Existing files/CLIs are unchanged.

Full derivations and source/Lean scope: [living nonlinear-fiber and stage-tube derivation](../dpt_research/20261012_second_order_goal_fiber.md).

## `goal_repair_cover.py` (robust finite-bank goal-tolerance feature cover)

A separate extension of `goal_ambiguity_audit.py`: the latter uses **Euclidean** observation-noise balls, while this optimizer uses **independent coordinatewise interval bounds** (Cartesian boxes), plus fixed per-history goal intervals. For each declared command `c`, the exact finite-bank minimax error after retaining features `S` is `max(max_i eta[i,c], max_compatible_pairs (abs(g[i,c]-g[j,c])+eta[i,c]+eta[j,c])/2)`. A finite library of candidate scalar pretarget features is solved as an exact weighted hitting set when the number of candidates is at most 18; for larger libraries a deterministic weighted-greedy feasible upper bound is reported.

Required NPZ: `observations (N,m)`, `goals (N,K)` (or one-column vector), `candidates (N,p)`, `observation_radii (m,)`, `candidate_radii (p,)`, `goal_tolerances (K,)`, `candidate_costs (p,)`. Optional `goal_uncertainty (N,K)`, `candidate_names (p,)`, `command_names (K,)`. Units must be consistent *per goal*; all histories must be legal and all goals use the same intended reference/scorer. Costs must be declared externally, including whether a feature is already archived, retained digitally, or requires fresh acquisition.

```bash
python goal_repair_cover.py finite_bank.npz --output feature_cover.json
python -m unittest -v test_goal_repair_cover.py
```

`EXACT_MIN_COST_REPAIR` proves the cheapest feature subset only within the **supplied finite candidate library and finite bank**. `NO_LIBRARY_REPAIR` gives an unseparated goal-conflicting history pair; `INTRINSIC_GOAL_UNCERTAINTY` means a single history already exceeds the requested goal tolerance; `GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM` is a feasible nonoptimality-qualified result. Neither finite-bank success nor an accepted native model prediction proves whole-reachable sufficiency, hardware noise, continuous-domain guarantees or autonomous future-command updating. [Derivation, source audit and adversarial cases](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md).

### Retained-history bit minimum with later side information (separate finite-bank mode)

The option **--retained-goal-bits** asks how many fixed-length bits are needed to retain information from an **exact already available archived command/transcript category**, given a separate later external observation available *before* the future goal. It does not optimize new sensors; raw waveform bits, analog quantization, acquisition cost, continuous source-state guarantees and runtime decoder storage are outside the model. Sensor error sets are coordinatewise closed boxes.

Input NPZ: observations(N,m), goals(N,K), transcript_ids(N,) as nonempty **Unicode** exact category labels, observation_radii(m), goal_tolerances(K). Optional goal_uncertainty(N,K) provides absolute uncertainty intervals around each evaluated goal (default zero). Each history, command and goal must use the same declared physical reference, and goal tolerances have the units of their corresponding goals.

```bash
python goal_repair_cover.py finite_history.npz --retained-goal-bits --output retained_bits.json
python goal_repair_cover.py finite_history.npz --retained-goal-bits --exact-transcript-cap 14
python -m unittest -v test_goal_repair_cover.py
```

Two histories conflict when their later observation boxes overlap yet some future-goal separation plus evaluation uncertainty exceeds twice that goal tolerance. Histories with the same archived transcript cannot be given different retained messages. An internal conflict returns **INTRINSIC_TRANSCRIPT_ALIAS**; intrinsic goal interval wider than allowed returns **INTRINSIC_GOAL_INTERVAL**. Otherwise the quotient graph on exact transcript classes is colored. **EXACT_FINITE_BANK_MESSAGE_MINIMUM** gives the verified chromatic number and ceiling binary logarithm when exact search succeeds. **FEASIBLE_COLORING_NOT_PROVEN_MINIMUM** gives an actual-clique lower bound and greedy feasible upper bound when search exceeds its declared class cap. Both statuses preserve a constructive encoding; the function decode_retained_goal computes valid interval-midpoint predictions for later compatible observations.

A five-cycle bank needs three messages/two bits even with clique size two: counting only a maximum conflicting pair underestimates retained history memory. This implements established [Witsenhausen one-shot zero-error side-information coding](https://doi.org/10.1109/TIT.1976.1055607), **not** the Gaussian-streaming lower bound of F140-A. Actual source legality, physical sensor/noise qualification, strong fully archived command ordinary and independent held-out command scores remain necessary. [Complete proof and DPT transfer contract](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md).

## `goal_lipschitz_stability.py` — stable scalar goal recovery and transition-pair floor

The preceding `goal_repair_cover.py` optimizes an **unrestricted decoder**. This companion tool enforces per-command *scalar* decoder gain `lipschitz_limits (K,)` under the same independently bounded **coordinatewise box** input uncertainty. It computes the **exact finite-bank minimax radius**

```math
R_{K_c}(S;c)=\tfrac12\max_{i,j}\bigl(|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}-K_c\,\mathrm{dist}(B_i^S,B_j^S)\bigr).
```

This is different from an empirical derivative and different from a global native Lipschitz certificate. A constructive scalar decoder is available as `decoder_value(...)`. With finite $`K_c`$, the minimum-price feature subset satisfies additive **squared-separation** margins, not the binary hitting-set condition; two individually insufficient features can jointly be sufficient. The separate `transition_pair_floor(current_states,next_states,update_lipschitz)` gives a **necessary** per-command lower bound on any uniform approximate autonomous update defect, not a sufficient vector-valued extension theorem.

NPZ requires `observations (N,m)`, `goals (N,K)`, `candidates (N,p)`, `observation_radii (m,)`, `candidate_radii (p,)`, `goal_uncertainty (N,K)`, `goal_tolerances (K,)`, `lipschitz_limits (K,)`, `candidate_costs (p,)`. Optional names are `candidate_names`, `command_names`. Costs/gains/scorers/noise budgets must be source-qualified and frozen, with candidate features legitimately available before future-command outcomes.

```bash
python goal_lipschitz_stability.py bank.npz --output stability.json
python -m unittest -v test_goal_lipschitz_stability.py
```

The exact optimality label is finite-bank/fixed-candidate-library only, with floating arithmetic; above 18 candidates, greedy feasibility is **not** minimum cost. The closure/solver link, scalar Lipschitz proof, original F332/F331/F110 source audit, and DPT acceptance gates are in [the derivation](../dpt_research/20261010_goal_stability_compositional_closure.md).


## contextual_goal_quotient.py — finite-command goal observability modulo shared nuisance

**Independent Math-only conditional test** synthesizing an appropriate limited form of F129 future-context distinguishability and F119 shared-nuisance cancellation (neither paper's theorem is applied to native SiC). In a common linear state chart, ordered command updates x_next=A_command x, recorded *pretarget* observation y=Hx+Nη with **unrestricted arbitrary nuisance** η, and selected future goals g_w=C A_(last)...A_(first) x, let U0 span ker(N.T). Available nuisance-invariant sensor rows are R=U0.T H; stack selected future goal rows into G_W. Then

    min_extra_ideal_rows = rank([R;G_W]) - rank(R).

This is the exact minimum number of **arbitrarily designed new noiseless source-linear scalar readout rows** needed for the given *finite* word family under the stated chart; not a physical minimum measurement, not a finite candidate-library choice, not an all-word nonlinear dynamic state, and not a noise-bounded prediction guarantee. In particular an accepted *unbounded* η makes absolute levels impossible to reconstruct unless they cancel or are calibrated; use the now-main goal_ellipsoid_recovery.py or contextual_goal_recovery.py under a qualified **bounded joint** uncertainty model instead.

JSON input keys: `updates` (K,n,n), `observation` (m,n), `nuisance` (m,p), `goal` (q,n), and `words` (list of index words, e.g. [[],[0],[0,1]]). Command words are applied in listed order, latest matrix multiplying on the left. Only those words are checked. Output includes rank quotient, goal-space residual per row, a same-observation opposite-history witness and its goal spread. All SVD ranks are floating diagnostics with explicitly stated thresholds; fix units/regularity and source domain before interpreting as physics.

    python contextual_goal_quotient.py input.json --output context_report.json
    python -m unittest -v test_contextual_goal_quotient.py

An analytic two-state fixture has nuisance N=[1,1].T, current goal (1,-1), and future command A=diag(1,-1): current goal is identifiable, while after A the goal is (1,1), requiring **one ideal new row** under arbitrary common offset. A pretarget CAL channel measuring only η (observation row [0,0], nuisance coefficient 1) repairs it within the toy. A locally executed separate 160-case integer-rational SymPy rank oracle agreed with numerical rank results; this remains **toy validation**, not a native replay. Full mathematical/scientific boundary: [F119/F129/F132 proof-level bridge](../dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md).


## Continuous scalar goal recovery: goal_ellipsoid_recovery.py

Source chart: $`x=x_0+Bz,\ \|z\|_2\le1`$; observation $`y-y_0=HBz+Ee,\ \|e\|_2\le1`$; scalar goal $`G-G_0=g^\top Bz`$. The rectangular/rank-deficient matrix E is a **joint deterministic hard sensor-error factor**, not unqualified covariance. The exact linear-model minimax risk, after eliminating any noise-free observation constraints, is

```math
R=\max_{\|v\|\le1,\|Av\|\le1}|c^\top v|
=\min_{a}\bigl(\|B^\top g-(HB)^\top a\|+\|E^\top a\|\bigr).
```

The full singular SVD projection, one-parameter q formula and proof are in [mixed-nuisance P1–P18 proof](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md). NPZ input: state_factor (n,n), observation (m,n), noise_factor (m,p), goal (n,). Run:

    python goal_ellipsoid_recovery.py linear_chart.npz --output goal_radius.json
    python -m unittest -v test_goal_ellipsoid_recovery.py

Output includes mathematical radius estimate, a separately evaluated linear decoder **dual upper**, reduced-coordinate feasible witness lower, their floating numerical gap, rank thresholds and external measurement weights. A second least-squares decoder candidate prevents catastrophic dual inflation when sensor error scales near 1e-10, and tolerance acceptance must use the actual upper bound—not a fixed 1e-9 additive slack. Small SVD singular values are not physical evidence of exact common errors.

### Separate stochastic quadratic-goal design mode (Gq and joint approximation error)

**Not the deterministic ellipsoid minimax model above.** The new `--quadratic-design` mode assumes a scaled Gaussian state prior `x~N(mu,P)`, an **affine** pretarget candidate observation `y=Hx+d+eps`, joint-Gaussian state/model discrepancy with covariance `D` and cross covariance `C=Cov(x,d)`, and independent positive-definite Gaussian sensor noise `R`. Every candidate sensor must be physically legal for the same source/preparation. The future goal is represented by its declared quadratic Taylor approximation about `goal_expansion_center` (default prior mean) with `goal_gradient` and `goal_hessian`; those derivatives are **goal-sensitive, not universal device parameters**.

This mode scores the data-averaged posterior variance **Gq**, the first-order goal-only variance **Gl**, the raw parameter posterior trace **A**, and parameter mutual information where prior covariance is invertible. Gq and Gl have *squared goal units*, A depends on parameter coordinate scaling, mutual information is in nats. It maintains the full joint covariance of state and model discrepancy. Omitting that cross covariance is a **different statistical model** and can change the best sensor.

Input NPZ arrays (same k candidates and m observation channels each): `prior_mean (n,)`, `prior_cov (n,n)`, `goal_gradient (n,)`, `goal_hessian (n,n)`, `candidate_observations (k,m,n)`, `candidate_noise_cov (k,m,m)`. Optional: `candidate_names (k,)` (Unicode), `goal_expansion_center (n,)`, `candidate_discrepancy_cov (k,m,m)`, `candidate_state_discrepancy_cross_cov (k,n,m)`. The joint state/discrepancy covariance must be positive semidefinite. Do not supply a nonzero C without physically justified D. All sensor values, uncertainty and source Hessians must have compatible physical scales.

```bash
python goal_ellipsoid_recovery.py qualified_oed.npz --quadratic-design --output oed.json
python -m unittest -v test_goal_ellipsoid_recovery.py
```

The report includes each candidate's posterior covariance, squared goal risk, risk without observation, curvature contribution and parameter ranking, plus the predicted best candidate under each criterion. The **same** recorded-command ordinary, acquisition/time cost and independent goal scorer must be used for assessment. A zero-gradient goal can have Gq benefit while Gl sees none; a nonlinear observation such as `y=x**2` at `x=0` can have zero Jacobian but carry the entire future quadratic goal, so the *linear observation assumption must be tested*. For genuinely nonlinear sensor likelihoods, compare an actual nonlinear forward/GO-EIG or controlled surrogate rather than promoting the Gq diagnostic.

[Full finite-Gaussian proof, analytical ranking reversals, correlated-BAE counterexample and original-literature source audit](../dpt_research/20261012_second_order_goal_fiber.md). Original Gq: [Neuberger et al. (2025)](https://doi.org/10.1007/s10915-025-03073-y). Correlated Bayesian approximation error: [Koval and Nicholson (2025)](https://doi.org/10.1007/s10915-025-03008-7). Nonlinear observation/goal rival: [Zhong et al. (2026)](https://arxiv.org/abs/2403.18072).

## Finite future-command robust recovery: contextual_goal_recovery.py

For one centered global source-state chart and all pretarget measurements, assume

```math
\begin{aligned}
x&=x_0+Bz,\qquad\|z\|\le1,\\
y-y_0&=HBz+N\eta+Ee,\\
\eta&\in\mathbb R^p,\qquad\|e\|\le1.
\end{aligned}
```

N is an **unbounded shared nuisance vector**; E is a separate **jointly bounded, possibly correlated measurement error**. The program projects onto $`\ker N^\top`$, then evaluates the scalar radius for every **explicitly listed finite future command word** and each goal row $`C F_w`$, preserving actual command multiplication order. The row-specific radius divided by its specified goal-unit tolerance yields a minimax risk ratio. One conservative external linear decoder is returned per word and goal. No nonlinear/global native DPT closure is claimed.

JSON schema: updates (K,n,n), state_factor (n,n), observation (m,n), unbounded_nuisance (m,p), bounded_noise (m,q), goal (g,n), words (lists of command indices; [] means immediate goal), goal_tolerances (g positive values). One example:

    {
      "updates": [[[1,0],[0,-1]]],
      "state_factor": [[1,0],[0,1]],
      "observation": [[1,0],[0,1]],
      "unbounded_nuisance": [[1],[1]],
      "bounded_noise": [[],[]],
      "goal": [[1,-1]],
      "words": [[],[0]],
      "goal_tolerances": [0.2]
    }

    python contextual_goal_recovery.py finite_words.json --output contextual_radius.json
    python -m unittest -v test_contextual_goal_recovery.py

Under this **dimensionless** two-state prior, the immediate goal x1-x2 has R=0, while the goal after A=diag(1,-1) is x1+x2 with R=sqrt(2). A legal pretarget shared-offset calibration can repair this information loss; independent sensor errors leave a nonzero residual. For physical replay, source preparation/reference, port definition, sensor/error joint factor, all command and CAL admissibility, goal units, stage event guards, nonlinear remainder and strong ordinary controls must each be verified. See [mixed-nuisance proof (legacy M17–M27)](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md). Tests are synthetic mathematics, not hardware evidence.


## fiber_goal_curvature.py — regular nonlinear fiber goal recovery and command Hessian pullback

This is a **conditional finite-dimensional math audit**, not a nonlinear SiC circuit solver. Inputs must use a single source reference and source-qualified future command.

Let $`O(h)`$ be the pretarget observation and $`G_w(h)`$ the future scalar goal. Assume $`DO(h_0)`$ has full row rank, $`Z`$ spans its null space and $`DG_w(h_0)Z=0`$. The **relative observation-fiber Hessian** is:

```math
\begin{aligned}
Q_w&=Z^\top\Bigl[
D^2G_w(h_0)\\
&\qquad-\sum_j\lambda_jD^2O_j(h_0)
\Bigr]Z,\\
DG_w(h_0)&=\lambda^\top DO(h_0).
\end{aligned}
```

On a true **source-legal exact fiber chart** with orthonormal tangent coordinates $`\|v\|\le r`$, a certified third derivative bound $`M`$ for the *composite fiber goal* controls its exact minimax scalar radius to within $`Mr^3/6`$ of

```math
R_2=\frac{r^2}{4}\left[
\max(0,\lambda_{\max}(Q_w))-
\min(0,\lambda_{\min}(Q_w))\right].
```

JSON input: observation_jacobian (m,n), goal_gradient (n,), observation_hessians (m,n,n), goal_hessian (n,n), radius (positive); optional fiber_third_derivative_bound (nonnegative and **externally source-certified**), rank_rtol.

    python fiber_goal_curvature.py chart.json --output fiber_goal.json
    python -m unittest -v test_fiber_goal_curvature.py

The report gives the relative Hessian, its eigenvalues and inertia, a local $`r^2`$ leading risk, plus rigorous lower/upper **only when** the actual third-derivative certificate is provided. No physical reality or source reachability is inferred from compatible array shapes.

The accompanying function pullback_goal_derivatives(J,H_f,g_next,H_next) implements a reverse command derivative transport: $`g_{\rm prev}=J^\top g_{\rm next}`$ and $`H_{\rm prev}=J^\top H_{\rm next}J+\sum_j (g_{\rm next})_j H_{f,j}`$. Each command-stage Jacobian and Hessian must be evaluated at its *legally reached state*. Twelve tests cover exact/curved observation fibers, a two-stage polynomial command oracle and 120 independent cubic-fiber cases.

[Full second-order fiber derivation](../dpt_research/20261012_second_order_goal_fiber.md), [nonlinear-fiber proof (legacy M40–M49)](../dpt_research/20261012_second_order_goal_fiber.md). Moving peak/events require further guard and timing qualification; local Hessians do not automatically certify source-native DPT targets.


## implicit_goal_hessian.py — source-residual second-order goal transport

This auditor connects the regular nonlinear observation-fiber Hessian to one **implicit** source-law state update without constructing an explicit nonlinear transition. For a fixed legal command u and the same-reference residual F(z,x;u)=0, the current-state Jacobian A=F_z must be invertible. Set J=-A^{-1}F_x and solve A.T lambda = grad g(z) for the chosen postcommand scalar goal g(z).

For previous-state perturbations a,b, extend the source perturbations to (Ja,a),(Jb,b) in the concatenated coordinates [next z, previous x]. The exact Hessian is:

```math
\begin{aligned}
D^2(g\circ f_u)[a,b]
&=(Ja)^\top D^2g(z)(Jb)\\
&\quad-\lambda^\top D^2F(z,x;u)
[(Ja,a),(Jb,b)].
\end{aligned}
```

Every current/previous source Hessian cross-block must be retained. JSON schema: current_jacobian (n,n), previous_jacobian (n,n), residual_hessians (n,2n,2n) with axes ordered [z,x], next_goal_gradient (n,), next_goal_hessian (n,n). Output: Jacobian update, source adjoint, goal gradient/Hessian in previous-state coordinates, solve residuals and Jacobian condition number.

    python implicit_goal_hessian.py implicit_chart.json --output goal_hessian.json
    python -m unittest -v test_implicit_goal_hessian.py

Seven analytic/regression tests include a mixed current/previous rational residual, other implicit nonlinear scalar sources, a two-state quadratic source and 200 independently generated random quadratic source laws. To make a native physical claim, provide full source-law F including network, charge and thermal equations, legal stage states and correct BE/TRAP time convention; confirm target work/peak guard qualification and a uniform error certificate. [implicit source-Hessian proof (legacy M50–M54)](../dpt_research/20261012_second_order_goal_fiber.md), [proof C15–C23](../dpt_research/20261012_second_order_goal_fiber.md).

## Goal27 projective_command_proxy.py — exact PREP-conditioned stored-proxy inverse (2026-10-17)

This is a **scoped mathematical consumer**, not an actual nonlinear source evaluator. It reads the controller's saved 2026-10-12 Goal27 five-current affine proxy coefficients and six radii as exact binary64 rationals using Python Fraction, then uses the three **already recorded digital PREP amplitudes** to recover the other three proxy coordinates (L, kappa, filter bandwidth). No source/native execution or new physical sensor is required.

- **certify(data):** exact determinant range for the command-conditioned 4x4 projective observation matrix H(a) is [-0.012864031844606,-0.012844315469064] A^4 on the full normalized PREP cube; full-bank proxy anchor D > 5.3726858484 A.
- **decode(data,a,five_currents_A):** cancels one unknown common positive record-level gain and offset, inverts H(a), recovers three proxy coordinates and the signed-work goal in J. Rejects invalid recorded-command bank, singular H or nonpositive gain orientation.
- **sensor_certificate(data,noise_abs_A,gain_lower):** conditional full-bank **proxy-only** worst-goal error using 2048 joint exact corners for five independent bounded component errors. At hypothetical epsilon=1mA, gamma>=0.9, arbitrary common offset, a strict 2.939193801103 nJ error upper and minimum effective gain >0.8995834925637281; this is NOT a real instrument source/native/TOTAL_ERROR guarantee.

**audit_source_gap(data,a,u,actual_currents,actual_goal_J):** strictly POST-HOC matched source replay, consuming the actual future signed work, not a prospective prediction. It evaluates P37's exact correlated nonlinear-source-versus-proxy goal numerator, preserving the shared five-current CAL correction; proof consumers may attempt a separate interval bound. Requires real same-source and filter/guard identity; **not** a source-wide or physical certificate. See [P37 exact gap identity](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md) and paired cancellation/negative-orientation regressions.

**Critical lower-bound correction.** The archived same-q corner60 pair has a goal gap of approximately 0.687175006510 nJ, but it has different digitally recorded PREP amplitudes. Its minimax radius 0.343587503255 nJ is only a lower bound for the deliberately **command-blind q-only decoder**, not a full-recorded-command indistinguishability bound. The stored affine proxy has zero noise-free goal radius conditioned on a and q under the stated free-affine gain/offset measurement model. Same-information full-CAL/source-law ordinary can match or beat the current five-current algorithm.

Run from dpt_tools: python -m unittest -v test_projective_command_proxy.py. Proof/evidence ceiling: [P36](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md). Separate rational actual-source gate: [S-L7](../dpt_research/20261010_goal_information_solver_fidelity.md). The new tool accepts coefficient dictionaries and contains no fixed controller filesystem path.

### 2026-10-18: exposed actual-S150 source-point and branch-conditioned jet gates

The existing [projective_command_proxy.py](projective_command_proxy.py) now contains two independently tested additions, with **separate evidence ceilings**:

1. **known_source_point_noise_gate(data,a,actual_currents_A,actual_goal_J,gain_lower,noise_abs_A,goal_tolerance_J)** computes the exact 32-corner deterministic five-sample sensor error range and sharp positive noise tolerance using binary64 stored source/current/goals promoted to rational numbers. It requires the **future actual signed work as an input** and is unconditionally POST-HOC, NEVER an online forecast, source-uniform certification or hardware-noise claim. The archived accepted S150 nonprotected T00–T06 readout/goal fixtures in [tests](test_projective_command_proxy.py) were already exposed, carry DIFFERENT digitally recorded PREP amplitudes, and produce max zero-new-noise retrospective error **0.005601739350126236 nJ**, hypothetical γ≥0.9 ±1mA component-box worst **2.928364786189582 nJ**, and sharp 1nJ-threshold ε ≈**0.340271015366445 mA**. Original archived source locator/sha, exact proof and full ordinary caveats: [P40](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md).
2. **source_deviation_univalence_gate(data,residual_upper_A,derivative_upper_A)** accepts independently certified **entire continuous actual-source** four anchored output residual and its source+RC propagated parameter-Jacobian bounds, with the *same recorded PREP, root branch and guard domain*. It uses exact full-cube P36 inverse-row rational bounds $k_0<0.21\ \mathrm{A}^{-1}, k_v<36.1\ \mathrm{A}^{-1}$ and the globally valid pairwise projective lower Lipschitz gate from [P41](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md). It does NOT calculate actual R/J from the saved proxy, seven physical source point snapshots or pointwise Jacobians; report **INCONCLUSIVE** unless given rigorous whole-source input. Positive homogeneous scale alone also does not certify **actual D>0**, which is a separate mandatory physical/sensor gate.

[Additional adversarial and source-law regression](test_paper_transfer_falsifiers.py) checks the P41 global fold (everywhere full local rank, noninjective full domain), P42 two-copy full-record sensor correlation, P43 prefilter-memory sixth-observation rank, D3 electrothermal positive-diode but full-unstable BE source, and actual G12/diode signed one-step S-L10 gate. Proof source and legal closure limits are in [mixed CAL/goal fiber](../dpt_research/20261012_mixed_nuisance_goal_radius_formal_derivation.md), [dynamic closure](../dpt_research/20261010_goal_stability_compositional_closure.md), and [goal source/solver](../dpt_research/20261010_goal_information_solver_fidelity.md). The strongest equal-information comparator always uses the complete digital command and FULL externally recorded CAL with one joint noise law. No source/native rerun, protected truth or Power Semiconductor/tmp used.


### Exact pre-push DPT math CI preflight (2026-10-18)

Use [the existing Actions workflow](../.github/workflows/dpt-math-auditors.yml) as the single dependency/check specification: Python 3.11, Node 22, MathJax mathjax-full@3.2.2. Run compileall, ALL discovered unittest test_*.py, markdown_math_audit.py on MAP + EVERY dpt_research/*.md + this README, and compile_mathjax.js on ALL extracted formulas with the unchanged 75ex width threshold. Then run the workflow's already existing POST to GitHub /markdown API for each **entire** Markdown file and require exact per-file equality between extracted math and rendered math-renderer nodes; source-lint and MathJax PASS alone are insufficient. Do this for the **candidate full tree before pushing**, then batch verified changes in one commit. For source formatting, use math fences and GitHub supported inline math when boundary/underscore ambiguity arises; preserve formula contents. No new workflow/files or Power Semiconductor local writes. The exact GFM issue on 2026-10-18 was 62 standalone dollar-display blocks without appropriate paragraph separation plus 53 inline formulas swallowed by adjacent GitHub Markdown rules. Source-row receipts and their scope caveats are in [existing tests](test_paper_transfer_falsifiers.py); these are NOT hardware or full-source certificates.
