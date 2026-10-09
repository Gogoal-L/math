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
