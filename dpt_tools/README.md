# DPT mechanical audit tools

These scripts turn two recurrent DPT research checks into reproducible numerical artifacts. They are deliberately conservative: a PASS never upgrades a numerical linearization into a native theorem. They require Python 3.10+ and NumPy (`pip install -r requirements.txt`).

## `predictive_state_audit.py`

Input is an `.npz` file with:

- `DO`: observation Jacobian, shape `(m_obs, n_state)`;
- `DG`: stacked future-goal Jacobian, shape `(m_goal, n_state)`;
- optional `DP`: candidate measurement Jacobian, shape `(m_meas, n_state)`;
- optional `DP_candidates`: one scalar candidate measurement per row;
- optional `candidate_labels`: labels aligned with `DP_candidates`;
- optional `DO_scales`, `DG_scales`, `DP_scales`: scale-indexed Jacobians;
- optional `radii`, `remainder_goal_coeff`, `remainder_measurement_coeff` for a supplied quadratic remainder certificate.

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

The multiscale block repeats the same audit at each supplied scale. If certified bounds

`||R_G|| <= C_G r^2` and `||R_P|| <= C_P r^2`

are supplied, the script reports the mechanical consequence

`||Delta G - A Delta P|| <= (C_G + ||A|| C_P) r^2`.

The script does not establish the supplied remainder bounds, rank persistence on a continuous neighborhood, native-model validity, or global identifiability.

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

A sampled PASS means only that every recorded inverse occurrence is numerically defined at those samples. A continuous command-domain certificate still requires an analytic, interval, or optimization lower bound on each inverse singular margin.

## Tests

```bash
python -m unittest -v test_dpt_tools.py
```
