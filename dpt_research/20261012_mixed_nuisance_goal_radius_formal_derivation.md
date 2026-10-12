# Proof notebook: finite-word scalar goal recovery with mixed nuisance, and physical DPT boundaries

**Status (2026-10-12):** independent conditional optimal-recovery derivations, analytical examples, source links, numerical regression tests. **No new SiC source-law result or new fundamental optimal-recovery theorem is claimed.** Intended companion to the formula-driven [Math main map M1–M33](../DPT_MATH_RESEARCH_MAP.md).

## I. The exact data contract

One fixed *global linear model* on a centered source-state chart:

```math
z\in \mathbb B_2^n,\qquad
y=A z+N\eta+E e,\qquad
e\in\mathbb B_2^q,\ \eta\in\mathbb R^p,\qquad
\gamma=c^\top z.
```

Here $`A=HB`$ when the actual state is $`x=x_0+Bz`$. Every observed row must belong to the *same* source reference and be available before the unknown future goal. The vector $`\eta`$ is an **unbounded common nuisance** across all recorded channels; its possible values are unrestricted. The vector e is a **single joint deterministic bounded factor**, not iid samples; its components may describe exact common-mode correlation. The two norms $`\|z\|\le1,\|e\|\le1`$ are **separate** hard budgets. Relative sensor timing and covariance estimates alone cannot establish E or its zero singular values.

Legal finite ordered command words $`w=(u_1,\ldots,u_\ell)`$ update $`x\mapsto F_w x`$, $`F_w=A_{u_\ell}\cdots A_{u_1}`$. For a goal row C the recovered scalar direction in z coordinates is $`c=B^\top F_w^\top C^\top`$. Each future command and engineering goal is scored **after** fixing the preparation, observable, and error budget.

## II. Exact minimax equality: proof that a linear decoder is optimal

Define $`\mathcal U=\{(z,e,\eta):\|z\|\le1,\|e\|\le1,\eta\in\mathbb R^p\}`$. For arbitrary, possibly nonlinear decoders $`\delta:\mathbb R^m\to\mathbb R`$, set

```math
R_*=\inf_\delta\sup_{\mathcal U}|c^\top z-\delta(Az+Ee+N\eta)|.
```

**Lower half, zero-observation antipodes.** Let z,e,η be admissible and satisfy $`Az+Ee+N\eta=0`$. The two admissible histories $`(z,e,\eta)`$ and $`(-z,-e,-\eta)`$ have identical recorded observation y=0, but goals $`+c^\top z,-c^\top z`$. Thus for every $`\delta`$,

**(P1)**

```math
R_*\ge\max_{\substack{\|z\|,\|e\|\le1\\Az+Ee\in\operatorname{im}N}}|c^\top z|
=:\rho.
```

**Dual support formula.** The feasible class in (P1) is a compact convex body after eliminating unbounded η, and z=e=0 lies in the relative interiors of their norm balls. The standard finite-dimensional convex separation/Fenchel dual for linear equality constraints therefore has no gap. Attach a Lagrange multiplier a to $`Az+Ee+N\eta=0`$. Its Lagrangian maximum over z,e,η is finite iff $`N^\top a=0`$; otherwise unbounded η drives it to $`+\infty`$. In the finite case,

**(P2)**

```math
\begin{aligned}
&\sup_{\|z\|\le1,\|e\|\le1,\eta}
\bigl(c^\top z-a^\top(Az+Ee+N\eta)\bigr)\\
&\qquad=\|c-A^\top a\|_2+\|E^\top a\|_2.
\end{aligned}
```

Hence the optimal-value equality is

**(P3)**

```math
\rho=\min_{N^\top a=0}\left(\|c-A^\top a\|_2+\|E^\top a\|_2\right).
```

(The existence of a minimizing a follows from standard quotient-space closedness/finite-dimensional convex duality; nonunique null coefficients can be removed without changing the objective.)

**Matching decoder upper.** For any feasible a with $`N^\top a=0`$, the directly implementable external linear prediction $`\delta_a(y)=a^\top y`$ satisfies

**(P4)**

```math
|c^\top z-a^\top(Az+N\eta+Ee)|
\le \|c-A^\top a\|_2+\|E^\top a\|_2.
```

Therefore $`R_*\le\min_{N^\top a=0}\{\ldots\}=\rho`$, matching the lower bound. A best **linear** decoder is minimax-optimal *among all measurable/nonlinear decoders for the entire declared symmetric linear model.* No individual $`\theta`$, full state or nuisance estimation is necessary.

A finite *observation-compatible pair* from native SiC remains a lower-bound witness even when this global linear model does not apply. It does **not** inherit the linear global upper bound without further source-law proof.

## III. Exact factorization: eliminate unbounded nuisance and zero-noise channels

Take an orthonormal basis U0 of $`\ker N^\top`$. Since a feasible decoder satisfies $`a=U_0 b`$, project:

```math
A_0=U_0^\top A,\qquad E_0=U_0^\top E.
```

Take the full left singular decomposition $`E_0=U_r\Sigma_r V_r^\top`$, and let $`U_\perp`$ span the orthogonal complement of its *exact* column range. A pair of opposite z states can produce the same measurement iff

**(P5)**

```math
U_\perp^\top A_0z=0,\qquad
\|\Sigma_r^{-1}U_r^\top A_0z\|_2\le1.
```

To see the noise budget equivalence, the minimum-norm solution e to $`E_0 e=-A_0z`$ lies in the right singular directions V_r and has norm precisely $`\|\Sigma_r^{-1}U_r^\top A_0 z\|`$. Let Z have orthonormal columns spanning $`\ker(U_\perp^\top A_0)`$; set $`z=Zv`$. Define

```math
M=\Sigma_r^{-1}U_r^\top A_0 Z,\qquad c_r=Z^\top c.
```

Then (P1) is exactly

**(P6)**

```math
\rho=\max_{\|v\|\le1,\|Mv\|\le1}|c_r^\top v|.
```

It has a **one-dimensional convex dual** (interpret endpoint inverse by its appropriate compatible limit):

**(P7)**

```math
\boxed{\rho^2=\min_{q\in[0,1]}
c_r^\top\big[(1-q)I+qM^\top M\big]^{-1}c_r.}
```

**Proof and constructive witness.** For $`D_q=(1-q)I+qM^\top M`$, every feasible v satisfies $`v^\top D_qv\le1`$; by Cauchy–Schwarz in the $`D_q`$ metric, $`(c_r^\top v)^2\le c_r^\top D_q^{-1}c_r`$. At an interior minimizer, define $`w=D_q^{-1}c_r`$. Differentiating $`c_r^\top D_q^{-1}c_r`$ yields

**(P8)**

```math
-\frac{d}{dq}(c_r^\top D_q^{-1}c_r)
=w^\top(M^\top M-I)w
=\|Mw\|^2-\|w\|^2.
```

Thus the two quadratic constraints are equally tight for the normalized witness $`v=w/\|w\|`$ (provided w nonzero), which attains the upper expression. An endpoint minimizer instead has one active bound; the same direct construction or a compatible limit completes strong duality. The zero c case has $`\rho=0`$ directly. The implemented decoder is reconstructed from the positive-noise U_r components and an unpenalized U_perp component enforcing equality in noise-free coordinates. Floating SVD **rank** is a numerical model decision, not a physical theorem.

**Counterexample to discarding correlation:** H=B=I2, E=σ[1,1].T. For c=[1,-1], a=[1,-1] obeys E.Ta=0, so $`\rho=0`$. For c=[1,1], $`\rho=2σ`$ when $`0<σ\le1/\sqrt2`$ (and saturates at $`\sqrt2`$ for larger σ). Adding independent $`[0,\tau]^\top`$ to E restores a nonzero difference goal radius $`\tau`$ in the small-noise regime. This is a deterministic analogue of the **correlated-noise invalid transfer** of F119, not a consequence of its independent BSC theorem.

## IV. Finite commands and pretarget CAL: observable information is goal dependent

For $`F_w=A_{u_\ell}\cdots A_{u_1}`$ and fixed goal rows C_j, run the scalar recovery with $`c_{w,j}=B^\top F_w^\top C_j^\top`$. If $`\tau_j>0`$ is the goal-specific engineering tolerance, and decoders may be different for different *known* future commands and goals, the whole-collection minimax max-relative error is

**(P9)**

```math
R_{\mathcal W,\infty}=\max_{w\in\mathcal W,j}
\frac{R(c_{w,j})}{\tau_j}.
```

Because max over finite j and supremum over uncertainties commute, independent optimizations of separate scalar decoder rows attain the collection optimum. **All goals share the same *available pretarget observation*, not the same decoder weights.** The method does not assert that one reduced state recursively evolves correctly under command switching, and no theorem extends it beyond the predeclared finite word library.

For pure noiseless observations E=0, $`\rho(c)=0`$ iff $`c\in\operatorname{row}(U_0^\top A)`$. Given finite future-goal row stack Γ, a freely chosen extra *ideal noiseless source-state* row increases rank by at most one, so the exact abstract minimum is

**(P10)**

```math
k^{\rm ideal}_{\min}
=\operatorname{rank}\!\begin{bmatrix}U_0^\top A\\\Gamma\end{bmatrix}
-\operatorname{rank}(U_0^\top A).
```

Real DPT sensor candidates have restricted units, ports, timing, impedance, calibration interventions and noise; P10 is **not** a physical minimum number of sensors.

**CAL confounding trap.** A genuine active pulse/calibration changes the physical state by K before the future command. Fix that same K-executed physics and compare withheld vs released CAL observation. Only then is the difference in minimax radii a *pure information effect*. Comparing measured CAL-executed future to uncalibrated/untouched future mixes information value and physical intervention effect, even when both models use the same device reference. See main MAP (M28–M29).

## V. Nonlinear transfer: one positive bound and two decisive cautions

On an actual reachable nonzero DPT chart, assume known residual envelopes $`\|r_O(z)\|\le\beta_O`$, $`|r_{G,w}(z)|\le\beta_{G,w}`$ uniformly over preparations, modes and commands. For any $`a:N^\top a=0`$,

**(P11)**

```math
|\widehat G_a-G_w|
\le\|c_w-A^\top a\|+\|E^\top a\|
+\beta_{G,w}+\|a\|\beta_O.
```

The last term is **readout-amplified observation mismatch**. Optimizing only the linear ideal radius (P3) and afterward ignoring $`\|a\|\beta_O`$ is unsound when weak sensor directions produce large coefficients. A correct nonlinear upper bound minimizes P11 or otherwise bounds decoder gain. This is a conditional sufficient **upper**; a finite bank of observed errors does not certify $`\beta_O`$ or $`\beta_G`$ for the full source domain.

For an exact nonlinear fiber, even perfect first-order tangent factorization can mislead. With $`\|(x,y)\|\le r`$, observation x, goal y², the center goal derivative vanishes but exact minimax scalar error is $`r²/2`$. Conversely **peak value** is Lipschitz directly in waveform sup norm even if time of maximum changes discontinuously; for two continuous waveforms on the *same* fixed window,

**(P12)**

```math
|\max V_1-\max V_2|\le\|V_1-V_2\|_\infty.
```

For fixed-window signed work a direct upper is

**(P13)**

```math
|\Delta W|
\le(b-a)\bigl(\|I_1\|_\infty\|\Delta V\|_\infty+
\|V_2\|_\infty\|\Delta I\|_\infty\bigr).
```

Neither bound needs a smooth unique peak time; they can be conservative relative to goal-specific signed cancellation. Moving event windows require the Leibniz boundary derivative and guard transversality in the main MAP (M21–M22).

## VI. What is actually verified and what would close the DPT physical loop

- Original F119/F129/F132 primary LaTeX proof links, conditional mathematical transfer and Lean-scope audit: [dedicated F119–F132 note](20261011_F119_F129_F132_proof_level_DPT_bridge.md). Upstream Boolean/noise or automaton theorems **never** prove a SiC circuit claim by analogy.
- `dpt_tools/goal_ellipsoid_recovery.py` implements P5–P8 after elimination of noise-free directions. `dpt_tools/contextual_goal_recovery.py` implements P9, while `dpt_tools/contextual_goal_quotient.py` is the zero-bounded-noise finite-word rank special case. Their analytic and CLI regression tests and full GitHub Actions suite [153 green tests](https://github.com/Gogoal-L/math/actions/runs/38180573299) verify **declared code fixtures**, not physical SiC admissibility. Independent SciPy primal feasible optimizations covered 70 random numerical examples, worst objective disagreement ~9.14e-12; some strict solver status flags are not optimality certificates.
- Independently symbolic-verified: sensor time-skew linearization $`\delta W=\delta_c[VI]_{t_a}^{t_b}+\delta_r\int(I\dot V-V\dot I)\,dt+O(\|\delta\|^2)`$ for fixed event-free integral window, and exact quadratic polynomial example with V=2+3t, I=5−2t: $`W_{\rm shifted}-W=5\delta_c+19\delta_r-6\delta_c^2+6\delta_r^2`$ over [0,1]. Moving windows, unmatched probe group delays and bandwidth filtering change that error model.
- Real scientific next packet must come from a **single** 150-V active source reference or separately the original 100-V R1 external cut: reachable prior B/chart and preparation; observation H, error-factor N/E with port, timing and joint calibration; legal future matrix/state transitions; goal gradients C and nonlinear radius envelopes; prospective held-out ordinary baselines. Currently there is **no native replay and no nonlinear R1 hardware/model certificate** from this note.

The best route is a **qualified, goal-aligned new measurement/conditioning decision**, not a forced full recovery of individual Lg/Ls/Ld/Lloop/Rg. If the required source factors are unavailable, report only the proved conditional linear result and the lower bounds from actual observed-compatible history pairs.


## VII. One actual supplied DPT charge law: a sharp source-level defect, not an analogy

The supplied IH2662 V6 §4.7 explicitly records a 600-V *coupled backward-Euler* source-evaluator body-diode branch with finite conduction $`i_{\rm cond}(v)=I_s(e^{v/a}-1)`$, stored charge $`q_D(v)=\tau I_s e^{v/a}`$, and BE storage current $`[q_D(v_n)-q_D(v_{n-1})]/h_n`$. The strong evolving-affine competitor replaces the charge surface at a fixed authorized BASE $`\bar v`$ by

**(P14)**

```math
q_D^{\rm aff}(v)=q_D(\bar v)+q_D'(\bar v)(v-\bar v),\qquad
q_D'(\bar v)=q_D(\bar v)/a.
```

Set $`u=(v-\bar v)/a`$. Direct algebra, not a transferred theorem, gives

**(P15)**

```math
q_D(v)-q_D^{\rm aff}(v)
=q_D(\bar v)(e^u-1-u).
```

For $`|u|\le t=d/a`$, this is nonnegative and the **sharp symmetric-interval maximum** occurs at $`u=t`$. Indeed $`r(u)=e^u-1-u`$ has r'(u)=e^u-1, so r decreases up to zero then increases. Comparing endpoints,
$`r(t)-r(-t)=2(\sinh t-t)\ge0`$. Hence

**(P16)**

```math
0\le q_D(v)-q_D^{\rm aff}(v)
\le q_D(\bar v)(e^{d/a}-1-d/a)
\le \frac{q_D(\bar v)}2e^{d/a}(d/a)^2.
```

The last inequality follows from $`\int_0^1(1-s)e^{us}\,ds=(e^u-1-u)/u^2`$ and $`|u|\le d/a`$. This has physically relevant units C; dividing the n and n−1 charge remainder by h_n converts the defect to A:

**(P17)**

```math
|R^{\rm full}_{D,n}-R^{\rm aff}_{D,n}|
\le[\epsilon_{q,n}+\epsilon_{q,n-1}]/h_n.
```

If the previous-step charge is not approximated, drop $`\epsilon_{q,n-1}`$. If T changes, then a(T), I_s(T), BASE and guards need uniform joint control; the scalar formula is not the full coupled residual.

**Contraction route to a goal bound (separate obligation).** For a full same-law residual $`F(x)`$, assume a closed weighted box around a, a fixed verified H, $`\sup_{\mathrm{box}}\|I-HJ_F\|_{\rho,\infty}\le\kappa<1`$, and a verified self-mapping condition $`\|HF(a)\|_{\rho,\infty}\le1-\kappa`$. Banach's theorem gives a unique root inside and

**(P18)**

```math
\|x^\star-a\|_{\rho,\infty}
\le\frac{\|HF(a)\|_{\rho,\infty}}{1-\kappa};
\quad |G(x^\star)-G(a)|
\le L_G\frac{\|HF(a)\|_{\rho,\infty}}{1-\kappa},
```

where $`L_G`$ includes the actual guarded goal/event/window map on the same box. V6 already describes a related componentwise certificate architecture in its nonlinear charge subclass, but the full vendor conduction/network/thermal/event certificate is **not** inherited by this derivation. The 600-V BE and the separate 150-V trapezoidal analysis remain distinct physical and numerical references.

This is the direct physical/scientific gain from original-paper frontier exploration: it makes the *missing source evidence* specific and calculable (voltage-domain bound d, conditioning H/κ, whole-system residual, goal Lipschitz) instead of merely saying “need a nonlinear remainder”. It also shows precisely why a low-cost one-Newton source solve and a surrogate affine-storage law have different error chains, as required by V6.
