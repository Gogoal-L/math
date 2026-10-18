# Proof notebook: finite-word scalar goal recovery with mixed nuisance, and physical DPT boundaries

**Status (2026-10-12):** independent conditional optimal-recovery derivations, analytical examples, source links, numerical regression tests. **No new SiC source-law result or new fundamental optimal-recovery theorem is claimed.** Companion to the [controller-side research transfer MAP](../DPT_MATH_RESEARCH_MAP.md); legacy M equations are preserved further below.

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
R_*\ge\max_{\substack{\|z\|,\|e\|\le1\\Az+Ee\in\mathop{\mathrm{im}}N}}|c^\top z|
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

For pure noiseless observations E=0, $`\rho(c)=0`$ iff $`c\in\mathop{\mathrm{row}}(U_0^\top A)`$. Given finite future-goal row stack Γ, a freely chosen extra *ideal noiseless source-state* row increases rank by at most one, so the exact abstract minimum is

**(P10)**

```math
k^{\rm ideal}_{\min}
=\mathop{\mathrm{rank}}\!\begin{bmatrix}U_0^\top A\\\Gamma\end{bmatrix}
-\mathop{\mathrm{rank}}(U_0^\top A).
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

---

## VIII. Retained-history bit budget for finite future-goal prediction (P19–P22)

**Scientific question and prior art.** Given exact legal preparation/command transcript categories available at encoding time, how many fixed-length persistent bits must be retained to predict declared future goals after a later pretarget sensor readout? This is a finite-bank deterministic instance of the **classical zero-error side-information graph-coloring theorem** (Witsenhausen 1976), extended here in its explicit data contract to *vector-valued future goals with per-goal interval tolerances and exact archived transcript classes*. Neither the chromatic-number identity nor the coloring algorithm is claimed as a new fundamental mathematical discovery.

**Contract.** Fix one reference/source-law and n legally prepared histories. History i has an **exact encoder-visible transcript** t_i (the encoder cannot observe its hidden source state), a later available pretarget side reading in an m-dimensional coordinatewise box B_i, and q prespecified future-command goals with interval uncertainty. The decoder receives the retained message z and later y in B_i, but no other information about the hidden history and no future target values. For scalar goal c let g_ic be its nominal value, eta_ic its absolute evaluation bound and tau_c its required prediction tolerance. Each side box is B_i = product over sensor channel l of [o_il-epsilon_l, o_il+epsilon_l]. The assumptions are finite-bank legality, a frozen future command/scorer for every goal, and a justified common box-noise observation model; Gaussian noise, stochastic priors, correlated ellipsoids, and continuous-domain guarantees are **not** assumed.

Two histories are mutually inconsistent with one decoder message if their allowed **later** sensor observations overlap yet one target cannot be approximated to its own tolerance for both:

**(P19)**

```math
\begin{aligned}
(i,j)\in E\quad\Longleftrightarrow\quad
& B_i\cap B_j\ne\varnothing,\\
& \exists c:\ |g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}>2\tau_c.
\end{aligned}
```

Partition histories into exact encoder-visible transcript classes T_alpha={i:t_i=alpha}. If an edge in E joins histories inside the *same* transcript class, no finite-memory function of that transcript can separate them; even infinitely many retained bits would not fix the missing information. Otherwise build the quotient graph H with one vertex per transcript class and an edge between two classes if **any** history pair across them belongs to E.

**Proposition (exact finite-bank one-shot retained-history message minimum).** Suppose every eta_ic <= tau_c. Among arbitrary deterministic encoders of the exact transcript category into a fixed-length bitstring, allowing any offline source-bank-aware decoder from the bitstring and later side readout, the minimum number of codewords and bits are

**(P20)**

```math
K_{\min}=\chi(H),\qquad
b_{\min}=\left\lceil\log_2\chi(H)\right\rceil.
```

**Proof, lower bound.** If adjacent transcript vertices receive the same codeword, select a witnessing pair of underlying histories (i,j), a common side observation y in their two boxes, and a goal c with the strict inequality in (P19). Under both histories the decoder receives identical (codeword,y); at least one allowed goal endpoint exceeds its tau_c error. Thus every feasible encoder is a proper coloring of H. If i and j share the exact transcript, every encoder maps them to the same word and the task is infeasible.

**Proof, upper bound and decoder construction.** Choose a proper K-coloring of H. Given received (z,y), let S(z,y) comprise all histories whose transcript color is z and whose side box contains y. For each goal c, every compatible history i permits the closed interval of forecasts [g_ic+eta_ic-tau_c, g_ic-eta_ic+tau_c]. Their common intersection is

**(P21)**

```math
I_c(z,y)=
\bigcap_{i\in S(z,y)}
[g_{ic}+\eta_{ic}-\tau_c,\ 
 g_{ic}-\eta_{ic}+\tau_c].
```

Any two members of S(z,y) have overlapping side boxes (at least at y) and identical colors, hence they cannot be a conflict edge. For each coordinate c the corresponding forecast intervals therefore intersect pairwise. Closed intervals on the real line have the **pairwise-Helly property**, implying I_c(z,y) is nonempty. Its midpoint is an explicit tolerance-feasible decoder. Choose coordinates independently because the declared goal uncertainty is a Cartesian product of intervals. Decoder behavior when S is empty is irrelevant outside the declared model domain. The proper coloring supplies K feasible messages, proving equality. The same proof shows that if eta_ic>tau_c for some single history, no decoder can cover even that history's goal interval.

**Sharp warning against naive pairwise memory counting.** Five histories have distinct exact transcripts; let their later side sensor centers be o_i=(cos(2 pi i/5),sin(2 pi i/5)), with common coordinate half-widths (0.6,0.6). Declare one future goal g_i=4i, eta_i=0 and tau=1. Exactly adjacent pentagon boxes intersect; nonadjacent boxes do not. All overlapping history pairs have goal gaps exceeding two. Thus the conflict graph is the chordless odd cycle C5. A largest all-conflicting compatible subset contains only two histories, but two retained messages cannot properly color this cycle:

**(P22)**

```math
\omega(C_5)=2<\chi(C_5)=3,\qquad
\left\lceil\log_2 2\right\rceil=1
<\left\lceil\log_2 3\right\rceil=2.
```

The exact budget is **2 bits**, exceeding the 1-bit bound inferred from the maximum clique. Uncompressed storage of all five transcript IDs would require 3 bits, an honest strong ordinary. This counterexample is synthetic geometry, **not a SiC or DPT measured case**.

**Executable verification and limits.** The existing [goal_repair_cover.py](../dpt_tools/goal_repair_cover.py) now exposes a separate command mode with option --retained-goal-bits. Required NPZ arrays: observations(n,m), goals(n,q), transcript_ids(n,) encoded as Unicode strings, observation_radii(m), goal_tolerances(q); optional goal_uncertainty(n,q). The output carries an explicit encoding, an exact chromatic minimum only when verified (default exhaustive search up to 17 distinct transcript classes), or a **feasible coloring upper bound and actual-clique lower bound**, never a false exact minimum. The independent tests include exhaustive small-graph color enumeration (2–6 histories), C5, transcript aliasing, interval edge cases, decoder interval feasibility and CLI input/output. GitHub Actions validates code and MathJax syntax, not native SiC physics.

**Deep reading: what was and was not transferred.** In upstream F140-A [original model and theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/build/sections/introduction.tex), a learner observes fresh independent Gaussian row/label pairs and retains at most 2^M persistent states, without rereading discarded observations. Its conclusion T >= c_A d log(1/epsilon) concerns **full-vector angular recovery**, not future scalar DPT goal prediction. Its [one-block proof](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/build/sections/blocks.tex) combines an exact projected density factor r^[a-m(1-1/q)] with a common projected support-volume factor r^[m(1-1/q)] by Holder, recovering r^a and charging N^(1/q) for N destinations. The actual [TikZ block-scaling proof diagram](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/build/figures/block-scaling.tex) makes that cancellation explicit. The [streaming continuation lemma](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/build/sections/streaming.tex) counts at most (m+2)2^M destinations; the [endpoint reflection argument](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Memory-and-precision-in-noiseless-Gaussian-regression-September-27-2026/build/sections/endpoint.tex) proves a full-data signal recovery limit without a finite-bit restriction. No such Gaussian theorem applies to arbitrary SiC preparation histories.

F365-B's [original PDE uniqueness theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Smooth-Anisotropic-Uniqueness-in-the-Calderon-Problem-from-One-Boundary-Patch-September-24-2026/build/sections/01-introduction.tex) assumes a complete density-valued local energy Dirichlet-to-Neumann operator on an open boundary patch for smooth metrics in dimension n>=3 and identifies only an interior-diffeomorphism **gauge class**. Its [product-cross continuation figure](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Smooth-Anisotropic-Uniqueness-in-the-Calderon-Problem-from-One-Boundary-Patch-September-24-2026/build/figures/product-cross.tex) uses conditional continuation on a product cross, including exponents gamma_1+gamma_2>1; shrinking-sphere estimates and global continuation require genuine PDE control. No finite DPT port identifiability or finite stability estimate is inherited from that theorem. The one-shot graph-coding mechanism instead has clear classical priority: [H. Witsenhausen, IEEE Trans. Information Theory 22(5), 592–593 (1976), DOI 10.1109/TIT.1976.1055607](https://doi.org/10.1109/TIT.1976.1055607).

**Actual DPT contract.** V6 Figure 4 identifies effective commutation L, nonlinear Q/C, driver/Kelvin feedback and observation-chain skew/bandwidth as interacting influences on ringing, peak and apparent work. For one named 100 V R1 or 150 V history/CAL source chart, the Main must supply: legitimate preparation states and complete command records; exactly which transcript categories are digitally available **before** the goal; later pretarget sensor ports and defensible joint error sets (Cartesian boxes only when justified); frozen ordered future words and work/peak/event-time windows; actual source goal uncertainty, tolerance and strong full-record ordinary. A conflict within a transcript class signals missing history information that extra **encoding of that same transcript** cannot restore. Positive 1–2-bit bank results do not imply a hardware minimum, a continuous-domain guarantee, or native adequacy. Source replay and a prospective holdout would be necessary to change MAIN_ACCEPTED.

---

## IX. Goal-specific repeatability and correlated-noise floor from OpenAI F122 (P23–P26)

**Scientific object.** P19–P22 calculate zero-error *deterministic finite-bank memory bits*. This section instead derives a *probabilistic two-history goal-recovery budget*: how many legally repeatable pretarget noisy sensor reads suffice to distinguish histories that produce separated **future** goals? The binary-testing reduction and Gaussian conditioning are classical mathematical ingredients, newly assembled as an explicitly bounded DPT acquisition question. They do not follow from F122's claimed sample-complexity exponent or constitute a new general theorem.

### IX.1. Four OpenAI primary-source comparisons, with exact transfer limits

**F122**, _Quantitative lower bounds for trace reconstruction_: [original theorem and deletion-channel model](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/quantitative-lower-bounds-for-trace-reconstruction-September-24-2026/build/sections/introduction.tex); [restoration, Hellinger/TV tensorization, binary testing](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/quantitative-lower-bounds-for-trace-reconstruction-September-24-2026/build/sections/transfer.tex); [Lean coverage statement](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/122.md). The paper claims superpolynomial repeated traces to reconstruct **every bit** of arbitrary strings through iid independent deletion at fixed rate. Its testing-reduction logic applies to any specified goal separation; the source's claimed worst-string rate does not transfer to analog DPT, corrupted timestamps or switching-event targets. Original statements and the final testing proof were inspected; the Lean proof was not rebuilt and all intermediate lemmas were not independently checked.

**F115**, _Exact uniform sampling of contingency tables_: [primary theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/introduction.tex), [repair graph method](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/model-and-graph.tex). A uniform prior on integer matrices with exact margins is not justified for correlated sensor or source-model errors. No physical noise law follows without a separately grounded coupling prior.

**F373**, _Nonattainment of the three-marginal Coulomb Monge problem_: [source theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/introduction.tex), [five-component supporting-potential certificate](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/certificate.tex). This special Coulomb cost can require a nondeterministic optimal three-marginal coupling, even though deterministic Monge infima agree. It is a useful warning against assuming all couplings are deterministic maps; it does not imply a non-Monge optimal coupling for Gaussian DPT measurement error.

**F139**, _Subpolynomial query complexity for strongly log-concave sampling_: [original model and theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections/introduction.tex). It assumes global I≤Hessian(V)≤2I and exact first-order potential/gradient oracle with unrestricted computation between queries. It is not a validated fast sampler or wall-clock guarantee for a switched multimodal SiC inverse problem. No new sampler is justified here.

### IX.2. Goal separation forces observable distribution separation

Fix a legal source reference and one frozen future ordered command. Two histories have scalar future goals g0,g1 with |g1−g0|>2tau, where tau is the goal tolerance. Let P_h^(m) be the **entire predictor-visible pretarget observation law**, including digitally recorded commands, under history h when m legal acquisitions are made. A possibly randomized predictor that succeeds with probability at least 1−alpha *under each history* must satisfy:

**(P23)**

```math
\mathrm{TV}(P_0^{(m)},P_1^{(m)})
\ \ge\ 1-2\alpha,\qquad 0<\alpha<1/2.
```

**Proof.** Successful forecast intervals around the two goals are disjoint. The event that the forecast lies within tau of g0 has probability at least 1−alpha under history 0 and at most alpha under history 1. Thus forecast-law TV is at least 1−2alpha; data processing bounds it above by observation-law TV. For genuinely iid observations only, product coupling gives TV(P0^m,P1^m)≤m TV(P0,P1), a necessary bound on m. Neither this inequality nor F122's iid-deletion arguments may be used after replacing repeated observations by correlated reads unless their joint law is explicitly modeled. A full recorded command that already reveals history must be present in the observation law; omitting it creates a weak ordinary.

### IX.3. Exact two-history Gaussian repeat-count theorem with shared drift

Under each h, assume identical lawful source preparation can be repeated, yielding a scalar *pretarget* sensor observation:

```math
Y_r=\mu_h+U+\varepsilon_r,\quad
U\sim N(0,\sigma_c^2),\quad
\varepsilon_r\overset{\mathrm{iid}}{\sim}N(0,\sigma_w^2).
```

The unknown U is drawn once per campaign, shared across repeats, and independent of within-run errors. Both hypotheses have the same covariance, and their pretarget sensor means differ by Delta=|mu1−mu0| **in sensor units**, not the future goal gap. No physically varying temperature/trap state, history-dependent variance or nonlinear observation transfer is assumed.

**(P24)**

```math
p_{\min}(m)=\Phi\left(
-\frac{\Delta}{2\sqrt{\sigma_c^2+\sigma_w^2/m}}
\right),\qquad m\ge1.
```

**Proof.** The m-vector covariance is sigma_w² I + sigma_c² 11^T. All directions orthogonal to the vector of ones have the same law under both histories. Its sufficient sample mean has variance sigma_c²+sigma_w²/m. The midpoint Gaussian likelihood-ratio threshold equalizes both conditional errors and attains the equal-prior Bayes lower bound, so it is minimax. For separated future goal intervals the winning binary decision followed by its known *hypothesis goal* attains the exact minimum failure (P24). If |g1−g0|≤2tau, a constant midpoint goal forecast is correct for both histories with **zero** reads.

Set z_alpha=Phi^(-1)(1−alpha), and Vcrit=Delta²/(4 z_alpha²). With separated goals, Delta>0, sigma_w>0 and Vcrit>sigma_c², the exact count is

**(P25)**

```math
m_{\min}=\max\left(
1,\left\lceil\frac{\sigma_w^2}{
V_{\mathrm{crit}}-\sigma_c^2}\right\rceil\right).
```

When sigma_w>0 and Vcrit≤sigma_c² **no finite repeat count works**. If sigma_w=0 one read is sufficient iff Vcrit≥sigma_c², and repeated reads cannot improve it. When Delta=0 and the goals are separated, identical observation laws make the goal permanently inaccessible. With sigma_c>0 the asymptotic failure floor is

**(P26)**

```math
p_\infty=\Phi\left(-\frac{\Delta}{2\sigma_c}\right).
```

The measurement law has a common stochastic drift, not an iid law in m; its posterior/statistical interpretation is source-conditional and distinct from the deterministic minimax sensor-box model.

### IX.4. Identical single-run distributions, different optimal experiments

In the analytical **synthetic** case g0=0,g1=4,tau=1,mu0=0,mu1=1,alpha=.05, three noise models all have exactly the same single-run distribution N(mu_h,1.04), but differ in cross-repeat covariance:

| Within-run noise variance | Shared calibration variance | Exact repeats for 95% worst-history success |
| ---: | ---: | ---: |
| 1.04 | 0 | **12** |
| 1.00 | 0.04 | **20** |
| 0.88 | 0.16 | **No finite number** |

Single-trace variance is therefore insufficient to decide whether repeating DPT acquisitions resolves a future-goal history alias. Pro18B's recorded **future** peak difference of 2.586995 V only requires historical discrimination for tolerances below 1.2934975 V; that future quantity is *not* Delta in (P24)–(P25).

### IX.5. Executable evidence and smallest Main input

The existing [goal_ambiguity_audit.py](../dpt_tools/goal_ambiguity_audit.py) offers a separate --gaussian-repeat-goal NPZ mode with observed_means(2,), future_goals(2,), scalar goal_tolerance, independent_sigma, shared_sigma and failure_probability. [Existing tests](../dpt_tools/test_goal_ceiling_tools.py) independently check exact thresholds, the m−1 failure, Monte Carlo errors, same-one-shot-different-correlation cases, shared-noise impossibility and CLI without breaking legacy Euclidean-ball mode. The software is a **two-history conditional Gaussian theorem evaluator** and does not demonstrate a native DPT measurement.

**Main handoff:** one accepted 100 V R1 or 150 V Pro18B/C source chart, truly repeatable legal preparation pair, full digitally recorded commands, named pretarget sensor and chronology, measured within-run versus shared drift covariance, future ordered command with frozen scalar goal/tolerance, and a fresh holdout. Compare full recorded-command ordinary, one different sensor and repeated existing sensor. If correlation-sensitive ranking cannot be qualified, return INCONCLUSIVE; synthetic PASS alone never upgrades MAIN_ACCEPTED.

---

## X. How much multi-sensor information survives unknown dependence? (P27–P30)

**Result identity (2026-10-12).** This section derives a sharp *two-history, finite-categorical, marginal-only* sensor-fusion theorem with an explicit attaining adversarial joint law and a deployable best-single-sensor decision rule. Its mathematical core is the classical total-variation/common-overlap and Fréchet-class coupling principle, NOT a novel property of OpenAI's sampling/transport papers. The new contribution to the DPT research programme is a precisely scoped, falsifiable **source-of-information decision contract**: adding an external sensor can yield huge goal discrimination, but if only each sensor's separate marginal law is qualified, **no improvement over the strongest single sensor is guaranteed for equal-prior average goal failure**. Actual SiC switching sources supply extra physical constraints, which could invalidate the adversarial coupling and unlock positive joint gains; their source-dependent form remains OPEN_RESEARCH.

### X.1. Original-proof exploitation, not just thematic analogies

**F122** ([source hypothesis-testing step](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/quantitative-lower-bounds-for-trace-reconstruction-September-24-2026/build/sections/transfer.tex)) gives a model-specific deletion-trace *testing* argument: if two laws are near in total variation, no estimator can reliably distinguish the generating string. Here we retain the **testing inequality**, replace deletion traces by the *complete predictor-visible multi-sensor readout*, and replace complete-string recovery by *two separated future goals*. The claimed F122 superpolynomial sample scaling is not used.

**F115-A** ([source fixed-margin table theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/introduction.tex), [padded graph/repair construction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Uniform-Sampling-of-Contingency-Tables-with-Arbitrary-Margins-September-24-2026/build/sections/model-and-graph.tex)) assumes fixed **integer row/column sums** and samples *uniformly over all feasible tables*. **F115-B** ([original cell-bounded FPRAS](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-FPRAS-for-Cell-Bounded-Contingency-Tables-September-24-2026/build/sections/introduction.tex), [bounded-flow-to-table bijection](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-FPRAS-for-Cell-Bounded-Contingency-Tables-September-24-2026/build/sections/flows.tex)) additionally permits structural zeros and integer capacity constraints. This shows how to *enumerate/count/sample a declared discretized feasibility family* once it is physically identified; its uniform counting measure is **not** a sensor noise probability law or posterior without separately justified exchangeability/calibration. This round therefore uses exact marginal constraints while retaining **all** compatible joint couplings; F115's substantial complexity theorem is not needed for the simple sharp TV minimization proved below. An eventual source-qualified Kirchhoff flow/charge-count discretization would be a different, more constrained physical task.

**F373** ([special smooth three-particle Coulomb example](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/introduction.tex), [dual support certificate](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/certificate.tex), [equality of infima without deterministic attainment](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-counterexample-to-the-Monge-ansatz-for-the-three-marginal-Coulomb-cost-September-25-2026/build/sections/infima.tex)) exhibits an optimal *nondeterministic* coupling for a special Coulomb transport cost when deterministic Monge maps never attain it. Our finite sensor-TV construction instead **attains** its bound by an explicit mixture of product couplings; the Coulomb nonattainment theorem is not transplanted. The useful warning is that restricting a probabilistic joint law to an unjustified deterministic correction map can delete admissible extremizers.

The classical broader setting is [Bartl, Kupper, Lux, Papapantoleon and Eckstein (2022), _Marginal and Dependence Uncertainty: Bounds, Optimal Transport, and Sharpness_](https://doi.org/10.1137/21M144709X): Fréchet classes distinguish specified marginals from unidentified dependence, and physical structural information can tighten bounds. Our particular finite-TV equality below is established directly, rather than attributed to an unidentified theorem in that article.

### X.2. Sharp worst-case joint-observation information, with constructive witness

Fix just two legal preparation histories h=0,1 under **the same frozen source reference**. There are p pretarget sensor/readout coordinates, each discretized into k labeled bins (zero-probability padding may represent sensors with fewer categories). The full, exact *marginal probability mass function* of sensor j under history h is p_hjb. A hypothesis-dependent joint sensor law Q_h is any probability law on the product alphabet whose j-th marginal equals p_hj. There are **no** conditional independence, Gaussian, covariance, support-mask, common-copula or cross-time constraints. The actual full recorded-command / pretarget digital transcript MUST be included as a predictor-visible feature whenever it is accessible. Let Gamma_h denote the class of all these joint laws.

**(P27)**

```math
\begin{aligned}
d_j &= \frac12\sum_{b=1}^{k}|p_{0jb}-p_{1jb}|,\\
d_*&=\max_{1\le j\le p}d_j,\\
\inf_{Q_0\in\Gamma_0,\ Q_1\in\Gamma_1}
\mathrm{TV}(Q_0,Q_1)&=d_*.
\end{aligned}
```

**Lower-bound proof.** Projecting any joint sensor law to coordinate j is a measurable map. Total variation cannot increase under projection, so TV(Q0,Q1) is at least d_j for every sensor and at least d_*. This alone does **not** prove equality; the missing piece is a single pair of joint laws achieving the strongest-marginal limit **simultaneously**.

**Attaining mixture construction.** Let s=1−d_* and t=d_*. For each sensor j, choose a nonnegative common subprobability c_j on its alphabet with total mass s and c_j(b) at most both history marginals. For s>0 one explicit choice is to rescale the pointwise overlap, which has total mass at least s:

**(P28)**

```math
\begin{aligned}
u_j(b)&=\min(p_{0jb},p_{1jb}),\quad
M_j=\sum_b u_j(b)\ge s,\\
c_j(b)&=s\,\frac{u_j(b)}{M_j},\qquad
r_{hj}(b)=\frac{p_{hjb}-c_j(b)}{t},\\
Q_h&=s\bigotimes_j(c_j/s)
+t\bigotimes_j r_{hj}.
\end{aligned}
```

When s=0 omit the common term; when t=0 omit both residual terms. Every r_hj is a probability mass function when t>0. Marginalizing Q_h in coordinate j gives exactly c_j+t r_hj=p_hj. Both joint laws contain the **same** product probability measure with weight s, giving TV(Q0,Q1)≤1−s=t=d_*. Combined with projection monotonicity, this yields equality in (P27). The construction is a compact factorized *attaining witness*; it never enumerates all k^p joint cells and does not require F115's sophisticated sampler.

### X.3. Exactly what forecasting risk follows, and what does not

For one frozen future command, assume g0 and g1 are distinct fixed scalar future goals and their acceptable prediction intervals [g_h−tau,g_h+tau] are **disjoint** (|g1−g0|>2tau). Consider the prior weighting h=0 and h=1 each with probability 1/2. A randomized decision rule may use all pretarget readings but not the hidden actual history or future goal outcome. For any known Q0,Q1 its optimal average goal-failure probability equals (1−TV(Q0,Q1))/2. The sharp minimax game over **unknown cross-sensor coupling** therefore satisfies

**(P29)**

```math
\inf_{\delta}\sup_{Q_h\in\Gamma_h}
\frac12\sum_{h=0}^{1}
Q_h\{\delta(Y)\ne h\}
=\frac{1-d_*}{2}.
```

**Proof/constructive ordinary.** The adversarial joint pair of (P28) makes the Bayes error exactly (1−d_*)/2, so no decoder can uniformly do better in equal-prior *average error*. Choose sensor j* maximizing d_j. Its binary likelihood rule returns history 1 for bins with p_1,j*(b)>p_0,j*(b), and returns 0 otherwise, breaking ties arbitrarily. Its average failure is (1−d_*)/2 **for every possible joint dependence**, since it does not observe other sensors. Hence the robust equality and a practically executable strong ordinary. When |g1−g0|≤2tau, a constant goal forecast in the overlapping intervals gives **zero** failure without reading any sensor.

**Critical per-history caveat.** Equal-prior average Bayes risk is not the same as the minimum maximum conditional error across the two preparations. For a single sensor with P0=(1,0), P1=(1/2,1/2), the marginal TV is 1/2 and equal-prior Bayes failure is 1/4; the obvious likelihood decision has conditional failure (0,1/2). The *randomized minimax worst-history* rule puts probability 1/3 on guessing history 1 at bin 0, and predicts history 1 at bin 1; both conditional errors become 1/3. Thus **1/4 cannot be advertised as a per-history 75%/95% guarantee**. P23's necessary TV test applies to worst-history success, but (P29) optimizes the different explicitly declared equal-prior objective. The new CLI reports the two error components of its single-sensor ordinary and does not invent a globally optimal worst-history classifier.

### X.4. Two opposite calibrated-dependence counterexamples

**(P30)**

```math
\begin{aligned}
P_{0j}=P_{1j}&=(1/2,1/2)\quad (j=1,2),\\
Q_0(0,0)=Q_0(1,1)&=1/2,\\
Q_1(0,1)=Q_1(1,0)&=1/2,\\
\max_j\mathrm{TV}(P_{0j},P_{1j})&=0,\\
\mathrm{TV}(Q_0,Q_1)&=1.
\end{aligned}
```

**Exact joint-only synergy, absent from all marginal probabilities.** Both histories have *identical* Bernoulli(1/2) marginal distributions on two sensors, so d_*=0 and (P29)'s worst-case equal-prior failure is 1/2. But suppose the physically qualified joint law under h=0 is P(Y1=Y2)=1 and under h=1 is P(Y1≠Y2)=1, with all two permitted configurations at probability 1/2. Their supports are disjoint: joint TV=1 and a joint decoder predicts the future goal **perfectly**. If those specific joint-dependence constraints are NOT qualified, a common independent joint law Q0=Q1 gives TV=0, so the perfect inference is not guaranteed by marginals alone.

**Positive independent-sensor ordinary.** Three conditionally independent binary pretarget sensors each have P0(bin 1)=.2 and P1(bin 1)=.8. Each sensor alone has TV=.6 and average optimal failure .2. Their **qualified independent joint product** has TV=.792, giving optimal equal-prior failure .104. Without the independence contract the exact worst joint TV returns to .6. Both are mathematically consistent; the source determines which model applies.

**What physical support would change the verdict?** If legal, source-qualified observation support masks are disjoint across histories, every feasible compatible joint law has TV=1—even with individually identical marginals. But any proposed support constraint requires its own source-law and noise/quantization proof. The present tool checks a supplied complete joint PMF against its marginals; it does **not** prove that empirical PMFs, support masks or noise distributions came from actual SiC experiments.

### X.5. A positive *support-qualified* repair from F115's flow viewpoint (P31–P32)

The weighted Hall feasibility criterion is classical and is explicitly distinguished from *full support* (positive mass on every declared allowed cell) in [Coscia, Tassy and Winkler (2026), _Sets that Support a Joint Distribution_, Theorems 1 and 4](https://arxiv.org/html/2608.04135v1). Our allowed masks mean **the true support is contained within the mask**, not equal to it, and the checker does **not** certify every allowed combination has positive probability. This source is a direct prior-art comparator independent of the OpenAI F115 counting/sampling paper.

The unrestricted Fréchet class in (P27) is deliberately conservative. The smallest *new* source information that can overturn the bound need not be a fully estimated 2-dimensional joint PMF: a **hard physically legal joint support set** or **credible upper bound on mass outside it** can already suffice. This observation is genuinely compatible with the exact *bounded-flow feasibility* viewpoint of F115-B, though its expensive counting/sampling result is NOT invoked.

Consider precisely **two** categorical pretarget sensors, with row and column marginals a_h and b_h under history h, each over k bins. A declared history-conditional joint support mask E_h is a set of permitted pairs (row bin, column bin). Let N_h(I) be the set of all column bins joined by an allowed edge to any row bin in subset I. The *sharp minimum possible probability leakage outside E_h* among all joint distributions with those marginals is the classical weighted Hall/max-flow deficiency:

**(P31)**

```math
\begin{aligned}
\ell_h^{\star}
&=\min_{Q_h:\,\text{marginals }(a_h,b_h)}
Q_h(E_h^{\,c})\\
&=\max_{I\subseteq\{1,\ldots,k\}}
\left[
\sum_{i\in I}a_h(i)
-\sum_{j\in N_h(I)}b_h(j)
\right]_+.
\end{aligned}
```

**Proof.** Any mass arising from a row subset I must go either to its allowed neighbor columns, whose total demand is at most b_h(N_h(I)), or outside the declared support. Every I therefore gives a necessary leakage lower bound. Conversely, solve the finite bipartite maximum-flow problem with row capacities a_h(i), column capacities b_h(j), and admissible internal arcs E_h of capacity one. The max-flow/min-cut theorem makes the maximal mass routed through E_h equal to 1−max_I[a_h(I)−b_h(N_h(I))]_+. Complete the residual row/column demand by a joint probability on the whole product alphabet. Because maximal flow has no remaining allowed row-to-column augmenting path between residual positive nodes, residual mass may be routed outside E_h, attaining the bound. This is a classical finite transport/cut duality, not a novel DPT theorem.

In particular, a **hard** allowed support (leakage=0) is compatible with the known marginals *if and only if* every Hall cut has nonpositive deficiency. The CLI enumerates nonempty row subsets (at most 2^14−1 per history) and returns a violating row subset if a claimed support/tail contract is incompatible with the supplied marginal masses. For the synthetic row masses a=(.9,.1), column masses b=(.1,.9) and a diagonal-only support, I={first row} yields exactly 0.9−0.1=**0.8** required leakage. A feasible table with off-support probability .8 attains it.

A positive *goal* claim follows when E_0 and E_1 are disjoint and are each correct with probability at least 1−epsilon_h. For the decision rule that predicts history 0 when the paired sensor bin lies in E_0 and predicts history 1 otherwise:

**(P32)**

```math
\begin{aligned}
Q_0(\delta(Y)\ne0)&\le\epsilon_0,\\
Q_1(\delta(Y)\ne1)&\le\epsilon_1,\\
\mathrm{TV}(Q_0,Q_1)&\ge
\max(d_*,\,1-\epsilon_0-\epsilon_1).
\end{aligned}
```

**Proof.** Under history 0, every correct-support readout is recognized, so failures live in E_0^c with mass at most epsilon_0. Since E_0 and E_1 do not overlap, every history-1 observation assigned history 0 belongs to E_1^c, with probability at most epsilon_1. On the event E_0, the difference Q_0(E_0)−Q_1(E_0) is at least 1−epsilon_0−epsilon_1, providing the TV lower bound; projection supplies d_* independently. For *future goal intervals separated by more than twice their tolerance*, outputting the declared hypothesis goal gives **two separate conditional prediction-error upper bounds**, which is stronger in decision meaning than the equal-prior-average statement (P29). If epsilon_0=epsilon_1=0, source-qualified disjoint supports yield perfect discrimination even though both marginal TVs may be zero (P30).

**Physical limitation and key falsifier.** A switched/guarded model might establish that two port-bin combinations are impossible inside a certified approximation/error tube. Oscilloscope Gaussian noise, timing skew, unmodeled capacitive memory or shared calibration can invalidate exact structural zeros. Therefore **soft, empirically qualified leakage bounds** are preferable when support is not truly hard. The checker validates arithmetic feasibility against exact supplied histograms; it cannot prove that a candidate support or its tail bound is physically true. If the masks overlap, it does not infer a strict TV improvement from those masks alone. Counts/sample uncertainty and source legality remain open, so no native MAIN_ACCEPTED promotion follows.

### X.6. What remains usable from F139: a precise stopping condition

F139's [original first-order-oracle theorem](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections/introduction.tex) assumes a globally strongly convex potential with Hessian bounded between the identity and twice the identity (in chosen normalized coordinates) and permits unrestricted arithmetic between queries. **An elementary nonlinear observation inverse problem violates this:** take Gaussian observation y=1 of f(x)=x², unit observation noise variance and a N(0,1) Gaussian prior. Up to an irrelevant constant, its negative log-posterior potential is V(x)=(x²−1)²/2+x²/2. Then V''(x)=6x²−1 and V''(0)=−1. It has two separated minima at x=±1/sqrt(2), violating global log-concavity and even convexity. Thus a well-conditioned Gaussian prior does not prove F139's likelihood assumptions, and F139's claimed low *oracle query* complexity does not imply cheap switched-source model evaluation. A source-qualified strongly convex chart could reopen that work; this generic goal-auditor does not.

### X.7. Independent numeric pressure, implementation and Main handoff

[goal_ambiguity_audit.py](../dpt_tools/goal_ambiguity_audit.py) gains a separate --marginal-only-fusion mode. Inputs: marginal_probabilities(2,p,k) and future_goals(2,), goal_tolerance, optional sensor_names(p) and *complete* joint_probabilities(2,k,...,k). Exact finite-categorical masses, frozen matching bin definitions and the same source reference are mandatory. It returns per-sensor TVs, **sharp worst joint TV**, an explicit two-mixture factorized adversarial coupling, the achievable equal-prior best-sensor decision and *both* conditional error components. If a full joint PMF is supplied, it checks normalization/marginal consistency and separately reports actual-joint TV and its gain over the strongest marginal. Numerical marginal agreement is NOT physical validation, and small-N empirical frequency tables do not magically become known exact probabilities.

Verification uses: independent product-law reconstruction across 96 random two-history banks (1–3 sensors, 2–3 bins), independent two-binary-sensor grid-search minimization of the coupling TV, the two opposite correlation/ranking counterexamples, per-history Bayes-versus-minimax falsifier, input/PMF checks and NPZ CLI replay. A separate off-repo exact linear-programming oracle using SciPy HiGHS agreed with (P27) on 100 random 2- and 3-binary-sensor banks; the repository regression deliberately requires NumPy only. Neither Python regression nor GitHub formula rendering is a formal verification of the original F115/F373/F139 mathematical statements.

**Smallest native DPT test.** On a single accepted 150 V Pro18B/C or original 100 V R1 chart, choose a legal two-preparation pair with separated prospective work/peak/event goals. Freeze the full digital command/history record, sensor-port timing, quantization bins, error tolerance and scorer. First estimate both *per-history sensor marginals* from truly independent, repeatably prepared calibration runs. Then seek a qualification of joint cross-port dependence or legal support from same-shot paired waveforms, with bandwidth/time skew, sample-size, source discrepancy and calibration drift controlled. Compare complete recorded-command ordinary, strongest single sensor, jointly calibrated two-sensor decision, and the independent-Gaussian repeat model P24 only if that separate Gaussian campaign contract is valid. The verdict delta is **measured joint-TV advantage that persists under source qualification and a fresh goal holdout**; otherwise keep SIDE_VERIFIED/READY_FOR_HANDOFF and label sensor synergy OPEN_RESEARCH.

---

## Legacy MAP mathematical derivations: recoverability, nuisance, observation and CAL

Original M-numbering and conditions are preserved below. The P-numbered proof above remains the primary derivation. The frozen [historical MAP](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/DPT_MATH_RESEARCH_MAP.md) fixes the preceding text.

### 0.1 科学目标不是恢复 θ，而是恢复规定命令下的 G

令 $`h\in\mathcal H_{\mathcal R}`$ 是由合法 preparation 在参考系统 $`\mathcal R`$ 中生成的 source-reachable 历史；$`O(h)`$ 是**目标计算之前允许取得的外部观测**；$`T_w(h)`$ 是按实际顺序执行合法有限命令字 $`w`$ 后的 source state；$`G_j(T_w(h))`$ 是具名 work/peak/event-time。参数 $`\theta=(L_g,L_s,L_d,L_{\rm loop},R_g,\ldots)`$ 及未测电荷/热态并不默认可由 $`O`$ 唯一恢复。正确的决策对象是：

**(M1)**

```math
\boxed{
\mathcal R_{j,w}(O,\mathcal H_{\mathcal R})=
\inf_{\widehat G:\,O\mapsto\mathbb R}\ 
\sup_{h\in\mathcal H_{\mathcal R},\ \text{合法误差}}
|\widehat G(O(h))-G_j(T_w(h))|.
}
```

若两个合法 $`h_+,h_-`$ 在误差合同下可生成同一观测 $`y`$，则任何观测型预测器在 $`y`$ 只能输出同一个数，三角不等式立即给

**(M2)**

```math
\mathcal R_{j,w}\ge\tfrac12|G_j(T_w(h_+))-G_j(T_w(h_-))|.
```

这解释 18B 的未来 peak 差是**不可避免误差的下界见证**，不是整个可达类的上界；18C 的 L 不唯一与目标 work 稳定可同时成立。有限 bank 的小 goal spread **不是**全域小 $`\mathcal R`$ 的证明。该统一对象既可作用于工程目标，也容纳 18A 的严格噪声/证书结果。

---

### 0.5 三篇真正联合的严格结果：future-goal minimax radius with mixed nuisance

这是本 Math 仓库的新**独立线性模型推导与实现**，不是宣称 F119/F129/F132 直接推出 SiC 定理。假设有限 source chart 由

**(M13)**

```math
\begin{aligned}
x&=x_0+Bz,\qquad \|z\|_2\le1,\\
y-y_0&=HBz+N\eta+Ee,\\
&\|e\|_2\le1,\qquad \eta\in\mathbb R^p.
\end{aligned}
```

这里 $`N\eta`$ 是**可任意大的同一个未知线性 nuisance**，$`Ee`$ 是**联合、可相关、确定性有界**的传感器误差；$`z,e`$ 是**彼此独立的两个单位球预算**，不能由普通样本 covariance 自动获得。命令 $`w=(u_1,\ldots,u_\ell)`$ 的 linear update 为 $`F_w=A_{u_\ell}\cdots A_{u_1}`$，第 $`j`$ 个未来目标的线性部分是 $`c_{w,j}^\top z`$，其中 $`c_{w,j}=B^\top F_w^\top C_j^\top`$。令 $`A=HB`$。

**定理（标量、有限维、整个声明线性 chart 的 minimax radius）：**

**(M14)**

```math
\begin{aligned}
R(c;A,N,E)
&=\inf_{\widehat g}\sup_{\|z\|,\|e\|\le1,\eta}
 |c^\top z-\widehat g(Az+N\eta+Ee)|\\
&=\max_{\substack{\|z\|\le1,\ \|e\|\le1\\Az+Ee\in\mathop{\mathrm{im}}N}}
 |c^\top z|\\
&=\min_{\substack{a\in\mathbb R^m\\N^\top a=0}}
 \left(\|c-A^\top a\|_2+\|E^\top a\|_2\right).
\end{aligned}
```

证明的三步：① 对可由反号 $`(z,e,\eta)`$ 形成同一 $`y=0`$ 的两条历史，所有 decoder 至少承担 $`|c^\top z|`$；② 对任意 $`N^\top a=0`$，线性预测器 $`a^\top(y-y_0)`$ 的误差由两个单位球的 support function 上界给出式 (M14) 最后一行；③ 将 $`(z,e)`$ 的紧凸对称积球与观测线性等式作 Lagrange/Fenchel dual（原点满足严格球内点），上下界相合。因此**存在最优线性外部 readout**，不需要先估计全部 $`x,\theta,\eta`$。该结论属于已有 optimal-recovery 范畴，相关标准来源：[Foucart–Liao, Journal of Complexity 83 (2024), 101841](https://doi.org/10.1016/j.jco.2024.101841)；这里只作具名 mixed-nuisance 归约与 DPT 使用合同。

**把无界 nuisance 与零噪声 contrast 分两次剔除：** 取 $`U_0`$ 张成 $`\ker N^\top`$，设 $`A_0=U_0^\top A,E_0=U_0^\top E`$。$`E_0`$ 的 compact/full-left SVD 写成 $`E_0=U_r\Sigma_rV_r^\top`$，其正交余方向为 $`U_\perp`$。由于 $`U_\perp^\top E_0=0`$，任何兼容状态差 $`z`$ 必须满足

**(M15)**

```math
Kz=0,\quad K=U_\perp^\top A_0;
\qquad z=Zv,\quad Z^\top Z=I,\quad\mathop{\mathrm{im}}Z=\ker K.
```

再定义 $`M=\Sigma_r^{-1}U_r^\top A_0Z`$、$`c_r=Z^\top c`$，则

**(M16)**

```math
\begin{aligned}
R&=\max_{\|v\|\le1,\ \|Mv\|\le1}|c_r^\top v|,\\
R^2&=\min_{0\le q\le1}
c_r^\top\bigl[(1-q)I+qM^\top M\bigr]^{-1}c_r.
\end{aligned}
```

端点奇异时沿 $`q\to0^+,1^-`$ 取兼容极限，不以盲目 Moore–Penrose 代替无穷方向。**推导而非仅引用优化器：** 对 $`D_q=(1-q)I+qM^\top M`$，Cauchy–Schwarz 给
$`(c_r^\top v)^2\le(c_r^\top D_q^{-1}c_r)(v^\top D_qv)\le c_r^\top D_q^{-1}c_r`$；在最小化的内点 $`q^\star`$，令 $`v_\star=D_{q^\star}^{-1}c_r`$，一阶导数为 $`\|v_\star\|^2-\|Mv_\star\|^2=0`$，规范化即可同时触及两个约束并达到上界。端点最优时对应单个活跃约束；若有奇异方向先依 (M15) 消去。故式 (M16) 是全局可计算结果，而不仅是局部 SVD heuristic。实际代码仍有 floating-rank 门槛，其“半径 0”只有在物理证明 exact common mode 时才可以作为物理零误差。

多个未来词、多个工程目标各有容许误差 $`\tau_j>0`$。对所有目标使用同一预测前观测、分别构造最优线性 decoder，**归一化 worst-case 最大误差**准确等于

**(M17)**

```math
R_{\infty,\mathcal W}=
\max_{w\in\mathcal W,\ j}\frac{R(c_{w,j};A,N,E)}{\tau_j}.
```

因此 $`R_{\infty,\mathcal W}\le1`$ 是声明模型/传感器/有限 word 下的**达到工程容差的充分且必要条件**；不是全 command language 或 nonlinear source 的证书。[contextual_goal_recovery.py](dpt_tools/contextual_goal_recovery.py) 实际计算此式，调用 [goal_ellipsoid_recovery.py](dpt_tools/goal_ellipsoid_recovery.py) 的一维 $`q`$ 求解器；[8 项解析＋CLI 测试](dpt_tools/test_contextual_goal_recovery.py) 覆盖命令先后、rank-one shared noise、independent noise、预测前 CAL 和非法输入。

**由 (M16) 退化出的无噪声 rank 定理：** 当 $`E=0`$，$`R(c)=0`$ 当且仅当 $`c\in\mathop{\mathrm{row}}(U_0^\top HB)`$。若一组未来目标在 $`z`$ 坐标堆为 $`\Gamma_{\mathcal W}`$，允许免费设计任意理想、无新增 nuisance 的标量测量，则最少还缺的独立读数为

**(M18)**

```math
k_{\rm ideal}=
\mathop{\mathrm{rank}}\begin{pmatrix}U_0^\top HB\\\Gamma_{\mathcal W}\end{pmatrix}
-\mathop{\mathrm{rank}}(U_0^\top HB).
```

这与已有 [contextual_goal_quotient.py](dpt_tools/contextual_goal_quotient.py) 一致；$`B`$ 非满秩时必须先写在可达 $`z`$ chart 中，不能把整个 ambient parameter space 当作真实 reachable space。真实 CAL/传感器只能从**有限合法候选库**购买，所需 channel 数可能大于理想 $`k_{\rm ideal}`$。

**精确小例子：** $`B=H=I_2,\ N=(1,1)^\top,\ E=0,\ C=(1,-1),\ A_{\rm future}=\mathrm{diag}(1,-1)`$。当前 goal 为 $`x_1-x_2`$，可用 $`y_1-y_2`$ 精确计算，$`R_{\rm now}=0`$；未来 goal 变成 $`x_1+x_2`$，却与无界共同 offset 混淆，$`R_{\rm future}=\sqrt2`$（状态先验是 $`\|z\|_2\le1`$，不是两个独立区间）。若合法预测前 CAL 另读 $`y_3=\eta`$，则 $`y_1+y_2-2y_3=x_1+x_2`$，future 半径归零。若原两通道分别有联合球 $`\|e\|\le1`$ 的 **0.1 倍独立误差**，CAL 后 $`R_{\rm future}=0.1\sqrt2`$；共享的 0.2 倍噪声 $`E=0.2(1,1)^\top`$ 则在差分方向仍完全消去。**这个小例子的单位是归一化状态/目标，不是 V、nH 或 nJ。**

---

### 0.6 非线性 DPT 恰好还缺的东西：余项、work 事件、peak 守卫

源器件电荷本构、Coss/Crss、body diode 与模式/事件切换一般使 (M13) 只是局部近似。在同一**具名合法非零域**，若观测与某个 future scalar goal 有

**(M19)**

```math
\begin{aligned}
O(z)&=y_0+Az+N\eta+Ee+r_O(z),\\
G_w(z)&=G_{w,0}+c_w^\top z+r_{G,w}(z),\\
\|r_O\|&\le\beta_O,\qquad |r_{G,w}|\le\beta_{G,w}.
\end{aligned}
```

则对任何 $`N^\top a=0`$，有可复算的**非线性条件上界**

**(M20)**

```math
\begin{aligned}
\sup|\widehat G_a-G_w|
&\le\|c_w-A^\top a\|+\|E^\top a\|\\
&\quad+\beta_{G,w}+\|a\|\beta_O,\\
\widehat G_a&=G_{w,0}+a^\top(y-y_0).
\end{aligned}
```

证明是展开残差、消去 $`N\eta`$、逐项取范数。最小化右侧时**应当把 $`\|a\|\beta_O`$ 一起计入**；先以 (M14) 选出放大系数很高的 decoder 再忽略 remainder，会虚报修复。关键不足是从 actual coupled source 给出 $`\beta_O,\beta_G`$ 在准备/未来共同合法域的统一上界，而不是把 finite-bank 最大残差称为证书。式 (M14) 的精确 minimax 下界不能在非线性 remainder 未控制时照搬。

对于真正的 DPT signed stage work（需固定端口、电流方向与窗口），设

```math
W(z)=\int_{t_a(z)}^{t_b(z)} V_{DS}(t,z)I_D(t,z)\,dt.
```

Leibniz rule 给出真实目标导数：

**(M21)**

```math
\begin{aligned}
DW[\delta z]
&=\int_{t_a}^{t_b}
\bigl(I_D\,DV_{DS}[\delta z]+V_{DS}\,DI_D[\delta z]\bigr)\,dt\\
&\quad+[V_{DS}I_D]_{t_b}Dt_b[\delta z]\\
&\quad-[V_{DS}I_D]_{t_a}Dt_a[\delta z].
\end{aligned}
```

若事件由 $`\phi(t,z)=0`$ 定义且 **transversal**，$`|\partial_t\phi|\ge\gamma>0`$，隐函数定理给

**(M22)**

```math
Dt_\ast[\delta z]=-\frac{D_z\phi[\delta z]}{\partial_t\phi}.
```

当 crossing 斜率接近 0、峰值多重或 guard 换支时，$`DG`$ 及 $`\beta_G`$ 可能剧增甚至失去该光滑表示。对于唯一内部光滑非退化 peak，包络定理的一阶 peak-value 导数是 $`D_z V_{DS}(t_\ast,z)`$，但 **peak time** 仍需另行求导；有多个几乎相等的 ringing peaks 时不能随意选择其中一个导数。

18B 的配对实值例子表明目标种类本身很重要：

**(M23)**

```math
\begin{aligned}
\Delta W_1&\approx+1.628664~\mu{\rm J},\\
\Delta W_2&\approx-1.686273~\mu{\rm J},\\
\Delta W_{\rm total}&\approx-57.609755~{\rm nJ},\\
1-\frac{|\Delta W_{\rm total}|}{|\Delta W_1|+|\Delta W_2|}
&\approx 98.26\%.
\end{aligned}
```

这解释了为什么单个 total-work goal 可以比两阶段 work、peak/event 更稳定。它**不是** total Eon/Eoff 的全局稳定定理；目标必须与正式窗口、积分符号及 source 端口一致。

---

### 0.7 回接原始 R1 的可辨识方向，而非把数学停在抽象 chart

在**声明 KVL 符号、实际 source 电流导数与明确 discrepancy**的低阶 turn-off 诊断中，可将外部 overshoot 近似写作

**(M24)**

```math
\begin{aligned}
u(t)&:=V_{DS}(t)-V_{\rm DC},\\
u(t)&\approx L_{\rm eff}s(t)
+R_{\rm loop}I_D(t)+b(t),\\
s(t)&=-\frac{dI_D}{dt}.
\end{aligned}
```

若将允许的 offset/电阻/传感器偏差基函数离散堆成 $`N_s`$，令 $`P_\perp`$ 是加权 $`W`$-内积对 $`\mathop{\mathrm{col}}N_s`$ 的正交投影，则在线性、已知 $`s`$ 情形

**(M25)**

```math
\widehat L_{\rm eff}
=\frac{\langle P_\perp s,P_\perp u\rangle_W}{\|P_\perp s\|_W^2},
\qquad
|\widehat L_{\rm eff}-L_{\rm eff}|
\le\frac{\|\epsilon\|_W}{\|P_\perp s\|_W}.
```

若 $`P_\perp s=0`$，该实验无法区分有效 L 和允许 nuisance；若它很小，即使 waveform 拟合完美，参数也会不稳定。注意 **s 的数值微分误差、gate-charge/Coss 非线性、internal Kelvin source 与 external cut port 不一致**均可破坏 (M24) 的条件；它不是 LTspice/硬件的已核验器件方程。更重要的是，某个未来 overshoot/work 的导数 $`DG`$ 可能在这个不可辨识方向上很小，于是 (M1)/(M14) 允许目标稳定而 L 不唯一。下一步该拿真实 R1 reference 的同源 $`O,DO,DG,s,N_s`$ 与设备外部 cut record 来检验，而不是借用 150 V CAL 的 chart 替 100 V R1 作证。

#### 传感器关联误差真正进入 stage-work：common time shift 与 relative deskew 的定量分解

这是一条来自 DPT 积分定义、独立于 F119 随机通道定理的**物理测量方程**。在固定窗口 $`[t_a,t_b]`$ 上，若探头读到 $`V_m(t)=V(t+\delta_v)`$、$`I_m(t)=I(t+\delta_i)`$，且两波形在声明窗口中 $`C^2`$、偏移足够小，Taylor 展开给

**(M26)**

```math
W_m-W
=\delta_v\!\int_{t_a}^{t_b}\dot V I\,dt
+\delta_i\!\int_{t_a}^{t_b}V\dot I\,dt+O(\|\delta\|^2).
```

设共同偏移 $`\delta_c=(\delta_v+\delta_i)/2`$、相对偏移 $`\delta_r=(\delta_v-\delta_i)/2`$，由分部积分 $`\int(\dot VI+V\dot I)=[VI]_{t_a}^{t_b}`$ 可得

**(M27)**

```math
\begin{aligned}
W_m-W
&=\delta_c[VI]_{t_a}^{t_b}\\
&\quad+\delta_r\int_{t_a}^{t_b}
(\dot V I-V\dot I)\,dt\\
&\quad+O(\|\delta\|^2).
\end{aligned}
```

**可检查的解析负控：** $`V(t)=2+3t,\ I(t)=5-2t,\ [t_a,t_b]=[0,1]`$，符号积分精确给 $`W=13.5`$，并且 $`W_m-W=5\delta_c+19\delta_r-6\delta_c^2+6\delta_r^2`$。两项的系数 5、19 与 (M27) 严格一致。若积分窗口也随两条波形**共同平移**而移动，完整时间平移可由换元消去；(M27) 的共同边界项是针对**固定物理积分窗口**，不可混到自动事件窗口中。若两探头带宽/滤波不同，其误差不等价于单一 timing skew，还必须纳入频率响应 discrepancy。DPT 原始测量指导：[Wolfspeed Dynamic Characterization](https://www.wolfspeed.com/knowledge-center/article/dynamic-characterization-and-measurement-methods/)；[Hardware Testing Methodologies for Wide Bandgap High-Power Converters, Electronics 13 (2024), 3918](https://www.mdpi.com/2079-9292/13/19/3918)。这才是 F119“信息依赖噪声相关结构”的**可执行物理启发**：实际 source 需要同一波形时标、校准手段和误差相关性证据才能兑现；公式本身不测量任何探头偏差。

---

### 0.8 真正的 acquisition 判别：CAL 是干预，不只是增加一行 sensor

对于允许购买的预测前观测集合 $`\mathcal S\subseteq\mathcal M_{\rm legal}`$，每一个 candidate 都要有实物端口、获取时间、共同 nuisance/误差关联列和成本 $`c_s`$。在**同一个 source reference 与未来目标**上，有限预算下的目标相关设计问题为

**(M28)**

```math
\boxed{
\min_{\mathcal S\subseteq\mathcal M_{\rm legal}}
\sum_{s\in\mathcal S}c_s
\quad\mathrm{s.t.}\quad
\max_{w,j}R_{w,j}(\mathcal S)/\tau_j\le1.
}
```

这里 $`R_{w,j}(\mathcal S)`$ 来自具名 observation/N/E/goal chart 的 (M14–M17)；并非以单个参数 Jacobian condition number 或“测量越多越好”来替代目标误差。**若增加一个纯观测而不改变 preparation/物理状态，且旧误差合同仍作为新合同的正确 marginal**，最优 minimax radius 不会变大：新预测器可以忽略新读数，直接复用旧预测器。若 CAL 同时改变了物理状态，单纯套这个单调性是错误的实验比较。

尤其对于 18C 的**主动** CAL，设 $`K:\mathcal H\to\mathcal H`$ 是实际 CAL 操作，$`O_K`$ 是 CAL 后得到的外部读数。CAL 后未来目标是 $`G_w^K(h)=G(T_wK(h))`$，而非原来的 $`G(T_wh)`$。要只估计 **CAL 带来的信息价值**，需要同样执行 $`K`$、同样的后续未来，但在 predictor 输入中分别**隐藏或开放 CAL 数据**：

**(M29)**

```math
\begin{aligned}
R_{\rm withheld}^{K}
&=\inf_\delta\sup_h
 |\delta(O_{\rm pre}(h))-G(T_wK(h))|,\\
R_{\rm measured}^{K}
&=\inf_\delta\sup_h
 |\delta(O_{\rm pre}(h),O_K(K(h)))-G(T_wK(h))|.
\end{aligned}
```

这两个对象固定 **同一 CAL-induced physical history**，所以 $`R_{\rm measured}^K\le R_{\rm withheld}^K`$；若把 $`R_{\rm measured}^K`$ 与 no-CAL future $`G(T_wh)`$ 直接比较，观测的信息增益和操作 $`K`$ 的物理效应已混在一起。必须单列 CAL-versus-NO-CAL **干预/状态转移效应**，才能科学地解释 Pro18C 结果。

**最低成本可取得信息**还必须打败强 ordinary：完整记录 command、固定波形/斜率估计、合格 deskew、已知 CAL 执行日志、基于原 source 的低阶近似。优先的下一项证据是 150 V 同 reference 的 CAL-executed-and-withheld 对照或真实 B/history pair 的 source chart，冻结未来 word 和目标后再算 (M28)；不是扩大 PDF 数目或把理想 rank 直接命名为真实 sensor minimum。

---

## Provenance annex: 20261011_continuous_goal_information_bridge

Complete prior proof and research record, retained with its hypotheses, negative evidence, source references and uncertainty semantics. [Original immutable version](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/dpt_research/20261011_continuous_goal_information_bridge.md). The original finite-bank interval geometry is distinct from the continuous Euclidean/joint-noise model above.

### Continuous goal-information radius under correlated bounded observation error

**Date:** 2026-10-11. **Scientific state:** exact finite-dimensional centered-ellipsoid **linear** model and numerically checked synthetic implementation. **Not** an accepted DPT source result, certified nonlinear reachability, calibrated metrology, hardware sensor minimum, or new universal optimal-recovery theorem. The DPT controller retains scientific authority.

#### Missing bridge and definitions

The existing Math tools cover finite-bank ambiguity and repair (goal_ambiguity_audit, goal_repair_cover, goal_lipschitz_stability) and supplied linear ordered-stage dynamics (goal_defect_transport). None of them directly evaluates a continuous, deterministic, *correlated-noise* goal-information radius. This module fills only that gap; it does not replace the DPT native constitutive-law forward model.

Fix one qualified finite-dimensional state/parameter chart and one future command:

```math
\begin{aligned}
x&=x_0+Bz,\qquad\|z\|_2\le1,\\
y&=Hx+Ee,\qquad\|e\|_2\le1,\\
G(x)&=G(x_0)+g^\top(x-x_0).
\end{aligned}
```

The entire ellipsoid B must be physically admissible, not just its tangent; H contains *pretarget* measurement rows; E specifies a **joint deterministic** error ellipsoid (not automatically the data covariance); g is the same-law gradient of a smooth future goal. E may be rectangular or rank deficient; B may be rank deficient and physical units stay explicit.

Set A=E^{-1}HB and $`c=B^\top g`$. Then the **global** scalar minimax risk over all estimators, possible observations and admissible states/noise is

```math
\begin{aligned}
R&=\max_{\|z\|\le1,\,\|Az\|\le1}|c^\top z|\\
&=\min_w\bigl(\|c-A^\top w\|_2+\|w\|_2\bigr)\\
&=\biggl[\min_{0\le q\le1}
c^\top\bigl[(1-q)I+qA^\top A\bigr]^{-1}c
\biggr]^{1/2}.
\end{aligned}
```

For a singular endpoint the last expression means its finite interior limit, or the pseudoinverse when c lies in the relevant range. R is expressed in the chosen **goal's units** (V, J etc.). The minimax-optimal linear predictor has unwhitened measurement weights a=E^{-T}w and an absolute offset G(x0)-$`a^\top Hx_0`$.

**Proof capsule.** Opposite admissible states z and -z produce an identical possible observation when $`\|Az\|_2\le1`$, with appropriate opposite errors; their goal gap $`2|c^\top z|`$ yields a lower bound for every estimator. For any whitened linear decoder w, the error is bounded by $`\|c-A^\top w\|`$+$`\|w\|_2`$. Convex support-function duality equates these extrema, establishing linear minimax optimality in this bounded symmetric *linear* model. Dualizing the two squared Euclidean constraints and eliminating the positive common Lagrange-multiplier scale gives the single parameter q. In an SVD basis of A its squared objective is f(q)=sum(c_i^2/(1-q+q s_i^2)), which is convex on the domain where finite. Its derivative admits globally convergent bisection, no SciPy dependency. At minimizing q, $`v=[(1-q)I+qA^\top A]^{-1}c`$, w=qAv. Numerical implementation reports the achieved decoder upper bound and a feasible z-witness lower bound, **floating diagnostics only**, not an outward-rounded interval certificate.

**Exact mathematical prior (not OpenAI Math):** Simon Foucart and Chunyang Liao, *Radius of Information for Two Intersected Centered Hyperellipsoids and Implications in Optimal Recovery from Inaccurate Data*, Journal of Complexity 83 (2024), 101841, DOI https://doi.org/10.1016/j.jco.2024.101841, preprint https://arxiv.org/abs/2401.11112; compare Theorems 1 and 8. These mathematical facts predate our implementation. What may be new in DPT is a source-grounded application combining legal reachable sets, correlated probes and prospective target scoring.

#### Synthetic verification and false claims excluded

Run from dpt_tools/:

    python -m unittest -v test_goal_ellipsoid_recovery.py

For B=I, H=[1,0], E=[0.2], the observed x1-goal has radius 0.2, while the unobserved x2-goal has radius 1. The complete state remains unidentified even though the first goal is robust. For target x1+x2, the radius is 0.2+sqrt(1-0.2^2), exercising an interior bottleneck; elliptical prior B=diag(2,1) has a separate analytic case. With H=I and E=[[0.1,0],[0.08,0.06]], the target x1+x2 radius when B=10I is ||E.T[1,1]||, preserving joint measurement-error geometry. An additional independent measurement reduces or preserves the information radius if the same original uncertainty budget remains available. Tests also cover m=0, shapes, singular E and actual NPZ-to-JSON CLI replay.

These numerical tests are **not** source-native DPT evidence. The code's algorithm_upper, feasible_witness_lower and numerical_gap fields diagnose optimizer arithmetic under its **assumed** linear chart, not the chart's physical validity.

#### Additional primary OpenAI Math reading

Inspected the listed original LaTeX statements and selected proof sections at openai/math main on 2026-10-11. This is targeted source inspection, **not** a full-proof or Lean audit. The new optimal-recovery formula does not come from these papers.

| Family | Original source / inspected locator | What transfers and what does not |
| --- | --- | --- |
| **F132** | [Sensitivity and block sensitivity introduction](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/00-introduction.tex), [Proposition prop:recurrences](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/02-recurrences.tex), [quantitative separation](https://github.com/openai/math/blob/main/preprints/A-superquadratic-separation-between-sensitivity-and-block-sensitivity-September-25-2026/build/sections/03-separation.tex) | **Design analogy**: grouped legal interventions can reveal a response missed by one-coordinate perturbations; existing DPT mixed_interaction_audit is the relevant test. Boolean exponent and sensitivity theorem do **not** transfer to analog SiC. |
| **F129** | [Two-way deterministic state lower bound introduction](https://github.com/openai/math/blob/main/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/introduction.tex), [rank-loss theorem](https://github.com/openai/math/blob/main/preprints/An-exponential-two-way-deterministic-state-lower-bound-for-one-way-liveness-September-25-2026/build/sections/rank.tex) | **PARK**: finite control must distinguish context words in that special *full relation monoid/growing alphabet* model. This does not prove minimum physical memory for nonlinear SiC. Existing DPT command_word_audit/goal_word_quotient cover restricted, relevant meanings. |
| **F119** | [Binary information-contraction theorem](https://github.com/openai/math/blob/main/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/main.tex), [entropy joining proof](https://github.com/openai/math/blob/main/preprints/Sharp-binary-information-contraction-on-the-discrete-cube-September-24-2026/build/sections/canonical.tex) | **REJECT for the present gate**: independent Bernoulli corruption of uniform binary inputs and mutual-information objective are not correlated bounded oscilloscope noise and voltage/work minimax accuracy. Reopen only if a separate calibrated stochastic measurement model becomes authoritative. |

**Research judgment revision:** the strongest new route is not transferring any of those top-line theorems. It is using an existing sharp optimal-recovery result to design a falsifiable DPT legal-observation comparator. Paper counts and thematic analogies must not become evidence of native identifiability.

#### Source-to-controller admission contract

1. **Select one reference.** Never combine 100-V scalar R1, 150-V active CAL/goal and 600-V native finite-command branches as if sharing a single B/H/E/g chart. Freeze model/topology, exact preparation and future command, ports/reference/window, target scorer and nuisance range.
2. **Prove joint eligibility.** Entire x0+B B2 must satisfy source constitutive law, implicit-solver branch/guard, Eth lift, valid state and parameter bounds. Calibrate a physically justified deterministic joint E including skew/gain correlations. A sample covariance without coverage evidence is insufficient.
3. **Take gradients on the same law.** H must use only truly obtainable pretarget information. g comes from same-law tangent/adjoint on the future goal; moving/tied peaks require an event-regularity analysis or a nonsmooth goal bound. Ordinary finite differences at one center are not a whole-domain certificate.
4. **Keep ordinary comparator and cost.** Compare NO_CAL against a genuinely legal active CAL row or already archived source/preparation information with identical prior and target, correctly adjusted joint E and sensor/command costs. Report R in goal units and engineering tolerance; don't rank by parameter sensitivity rank alone.
5. **Hold-out falsification.** If two actually legal histories satisfy the same observed-error budget but their future goal gap exceeds 2R plus independently qualified nonlinear/evaluation allowances, the proposed continuous chart is falsified. Passing finite source members does not prove a global continuous bound.

**First input to request from the local controller:** one actual-law **150-V Pro18C** B/H/E/g packet with units, legal-region identity, full correlated deterministic error budget, goal-gradient check, source-complete ordinary predictor and one predeclared holdout active-CAL query. Compare NO_CAL against CAL while respecting access time. The Pro18C seven-member near-observation work diameter (0.335303 nJ) becomes a consistency challenge **only if** these are the same observation and goal contracts. Pro18B's dynamic failure requires a separate recursive-state/update analysis and is not repaired by this static one-command result.

**Strongest counterexamples.** G(x)=x^2 on [-1,1] centered at 0 has derivative g=0 and therefore zero linearized radius but nonzero true goal variation: a linear chart cannot certify a nonlinear DPT goal without an independent remainder. Correlated measurement error cannot be reinterpreted as unrelated axis-aligned boxes without changing the uncertainty set. A source-complete ordinary native predictor may already satisfy the declared work/peak tolerance without added information; this is a valid NO_NEW_MEASUREMENT outcome.

**Terminal:** Math-only conditional construction and synthetic numerical validation. Do not promote, freeze S09, or claim a native performance improvement until the local scientific owner supplies and scores a legal same-reference prospective packet.


#### Extension: rank-deficient/common-mode deterministic observation uncertainty (2026-10-11)

**Motivation from a deliberately invalid F119 transfer.** The OpenAI Math F119 binary-coordinate optimum requires *independently* corrupted channels. With perfectly correlated sensor noise, a goal-aligned contrast can be exact although neither individual sensor is noiseless. The original E^{-1} implementation silently excludes this physically important regime. The extension allows E in R^{m x p} of any rank (including 0), with a **joint hard error ball** ||e||_2<=1; it does not assume independent sensor errors.

**Reduction and proof.** Start with the same centered prior ||z||<=1, observations H B z+E e, and goal c.T z. Take a full left SVD E=U_r Sigma_r V_r.T and complement U_0. Two opposite states z and -z are observation-indistinguishable exactly when H B z belongs to E(B2), equivalent to the pair of conditions

    C z=0,                        C=U_0.T @ H @ B;
    ||Sigma_r^-1 U_r.T H B z|| <=1.

Choose orthonormal columns Z spanning ker C. Then the information radius reduces without approximation (for **mathematically exact ranks**) to

    R = max_{||v||<=1, ||A v||<=1} |c_red.T v|,
    A=Sigma_r^-1 U_r.T H B Z,  c_red=Z.T c.

It is the same convex two-ellipsoid problem **after** enforcing exact noiseless observations. An optimal full linear decoder a is obtained by (i) solving the dual in noisy U_r directions, (ii) adding U_0 components to match the goal response in row(C), which costs zero measurement error because E.T U_0=0. The code returns the achieved upper ||c-(HB).T a||+||E.T a||, a feasible opposite-state lower, and their floating gap. No pseudo-inverse of the full E is used for inversion on its nullspace.

**Independent analytic fixtures and numerically checkable consequences.**

- H=B=I_2, E=[0.2,0.2].T, target g=(1,-1): observation difference exactly cancels the common factor, R=0, a=(1,-1).
- Same prior/measurement, g=(1,1): common source uncertainty remains, R=0.4.
- Add an *independent* uncertainty factor (0,0.05).T to E: target g=(1,-1) now has R=0.05.
- Make E a two-column rank-one matrix; the same R=0 holds.
- E shape (2,0) represents ideal noiseless recording; full H=I removes all uncertainty for a linear goal.
- Legacy full-rank correlated-noise, elliptical prior, no-observation and independent-measurement fixtures remain in the test suite.

This feature was developed with a failing-test-first record (old model rejected valid E), then corrected the older test that still expected such rejection; 13 focused tests and 350 seeded heterogeneous random matrix diagnostics were executed locally. **GitHub Actions run** [38178623705](https://github.com/Gogoal-L/math/actions/runs/38178623705) after source+test update ran all 128 current branch tests and passed. Conditional mathematical validity and floating arithmetic are separate from a physically qualified SiC instrument.

**Critical numerical/scientific qualification.** This computation branches on floating SVD thresholds. If a tiny *nonzero* unshared noise mode is truncated, it can spuriously label a noisy contrast exact and understate physical risk. Noise covariance alone is neither an absolute error ball nor a certificate that a small singular value is zero. Set and justify signal units, correlation drift, common gain/offset/skew origin, acquisition timing, and a reliable bound on all unshared components. In particular, the ideal R=0 in the synthetic rank-one model is **not** a prediction of 0-V or 0-nJ physical uncertainty in an actual DPT waveform. Nonlinear remainder and legally reachable ellipsoid still require separate certificates.

**Closest original mathematical foundation:** Foucart--Liao (2024) remains the general optimal-recovery prior. This is a structured reduction for singular sensor uncertainty, not a claimed new theorem. The F119/F129/F132 deep proof audit and three-mechanism DPT test are maintained on main at [20261011_F119_F129_F132_proof_level_DPT_bridge.md](../dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md).

---

## Provenance annex: 20261010_goal_tolerance_repair_cover

Complete prior proof and research record, retained with its hypotheses, negative evidence, source references and uncertainty semantics. [Original immutable version](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/dpt_research/20261010_goal_tolerance_repair_cover.md). The original finite-bank interval geometry is distinct from the continuous Euclidean/joint-noise model above.

### Frontier V: finite-bank goal-tolerance repair, source-inspired but independently derived

**Date:** 2026-10-10. **Upstream version:** `openai/math` [`fd4aeeb2`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). **Scientific authority:** independent algebraic result and synthetic executable, not a claim that S09 native dynamics satisfy any new hypothesis. The DPT controller remains owner of the legitimate preparation set, known command conditions, scorer, model identity and acquisition decisions.

#### The sharper question

Existing DPT-R1 results distinguish a source tangent nullspace, fixed-Q one/two-row behavior at different preparation radii, one-Newton versus full/affine goal adequacy, a valid local Eth lift and command-order contrasts. The unresolved practical question is not just *whether* a missing direction exists. It is **which collection of actual affordable pretarget readouts would remove every materially goal-distinct but observation-indistinguishable pair across a declared command family**. No differentiability is required for a finite, possibly nonsmooth bank.

This is a mathematically exact *finite-bank, fixed-candidate-library* question. It does **not** establish a globally minimal physical state, an autonomous update, or an upper bound on the entire reachable preparation family. A known-answer bank contains only the specified same-law, physically legal histories if the controller establishes that fact; the tool does not.

#### Proposition A: interval minimax equals the largest compatible goal-interval diameter

Let `H={h_1,...,h_N}` be a finite set of legal histories in a **single model/source and matched reference**, and let `C` be a finite family of fixed, available future commands or command words. Existing retained observations are `O_i in R^m`; candidate scalar features are `P_ij`, `j=1,...,p`. The true readout of each component may lie in **the independent coordinate interval** `[O_ir-sigmaO_r,O_ir+sigmaO_r]` or `[P_ij-sigmaP_j,P_ij+sigmaP_j]`. Here 'independent coordinate interval' is a Cartesian-product uncertainty set, **not a probability/independence claim**. Per history and command, the true scalar future goal may lie in `[g_ic-eta_ic,g_ic+eta_ic]`. All radii are nonnegative and the same declared goal units apply within each command.

For a fixed nonadaptive feature subset `S`, call `i,j` *compatible* if their retained observation intervals and all chosen feature intervals overlap componentwise. For `i != j`, this is equivalent to

```
all_r abs(O_ir - O_jr) <= 2*sigmaO_r
and all_s_in_S abs(P_is - P_js) <= 2*sigmaP_s.
```

Equality is compatibility (closed intervals touch), **not separation**. All histories are self-compatible. The optimum worst-case deterministic scalar-goal prediction error when the decoder knows the command `c` is exactly

```math
R_c(S)=\max\left\{\max_i\eta_{ic},\quad
\frac12\max_{i<j:\,i\sim_S j}(|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc})\right\},
```

where the second maximum is omitted if no distinct compatible pair exists. The overall command-coordinatewise tolerance requirement is `R_c(S) <= tau_c` for **every** `c`. Each command may use a different decoder, but **the same feature subset** is retained before the target; no future goal is an input. This theorem presumes simultaneous Cartesian worst-case uncertainty across histories and intervals; no stochastic noise law, confidence level, or source correlations are inferred.

**Proof.** Every possible readout `y` determines a set `H_y` of compatible histories. For that `y` and command `c`, all feasible true goals form a union of intervals; the midpoint between its smallest possible value and largest possible value minimizes worst-case absolute error with radius half their span. Across all `y`, any pair of compatible histories has a common readout `y`, giving the lower bound. Conversely the maximal span of any `H_y` is bounded by the largest pairwise upper-endpoint/lower-endpoint difference among its histories, with self intervals included. Taking maxima across `y` gives the formula. A single history with `eta_ic > tau_c` cannot be repaired by *any* more precise measurement of its identity.

**Important quantifier.** This is a minimax over **arbitrary deterministic decoders** on the finite bank, stronger than checking a particular linear or neural decoder fit. It is **not** an achieved error of the current DPT decoder and cannot rescue poor approximation architecture by itself.

#### Proposition B: minimum-cost robust measurement repair is an exact hitting-set problem

Suppose all `eta_ic <= tau_c`. First form the **base-ambiguous and goal-conflicting pair universe**

```math
\begin{aligned}
\mathcal U=\bigl\{\{i,j\}:\
&i<j,\\
&|O_{ir}-O_{jr}|\le2\sigma_r^O\quad(\forall r),\\
&\exists c\in C:\ 
|g_{ic}-g_{jc}|+\eta_{ic}+\eta_{jc}>2\tau_c
\bigr\}.
\end{aligned}
```

Candidate feature `s` resolves the conflicts

```math
E_s=\{\{i,j\}\in\mathcal U:|P_{is}-P_{js}|>2\sigma_s^P\}.
```

Then `R_c(S)<=tau_c` for every command `c` **if and only if** `union_{s in S} E_s = U`. Proof: Proposition A says exactly those conflicting pairs must become incompatible, and a Cartesian coordinate product makes a pair incompatible precisely when at least one selected scalar coordinate is separated. With positive additive declared costs `w_s`, the minimum feasible total cost is the weighted set-cover optimum. When a conflict lies in no `E_s`, the supplied feature library cannot meet the goal contract; output the failing same-law history pair and its command.

For `p<=18` by default, [`goal_repair_cover.py`](../dpt_tools/goal_repair_cover.py) finds the exact minimum-cost subset using branch-and-bound; larger libraries use weighted-greedy and label the minimum cost **unproven**. For M nonempty conflicts, ordinary weighted greedy has the classical harmonic approximation factor `H_M`, conditional on cost additivity, fixed cover sets, and feasibility. This is not an application of F175's special constant-factor expectation-threshold comparison theorem.

##### A hand-checkable obstruction and a relaxation gap

Construct six histories forming three isolated matched base-observation pairs: `(0,1)`, `(2,3)`, `(4,5)`. The members of each pair have fixed future goal values 0 and 4, so each pair is a conflict at `tau=1`. Three candidate features have separation sets

```
A covers pairs 0 and 1;
B covers pairs 1 and 2;
C covers pairs 0 and 2.
```

All three unit-cost integer sensor choices require at least two features, and any two work. A **fractional** relaxation assigning `x_A=x_B=x_C=1/2` satisfies all constraints at cost `3/2`; summing the three pair constraints shows this is the fractional optimum. The integral optimum is 2; **integrality gap 4/3**. F175 does not erase this gap: its setting is a monotone family of subsets, random Bernoulli event-costs `p^|S|`, and a threshold rescaling, not arbitrary acquisition-price hitting set.

**Noise counterexample.** For two candidate readings whose pairwise gaps are both 0.8 and interval radii both 0.5, neither alone nor both together separates the pair in our coordinatewise-box model. A *different* model with a joint Euclidean-radius-0.5 ball would separate them jointly because `sqrt(0.8^2+0.8^2)>1`; the set-cover reduction **does not apply without modification** under Euclidean joint noise. Do not silently reuse the old `goal_ambiguity_audit.py` Euclidean observation-radius formula.

**Sub-picocost numeric counterexample.** A pruning rule with an arbitrary `1e-12` cost tolerance can falsely claim cost optimality for candidate prices on the order of `1e-15`. The tool uses strict positive-price comparisons and reports a *numerical exact search on supplied float costs*, not a symbolic real-arithmetic proof.

#### Source-critical OpenAI Math research: new families, real and failed transfers

The original source manuscripts below are pinned to `fd4aeeb2`. The examined surface is named; no claim of exhaustive PDF page-by-page visual verification or independent proof of the source headline is made. The cited Lean descriptions are *selected statement scopes*, not separate transfer proofs.

| Family and inspected primary sections | Strongest source-grounded contribution | Constructive transfer, strongest obstruction, and decision |
|---|---|---|
| **F175**, [Integral and fractional expectation thresholds](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Integral-and-fractional-expectation-thresholds-are-equivalent-September-23-2026/build/source/sections), inspected all four included section files' theorem/proof mechanisms including multiscale selector and rounding (see `selector.tex` and `rounding.tex`) | For a nonempty proper increasing finite set family, defines integral and fractional **Bernoulli-price expectation thresholds** and shows `q_f <=25*512^4*q`. The rounding constructs a multiscale mass capture and uses a random-color expectation contradiction. [Lean selected scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/175.md). | **TRANSFER AS PROOF DISCIPLINE ONLY.** First define exact cover semantics and price; a fractional surrogate may be cheaper and require honest integrality analysis. Its numeric theorem **does not** give a universal fixed-cost DPT sensor-rounding factor. |
| **F125**, [Single-exponential k-median recovery](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Single-Exponential-Recovery-and-Bounded-Price-Strictness-for-Metric-k-Median-September-24-2026/build/sections), inspected introduction/recovery theorem and stability-dichotomy/final assembly proof | Supplied anchor with accurate *distinct* proxies for all but `O(log N)` comparison clusters allows exact-budget recovery in normalized integral metrics. A dichotomy distinguishes a flat `opt_k` curve from a cardinality sensitivity jump. [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/125.md). | **WATCH, high pilot value.** Inspect whether most reachable history fibers share one low-information decoder and a small *predeclared* exceptional domain needs a different feature. Selecting excluded histories after seeing failure is invalid. Neither metric k-median's `1+2/e` nor its cluster-complexity guarantee transfers to DPT. |
| **F139**, [Subpolynomial query complexity for log-concave sampling](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026/build/sections), inspected main theorem/model, proof overview, Gaussian block-Krylov lower construction | Exact value+gradient oracle, minimizer known, `I<=D2V<=2I`, arbitrary computation between calls: `Q(d)<=C_eps*d^eps` and `Q(d)>=c log d` for fixed total-variation accuracy. The lower bound uses hidden random rotations and a Gaussian statistic. [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/139.md). | **PARK** for immediate DPT. Crucial lesson is *oracle-call count is not total compute, physical data acquisition, or measurement count*. Do not use this headline to claim two native LTspice runs suffice or GPU cost vanishes. |
| **F327**, [Nontrivial Markov type forces superreflexivity](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Nontrivial-Markov-Type-Forces-Superreflexivity-September-23-2026/build/main.tex), inspected stationary/reversible finite-Markov definition and main theorem; [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/327.md) | Under stationary reversible finite-Markov walks, Markov-type bounds control expected powered displacement in a Banach target; the paper characterizes superreflexivity via nontrivial Markov type. | **PARK** until genuinely stochastic stage uncertainty is measured. Deterministic LTspice discretization/branch bias is not an unbiased reversible Markov error. A separate martingale RMS identity may be useful with measured zero-mean/orthogonality conditions, independently of F327's theorem. |
| **F110**, [squared-log randomized k-server](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Squared-logarithmic-randomized-k-server-on-arbitrary-metrics-September-24-2026/build/source/main.tex), inspected model statement and complete manuscript chapter map; [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/110.md) | One policy obtains an online movement-cost guarantee against all *oblivious* request sequences, given a k-server metric and initial configuration. | **PARK**: request servicing/movement cost and online adversary are not equal to adaptive choice of LTspice switching command, whose value is discrimination rather than servicing a metric request. |
| **F331**, [reflexive midpoint / diamond distortion](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Asymptotic-midpoint-uniform-convexity-and-unbounded-diamond-distortion-in-a-reflexive-tree-space-September-27-2026/build/main.tex), inspected statement and formalization scope; [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/331.md) | Reflexive Banach example with asymptotic midpoint uniform convexity but diamond-depth `k` distortion at least `sqrt(1+k/12)`. | **WATCH** as a warning against extrapolating local midpoint or tangent regularity into globally stable multi-word charts. No claim that the actual DPT preparation metric is the constructed Banach metric. |

##### Closest-prior subtraction (not an originality claim about set cover)

- [Healy and Leo (2026), *Which experiments test a model?*](https://doi.org/10.1016/j.jet.2026.106191) explicitly uses pairwise separation and integer set cover to select minimal classification/testing experiments in a deterministic preference-model setting. Our pair-cover reduction is not a novel abstract algorithm or generic combinatorial theorem.
- [Krause, McMahan, Guestrin, Gupta (2008), *Robust Submodular Observation Selection*](https://www.jmlr.org/papers/v9/krause08b.html) studies robust observation choice under specific submodularity assumptions. The present goal-diameter design is not automatically the same objective or a Gaussian/Bayesian information gain.
- [Willems (1986), *From time series to linear system*](https://doi.org/10.1016/0005-1098(86)90066-X) places trajectory families and state equivalence before representation. Even if the finite feature set predicts a designated list of goals, autonomous state updates must satisfy a stronger **future-word closure**. The current tool does not claim behavioral realization.

**Potential DPT residual contribution:** not hitting set itself. Rather: same-law physical reachable history selection, pulse/command-specific true goal-tolerance boundaries, correct interval/numeric/model error accounting, pretarget feature availability and acquisition-versus-retention cost, and prospective discrimination versus strong ordinary/one-Newton. A successful native generalization across fresh histories is needed before treating it as a scientific method result.

#### Adversarial simulated roundtable (public ideas reconstructed; NOT actual statements)

**Question:** Does cheap predictive sufficiency mean low-dimensional physical dynamics, few actual sensors, or a low-cost finite-table decoder?

**Willems lens (behavioral system):** The equivalence relation must persist under future concatenation, or a current-goal code will fail after an unseen command. Response: specify the command language and horizon; distinguish bank goal prediction from right-congruence and autonomous `T_a`.

**Talagrand/F175 lens (covering certificates):** A fractional feasibility certificate is not automatically an implementable integer collection of sensors; check the underlying probabilistic cost. Response: our criterion uses fixed-price hitting set with an observed `4/3` gap in a three-conflict example, not the F175 constant-factor theorem.

**Krause lens (sensor utility):** A small feature count is not the same as minimized measurement cost or robust utility. Response: costs and goal-coordinatewise radii are explicit; *joint correlated noise* and physical sensor qualification remain outside the mathematical oracle.

**Moderator's live crux:** the scientifically decisive information is **which admissible history pairs remain inseparable under a legitimately obtainable pretarget feature**, not the number of parameters in a simulator or how many PDFs were read. An apparent cheap state is meaningless if its features are only posttarget outputs or hidden internal states at deployment.

#### Material candidate portfolio, after hostile pruning

| Hypothesis / move | Observable discriminator | Disposition |
|---|---|---|
| H1. A small pretarget feature set controls goal ambiguity for all currently relevant commands | Construct same-law, source-reachable bank; run minimal cover against fixed tau; recheck on new legal histories | **PURSUE: executable independent candidate** |
| H2. One fixed-Q row fails only on a few physically definable preparation regimes | Compare a domain-qualified exception set selected **before** goal scoring with both ordinary full state and low-Q decoder on same-law examples | **CONDITIONAL pilot**, inspired by F125's few bad clusters but not guaranteed by it |
| H3. Low feature count implies low autonomous state dimension | Compare single-command goals versus same histories after `AB`/`BA` future words and legitimate Eth lift | **REJECT as stated**: can predict immediate goals yet fail future-update closure |
| H4. An LP fractional sensor weighting certifies that many fewer actual sensors suffice | On three conflict pairs, fractional cost=1.5 versus discrete=2 | **REJECT** in generic fixed-cost cover; no transfer of F175 constant loss |
| H5. Stochastic aggregation can improve linear-stage defect budget from sum to RMS | Verify martingale differences and stage covariance rather than infer from numerical tolerance | **PARK** until actual noise process exists |
| H6. Few exact solver calls imply cheap physical measurement | Compare F139 oracle assumptions with actual input/circuit/CPU costs | **REJECT**: exact value-gradient oracle / unbounded between-call work is not LTspice cost |

##### Stronger next questions, not new simulator authorization

1. **Existing-data pilot:** on one *physically legal* bank of 150/600 V histories, construct aligned `[histories x commands]` scalar goal matrix for full, affine and one-Newton under the same declared scoring operator, but do **not** mix rival goal predictions into a single ground-truth bank. Separately construct `O`, the available candidate `P`, measurement uncertainty and per-command tolerance. Does the two-row fixed-Q feature set eliminate conflicts one row misses? What is the actual extra RAW/storage/acquisition cost?
2. **Command extension:** does the winning subset remain sufficient on a predeclared new future command word (including event readout and target normalization)? If not, record the shortest and largest material pair witness; upgrade the library only with legitimate pretarget features.
3. **Continuous-domain check:** check whether finite witness direction agrees with source-null and nonlinear fiber-curvature auditors. A bank positive gives no all-reachable upper bound; a bank failure gives a valid lower bound only when histories themselves are accepted as physically reachable.
4. **Stage update test:** if feature set predicts endpoint goals but fails a stage-right-congruence check, do not call it an autonomous predictive state. Check Sol9 Eth transition with real guard and lift, then estimate added information or resort to direct command-to-goal decoders.

#### Reproducible contract and results (synthetic only)

CLI: `python goal_repair_cover.py matched_history_bank.npz --output repair_report.json`. Required NPZ keys: `observations (N,m)`, `goals (N,K)`, `candidates (N,p)`, `observation_radii (m,)`, `candidate_radii (p,)`, `goal_tolerances (K,)`, `candidate_costs (p,)`; optional `goal_uncertainty (N,K)`, `candidate_names (p,)`, `command_names (K,)`. All numeric inputs finite; radii/tolerances nonnegative and costs strictly positive. `N>=1`, `K>=1`; columns may be zero. With equal goal rows the same bank may support several matched fixed commands. No assumption about normalized relative RMS versus absolute goal units is made by the software.

Outputs include baseline and selected exact finite-bank minimax errors per command, chosen feature indices/labels and price, source conflict count, or an unrepairable-pair witness. `NO_REPAIR_NEEDED`, `INTRINSIC_GOAL_UNCERTAINTY`, `NO_LIBRARY_REPAIR`, `EXACT_MIN_COST_REPAIR`, and `GREEDY_FEASIBLE_NOT_PROVEN_MINIMUM` are separate statuses. An exact cost solver is enabled up to 18 candidate features by default; larger inputs return a feasible weighted-greedy upper bound and the classical `H_M` set-cover factor, not a proven optimal price.

Direct focused test evidence: 14 tests, including 80 random independent weighted-set-cover brute-force checks, 65 general random noise/goal-interval full-subset checks, analytic hand cases, impossible regimes, exact-touching thresholds, Euclidean-versus-box counterexample, sub-picocost guard, and end-to-end NPZ CLI. **These tests are mathematical/synthetic only**. The library doesn't access private S09 data, update frozen predictions or trigger LTspice.

**Exit condition:** deliver to the controller only after input ancestry and pretarget provenance are known; if source history bank cannot be aligned without outcome leakage, classify this as an OPEN data contract, not a model failure. A negative finding can rationally favor direct command-to-goal prediction over adding hidden state.

## 2026-10-17 independent nonlinear goal-fiber enclosure: finite net to continuous source domain (P33)

**Hypotheses and status.** Fix a source reference, legal PREP, the complete available pretarget recorded command, a closed compact metric world set $(\Theta,d)$, one qualified branch/guard and a genuine *joint* sensor-error set $E\subseteq\mathbb R^m$. Let $O:\Theta\to\mathbb R^m$ be the pretarget readout and $G_u:\Theta\to\mathbb R$ the frozen future scalar goal for each predeclared command $u$. Assume **source-validated uniform Lipschitz bounds** $\|O(\theta)-O(\theta')\|\le L_Od(\theta,\theta')$, $|G_u(\theta)-G_u(\theta')|\le L_{G,u}d(\theta,\theta')$ and a genuine $\rho$-net $\{\theta_i\}_{i=1}^N$ **covering the entire** legal $\Theta$ in this same metric, not merely a finite sample bank.

**(P33) Conditional continuous goal interval.** For observed $y$, define $\mathcal C(y)=\{\theta\in\Theta:y-O(\theta)\in E\}$ and $B_\rho(y)=\{i:\mathrm{dist}(y-O(\theta_i),E)\le L_O\rho\}$. When $\mathcal C(y)\ne\varnothing$, the set $B_\rho(y)$ is nonempty and
```math
G_u(\mathcal C(y))\subseteq
[\min_{i\in B_\rho(y)}G_u(\theta_i)-L_{G,u}\rho,\;
 \max_{i\in B_\rho(y)}G_u(\theta_i)+L_{G,u}\rho].
```
Consequently a scalar midpoint decoder based on the full pretarget $y$ has certified worst-case error
```math
R_{u,\rho}(y)=\frac{\max_{B_\rho(y)}G_u(\theta_i)-\min_{B_\rho(y)}G_u(\theta_i)}2+L_{G,u}\rho .
```
For any compatible $\theta$ choose a covered center with $d(\theta,\theta_i)\le\rho$. The **same joint** $e=y-O(\theta)\in E$ then witnesses $\mathrm{dist}(y-O(\theta_i),E)\le\|O(\theta)-O(\theta_i)\|\le L_O\rho$; the goal Lipschitz bound supplies the interval. A certified **stable accept-or-abstain subset** is the set of eligible $y$ for which $R_{u,\rho}(y)\le\tau_u$ for every frozen future $u$. Predictions outside it must be marked INCONCLUSIVE; the error bound is conditional on true $\theta\in\Theta$ and a valid source/observation budget. Multiple scalar midpoints need not correspond to one joint physical future trajectory.

**Sharp negative and ordinary comparison.** For a compact nonempty fiber $\mathcal C(y)$, scalar minimax absolute error over unconstrained scalar decoders is exactly half its goal diameter $\frac12[\sup_{\mathcal C(y)}G_u-\inf_{\mathcal C(y)}G_u]$, achieved at the extremal midpoint. A single pair with goal gap $>2\tau_u$ rules out $\tau_u$-adequacy, provided both worlds are legal and compatible with the **same full recorded transcript**. Yet a finite bank can falsely appear stable: on $\Theta=[0,1]$, $O(\theta)=0$, $G(\theta)=4\theta(1-\theta)$, the bank $\{0,1\}$ has zero goal gap while the continuous fiber diameter is $1$. No finite-bank maximum is a full-source upper absent certified net coverage and the uniform Lipschitz constants. Compare first with a full-source, full-waveform, same-cost ordinary interval decoder: if it already meets $\tau_u$, extra compression or an I3 port has no demonstrated benefit.

**Paper boundary and next DPT source contract.** F329 Theorem 1.1 (PDF p.1), Lemma 2.1 (p.4), Proposition 3.2 (pp.6–9), Corollary 5.1 (p.14) construct a failure of **polar covering-entropy duality**, not a DPT sensor-information theorem. P33 is proved here independently by metric covering and Lipschitz extension. This is particularly relevant to the local controller's 150 V Goal27 fractional-linear five-current *proxy*, which has a scoped bank-wide bound but does not yet certify actual whole-fork nonlinear $G-p(O)$. To transport P33 require the same legal physical source family, PREP/CAL transcript cutoff, branch/guard consistency, validated $\rho$-cover, actual pretarget sensor $O$ and joint $E$, source-wide $L_O,L_G$ with units, readout/clock error and a frozen future signed-work $G_u$. Without all of these the result remains **SIDE_VERIFIED conditional mathematics / OPEN_RESEARCH actual source**. See [finite goal repair tool](../dpt_tools/goal_repair_cover.py), [nonlinear fiber auditor](../dpt_tools/fiber_goal_curvature.py), and [P33 analytic tests](../dpt_tools/test_paper_transfer_falsifiers.py).

## 2026-10-17 sequential pretarget goal information with joint noise and optional stopping (P34)

**Independent DPT set theorem, not Gaussian F140 transfer.** Fix one actual source reference, legally prepared full-information archive $D$ including its entire recorded digital PREP/CAL command and raw sensor samples, a finite frozen bank of unseen future words $w$, and their exact scalar signed terminal-work goals $W_w(h)$ with declared units J and tolerance $\tau_w$. Let $\Omega_0$ be the set of **all source-legal** prepared histories together with one jointly admissible nuisance/measurement trajectory consistent with $D$; new noninvasive *pretarget* sensor/action $j_t$ must be selected from information legitimately available through time $t$, with an explicit acquisition/clock cost and no future-goal data. For observed $y_1,\ldots,y_t$, define the feasible nested sets
```math
\begin{gathered}\Omega_t=\{\omega\in\Omega_0:\exists e\in E,\\\text{producing every }(j_s,y_s),~s\le t\}\end{gathered}
```
We use the same latent error trajectory across time: it is invalid to independently choose a new nuisance realization for each step or to infer a conditional noise bound from a marginal single-shot bound. The physical world is one fixed $\omega^\star$ over a stopped path; for all $t$, $\Omega_{t+1}\subseteq\Omega_t$ (after projecting the augmented source/error coordinates into the same full-history space). For each future word define the scalar minimax radius
```math
r_t(w)=\tfrac12(\sup_{\Omega_t}W_w-\inf_{\Omega_t}W_w),
```
with the midpoint as an exact optimal unconstrained scalar predictor over the feasible set. This formula is a *conditional mathematical equality*, not an executable number when $\Omega_t$ has not been source-certified.

**(P34) Simultaneous validity at data-dependent stopping times.** Suppose **one joint coverage event** $A$ of probability at least $1-\alpha$ (uniformly for each legally prepared true world under the stated stochastic calibration model) guarantees the true joint error trajectory is inside $E$ for every admissible pretarget observation and every time at most the frozen finite horizon $T$. For any predictable sensor choices and any observation-based stopping time $\sigma\le T$, on the *same event* $A$ the true history stays in $\Omega_\sigma$; hence the midpoint errors simultaneously satisfy
```math
|\widehat W_{\sigma,w}-W_w(\omega^\star)|\le r_\sigma(w)\qquad\text{for every frozen word }w.
```
**Proof:** one joint trajectory is feasible at every prefix on $A$; apply interval midpoint geometry at the stopped feasible fiber for each goal. Because $A$ is simultaneous over the whole adaptive transcript, no extra optional-stopping penalty is needed. If only per-time/per-sensor marginal error probabilities are known, the argument fails: the claimed $1-\alpha$ must first be proved for all selected possibilities including stopping/selection dependence. No distribution-free new sample upper bound or measurement optimality is asserted.

**(P34-a) Exact finite-library sensor repair gate.** At a current feasible set $\Omega_t$, a candidate legal pretarget measurement $j$ is guaranteed to reduce the worst-case radius for goal $w$ to $\le\tau_w$ after one further readout **if and only if** every pair of histories and admissible nuisance continuations that can produce the *same* next reading has goal difference $\le2\tau_w$ (for all frozen $w$). Necessity is the two-point minimax lower bound; sufficiency is the midpoint on each readout fiber. The full recorded-data ordinary predictor is the baseline: if the full history/command/raw source-law already meets tolerance, no compressed or extra-sensor advantage follows. When a physical CAL pulse changes the prepared state, its intervention effect must be included in **both** compared futures; only the value of releasing versus withholding the post-CAL readout on an identical executed pulse is pure information gain.

**Correlation counterexample and negative control (synthetic).** Hidden sign $h\in\{-1,+1\}$ and fixed common offset $\eta$ give $y_1=h+\eta$, $y_2=\eta$; both individual sensors under an unknown shared drift can overlap, while the same-shot difference $y_1-y_2=h$ recovers the goal sign exactly. With independently wandering offsets $\eta_1,\eta_2$, this cancellation is not certified. Conversely $\Omega_t$ can shrink under new probes while *every future goal interval remains unchanged*; information about irrelevant hidden coordinates is not a goal-value improvement. P34 uses a genuine **joint** error/event and same underlying prepared world, not new iid Gaussian rows.

**Original-paper scope.** F140-B, *Posterior replicas and conditional information in Gaussian regression*, §Introduction theorem `thm:gaussian-block` and §02 lemma `lem:replica-information` require spherical prior with bounded density, exact iid Gaussian rows and *independent* fresh projections; its conditional mutual information bound cannot be inserted as a DPT sensor lower bound. F140-C, *Localization costs and information growth for exact Gaussian observations*, §02 theorem `ld:thm:main` and the dyadic-entropy regularization lemma account for analyzer-only truth-based nested cells and entire stopping transcripts; those cells are not legal physical readouts. Original selected Lean comparators include theorem-shaped stubs with `sorry` and do not by themselves establish machine-verified claims. P34 is a project-own elementary set-/coverage statement derived independently. To attempt actual S150 use true pretarget sensor times/ports/joint nuisance calibration, source-validated feasible $\Omega_t$, original signed scorer and a future command holdout; report whether the candidate observation provably decreases $\max_w r_t(w)/\tau_w$ per incremental acquisition cost, compared against full-record ordinary. **Status: SIDE_VERIFIED conditional math / OPEN_RESEARCH actual source and noise coverage.**

## 2026-10-17 five-current affine calibration group versus projective goal information (P35)

**Independent exact nuisance-equivalence theorem (mathematical, not actual-source certificate).** Fix a legally prepared same-source S150 family $\Theta$ with a deterministic noise-free five-current observation
```math
m(\theta)=(I_{12},I_{31},I_{42},I_{46},I_{60})^\top,\qquad D(\theta)=I_{60}-I_{12}>0
```
for every eligible world. Assume that each complete five-sample **record** has one arbitrary unknown common positive gain $a>0$ and one arbitrary common offset $b\in\mathbb R$ and that there are **no further constraints or independent calibration data**: $y=a\,m(\theta)+b\boldsymbol1$. Define
```math
q(m)=((I_{31}-I_{12})/D,\ (I_{42}-I_{12})/D,\ (I_{46}-I_{12})/D).
```
Then $`q(y)=q(m)`$ and **two raw five-current records are related by such a positive affine transformation iff they have exactly the same normalized $`q`$**. For sufficiency take $`a=(m'_5-m'_1)/(m_5-m_1)>0`$ and $`b=m'_1-a m_1`$; equality of each $`q`$ component forces every other $`m'_j=a m_j+b`$. Hence $`q`$ labels the full orbits of the nuisance group: it is a **maximal invariant**, while full uncalibrated raw-five-current observations contain no further deterministic information that can distinguish physical worlds within a $`q`$ orbit.

For a frozen scalar future work $G(\theta)$, the compatible set given any raw observation $y$ with arbitrary free affine nuisance is exactly $\{\theta:q(m(\theta))=q(y)\}$. Therefore the exact **all-decoder, worst-case goal minimax radius** is
```math
R_{\rm raw5,free-affine}=R_q
=\tfrac12\sup_{\xi\in q(\Theta)}
\Bigl(\sup_{\theta:q(m(\theta))=\xi}G(\theta)
-\inf_{\theta:q(m(\theta))=\xi}G(\theta)\Bigr)
```
whenever these suprema are finite; the scalar midpoint of each fiber is optimal. Proof: same raw observation is compatible with any two same-$`q`$ worlds via admissible $`a,b`$, so triangle inequality gives the lower bound; the midpoint of $`q(y)`$'s goal range attains it. The theorem is not a Gaussian/noise-induced mutual-information statement and does not require physical L uniquely recoverable. **The role of common gain across the five timestamps is essential**: time-varying gains, per-sensor offsets, mixed instrument chains, or cross-record shared calibration constraints change the observational quotient.

**Falsification / stronger ordinary.** The controller's Goal27 rational *proxy* has a certified exact same-$`q`$ pair with goal gap $`\approx0.687175006510\,`$nJ, implying $`\approx0.343587503255\,`$nJ minimax lower under this proxy and unconstrained shared-affine nuisance. A record with **known absolute gain/offset** or an independently calibrated denominator $`D`$ carries *additional* data and may have a smaller radius; the controller's corresponding proxy results $`\approx0.003780563`$ and $`\approx0.0115878648465\,`$nJ apply to those **different** budgets. If gain is constrained, e.g. $`a\in[0.9,1.1]`$, or noise/filter/clock budgets are nonzero, positive affine group orbits can be partially distinguished and the equality $`R_{\rm raw5,free-affine}=R_q`$ no longer follows without a new joint-compatibility proof. For example $`m'=(3/2)m+(1/10)\boldsymbol1`$ has the same $`q`$ but violates a same-record gain limit $`a\le1.1`$. The local actual nonlinear Goal27 source-wide $`G-p(O)`$ bound remains OPEN; exact equality of **proxy** information does not certify physically achievable sensor CAL or native work.

**Literature scope and next consumer.** F374's $1/3$-Hölder Brenier map result (Theorem 1.1) is under compact quadratic optimal-transport measures, **not** fixed DPT observations; F098's unembeddable doubling subset is infinite-dimensional; F094 permits freely chosen finite-point embeddings. P35 is an independently proven elementary affine quotient with explicit physical source ports/measurement roles, not a transfer of those papers. First audit the actual calibration contract (positive record-level gain, common offset, filter initial state, joint sensor noise, admissible parameter bank and denominator sign) and compare real full CAL+recorded command against projective q on **identical** information and cost, before buying I3 or an absolute-gain measurement. [Exact toy group-orbit tests](../dpt_tools/test_paper_transfer_falsifiers.py). **Status: conditional identity SIDE_VERIFIED, actual S150 full-nonlinear scope OPEN_RESEARCH.**

## 2026-10-17 P36: command-conditioned projective inversion and exact joint-noise radius (new scoped positive)

**Correction to the P35/Goal27 lower witness.** The controller's stored `goal27_projective_bank.json::finite_worst_fiber.corner60` has two exact *five-current same-q* proxy points with signed-goal gap $0.687175006510\,\mathrm{nJ}$. But its first three normalized bank coordinates are respectively $(+1,+1,+1)$ and $(-1,-1,-1)$, radii $0.14\,\mathrm V$ each about source-command center $0.3\,\mathrm V$: the two worlds use different digitally recorded PREP amplitudes (nominally $0.44$ vs $0.16\,\mathrm V$). Therefore the valid $0.343587503255\,\mathrm{nJ}$ **q-only/unrecorded-command proxy lower bound must NEVER be called a same-*complete*-recorded-command indistinguishability lower bound**. It remains correct for the restricted decoder that *discards* the three digital amplitudes. The P35 theorem about the five currents modulo a free affine measurement group remains true **after conditioning the admissible family on the same complete PREP command**; this stronger information condition yields the positive below.

**P36 exact global invertibility in the stored 6-axis proxy (not actual source).** Take the frozen binary64 arrays in local controller `Power Semiconductor/docs/derivations/replay/goal27_projective_bank.json` (2026-10-12, original input receipts preserved there), interpreted as exact rationals. In this proxy only, $m(x)=m_0+Cx$ (A) and $G(x)=G_0+c^\top x$ (J), $x=(a,u)\in[-1,1]^6$, where $C=M\mathrm{diag}(r)$, $c=g\mathrm{diag}(r)$, the **recorded** command $a=(a_1,a_2,a_3)$ comprises the first three normalized PREP voltage amplitudes, and $u=(L,\kappa,b)$ comprises the other three normalized coordinates (external inductance, source parameter, filter bandwidth). The last $b$ belongs to the observation filter, not an extra independent physical 50-state source equation. For any fixed recorded $a$ define $D=m_{60}-m_{12}$, $B=(m_{31}-m_{12},m_{42}-m_{12},m_{46}-m_{12})^\top$ and the **observable** $4\times4$ matrix $H(a)$ by
```math
H(a)\begin{pmatrix}1\\u\end{pmatrix}
=\begin{pmatrix}D\\B\end{pmatrix}
=D\begin{pmatrix}1\\q\end{pmatrix},
\qquad q_i=B_i/D.
```
Its first column is affine in the three recorded $a$; its other three columns are the fixed source-array $C_i-C_{12}$ for $u$. Hence $\det H(a)=d_0+\sum_{j=1}^3d_j a_j$ **exactly** (not a local derivative approximation). The archived binary64 coefficients reconstructed independently with `Fraction(float)` give $d_0\approx-0.012854173656835484\,\mathrm A^4$, slopes $\approx(-3.0007543936912015,-3.2885445898083136,-3.5688887869899952)\times10^{-6}\,\mathrm A^4$. Exact rational support on **all** $a\in[-1,1]^3$ lies within the displayed outward-rounded interval
```math
-0.012864031844606<\det H(a)<-0.012844315469064\quad(\mathrm A^4),
```
and the original full-six-axis proxy has $D_{\min}\approx5.372685848430501\,\mathrm A>0$. Thus $H(a)$ is invertible and the *noise-free* $(a,q)\mapsto u\mapsto G$ is **globally single-valued across the full original bank for every fixed recorded command**. For raw five-current measurements $y=\gamma m+\beta\mathbf1$ with a single unknown record-level $\gamma>0,\beta\in\mathbb R$, form $d(y)=(y_{60}-y_{12},y_{31}-y_{12},y_{42}-y_{12},y_{46}-y_{12})^\top$, $v=H(a)^{-1}d(y)$. Then $v=\gamma(1,u)^\top$, so
```math
\boxed{\widehat u=v_{1:3}/v_0,\qquad
\widehat G=G_0+c_a^\top a+c_u^\top\widehat u}.
```
This uses no absolute gain/offset calibration, additional current channel, or withheld target truth; $a$ was already recorded with the digital PREP. It **exactly recovers proxy goal** in zero measurement noise. Its all-decoder minimax radius conditioned on the same digital PREP and this proxy is **zero**; this does not conflict with the original $0.3435875\,\mathrm{nJ}$ lower for a deliberately *command-blind* decoder.

**P36 measurement-noise positive (2048 exact rational corners, CONDITIONAL_PROXY).** Let the five recorded current samples have one common $\gamma\ge0.9$, arbitrary common offset, and additional individual bounded errors $|e_t|\le\epsilon=1\,\mathrm{mA}$. This is the controller's **hypothetical mathematical sensor scenario**, not an instrument specification. For the same $H(a)$, put $\delta=(e_{60}-e_{12},e_{31}-e_{12},e_{42}-e_{12},e_{46}-e_{12})^\top$, $w=H(a)^{-1}\delta$. The noisy estimate satisfies the **exact correlated formula**
```math
\widehat G-G_{\rm aff}
=\frac{c_u^\top w_{1:3}-(c_u^\top u)w_0}{\gamma+w_0}.
```
This explicitly retains the common anchor noise: independently bounding four differences would lose it. Since only the first column of $H(a)$ changes with $a$, the entries of $\mathrm{adj}H(a)$ and $\det H(a)$ are affine in $a$. For each fixed other coordinate the displayed rational expression is linear-fractional in each $a_j$ and each $e_t$, affine in $u_j$, and its absolute value decreases as $\gamma$ increases when its effective denominator is positive. Thus its continuous-box extrema occur at $(a,u,e/\epsilon)\in\{-1,+1\}^{3+3+5}$, $\gamma=0.9$, **2048 jointly enumerated exact cases**. The same corner/linear-fractional argument certifies the global effective gain floor $\gamma+w_0\ge0.8995834925637281>0$, while the exact worst proxy signed-goal error is
```math
\begin{gathered}\sup|\widehat G-G_{\rm aff}|\\\approx2.9391938011026248404\,\mathrm{nJ}\\<2.939193801103\,\mathrm{nJ}\end{gathered}
```
(an outward strict upper follows from the saved exact rational extremum; this is a **conditional upper and a reachable proxy/noise-corner absolute maximum**, not actual SiC TOTAL_ERROR). Compared with the controller's original frozen *command-blind* $p(q)$ proxy-plus-1mA upper $3.848345919\,\mathrm{nJ}$, the new known-command decoder has a numerically smaller certified proxy bound. This is a stronger algorithm using a field already legally recorded; it **does not prove superiority over the best same-information full-record ordinary**, which can use $a$ and the entire waveform too.

**Strongest ordinary, source bridge and failure gate.** The strongest rival knows the same complete digital command, original full pretarget CAL waveform/RC memory, joint gain/offset/noise and the same frozen future source law; it may exactly match or improve this five-current decoder. Actual nonlinear $G_{\rm actual}-\widehat G(a,m_{\rm actual})$ uniform coverage, joint finite sensor error over the **actual** observation manifold, real $D_{\rm actual}>0$, physical actuation error, all-root/guard qualification, and native/physical calibration remain OPEN. The 2.939 nJ proxy scenario **cannot simply be added** to a nonexistent actual-source gap: its global Lipschitz/corner certificate covers only the stored affine proxy image. Next qualified actual test should use the saved same-source PREP/CAL/target checkpoints and original 100-MHz filter initialization, compute the *command-conditioned* corrected-goal source residual with full recorded $a$, validate the actual denominator and joint noise over a meaningful lawful source domain, and compare its goal range against the identical-input full-CAL ordinary. Falsifier: fixed identical digital $a$, qualified actual source pair within the same complete raw CAL/joint noise with future signed-work gap $>2\tau$, or actual branch/denominator collision. A changed-command pair is **not** such a falsifier.

**Reproducible consumer.** [`projective_command_proxy.py`](../dpt_tools/projective_command_proxy.py) reads the archived proxy coefficient schema or an equivalent 5x6 array, performs exact Fraction determinant/rank/denominator audit, projective inverse and 2048-corner hypothetical sensor check; [regressions](../dpt_tools/test_projective_command_proxy.py) use a minimal attributed snapshot of the accepted coefficient arrays. These tests certify **exact interpreted coefficients and mathematics**, not the coefficient derivation from original source Jacobians. Claim status: SIDE_VERIFIED strict *proxy* theorem and executable scenario; actual S150 source/root, nonlinear sensor and unseen command: OPEN_RESEARCH; no Main acceptance implied.

## 2026-10-17 P37: exact nonlinear-source-to-command-conditioned projective goal defect (strictly correlated bridge)

**Different task than P36 proxy invertibility.** Fix the SAME digital PREP command $a$, full source-law parameters $u=(L,\kappa,b)$ (normalized proxy coordinates, with $b$ in the qualified 100MHz observation-filter family), source time stamps and signed future work scorer for each legal actual nonlinear member. Let the stored affine-model current vector be $m_{\mathrm{aff}}(a,u)$, actual source (not new instrument data) five-current vector be $m_{\mathrm{src}}(a,u)$, and future goals $G_{\mathrm{aff}},G_{\mathrm{src}}$ in J. Define the common-offset-free **four differences**
```math
t(m)=(m_{60}-m_{12},m_{31}-m_{12},m_{42}-m_{12},m_{46}-m_{12})^\top\quad [\mathrm A].
```
Retain the exact stored proxy $H(a)$ from P36, $H(a)(1,u)^\top=t(m_{\mathrm{aff}})$, and define the **single correlated source-output discrepancy**
```math
\begin{gathered}w=H(a)^{-1}[t(m_{\rm src})-t(m_{\rm aff})],\\w=(w_0,w_u)\in\mathbb R^4,\\e_G=G_{\rm src}-G_{\rm aff}\ [\mathrm J]\end{gathered}
```
At every qualified actual member with $1+w_0>0$ and valid physical source/guard/anchor denominator, applying **the same frozen command-conditioned P36 decoder** to its actual source CAL yields exactly
```math
\begin{gathered}G_{\rm src}-\widehat G(a,m_{\rm src})\\=e_G-\frac{c_u^\top(w_u-u w_0)}{1+w_0}\\=\frac{(1+w_0)e_G-c_u^\top(w_u-u w_0)}{1+w_0}\end{gathered}
```
**Proof:** $H(a)^{-1}t(m_{\mathrm{src}})=(1,u)+w$. The homogeneous inverse gives $\widehat u=(u+w_u)/(1+w_0)$; then subtract $\widehat G=G_0+c_a^\top a+c_u^\top\widehat u$ from $G_{\mathrm{src}}=G_0+c_a^\top a+c_u^\top u+e_G$. All variables and residuals of the actual 50-state source belong to the **lawful construction of $m_{\mathrm{src}},G_{\mathrm{src}}$**, but the algebraic identity alone does not certify they exist for every bank member.

**A more economical eventual actual-source certificate (still OPEN).** A source/guard-validated all-parameter outer family $\mathcal B$ and directed whole-expression evaluator need only prove
```math
1+w_0\ge\alpha>0,\qquad
\sup_{\mathcal B}|(1+w_0)e_G-c_u^\top(w_u-u\,w_0)|\le\alpha\,\epsilon ,
```
to ensure $|G_{\mathrm{src}}-\widehat G|\le\epsilon$ J for every covered actual root. This keeps **goal discrepancy and measured CAL discrepancy in one signed scalar numerator**, and can succeed even when separate absolute $|e_G|$ and $\|w\|$ budgets are large. It is a concrete *same-source representation of the S-L6/S-L7 corrected goal*, not an independently solved whole-source bound or a novel optimization duality theorem. Root/guard/nonlinear filter/actuation and sensor errors must be certified **before** the boxed actual inequality is called predictive. For post-gain/offset joint e, replace the true source CAL by the legal joint $y=\gamma m_{\mathrm{src}}+\beta\mathbf 1+e$, retain the shared anchor error inside $t(y)$, and qualify the additional combined quotient error rather than blindly append the P36 proxy-only 2.939 nJ bound.

**Two exact nonphysical mechanisms (independent counterchecks).** Take any legal stored proxy point and let $m_{\mathrm{src}}=\frac54 m_{\mathrm{aff}}+\frac27\mathbf1$ and $G_{\mathrm{src}}=G_{\mathrm{aff}}$. Even though the five currents individually change substantially, $w=(1/4,u/4)$, so $w_u-u\,w_0=0$ and the exact future prediction defect vanishes; this is a *synthetic source-output discrepancy*, **not** evidence that a physical device law is permitted to have arbitrary gain. Alternatively let $m_{\mathrm{src}}=m_{\mathrm{aff}}(a,u+\delta u)$ and $G_{\mathrm{src}}=G_{\mathrm{aff}}(a,u+\delta u)$, so each of goal and CAL changes while their joint numerator cancels exactly. A source with $1+w_0=0$ makes the homogeneous inverse singular even when $\det H(a)\neq0$; positive proxy $D_{\mathrm{aff}}$ does not prevent that actual-source failure. [Executable retrospective known-answer](../dpt_tools/test_projective_command_proxy.py) checks both cancellations and the singular-orientation rejection; [audit-only function](../dpt_tools/projective_command_proxy.py) takes **future actual work as input** and is explicitly NOT a prospective predictor or a leakage-safe fit.

**Scientific priority relative to an ordinary.** P37 shows the exact *single joint scalar* that should be interval-certified from actual source checkpoint outputs before buying high-dimensional separate $L_G/L_O$ bounds. But a full-pretarget-CAL ordinary using the **same digital PREP, 4801-sample source record and same joint sensor law** remains strictly at least as informative as its five-current restriction. Any actual source-bound cost/sensor comparison must give that ordinary the opportunity to use P37's same physics, and must score a frozen heldout signed-work goal under new lawful commands and matched PREP. Failure to bound the P37 numerator with true root coverage returns OPEN_RESEARCH; it is not evidence of an intrinsic complete-observation information lower bound.

## 2026-10-17 P38: exact common-sensor nuisance elimination and full-CAL goal-strip duality

**Distinct from P35, P36/P37 and S-L6/S-L7.** Fix the same legally recorded digital PREP/command, original **complete raw pretarget CAL**, one source-filter initial state and original current channel. Let the **actual nonlinear source** filtered currents be $m_k(\omega)$, one per timestamp $k\in{\cal T}$, and $y_k=\gamma m_k(\omega)+\beta+e_k$ for unknown **one common** positive record gain $\gamma$, one common offset $\beta$, and one whole-record joint noise trajectory $e\in E$. The calibration ranges $\gamma\in[\gamma_-,\gamma_+]$, $\beta\in[\beta_-,\beta_+]$ are declared independently. Define actual $D=m_{60}-m_{12}>0$, $w_k=y_k-y_{12}-(e_k-e_{12})$ and $d=w_{60}$.

**(P38-a) Exact algebraic iff.** There exists an admissible pair of common gain/offset explaining **every** raw recorded current iff some admissible **joint** $e\in E$ satisfies, for all $k\in{\cal T}$,
```math
\begin{gathered}Dw_k=d(m_k-m_{12}),\qquad D>0,\\\gamma_-D\le d\le\gamma_+D,\\\beta_-D\le D(y_{12}-e_{12})-d m_{12}\\\le\beta_+D\end{gathered}
```
**Proof:** subtract the 12 ns anchor, obtaining $w_k=\gamma(m_k-m_{12})$, and multiply by $D$ using $d=\gamma D$. Conversely set $\gamma=d/D$, $\beta=y_{12}-e_{12}-\gamma m_{12}$, which reconstructs **all** sample equations and obeys the declared bounds. This polynomialized identity eliminates free nuisance variables *without discarding the full CAL or dividing by D off the source roots*. The real source pole/guard, time-varying gain, independent channel offsets and unknown noise dependence are separate gates. The proxy's strictly positive $D_{\rm aff}$ is not a true-source lower bound.

**(P38-b) Source-compatible goal strip.** Let ${\cal C}(y)$ contain ALL physically legal PREP/CAL/target source roots compatible with the recorded command and (P38-a) on the SAME joint noise event. Suppose a sound compact **semialgebraic outer** $\widehat{\cal C}(y)=\{v:h_j(v;y)\ge0\}$ covers all actual roots and a polynomial lift $g(v)$ of the frozen future signed terminal work satisfies $|G-g|\le\eta_G$ for every eligible root. If exact or rigorously outward-checked polynomial identities
```math
U-g=\sigma_0+\sum_j\sigma_jh_j,\qquad
g-L=\tau_0+\sum_j\tau_jh_j

```
hold, with all $\sigma_j,\tau_j$ sums of squares, then each actual goal lies in $[L-\eta_G,U+\eta_G]$ J and its *pretarget-defined* midpoint has error at most $(U-L)/2+\eta_G$. The proof is termwise nonnegativity. **No unique source state, root inverse, or point-estimated Hessian is needed**, but the exhaustive real-source outer, nonpolynomial exp/clip/GL32/thermal lift, actual timebase/guard, retained preparation memory and rigorously validated arithmetic may be prohibitively expensive. Under an independently justified Archimedean polynomial module, strict goal positivity can have an SOS representation; this does not promise low degree or finite optimum capture. Do not interpret an SDP failure as physics nonidentifiability.

**Exact sharp two-world toy (not SiC).** Hidden legal $t\in[-1,1]$, identical digital command and full noiseless reading $m=(0,t^2,0,0,1)$ A has $D=1$ A and recorded $y=t^2$. Take constraints $h_1=t^2-y\ge0,h_2=y-t^2\ge0$. Future signed goal $G_+(t)=t^2$ J admits $L=U=y$ because $U-g=h_2$ and $g-L=h_1$, both exact SOS-identity multipliers 1: two hidden states $\pm\sqrt y$ but ZERO goal ambiguity. In contrast future $G_-(t)=t$ J at $y=1/4$ permits $t=\pm1/2$, hence any same-record predictor has worst error $\ge 1/2$ J. The stronger information budget full raw+digital command ordinary gives exactly this minimax bound; compressed q or future-truth oracle cannot be substituted. Source-compatible observation-then-relaxation is necessary: convexifying all $(O,G)$ before conditioning the observed y can introduce spurious goal worlds.

**Original-paper transfer condition:** J.-B. Lasserre, “Global Optimization with Polynomials and the Problem of Moments,” SIAM J. Optim. 11 (2001), 796–817, DOI [10.1137/S1052623400366802](https://doi.org/10.1137/S1052623400366802), Assumption 4.1 p809 / Theorem 4.2 p810, uses compact basic semialgebraic plus Archimedean/moment convergence hypotheses. Neither F329 polar covering entropy, F357 RCD maps, nor the SOS hierarchy proves S150 nonlinear source polynomiality/qualification. The decisive source input is all-branch actual source-root outer, entire raw CAL+joint gain/offset/noise, actual $D>0$, source-to-polynomial validated lift and its work discrepancy, followed by a certified SOS identity and same-information FULL ordinary. Status SIDE_VERIFIED conditional algebra; actual source/domain/metric OPEN; legacy whole-fork beta PARK.

## 2026-10-17 P39: full-record conditional experiment ordering, active-CAL target drift and no-new-hardware observation repair

**New decision theorem beyond the P34 nested-set and P35 five-point quotient.** Condition on the FULL legal, already recorded S150 digital PREP/command/raw CAL/clock/calibration archive $`D`$, and let $`\Theta_D`$ contain all compatible same-source prepared histories together with the qualified *joint* gain/offset/filter/noise laws. For each candidate sensor/acquisition action $`a`$, define the probability law $`P_\theta^a`$ of its **complete** legally adaptive observation/action/stopping transcript. The action may itself alter the prepared state and the future finite-$`\Delta L`$ signed external-work curve $`G_a(\theta,\ell)`$, $`\ell\in I`$. For another action $`b`$, define **uniform** experiment deficiency
```math
\begin{gathered}\delta_D(a\to b)=\inf_{K\text{ independent of hidden }\theta}\\\sup_{\theta\in\Theta_D}\|KP_\theta^a-P_\theta^b\|_{\rm TV},\\\beta_{ab}=\frac1\tau\sup_{\theta,\ell\in I}\\|G_a(\theta,\ell)-G_b(\theta,\ell)|\end{gathered}
```
Here a simulation kernel $K$ may use the **already known** archive $D$, but cannot secretly depend on the unknown physical world. For the bounded goal-curve loss $L_a(\theta,f)=\min\{1,\sup_{\ell\in I}|f(\ell)-G_a(\theta,\ell)|/\tau\}$ and minimax expected risk $V_a=\inf_{\text{transcript decision }f}\sup_{\theta}\mathbb E_\theta^a L_a(\theta,f)$, the independently proved **conditional transfer inequality** is
```math
\boxed{\quad V_a\le V_b+\delta_D(a\to b)+\min(1,\beta_{ab}).\quad}

```
**Proof:** simulate any b-decision from a-transcripts using the single $K$; expectation of a bounded loss changes by at most the uniform total variation gap. For the same numerical output curve, replacing goal $G_b$ by the **physically action-changed** $G_a$ changes clipped loss by at most $\min(1,\beta_{ab})$. Take the worst source world, then optimize decisions and approximating kernels. **Sign of the simulation direction matters:** $\delta(a\to b)=0$ means a's data can simulate b's, so a is at least as useful **only when the target action does not drift**. A posterior- or world-dependent simulation kernel, source family mismatch or Gaussian iid approximation cannot certify uniform risk. If one executes the SAME active CAL pulse and compares revealing versus withholding its readout, $\beta=0$; otherwise an apparent sensor benefit may be the intervention changing the target.

**Continuous finite-domain and purchase gate.** Suppose original same-source PREP/guard and entire $\ell\in I$ have a verified $|\partial_\ell^2G_a(\theta,\ell)|\le M$ for **every** eligible history. On an $\ell$ grid of maximum spacing $h$, the linear interpolation error per history is at most $Mh^2/8$; hence the continuous compatible-goal *half*-diameter is at most the maximum of qualified grid half-diameters plus $Mh^2/8$. This is a conditional constructive continuum bound, not a finite bank maximum. Only consider additional instrument time/hardware if a source-verified same-action full-record ordinary upper $U_{\rm new}\le\tau$ and an independent withheld-information **lower** $L_{\rm old}>U_{\rm new}$ survive true marginal acquisition cost $c_a$; compare a cost threshold such as $(L_{\rm old}-U_{\rm new})/c_a>\lambda$. When $M$ or guard/source control is unavailable, use a separately validated Lipschitz extension or label OPEN; never fill it with empirical r1/r2/r4 movement.

**Zero-hardware full-waveform normalization test.** If the whole pretarget SAME-current-channel raw record has $n$ timestamps sharing one unknown positive gain and offset, no extra noise, and positive anchor $D=m_{60}-m_{12}$, the vector
```math
q_{\rm full}=\bigl((m_t-m_{12})/D\bigr)_{t\ne12,60}
```
is the *maximal invariant of the entire n-sample affine nuisance orbit* (same proof as P35 for five). Five-point $q_3$ is merely a projection of $q_{\rm full}$. **Before buying I3 or calibration**, apply the same original full-CAL legally stored timestamps to the strongest source-law ordinary, since the extra samples have zero **new** hardware cost. For correlated additive errors $y_t=\gamma m_t+\beta+e_t$,
```math
\widehat q_t-q_t=
\frac{e_t+(q_t-1)e_{12}-q_t e_{60}}
{\gamma D+e_{60}-e_{12}} .
```
The original **joint** error support, filter/timebase and a positive denominator lower are essential; common offset cancels, timestamp-specific drift generally does not.

Synthetic two-world control: five fixed anchor currents $(m_{12},m_{31},m_{42},m_{46},m_{60})=(0,2,4,6,10)$ A match *exactly*, while one **already archived** additional current $m_{50}=8$ versus 9 A produces $q_{\rm full,50}=0.8$ versus 0.9. If frozen goals are $\mp(1+\ell)$ nJ, $\ell\in[-0.5,0.5]$, the five-point, command-matched restricted decoder has full-domain radius 1.5 nJ, but the full-record noiseless decoder identifies the two worlds and has radius 0. This is **not** an S150 source-legal pair; if the extra current has its own unqualified offset/drift or the gain collapses, the repair may disappear. In the existing **P36 six-axis affine proxy**, known digital PREP plus three ratios already has zero noise-free radius, so more CAL points cannot strictly improve that zero proxy lower; its practical relevance would be **actual nonlinear source stability or noisy gain**, both still OPEN.

**Primary literature boundary.** Blackwell (1953), “Equivalent Comparisons of Experiments,” Ann. Math. Stat. 24:265–272, DOI 10.1214/aoms/1177729032, and Le Cam (1964), “Sufficiency and Approximate Sufficiency,” Ann. Math. Stat. 35:1419–1455, DOI 10.1214/aoms/1177700372, motivate experiment randomization/deficiency; the original historical full texts were **not independently rederived here**, so (P39) is explicitly proved from the TV definition above. A source-readable modern treatment is Fritz et al., [arXiv:2010.07416](https://arxiv.org/abs/2010.07416), Theorem 5.6/Proposition 5.19 on uniform versus state-dependent randomization; Howard et al., [arXiv:1810.08240](https://arxiv.org/abs/1810.08240), Theorem 1, requires valid nonnegative test-supermartingale assumptions for anytime confidence and does not license correlated biased sensor noise. Neither F140-B/C iid exact Gaussian message bounds nor a nominal 1mA budget are DPT physical information guarantees. **Status SIDE_VERIFIED conditional math; actual action laws/source/continuous finite-$`\Delta L`$ interval and instrument cost OPEN.**

## 2026-10-18 P40: first frozen-P36 replay on seven saved actual S150 source members; sharp postfilter sensor threshold

**Actual source evidence, rigorously limited.** The nonprotected controller-accepted archive Power Semiconductor/pro_runs/20261010_pro18_goal_adequacy_frontier/artifacts/run_C/pro18c_submission/evidence.json (original ZIP SHA256 250aa4ea17514ffdeda3a51d95bedf8e034b181f97bdc254db29ddc36281b9c8) contains source-computed members T00–T06: five filtered CAL currents and source coordinates in records[pro18c_final_same_fiber_observations.json] (JSON lines 13616–13808), plus the future actual signed terminal work in records[pro18c_final_same_fiber_results.json] (lines 13808–14055). These 2026-10-11 accepted source outputs are **already exposed**; their three digitally commanded PREP amplitudes **differ** between members. The new calculation uses the ALREADY FROZEN P36 projective coefficients/decoder; it does not refit, access protected truth, compute a new source/native run or certify all source roots. All stored binary64 literals are independently promoted to exact rational numbers before any operation, which proves *arithmetic identity for those stored numbers*, not physical/numerical-path error of the approximate roots.

**Seven-source numerical replay (not blind or global).** Apply P36 to each published source-current vector with that member's own known PREP amplitudes; evaluate signed predicted work minus the member's published source work. T00 through T06 errors (nJ) are approximately $-0.005577264590,\,-0.002567150216,\,-0.000747960435,\,-0.000139341460,\,-0.000744093746,\,-0.002568657160,\,-0.005601739350$; max absolute error is **0.005601739350126236 nJ** (T06). The same seven records give max absolute old command-blind fixed affine-q work error **0.173302707696352 nJ**, while command-only affine-proxy error is **0.136016350890536 nJ**. These are restricted decoders; the strongest **same-information** baseline uses each full recorded command AND all available raw CAL external traces. The hidden-parameter-known affine goal's max **0.001747198704425135 nJ** discrepancy is a separate information-richer oracle diagnostic, NOT a comparable full-CAL ordinary. Differences in PREP commands disqualify the seven records as a two-world full-record nonidentifiability witness.

**(P40) Sharp one-SAVED-source-point goal robustness under a hypothetical joint sensor box.** Fix that source-solved filtered five-current vector $m$, source future work $G_s$ [J], the same recorded digital command $a$, and frozen P36 proxy $H(a),G_0,c_a,c_u$. Hypothesize one common **postfilter** gain $\gamma\ge\gamma_{\min}>0$, arbitrary common **postfilter** offset, and ONE deterministic joint error vector with components $|e_i|\le\epsilon$ A (no iid or Gaussian claim). Define $t(m)=(m_{60}-m_{12},m_{31}-m_{12},m_{42}-m_{12},m_{46}-m_{12})^\top$, $v=H(a)^{-1}t(m)$, $b_0=G_0+c_a^\top a-G_s$. For every sign vector $s\in\{-1,+1\}^5$, put $z_s=H(a)^{-1}t(s)$ and
```math
\begin{gathered}A=\gamma_{\min}(b_0v_0+c_u^\top v_u),\\C=\gamma_{\min}v_0,\\B_s=b_0z_{s,0}+c_u^\top z_{s,u},\\D_s=z_{s,0}\end{gathered}
```
At minimum gain, the exact signed goal error for the sign-corner perturbation is
```math
E_s(\epsilon)=\frac{A+\epsilon B_s}{C+\epsilon D_s}\quad[\mathrm J],
\qquad C+\epsilon D_s>0 .
```
**Proof of exact box extrema:** with positive projective denominator, the decoder is linear-fractional in each sample error separately; extrema over the *entire continuous five-dimensional error box* occur at one of its 32 joint vertices. Any larger gain rescales the additive-error box to $\epsilon/\gamma\le\epsilon/\gamma_{\min}$, whose feasible error interval is nested inside that for the minimum gain. Thus the exact worst-case absolute goal error on this specified source point and measurement family is $\max_s|E_s(\epsilon)|$ while all denominators remain positive. For $\tau>0$ J, the sharp safe noise radius is obtained **algebraically**, not by sampling, as the first nonnegative crossing over all 32 signs of $A+\epsilon B_s=\pm\tau(C+\epsilon D_s)$ or the strict denominator positivity gate $C+\epsilon D_s=0$; if zero-noise already fails, return zero. This conditional theorem is specific to the fixed P36 decoder and uses **future actual work as input** for retrospective verification; it cannot be called a prospective calibrated predictor.

**First source-connected quantitative consequence.** With the seven archived source outputs, $\gamma_{\min}=0.9$, **hypothetical** ±1mA per filtered current sample and common arbitrary postfilter offset, exactly $7\times32=224$ rational corners yield a worst absolute signed-work error of **2.928364786189582 nJ** (T06, signs $+,-,-,+,+$); all 224 denominator orientations remain positive. Therefore that **particular fixed five-sample decoder** fails a proposed 1nJ worst-case tolerance on the stated seven-source-point-plus-noise scenario, but no all-decoder impossibility or actual instrument noise statement follows. The precisely computed maximal common ε for all seven to have |work error|≤**1nJ** is about **0.340271015366445 mA**, attained at T06 with signs $+,-,-,+,+$ and a goal-lower crossing (not a denominator pole). An independent adversarial read-only replay reproduced the extrema and noise threshold to >10 decimals. Implementation: [posthoc exact archive gate](../dpt_tools/projective_command_proxy.py) known_source_point_noise_gate; [regression with accepted nonprotected saved numeric receipts](../dpt_tools/test_projective_command_proxy.py). Source path, date and SHA above; claim level VERIFIED_FRESH on saved-source-point rational calculations / not actual source-wide.

**Next legal zero-native decision.** The local OBS-E06A operator explicitly distinguishes postfilter bias from prewindow filter-memory response. The real shared 100MHz initialization, clock/gain dependence and **joint noise across the whole 4801-sample CAL** must be qualified: the hypothetical five-component box does not define a real instrument or complete recorded-data noise contract. Run same-information full-CAL ordinary first; it can strictly dominate this five-sample decoder. Uniform actual nonlinear S150 $G-p(O)$ still requires all legal 50-state source roots/guard/GL32/thermal coverage, true $D_{\rm actual}>0$, and a signed CAL/work residual bound. The old whole-fork beta remains PARK. Nothing here is a new future-query blind result or MAIN_ACCEPTED.

## 2026-10-18 P41: a testable nonlinear S150 projective output-injectivity gate, stronger than center rank

**New named actual-source proof obligation.** The proven P36 rank is the exact *stored proxy* $4\times4$ homogeneous $H(a)$ for the three normalized, digitally recorded PREP amplitudes $a$ and three remaining normalized unknowns $u=(L,\kappa,b)\in[-1,1]^3$; $b$ enters the shared RC filter, not the internal physical source. On a **single source-qualified smooth continuous branch** containing every $u$ in the convex cube, define the truly filtered actual anchor-difference map $t_{\rm src}(a,u)=(D,B_1,B_2,B_3)^\top$, using the **same** lawful PREP/50-state source/filter initialization and recorded current channel. Define
```math
\begin{gathered}r=t_{\rm src}-H(a)(1,u)^\top\quad[\mathrm A],\\w=H(a)^{-1}r=(w_0,w_u)\end{gathered}
```
The algebraic factorization is EXACT even for nonlinear source outputs:
```math
t_{\rm src}=(1+w_0)\,H(a)(1,T(u))^\top,\qquad
T(u)=\frac{u+w_u}{1+w_0}.
```
A *second* independently qualified actual denominator $D_{\rm src}>0$ is required; $1+w_0>0$ is **not** equivalent to this physical positive-anchor gate. When both hold, $q_{\rm src}(u)=q_{\rm aff}(T(u))$ and the full-rank P36 homogeneous map maps equal normalized observations to equal $T$.

**(P41) Conditional global source-output recovery, strengthened after adversarial two-world proof.** Assume outward interval source-root/guard/parameter continuation proves on the entire same-command, smooth, convex parameter branch that $`\|r(a,u)\|_\infty\le R`$ A and $`\|D_u r(a,u)\|_\infty\le J`$ A per normalized parameter. The original P36 $`H(a)`$ depends on the **fixed recorded a**, not on $`u`$. Split its exact eight-PREP-corner inverse norm into homogeneous first row and remaining three rows:
```math
k_0=\sup_a\|[H(a)^{-1}]_{0,:}\|_1
=0.208253718136\ldots\ \mathrm{A}^{-1}<0.21\ \mathrm{A}^{-1},
```
```math
\begin{gathered}k_v=\sup_a\max_{i=1,2,3}\|[H(a)^{-1}]_{i,:}\|_1\\=36.0458273992841\ldots\;\mathrm A^{-1}\\<36.1\;\mathrm A^{-1}\end{gathered}
```
The supremum on the WHOLE original recorded-PREP cube occurs among its 8 corners because each signed inverse-row support is a linear-fractional function of $`a`$ with a certified fixed-sign affine denominator. Set $`\rho_0=k_0R`$, $`\rho_v=k_vR`$, $`s_0=k_0J`$, $`s_v=k_vJ`$ and $`M_T=(1+\rho_v)/(1-\rho_0)`$. For $`\rho_0<1`$, all actual homogeneous scales satisfy $`1+w_0>0`$, and $`\|T\|_\infty\le M_T`$. The **exact two-world identity**, which directly bounds globally separated worlds rather than checking merely a Jacobian, is
```math
\begin{gathered}(1+w_0(u))[T(u)-T(v)]\\=(u-v)+[w_v(u)-w_v(v)]\\-T(v)[w_0(u)-w_0(v)]\end{gathered}
```
Hence, by the whole-domain Lipschitz bounds on $w$ from the verified source derivatives,
```math
\boxed{
\|T(u)-T(v)\|_\infty\ge
\frac{1-s_v-M_T s_0}{1+\rho_0}\,\|u-v\|_\infty .
}
```
Therefore a **strictly positive right-hand multiplier** is a sufficient *global* source-output univalence gate. Equivalently the independently qualified source derivative must satisfy
```math
k_0 R<1,\qquad
J<\left[k_v+
\frac{k_0(1+k_v R)}{1-k_0R}
\right]^{-1}.
```
For example, using safe **outward proxy constants** $k_0<0.21,\ k_v<36.1\ \mathrm{A}^{-1}$ and hypothetical **whole-source** $R=0.010$ A, this permits $J<0.02748278711$ A/normalized parameter. The old near-identity Jacobian gate $\|DT-I\|_\infty\le [\rho(1-\rho)+2s]/(1-\rho)^2<1$, $\rho=\max(k_0,k_v)R,\ s=\max(k_0,k_v)J$, is also valid, but can be **strictly weaker** than this source-output two-world gate. A separate conservative $K(3R+2J)<1$ is sufficient, but not economical.

**Explicit correction after independent adversarial review:** An earlier draft incorrectly stated that $2K(R+J)<1$ established only local Jacobian invertibility. Because $w$ is a **single-valued globally Lipschitz function on the convex parameter cube** (a crucial extra hypothesis!), the same two-world identity in fact shows $K(R+2J)<1$ is sufficient for global injection; $2K(R+J)<1$ is still a valid but conservative sufficient rule. A pointwise augmented-Jacobian nonsingularity WITHOUT a joint cross-world derivative/branch-domain bound is insufficient. Never transfer the global conclusion between distinct guard branches or disconnected PREP components without an all-branch pair certificate. Moreover actual $D_{\rm src}>0$ remains a **separate mandatory condition**: even global $T$ injection and $1+w_0>0$ do not rule out a source observation denominator zero.

**Exact practical check and true-source scope.** The new [exact-rational source-Jet gate](../dpt_tools/projective_command_proxy.py) source_deviation_univalence_gate uses these separated inverse-row constants and returns a certified two-world lower Lipschitz multiplier or INCONCLUSIVE; [regressions](../dpt_tools/test_projective_command_proxy.py) show an $R=0.010$ A, $J=0.025$ A case where the older near-identity $\kappa_T\ge1$ fails but the valid global pair-bound succeeds. The historical seven actual numeric source records only show $\max_i\|r(a_i,u_i)\|_\infty\simeq6.6988783\times10^{-5}$ A at seven **different** PREP commands; these finite residuals are NOT upper bounds on the continuous $R$, on $J$, on all 50-state roots or on the physical sensor. For present Goal27, actual filter-state/GL32/thermal source-wide $J$ and true D-positive guard remain OPEN. P36 proxy invertibility and this conditional source theorem do not beat the strongest complete-CAL ordinary by information alone.

**Why local rank is inadequate (analytic fold).** Let the actual-source-like output abstraction on a fixed $a$ be $t_{\rm fake}(u)=H(a)(1,T_{\rm fold}(u))^\top$, with
```math
T_{\rm fold}(u)=\left(\tfrac14e^{u_1/5}\cos(2\pi u_2),
\tfrac14e^{u_1/5}\sin(2\pi u_2),u_3\right).
```
Every $u\in[-1,1]^3$ maps to the original proxy's positive-D domain and $\det DT_{\rm fold}=2\pi(1/5)(e^{u_1/5}/4)^2>0$ **everywhere**, yet $u_2=0$ and $u_2=1$ have the **same five-current positive-affine orbit** under the same recorded digital $a$. If the synthetic future goal is $G_{\rm aff}(a,u)$, the two corresponding goals differ by $|c_{\kappa}|=55.102110\ldots$ nJ, while $q$ is identical. This disproves the inference "nonvanishing determinant everywhere ⇒ globally unique future goal" even with positive denominator; it is **not an actual SiC source or same-4801-point-Full-CAL collision**. The true nonlinear source must have its own interval parameter-Jacobian or stronger Gale–Nikaidō-type hypotheses.

**Original-paper theorem/proof locator.** Gale & Nikaidō, “The Jacobian Matrix and Global Univalence of Mappings,” *Math. Ann.* 159 (1965), 81–93, original author-era paper [scanned PDF](https://fig.if.usp.br/~marchett/fluidos/jacobian-matrix-global-univalence-mapping_gale-nikaido.pdf): Theorem 3 at print pp.85–86 proves an order-separation property by minimal-element induction; Theorem 4 and proof at **print p.86/PDF page 6** prove injectivity **if the full Jacobian is a P-matrix at every point of a rectangular domain**, by sign conjugation and Theorem 3. Print p.82 also gives a counterexample to nonvanishing *leading minors* implying global uniqueness. Here P41 is independently proved by a **uniform near-identity differential bound** and does not claim the actual switched DAE satisfies Gale–Nikaidō, which would require complete source branch/root, smoothness and domain checks.

**Smallest next actual no-native input:** existing original prepared/cal/target source law and finite checkpoints *plus* a **strict interval bound** on filtered five-output anchor residual $r$ and its three-column **full PREP-and-filter-propagated** parameter Jacobian over each declared same-digital-command source/root/guard domain, actual D_src positive with certified filter init, and one joint sensor error set. A single center linearization, 7 saved forward samples, point invertibility, a synthetically PASS Gaussian model or an unvalidated global Hessian does NOT satisfy these obligations. Compare any successful source-output inverse/goal range against the strongest full recorded-CAL ordinary under identical physical information, and exclude or retain actual competing root branches. Actual Goal27 source-wide signed-work certificate **remains OPEN**, old whole-fork beta **PARK**.

## 2026-10-18 P42: two-copy *full raw CAL* source residual bound on the optimal future goal diameter

**Second genuinely different Goal27 positive closure candidate, beyond the P38 single-world SOS goal strip.** Freeze one **complete, identical digital PREP/command record**, all original source/guard/filter states, the entire 4801-point raw CAL record $y$, its true joint temporally persistent sensor error set $E$, and one predeclared unseen signed external work $G$. For a lawful complete S150 world $x$ let $F(x)=0$ include full 126 PREP stages and CAL/target forks with the common prepared endpoint and correct nonlinear 50-state law; $O(x)$ is the full externally recorded pretarget observation, not five $q$ samples. The compatible fiber is $\mathcal C(y)=\{x:F(x)=0,\;x\text{ source/guard legal},\;y-O(x)\in E\}$. The ideal strongest same-information scalar ordinary is its Chebyshev midpoint; its minimax absolute error is $\tfrac12\mathrm{diam}G(\mathcal C(y))$ and cannot be beaten without extra information.

**(P42) Pairwise residual/measurement dual.** Let verified *exhaustive* bounded pair boxes $\mathcal B_j$ cover every ordered compatible root pair $(x_+,x_-)\in\mathcal C(y)^2$, including different legal root branches and noise dependence. For each box preselect a vector $\kappa_j$ of units J/observable-unit (one coefficient per declared full CAL sample, or a rigorously supported reduced projection) and physical row-scaled source residual multipliers $\lambda_{j,+},\lambda_{j,-}$. On all of $\mathcal B_j$ verify with directed arithmetic
```math
\begin{gathered}\Delta G=G(x_+)-G(x_-),\\\Delta O=O(x_+)-O(x_-),\\|\Delta G-\kappa_j^\top\Delta O\\-\lambda_{j,+}^\top F(x_+)\\-\lambda_{j,-}^\top F(x_-)|\le c_j\;[\mathrm J]\end{gathered}
```
Define the **one joint-error-difference** support
```math
s_j=\sup_{d\in E-E}|\kappa_j^\top d|
=\max\{\sigma_{E-E}(\kappa_j),\sigma_{E-E}(-\kappa_j)\}\quad[\mathrm J].
```
At true compatible roots each residual vanishes, and because **the same recorded $y$** is matched by each world, $\Delta O=e_- -e_+\in E-E$, with the actual physical joint error models/initializations used consistently. Hence
```math
\mathrm{diam}G(\mathcal C(y))
\le U:=\max_j(c_j+s_j),\qquad
R_{\rm full}^{\star}(y)\le U/2.
```
A qualified real source pair with exactly the SAME complete PREP command/full CAL joint-error contract and future work gap $L$ independently gives $R_{\rm full}^{\star}(y)\ge L/2$. Thus an enclosing bracket $[L/2,U/2]$ is obtained **without solving the full-state inverse or using a fixed five-q predictor**. The pair-box proof is elementary residual substitution and support functions, NOT strong Lagrange duality: an interval/SOS search returning no useful $U$ is **inconclusive** and does not imply source ambiguity. The pair cover and acceptable source root/guard are the actual hard parts. The dual vector must be legal from the *pretarget archive*, never trained on hidden future outputs.

**Exact nontrivial joint-calibration toy and a wrong-independent-noise falsifier.** A physical-style two-step causal filter has true source residual $F(z)=z^2-1$, two pretarget outputs $O(z)=(z/2,-z/4)$ from a COMMON prepared $z$, and a future signed synthetic goal $G(z)=z^3$. Suppose one persistent shared additive sensor drift $\eta\in[-1,1]$ produces the complete two-sample recording $y=O(z)+(\eta,\eta)$. With $\kappa=(4/3,-4/3)$, the exact signed source identity $G(z)-\kappa^\top O(z)=zF(z)$ holds **for every real z**, and $\kappa^\top(\eta,\eta)=0$ for every legal persistent drift. Taking pair residual multipliers $\lambda_+=z_+,\lambda_-=-z_-$ gives **$c=s=U=0$** even though the hidden source has two legal roots $\pm1$: the full correlated pretarget record uniquely determines the future goal, no hidden-state inversion required. For observed $y=(1/2,-1/4)$, $z=1$ with drift0 is legal, but $z=-1$ would require error $(1,-1/2)$, which is **not one shared drift**; incorrectly replacing the joint noise with independent two-sample boxes $[-1,1]^2$ adds a false compatible goal $-1$ and raises the minimax half-diameter to 1. This is an exact synthetic source/measurement counterexample, NOT actual S150 proof or another P34 stopping-time theorem.

**New original primary and transfer limits.** Schichl & Neumaier, “Interval Analysis on Directed Acyclic Graphs for Global Optimization,” *J. Global Optim.* 33 (2005), 541–562, DOI [10.1007/s10898-005-0937-x](https://doi.org/10.1007/s10898-005-0937-x), original [author PDF](https://arnold-neumaier.at/ms/dag.pdf), §§5,7 especially Proposition 7.1 (author PDF p.14), provides sound DAG interval propagation and affine relaxations for **declared bounded boxes**. It does not prove source root existence/coverage, real DPT GL32/thermal analytic-polynomial lifts, or solver/native correctness. F329 metric-entropy duality failure is a separate theorem and supplies no physical dual gap bound; F357 RCD bi-Lipschitz charts assume geometric measure regularity absent here. Practical first target: use source/guard-exhaustive pair boxes on **FULL** externally recorded CAL (not P36 five points), joint noise subtraction, timebase and common filter init, and original fixed signed target scorer; compare derived $U/2$ against the same-source full-record ordinary and the P40 posthoc decoder floor. Until all legitimate root/guard boxes are certified, **P42 is SIDE_VERIFIED conditional mathematics / actual Goal27 full-CAL future-work range OPEN**, whole-fork beta remains PARK.

## 2026-10-18 P43: shared RC-filter initialization is an additional observability coordinate; a sixth already recorded CAL sample can repair it

**Physical operator issue found by adversarial source reading.** The local controller's canonical observation operator OBS-E06/E06A/E07 (dpt_r1_03_observation_operator.tex, original lines 272–313, source edited 2026-10-17) places a fixed postfilter channel bias **after** causal filtering/sampling, while separately keeping the prewindow/initialization response $r_{\rm pre}$. They are distinct physical/calibration objects. The five-current P36 affine orbit assumes one **postfilter** gain and a single constant postfilter offset. An unknown prefilter bias or a free filter initial condition generally yields the time-varying vector $h_t(b)=\exp[-(t-t_0)/\tau(b)]$ instead of a constant offset; for the 100 MHz source readout $\tau(b)=[2\pi b]^{-1}$. The controller's P36 producer initializes the stored RC recurrence from an inherited source state at CAL entry (goal27_projective_bank.py lines 55–65), but this does not prove an *instrument* initial-state uncertainty is absent or calibrated over the full raw record.

**(P43) Exact local necessary information and minimal legal repair test.** On one source-qualified recorded PREP command $a$, write the observation family
```math
y_t=\gamma m_{{\rm src},t}(a,u,b)+\beta+\xi h_t(b)
```
for three unknown normalized source/filter coordinates $u$ (including bandwidth $b$), common record-level positive gain $\gamma$, postfilter constant offset $\beta$ and one optional unknown **shared** filter transient amplitude $\xi$. This is a *sensor-contract extension*, not an assertion that real S150 has an additional free initial state. Let the frozen five-point map at $\xi=0$ be $f_5(\eta,\xi)$ with $\eta=(u_1,u_2,u_3,\gamma,\beta)\in\mathbb R^5$. If the $5\times5$ Jacobian $J_5=D_\eta f_5(\eta_0,0)$ is nonsingular (as in the exact P36 affine-proxy homogeneity at $\gamma>0,D>0$), the **implicit function theorem** gives a unique local compensating curve $\eta(\xi)$ through the identical five sample readings, with
```math
\eta'(0)=-J_5^{-1}h_5,\qquad
\frac{dG}{d\xi}(0)=D_\eta G\,\eta'(0)+\partial_\xi G .
```
Thus **five raw samples generically do not determine both the old three source unknowns AND an additional free filter-memory coordinate**, even though P36 was globally invertible for the smaller nuisance group. A nonzero goal derivative along this legal nuisance-compensation curve produces *local goal ambiguity for that extended five-sample measurement contract*. This result is not a statement about a full 4801-point CAL: with a sixth already archived pretarget sample the combined $6\times6$ derivative is nonsingular **iff**
```math
\boxed{\quad h_6-j_6 J_5^{-1}h_5\ne0,\quad j_6=D_\eta f_6(\eta_0,0).\quad}
```
This Schur-complement rank test supplies the **minimal one-more-observation local repair**, at zero additional hardware cost *if the sixth calibrated sample already belongs to the legally recorded raw CAL*. In the noisy source case require a verified **gap away from zero relative to joint noise** and all-branch/guard; otherwise extra samples do not establish robust goal resolution. If $b$ changes between worlds, $h_t(b)$ must be differentiated as such; treating $h$ as fixed away from $\xi=0$ is invalid unless the memory pole is independently fixed.

**Numerical control on the exact frozen proxy, NOT actual source/full CAL.** Using the saved five-current coefficient matrix at centered $`a=u=0,\gamma=1`$, and 100 MHz sampled h at (12,31,42,46,60)ns, exact rational algebra for the recorded binary64 proxy coefficients and fixed sampled h gives a valid **separate-fixed-pole** five-sample compensation at $`\xi=0.1`$ A, with all five observed currents exactly identical, common gain about 1.00001106, common offset about $`-5.31\times10^{-5}`$ A and future *proxy* goal gap approximately **0.00942034413 nJ**. When h consistently depends on the shifted unknown b, an independently solved smooth finite-$`\xi=0.1`$ proxy+filter-initial-state equation still achieves numerical five-sample residual below $`9\times10^{-16}`$ A and goal gap about **0.00941956128 nJ**; this latter is a **floating numerical diagnostic, not an interval-certified two-world theorem**. The local derivative criterion at $`\xi=0`$ remains exact conditional mathematics for variable b, because terms proportional to $`\xi D_bh`$ vanish at the base point. No additional source roots, full 4801-point CAL collision, real hardware nuisance permission, or future measured work were established by this synthetic construction.

**Strongest ordinary/next source requirement.** Before buying a new sensor, audit the ORIGINAL full CAL sample count and common filter-initialization receipt; calculate the Schur residual $h_t-j_tJ_5^{-1}h_5$ at several *already recorded* pretarget times from source/observation derivatives with units and one persistent joint gain/offset/noise. A verified nonzero robust residual can distinguish a free RC-init mode and shrink its goal fiber with ZERO new native/hardware; if it is zero for every legitimate extra sample, locate the specific unobserved mode and propose an independently legal reset/dwell calibration, always comparing the entire raw-record same-information ordinary. Original P35/P36 max-invariant claims remain valid under their narrower stated nuisance contracts; real instrument initialization, source guard, actual target signed work and noise legality all remain OPEN.

## 2026-10-18 P44: all-4801-CAL RC-memory annihilator and joint-error candidate exclusion (new)

**Actual operator and domain.** Controller's nonprotected \`docs/derivations/dpt_r1_03_observation_operator.tex\` OBS-E06/E06A/E07 (L272–313) separately retains prewindow filter memory and postfilter offset; archived \`replay/goal27_projective_bank.py\` L55–65 uses one first-order RC recurrence. For one **fixed recorded digital PREP/command**, true 4801-timestamp filtered source trace $m$, unknown common positive record gain $\gamma$, constant postfilter offset $\beta$, optional single shared RC-init amplitude $\xi$, known candidate bandwidth $b>0$, and one *whole-record joint* deterministic noise $e\in E$, the declared observation extension is $y=\gamma m+\beta{\bf1}+\xi h_b+e$, where $h_{b,n}=\exp[-2\pi b(t_n-t_0)]$. The optional free $\xi$ is a **conditional nuisance enlargement**, NOT evidence that actual qualified preparation permits it. It is not a new independent per-time perturbation.

**P44a (exact full-record quotient theorem).** For strict increasing timestamps, define
```math
\begin{gathered}
r_n(v)=v_{n+1}-\alpha_n v_n,\\
\alpha_n=e^{-2\pi b(t_{n+1}-t_n)}.
\end{gathered}
```
For $n=0,\ldots,4798$ put
```math
\begin{gathered}
(L_bv)_n=(1-\alpha_n)r_{n+1}(v)\\
-(1-\alpha_{n+1})r_n(v).
\end{gathered}
```
Then **exactly**, including nonuniform timebase,
```math
\begin{gathered}
\ker L_b=\mathrm{span}\{{\bf1},h_b\},\\
\mathrm{rank}L_b=4799.
\end{gathered}
```
*Proof.* $L_bv=0$ forces $r_n(v)/(1-\alpha_n)$ to equal the same constant for every $n$, hence $v_n=\beta'+\xi' h_{b,n}$; conversely both generating vectors are annihilated. Each $\alpha_n\in(0,1)$, so the kernel generators are linearly independent. Thus if $\beta,\xi$ are unconstrained, at fixed candidate $b$ a complete CAL record is compatible precisely if some legal $\gamma,e$ obey
```math
L_by\in \Gamma L_bm+L_bE.
```
For compact positive gain interval $\Gamma$ and compact convex **joint** $E$, convex separation makes this equivalent to the support inequalities, for every $\kappa\in{\mathbb R}^{4799}$,
```math
\begin{gathered}
\kappa^\top L_by\le \sigma_\Gamma(\kappa^\top L_bm)\\
+\sigma_E(L_b^\top\kappa).
\end{gathered}
```
A single outward strict violation **rejects a candidate source future goal** without a full-history inverse, source-wide denominator $D>0$, five-sample selection or future target label. If $\beta,\xi$ are bounded, physically prepared, or coupled to hidden source state, the quotient is only **necessary**; recover the discarded two coordinates and check their constraints. The candidate $b$ must vary with source world: never set all $b$ to a nominal 100 MHz.

**Full-record local rank and cross-bandwidth pair geometry.** With source coordinates $(L,\kappa,b)$ and gain $\gamma$, let $J_4=[\gamma D_Lm,\gamma D_\kappa m,\gamma D_bm+\xi D_bh_b,m]$. The complete six-parameter observation Jacobian has rank six if and only if $\mathrm{rank}(L_bJ_4)=4$ on one smooth, branch-valid source chart. Both $D_bh_b$ and prepared-source/filter history derivative are mandatory. This is not a global root/guard result. For two worlds with possibly distinct $b_\pm$, choose any exact annihilator $Q$ of $\mathrm{span}\{{\bf1},h_{b_+},h_{b_-}\}$. Under independently free $\beta_\pm,\xi_\pm$, their **same-full-CAL** observation sets intersect if and only if $0\in\Gamma Qm_+-\Gamma Qm_-+Q(E-E)$. Every proposed pair with $|G_+-G_-|>2\tau$ must be excluded **on the same digital command and entire joint noise contract** before claiming an all-decoder $\tau$ goal upper. With constrained initial-state memory, projected intersection is not sufficient to establish a legal pair. The strongest ordinary remains the full-compatible-fiber Chebyshev half diameter, which this test cannot outperform.

**Known-answer, evidence and missing input.** Independent Fraction five-point nonuniform $\alpha=(2/3,3/4,4/5,5/6)$ verifies both kernel generators, rank $3=5-2$, and one shared offset/RC/noise mode; a separate nonuniform 4801-point float check of the analytic invariants has maximum residual $3.28\times10^{-17}$ A. The nonprotected Pro18C evidence.json T00–T06 (L13616–14055) saves only five filtered currents for each **different** digital PREP command; the archived same-fiber NPZ has H/ports/parameters, not seven 4801-point currents. Thus no actual S150 full-CAL rank, same-command collision, goal-radius reduction or actual sensor contract has been numerically certified. Need the original $y[4801],t[4801]$, qualified one-record $\Gamma,E,\beta,\xi$ law, true RC initial receipt and all legal source candidate $m[4801]$/guards before using strict separation. Regression: [original-transfer tests](../dpt_tools/test_paper_transfer_falsifiers.py). Status **SIDE_VERIFIED exact conditional operator / actual whole-source goal OPEN**.

**P45 conditional cross-branch certificate and anchor audit.** On a finite **exhaustively enumerated** disjoint union of compact $C^1$ three-dimensional lawful source/guard charts, if the continuous actual projective map $q=(B_1,B_2,B_3)/D$ has nonzero Jacobian determinant on every chart interior and $D\ne0$, then for any connected open $U$ disjoint from **all** chart and guard/root-birth boundary images, $q:q^{-1}(U)\to U$ is a proper local homeomorphism, hence a finite covering. Its cross-branch preimage count is constant on $U$; a **certified exhaustive seed count exactly one** propagates global injectivity over $U$. This is a project-owned application of Chung-Wu Ho, [*A Note on Proper Maps*](https://doi.org/10.1090/S0002-9939-1975-0370471-3), *Proc. AMS* 51 (1975), 237–241, Lemmas 2–3 (proper local homeomorphism/covering), not a proof that actual S150 meets the hypotheses. Two disjoint identical-output charts with $D=5$ A and $q=u$ have locally positive determinant yet two global sheets: point Jacobian positivity alone is insufficient. Separately, if the **same full-branch residual bound** of P41 includes $D_{\rm src}=D_{\rm aff}+r_D$ with $|r_D|\le R$, then $D_{\rm aff,min}=5.372685848430501$ A and $k_0R<1$, $k_0=0.2082537181359361\ {\rm A}^{-1}$, imply $D_{\rm src}>0.570850813$ A; actual $R$ is **not** known source-wide and any branch not covered remains open. The *measured* positive denominator independently requires $\gamma_{\min}D_{\min}>\sup_{e\in E}(e_{12}-e_{60})$. No 2K(R+J) local-Jacobian shortcut to global injectivity is used.



## 2026-10-18 P46: PREP-linked bounded RC-memory support on the original full 4801-point S150 CAL

**Actual saved observation found; previous seven-point limitation corrected.** Nonprotected Pro18E artifacts/run_E/core/e_saved_cal.npz contains time_s(4927), source state50(4927,50), original H_s(4801) and measurement_V_A(4801,2). Pro18F run_F/pro18f_arrays.npz::original_CAL_measurement_V_A is that SAME archived array (SHA256 d55cca1bf277a245186fd2156d23fef85150c2d0a39360ee621b5f4ad7306e91), not a second independent observation. A read-only replay of the full prepared x36 through the literal piecewise-linear 100-MHz RC, then common gain 1.02 and offset +0.01 A, matches the archived simulated CAL within 5.967e-11 A; the inherited filtered entrance current 0.0004651381474658461 A differs from instantaneous source 0.000492232878120678 A. Retaining that entrance exponent recovers the full filter to 7.4e-15 A, whereas unfiltered raw x36 can differ from archived measured current by 3.556272414 A. **These are one source-valid archived numerical path and synthetic calibrated readout, not seven same-command trajectories, true hardware raw sensor noise, or a whole S150 source-fiber interval.**

**P46 new exact bounded-nuisance candidate rejection, not P44 free-memory annihilation.** For one complete lawful same-recorded-command source path theta, filtered m(theta,b) in R^4801 and h_b(t)=exp[-2pi b(t-t_CAL0)], let one common positive gain gamma in compact Gamma, postfilter constant beta in compact B, **PREP-tied pre-gain CAL initial-state deviation** xi in [l_theta,u_theta], and ONE complete-record joint compact convex noise set E. Every candidate reading is y=gamma*m+beta*1+gamma*xi*h_b+e. Defining zeta=gamma*xi and A_theta=[m,1,h_b], the finite polytope is:
```math
\begin{gathered}
P_\theta=\{(\gamma,\beta,\zeta):
\gamma\in\Gamma,\ \beta\in B,\\
\gamma l_\theta\le\zeta\le\gamma u_\theta\}.
\end{gathered}
```
Because gamma is strictly positive, the transformation is reversible. Thus this **entire 4801-point source candidate** is compatible iff y is in A_theta P_theta + E, and by compact convex separation iff all k in R^4801 satisfy:
```math
\begin{gathered}
k^\top y\le
\max_{v\in\mathrm{Vert}(P_\theta)}
k^\top A_\theta v+\sigma_E(k).
\end{gathered}
```
A single **strict outward violation** rejects that source candidate and any future goal attached to it WITHOUT a preselected five-current denominator or future label. If E is nonconvex, support violation still rejects but passing its convex hull is only necessary. Real PREP physical constraints may further correlate gamma,beta,xi and the source state; dropping them creates a conservative outer but never a false rejection. Where justified, an initial PREP discrepancy is attenuated by exp(-2pi*b*T_PREP), which can make h-direction discrepancies **detectable**, unlike the free-init annihilator P44. Only if every lawful, same-digital-PREP, all-root candidate with goal beyond [L,U] is excluded can this produce a prospective signed-work interval; P46 is not a theorem that such exhaustive candidate certificates currently exist.

**Nontrivial archived CAL zero-native discriminator; hypothetical nuisance budgets.** Assume solely for a mathematical source-point gate that PREP input initial discrepancy <=0.1 A and a qualified 8-ns 100MHz relaxation gives |xi_CAL|<=0.000656142 A, gamma in [1,1.04], beta in [.005,.015] A, and joint E={eta*sin(2pi*25MHz*(H-H0))+d: |eta|<=10 microA, |d_i|<=1e-10 A}. A unit contrast k orthogonal to archived m, ones and this one shared noise mode has k·h=7.604323339 and **support upper** 0.005189099516 A. A synthetic **pretarget-only** +0.002 A*h deviation on the SAME archived record gives k·y~0.015208646209 A, exceeding the cap by 0.010019546693 A and rigorously rejecting that altered candidate under the declared example. The actual archived record gives k·y~-4.69e-10 A, as expected. No target truth is an online input; actual instrument E, other roots/guards and goal-radius reduction remain OPEN. The strongest same-information ordinary is the Chebyshev midpoint of goal values of all source-legal worlds compatible with **both complete original V/I CAL channels**, recorded digital PREP/command and one joint error/filter law; our current-only contrast cannot beat it.

**P47 independent full-CAL branch/adversary caveat.** P45's Ho (1975, Lemmas 2–3 pp238–239) finite-sheet local-homeomorphism certificate needs an exhaustively compact union of all source branches/guards, their CLOSED guard/frontier images, all target continuations, and any extra sensor-memory coordinate. A strict-guard sheet u1>0 entering an open observation region has nonsingular local Jacobian yet changing sheet count when its missing closure boundary is ignored; point-Jacobian nonsingularity and P41 2K(R+J)<1 do NOT imply global injectivity. For a branch j, any full-CAL contrast v·1=0 with v·y greater than sup_(legal branch,gamma,b,xi)[gamma*v·m_j+gamma*xi*v·h_b]+sigma_E(v) is a strict cross-branch exclusion. A synthetic two-root causal RC example can exactly hide c(1-h_b), c=.05 A, by CAL offset -c and postgain initial shift +c over ALL 4801 samples while true source D remains ~5 A, producing two different future goals; this is **NOT actual S150 50D alias** and may cease to be indistinguishable when full analog PREP shares the same calibrated chain. The conditional Pro18C report permits pre-gain ±0.1 A init and gain<=1.1 (postgain init max .11 A), not a free actual physical initial state. Original-paper numbering correction: F325-A *Optimal metric* and *Common positive representation* are Theorems 1.2/1.3 (after Lemma1.1), F325-B fixed-operator theorem is 1.1, and F140-A main theorem is 1.2; their operator/geometry/iid assumptions do not establish any 50-state SiC source claim.


## 2026-10-18 P48: first same-full-digital-command actual two-source CAL candidate separation

**Two independent nonprotected source paths (NOT two independent sensor experiments).** The original Pro18E run_E/core/e_saved_cal.npz (SHA256 baafdd8cb489adb186677658c4a8031130cc53a9a1854c4997211d437daf8b3e) has L=4.30 nH, kappa=1.007, 4927 t, 4927x50 states, H4801 and measured full 4801x2 CAL. Pro19A pro_runs/20261014_pro19_physical_recovery_response_frontier/artifacts/run_A/pro19a_source_path.npz (SHA256 98f83174aef3345d81e0c500789ae59c16330874c045cfd85639d6da685c61e1) has L=4.55 nH, kappa=1.007, *own* PREP126, shared public initial50, PREP+CAL4800 accepted finite solver steps. Source receipt L2–15 and Pro18E source_identity_json both pin ORIGINAL actual_law.py SHA256 51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d. All 4927 timestamps, full digital command vector, and H4801 are **bitwise equal** (command SHA256 260bd5b3480ce9b32151348631a78e75564a720cb19a88a24d725374491b6bc1). First full 50D state equals; later states differ under independently lawful PREP. Ports are V=x0-x1 [V], I=x36 [A], Pro18E voltage sensor 0.995*V+0.2 V and causal PL 100MHz current sensor 1.02*I_filtered+0.01 A with PREP-inherited filter state; Pro19A receipt independently validates the raw source 50D identities.

On the same H4801, re-filtering Pro19A entire time history and applying those nominal sensor coefficients gives *max point differences* from Pro18E uploaded y_D: 0.39269836 V (V channel), 0.06114388 A (I). These are one pair of saved solver paths, not a robust all-root interval, and source numerical error/claimed instrument tolerance are not yet independently bounded. The actual recorded sample denominator remains positive: Pro18E measured I60-I12=5.56039360713 A; the Pro19A 100MHz source-filtered I60-I12=5.49596836350 A. They **do not** establish D_actual>0 on all parameters, root branches, joint noise or across bandwidth.

**P48 exact three-voltage necessary joint-error gate stronger than pointwise nominal calibration.** At the SAME recorded CAL times 31.0000, 51.8375 and 47.5125 ns (H indices 2480,4147,3801), let m=(136.7755303684663, -1.74323589650744, 7.914605249728017) V be the archived Pro19A *raw source* voltage, and y=(136.63553408431386, -1.1418213588596062, 7.700426513248537) V the original uploaded Pro18E *measured* voltage. For an unknown arbitrary COMMON affine voltage readout y=gamma_V*m+beta_V*1+e on these times, define w=(m2-m3,m3-m1,m1-m2), scaled so ||w||1=1. Exactly, w dot m=0 and w dot 1=0. Thus every candidate and any **temporally correlated** voltage error e with ||e||infty<=epsilon_V must satisfy:
```math
\begin{gathered}
|w^\top y|\le\epsilon_V,\qquad
w^\top{\bf1}=w^\top m=0,\quad\|w\|_1=1,\\
|w^\top y_D|=0.3819502187980276\ {\rm V}.
\end{gathered}
```
Independent Python Fraction.from_float on all six archived float readings gives that 0.381950218798 V contrast. **If independently licensed total error epsilon_V < 0.381950218798 V at those samples (including interpolation/source and instrument), this specific legitimate same-command L=4.55 nH numerical source candidate is strictly impossible**, irrespective of common gain, offset, *current-channel* RC initial state or current joint noise. This strict exclusion requires only three existing full-record voltages and is available to the strongest full-record ordinary, not a five-current decoder achievement. Example hypothetical epsilon_V=0.1 V gives margin 0.281950218798 V, explicitly NOT an instrument calibration. If epsilon_V is larger, or voltage skew/unknown transfer shape is independently legal, the gate returns INCONCLUSIVE, not compatible. [Reusable three-sample API](../dpt_tools/measurement_factor_audit.py) takes arrays, indices, epsilon_V and checks exact archived-binary64 signed contrast; [independent finite regressions](../dpt_tools/test_paper_transfer_falsifiers.py). No actual future-work labels enter this test.

**Stronger archived full-record ordinary comparison (independent worker verification).** A 4801-sample Chebyshev minimax fit over *all possible common affine voltage gain/offset* finds a primal floating maximum residual ~0.38362466164383546 V, and an independent **exact-binary64 dual** three-time contrast proves **necessary epsilon_V >=0.383624661643811894110279... V**, with a primal–dual floating gap <3e-14 V. The sharper witness selects H indices (2614,3800,4147), relative times (32.675,47.5,51.8375) ns. The uncalibrated Pro19A raw V samples are (133.23152198984246,7.992853605366054,-1.74323589650744) V and uploaded original measured V=(133.1570827108408,7.778267680238221,-1.1418213588596062) V. Exact normalized contrast w=(+.03606633438109731,-.5,+.4639336656189027) satisfies w·1=w·m=0, ||w||1=1, and |w·y|=0.3836246616438119 V. This **improves the initial sparse necessary exclusion by 0.0016744428458 V** and is equally available to the strongest full-record ordinary. The exact dual is a rigorous stored-value **necessary** bound; the float primal is a near-matching diagnostic, not a certified global optimum over unknown source roots. [Same generic witness implementation](../dpt_tools/measurement_factor_audit.py), [numeric regression](../dpt_tools/test_paper_transfer_falsifiers.py).

**Separate bandwidth-uniform current-channel source-point gate (conditional).** The same Pro19A archived PL source current and Pro18E y_D admit a late-time dual contrast supported at H indices 4039 and 4414; its signed 100-MHz source-point margin under one explicitly **hypothetical** jointly shared sinusoidal V/I nuisance and residual boxes is +4.004354121805 weighted A. Exact PL convolution differentiates with respect to bandwidth b_MHz as 2 pi 10^6 integral (t-s) exp[-2 pi 10^6 b(t-s)] I'(s) ds. Bounding the complete saved source PL slopes and the 10-ns exponential tail gives a bandwidth sensitivity <3.572009064 weighted A/MHz on b in [99,101] MHz; prepared filter-initial homogeneous leakage at these late samples is <8e-16 weighted A. Therefore the strict candidate separation has **minimum positive margin >0.43234 weighted A across that entire 2-MHz band** under the *specified hypothetical* joint E, gain [.95,1.05], offset bounds, and PREP initial ±0.1 A. This is a continuous-band analytic gate beyond sampling a few b values, but NOT a calibrated 90–110MHz instrument guarantee, not a whole source-parameter/root cover, and does not prove an independent improvement over the stronger available full-record voltage witness.

**Important competing mechanisms and inference ceiling.** Relative to the *nominal known* voltage gain/offset the max difference 0.392698 V is a pointwise rejection only with a licensed error bound; P48 deliberately tolerates arbitrary common affine calibration. For the same Pro19A candidate, treating the complete current chain with unknown gain/offset/one nominal 100MHz entry-ξ leaves an L2-projected witness requiring at least ~0.0320 A per-sample uniform noise, but it is not bandwidth-uniform and can be weaker or stronger under real E. To prove a **full S150 goal interval**, EVERY incompatible-G source trajectory/root/guard and every bandwidth/joint-nuisance variation must be excluded; we have only eliminated one archived candidate under a stated error cap. The source-compatible goal diameter reduction relative to the baseline remains **not established**. Pro18E's archived gamma∈[.5,2] charge-constitutive family with bitwise-equal generated y_E is an alternative *law above 205 V*, not the same single frozen original Rev6 source; uploaded y_D differs generated y_E by max (1.68035e-8 V,6.08058e-11 A), so y_D membership additionally requires that **whole correlated discrepancy vector** belongs to E. Its 10-microsecond, L=7 nH, future-turnoff recorded 4.778827979nJ pair is prior Pro18E work, not the Goal27 84ns source goal, nor a new claim here. Pro19A and the distinct original saved Pro18C 84ns target have archived G12 control voltages below 205 V; no evidence transfers the deep-charge alternative's future gap to that frozen target. Strongest ordinary must consume both original 4801 CAL V/I, same digital PREP, any legally recorded analog PREP, one persistent gain/offset/RC/clock/noise law and all root/guard continuations, with the identical signed scorer.


## 2026-10-18 P49: clock-aware full-CAL necessary gate, positive denominator, and source-recoverable load-current memory

**Full-record P48 with a single common clock shift is not the same test.** P48's exact voltage three-index witness has k^T 1=k^T m(t)=0 only at the *original aligned times*. If the candidate voltage calibration is y_i=gamma m(t_i+delta)+beta+e_i and |delta|<=tau_clock with |gamma|<=gamma_max and **source-qualified** |m'(s)|<=M_i over the entire shifted interval, any candidate must satisfy, in volts,
```math
\|e\|_\infty\ge
\max\{0,\,|k^T y|-
\gamma_{\max}\tau_{\rm clock}
\sum_i |k_i|M_i\},\quad \|k\|_1=1 .
```
Proof: subtract the common affine baseline, use the mean-value bound pointwise and dual support. This is a rigorous **conditional single-candidate exclusion threshold**, not a 4801 full-parameter optimization or qualification of a real clock spec. Counterexample: candidate m(t)=t^2 at t=(0,1,2), common delta=.01, no noise, k=(-3,4,-1)/8 nulls 1 and m(t) but k^T m(t+.01)=-.005. Thus one MUST include source slope/clock bounds before importing P48's >=.383624661644 V fixed-clock contrast to a clock-uncertain joint E. If gamma or clock shift is unbounded, this fixed witness has no finite noise exclusion. The strongest full-record ordinary is free to optimize jointly over ONE shared delta/gain/offset, not three unrelated sample shifts.

**Actual archived small-clock instance for the original P48 candidate.** Pro19A source full saved PL voltage, observed Pro18E y_D, three active indices (2614,3800,4147), exact affine w≈(+.03606633438,−.5,+.46393366562) have |w·y_D|=.383624661643812 V. On EACH ±1 ps vicinity of its three actual source times, maximum stored PL segment slopes are at most respectively (2.362835,6.289874,3.699179) V/ns; direct full source-time binary64 differences support a conservative weighted slope sum <4.947 V/ns. Therefore for a **single common** unknown shift |delta|<=1 ps, common positive voltage gain ≤1.1 and ANY correlated voltage noise vector with per-sample |e|<=epsilonV, this named saved candidate necessarily satisfies epsilonV >=.383624661643812 V − (1.1*4.947 V/ns)*|delta|. At the full declared 1 ps skew this still requires **epsilonV >.37818 V**. This is a new archived-source local skew-robust exclusion threshold for one candidate; 1 ps and gain bound are **hypothetical** and producer/time-interpolation error are not calibrated. DO NOT extrapolate local slopes to a 50 ps shift or an unknown transfer/timebase; a separate source interval bound would be needed.

**Point-independent filtered denominator sign under ONE shared PREP-tied RC model.** Define D_y=y_I(60ns)-y_I(12ns) on the entire supplied Pro18E CAL; its archived measured value is +5.56039360713 A. For every compatible source root/path with a constant positive common gamma in [0.9,1.1], one beta and a causal filtered source m_b plus a single PREP-bounded entry xi_b,
```math
D_m=\frac{D_y-(e_{60}-e_{12})}{\gamma}
+\xi_b(h_b(12)-h_b(60)),\quad
h_b(t)=e^{-2\pi b t}.
```
For the explicitly **hypothetical, not calibrated** sensor contract b in [90,110] MHz, |e_t|<=.001A at both times, and |xi_b|<=.1exp(-2*pi*b*8ns)A, its worst-case signed lower bound is >5.05308 A. This excludes a zero/negative **filtered-source denominator** in ANY world compatible with that joint observation equation and budget; it does not prove the true unfiltered source P41 D_actual>0 or global P41 injectivity across future branches. The bound is prospective and depends on no future labels; if true E exceeds that contract, recheck the exact inequality rather than claiming unconditional positivity.

**Source-input-recoverable load-coil memory: a new physically relevant reduction.** On any legal fixed-L own-PREP branch where raw port V_ext(t)=v_D-v_sl and I_ext=i_s plus common initial load current j0 are available, the exact source BE coil rows imply
```math
\begin{gathered}
j_n=j_0+\frac{L_s}{L_D}(i_n-i_0)
+\frac1{L_D}\sum_{k=1}^n h_k(V_k-150)\\
+\frac1{L_D}\sum_{k=1}^n h_k(r_{37,k}-r_{36,k}).
\end{gathered}
```
Thus unknown load-coil HISTORY j_n is not an independent arbitrary hidden coordinate once source-L, common j0, raw V/I and coil residuals are qualified. A conditional uniform readout/error bound is |j_n-jhat_n|<=eps_j0+(T eps_V+2Ls eps_I+sum h(eps36+eps37))/LD [A]. This is a **goal-relevant physical information-repair path**: it replaces an unconstrained load-current trajectory in D7/P42 by one external-ports-derived trajectory plus a correlated error operator. It does NOT recover the other 49 coordinates from filtered-current CAL alone; deconvolution of causal 100MHz current with unknown initial, bandwidth and joint noise remains required. In one separate Pro18D legal own-PREP/continuous future command pair, archived 4 source variants verify the exact j reconstruction to ~2e−14 A, with residual absolute cumulative budget <1.4e−12 A (original acceptance/pro18d_local_check.npz SHA256 661462ce324f29c6b2b53393281e29ac12404e4249e4f07afa66551fe2135f84). The D2 H561 future and L7nH differ from original Goal27 H841 and bank; do not promote its PREP-only same-information lower bound to original full-CAL identification.

**Remaining high-value test:** obtain an actually licensed single joint PREP/CAL voltage/current/error/timebase contract and an all-root source-guard outer; evaluate the same residual/clock/RC support for every bad-future-work source candidate, with the strong ordinary using the full 4801x2 record. The minimum source information to repair one missing memory is the common j0 or an external load-current measurement plus its absolute calibration, not the future goal label.


## 2026-10-18 P50: actual SAME-COMMAND joint V/I gain from ONE correlated nuisance, and femtosecond clock falsifier

**An additional independently lawful source path, with an expanded-model warning.** Original Pro18E run_E/core/e_saved_cal.npz SHA256 baafdd8cb489adb186677658c4a8031130cc53a9a1854c4997211d437daf8b3e uses original load100microH, L4.3nH and recorded 4927 digital command/time (CAL H4801). Nonprotected Pro19B pro_runs/20261014_pro19_physical_recovery_response_frontier/artifacts/run_B/pro19b_arrays/load43_Full_r1.npz SHA256 d1029363e05b930ea2304e02b69fbd422c7ff3e13fefc71969bdab842a03a447 changes fixed load100 to 140microH, retains ORIGINAL source-law SHA 51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d, initial50, identical 4927 recorded digital command, time, and CAL H, and independent own PREP126. Its original synthetic readout current is PL first-order 100MHz across the WHOLE shared-prefix time before H4801 sampling; voltage x0-x1 is unfiltered. This is a **real saved 50D source-law family with a changed load**, but outside the original fixed-load Goal27 continuous L/kappa/b parameter class. Never call its goal separation the original Goal27 full-fiber radius.

**ONE cross-channel correlated error vector is different from two independent sensor errors.** For a candidate pair of archived source V and filtered I with common t, allow independent channel gains gammaV,gammaI in [.90,1.10], constant offsets betaV in ±.5V and betaI in ±.05A, one source-PREP-tied RC-entry mode xi with bound ±.1A at PREP start, b in [90,110]MHz, and a single shared eta in [-1,1] acting on both channels with functions (0.02 V sin(2pi*25MHz*t), 0.002 A sin(2pi*25MHz*t)). Add local residual boxes (0.004 epsilon V,0.0045 epsilon A). For a stacked dual k=(kV,kI), the correlated nuisance support is
```math
\begin{gathered}
\sigma_{\rm one\ }\eta(k)=
\left|\,0.02{\rm V}\,k_V^\top\phi
+0.002{\rm A}\,k_I^\top\phi\,\right|,\\
\sigma_{\rm two\ }\eta(k)=
\left|0.02{\rm V}\,k_V^\top\phi\right|
+\left|0.002{\rm A}\,k_I^\top\phi\right|.
\end{gathered}
```
The same full-record ordinary can exploit this exact cancellation. A worker independently solved the full 4801-point affine source/nuisance Chebyshev linear program for the ACTUAL saved Pro19B load140microH candidate: fixed-clock V-only critical noise scale epsilon≈1.012847224, I-only with variable b critical≈1.010685807, but the common-eta BOTH-channel critical scale≈1.021228469 at b≈99.99163MHz. Numerical LP-dual certificates on 87 bandwidth subintervals covering [90,110]MHz plus conservative analytical PL derivative/tail allowance gave a conditional **numeric lower >1.02009**, not an outward floating-point enclosure; do not call this a source-wide proof. At a declared hypothetical epsilon=1.015 the candidate survives either channel alone but is rejected jointly under EXACT common clock. The dual's shared sinusoidal V/I terms cancel (~0.06466195 in each opposing channel); allowing INDEPENDENT etaV,etaI reintroduces ~0.12932391 support and removes the joint exclusion. This negative control demonstrates genuine cross-channel information caused by shared nuisance, not an artificially weakened ordinary.

**Essential source-level falsifier: shared clock warping eliminates the putative advantage.** A single permitted (if instrument contract allows it) deterministic smooth timebase deviation delta_t(t)=+8 femtoseconds * sin(pi*(t-H0)/(Hend-H0)) with zero endpoints, applied to the full candidate source voltage and current along the SAME warped H, admits a joint nuisance fit at b≈99.992MHz with epsilon≈1.0127413 <1.015 (worker complete-source cached PL fit). Therefore the fixed-clock exclusion at epsilon=1.015 **does not survive even this 8-fs timebase freedom**; 8-fs is a counterexample to silently assuming exact H, not an assertion that a real instrument has such warp. A conservative, NOT directed, slope-based sufficient clock restriction reported by the source archive audit is <0.5065 femtoseconds for the entire b90–110MHz conditional exclusion. No actual clock calibration or joint instrument E has been provided. The prior P48 voltage-only L4.55nH candidate exclusion and its separately computed ±1ps local clock threshold concern DIFFERENT source candidate/nuisance geometry and cannot be substituted.

**Implication.** Source-command equality and full-record ordinary are necessary controls, but source law alone does not make an instrument's shared-clock/error support known. This actual-source numerics demonstrates that a two-channel joint E CAN reject a candidate when single channels cannot, **and** that this exclusion can vanish under a microscopic physically unconstrained timebase. Neither finding shrinks the original S150 fixed-load Goal27 future-work interval. To promote it, require independent qualified bounds on clock warp, source/discretization error, ONE correlated error structure, and an all-root/future-goal outer, rather than a synthetic threshold.


## 2026-10-18 P51: same original full digital command, legal fixed-load L4.85 source two-resolution exclusion

**NEW archived candidate and mathematical dual, distinct from P48 L4.55 and P50 changed-load law.** Nonprotected Pro19B run_B/pro19b_arrays/L485_Full_r1.npz SHA256 3472e6824c4553a29000a268f30500dd365405d0a0dd68c4575d34d4c8ecf67a and L485_Full_r2.npz SHA256 06f41dcd9751866823d7c23e5e47cd4d282104de35808071d496bd322fc72d74, from frozen pro19b_prediction_contract.json lines15–20,88–104, are lawful static L4.85nH with OWN PREP (126 stages in r1,252 in r2), fixed original load100microH/Rg7.5ohm/kappa1.007 and same initial 50D. Source actual_law.py SHA256 51b78f729393d29745f59ca150adfef69e1847bf26a8853c6cef3d6be9e2083d. Coarse r1 source t4927 and exact recorded digital PREP+CAL command match Pro18E E/core/e_saved_cal.npz; fine r2 source t9853 even subsamples match r1; both H4801 are identical. Measurement y_D is the full synthetic Pro18E externally exposed 4801×2 after original 100MHz PREP-initialized PL-current filter and gain/offset, not hardware metrology. Importantly, **L4.85nH is outside the original frozen Goal27 L∈[4.02,4.58]nH family**; this candidate cannot define its Goal27 diameter.

**A novel exact 4-time two-resolution affine-quotient witness.** Let v1(H),v2(H) be the two saved unfiltered-voltage H4801 arrays and y(H)=the original measured voltage. At zero-based indices i=(2673,3827,4176,4177), H relative times (33.4125,47.8375,52.2000,52.2125) ns, compute the exact rational null vector w (3×4 cofactor minors) of the rows 1,v1,v2 and scale to ||w||1=1. Its stored-binary64 real-lift coefficients are approximately (+.027022410622198414,−.5,+.40373255399355723,+.06924503538424438). Fraction arithmetic independently verifies EXACTLY w·1=w·v1=w·v2=0 and
```math
|w^\top y| =
0.83206732713215963960950822947\ {\rm V}.
```
Therefore ANY candidate voltage in the AFFINE SPAN {a v1+b v2+c} with completely unknown common constant a,b,c requires ||eV||infinity ≥0.8320673271321596V at the exact H timebase, irrespective of the current-channel RC/bandwidth. The all-4801 primal Chebyshev residual≈0.8320673271321033V agrees within 6e−14V, floating not a certified optimizer. This is a two-resolution **numerical span** exclusion, NOT an enclosure of all continuous L near4.85 or of true-source numerical error; allowing arbitrary affine mixtures over two separate discretization grids is only a nuisance-model stress test.

**Actual archived common CLOCK effect is bounded on a calibrated local interval.** If one further restricts to ONE positive voltage gain gamma≤1.1 multiplying a CONVEX mixture λv1+(1−λ)v2, 0≤λ≤1, plus common offset and one common H shift |delta|≤130ps, source timewise PL slopes on every ±130ps neighborhood at those four times are bounded by exact archived-binary64 secants M=(3.405145572,6.697317765,4.121298635,4.124647131) V/ns. The weighted archived support is B=Σ|w_i|M_i=5.390187884385759 V/ns by independent exact-Fraction ratio computation; every such candidate with voltage error eV and separate source/interpolation error rho_source must obey
```math
\epsilon_V+\gamma_{\max}\rho_{\rm source}
\ge 0.8320673271321596\ {\rm V}
-1.1(5.390188\ {\rm V/ns})\,|\delta|.
```
At the declared hypothetical **130ps** common skew, this implies epsilonV+1.1rho_source > **0.0612704V** (conservative decimal <B exact). The example epsilonV=.05V excludes these TWO saved candidates and their particular convex mixtures only if true clock/gain/source-error contract satisfies the inequality. The common-clock bound is NOT justified for arbitrary unbounded affine mixing, unknown nonuniform time warp or extrapolation beyond ±130ps. The source states/measurement errors are not directed-validated and the instrument contract is unqualified; no full physical-world or Goal27 claim.

**A separate joint-current conditional gate.** Source original full-prefix PL current at b∈[90,110]MHz, shared PREP RC initialization, gains in [.9,1.1], ±.1A source filter init and a common 25MHz correlated sinusoid amplitude .05A allow an all-H4801 Chebyshev current LP. A worker's analytic source-PL b-slope / sparse dual grid gives a numeric conservative epsilonI>0.10260A uniformly over b, or >0.09951A with an additional common <=1ps skew; numeric LP and slope inflation are NOT directed certificates. This is a HYPOTHETICAL sensor/noise contract, not a calibrated strong guarantee. Strongest ordinary sees exactly the same full 4801 V/I and common command, and can apply these identical witnesses. To reach a source-wide Goal27 finite-L future-work bound requires an ACTUAL L interval derivative/solver-error outer, common fixed-load/legal-parameter domain, all-source-root/guard coverage, a licensed joint E and a future signed scorer path family. None is supplied by this candidate.

## 2026-10-18 P52: NEW in-frozen L4.50 full-CAL voltage dual and clock-fragile joint information

**Original-domain provenance and ceiling.** Pro18F nonprotected `analysis/acceptance/pro18f_physical_core/source_flow_response.npz` SHA256 `afcd9f4553e675efcf7384dd12a69dfd4788670e0dd1fc5964bc9e758340d108` / `source_flow_receipt.json` (source 50D actual law, L=4.50 nH, Rg=7.5 ohm, kappa=1.007, load=100 microH) uses the SAME original 4927 digital PREP/CAL command, initial50, own PREP126, H4801 and original source law as Pro18E. This is **within original Goal27 L in [4.02,4.58] nH**, unlike P51 L4.85 and P50 load140. Only original H4801 raw V/I outputs were saved, `state50_saved=false`; no archived full 4927x50 root/guard outer or future target for this candidate. Pro18E `e_saved_cal.npz` SHA256 `baafdd8cb489adb186677658c4a8031130cc53a9a1854c4997211d437daf8b3e` supplies source-generated CAL observed readout, NOT measured hardware.

**Strict stored-binary64 candidate exclusion at exact clock.** Using V=x0−x1 from Pro18F at zero-based H indices (2614,3799,4146) (times 6.940675,6.9554875,6.959825 microseconds) and original observed `y_D,V`, the exact Fraction null vector of rows `(1,V_L450)`, normalized L1=1, is approximately `w=(+.03593879435717655,−.5,+.46406120564282344)`. Its exact rational products `w·1=w·V_L450=0` and `|w·y_D|=0.306537239638883326... V` independently reproduced the entire 4801-point unknown-gain/offset Chebyshev minimum 0.3065372396388826 V (gap below 8e−16 V). Thus ANY constant affine gain/offset model of **this one** saved candidate requires `epsilon_V>=0.3065372396388833 V` at exact clock; this is candidate exclusion, NOT a continuous-L interval, a physical sensor-noise limit, or a bound on signed future work.

**Clock and correlated full-record observation caution.** Under an ADDITIONAL common positive gain <=1.1, |constant clock shift|<=1ps and independently checked source PL local slope support `B=4.904027168673593 V/ns`, the same exact support requires `epsilon_V+1.1 rho_source>0.3011428 V`; `rho_source` requires independent qualification. Pro18F raw H current permits a CAL-only exact PL low-pass model for b in [90,110] MHz plus ONE unknown RC initial transient `zeta exp(−2pi b(t−H0))`. A numerical all-b LP under a HYPOTHETICAL sensor contract (V/I gains [.9,1.1], independent offsets, one record-wide correlated 25 MHz amplitude mode with shared eta, residual budgets .30558 V/.04010 A) gives **V-only and I-only feasible**, but **joint-only** exact-clock optimum `epsilon≈1.00275026>1`; 93 sparse dual LPs over 47 b cells gave numerical conservative lower `>1.00000767`, NOT directed source/evaluator/instrument certification. Critically, ONE shared smooth time warp `delta_t=+400 fs sin(pi(t−H0)/(Hend−H0))` makes the same two-channel candidate feasible with `epsilon≈0.999585`. Consequently no realistic joint exclusion is claimed before one qualified timebase correlation/warp contract; an independent per-channel eta also removes the joint-only advantage. The strongest ordinary receives ALL identical 4801 V/I, digital commands, source and nuisance constraints and can apply the same witnesses; no five-point baseline is allowed.

**Pair-identity negative control.** The original H841 Pro18B/C Goal1 kappa=.98 versus1.02 worlds have a reported valid future work difference about 122.138 nJ but **no full-CAL flows**. DIFFERENT Goal5 kappa=.985 versus1.015 worlds have shared initial/full4801 raw CAL (max separate pair distance 6.421264377 V and .491101979 A) but their attempted full future target FAILED/NO RETRY. Under ONLY a componentwise symmetric raw error model their same-observation halfwidths would need >=3.210632189 V and >=.245550990 A; these numbers cannot be paired with Goal1's future work gap. Pro18E altered-G12 gamma worlds are a separate 10-microsecond/H1201 law and future protocol, not original H841. No original-C same-fullCAL, source-qualified future pair or licensed joint sensor E was proven here. Original Goal27 all-fiber future-work diameter shrinkage remains **ZERO CERTIFIED**.

## 2026-10-18 P53: in-domain full-CAL joint support with real-lift bandwidth/clock coverings

**New above P52, still an intentionally hypothetical observation law.** Original Pro18F L=4.50nH/fixed100microH source CAL raw4801, same full4927 digital PREP, original initial50 and own-PREP, and original Pro18E synthetic `y_D` are the same source-program inputs documented under P52. Freeze a SINGLE record-wide correlated calibration mode `eta sin(2pi·25MHz·(t−H0))` with paired voltage/current amplitudes (.02V,.05A), independent gains [.9,1.1], free channel offsets, first-order exact PL current filter b∈[90,110]MHz, ONE unknown inherited RC initial coefficient `zeta exp(−2pi b(t−H0))`, and rectangular residual (.30558V,.0401A)×epsilon. Model ONE common endpoint-anchored clock sequence `delta[0]=delta[4800]=0`, arbitrary interior per-time offsets up to 150fs. Neither this E nor actual source root numerical error has hardware qualification.

**Joint-only exact stored-value dual.** Assume epsilon≤1: original CAL endpoints imply |zeta|<20.071045A, |betaI|<21.101133A, |betaV|<324.138417V; use looser support 21A/22A/400V. For each dyadic bandwidth cell, an arbitrary signed two-channel sparse dual w yields a necessary epsilon via exact full4801 numerator minus maximized jointly correlated gain/offset/RC/noise support and a derivative envelope in b plus common clock. 199 midpoint LPs produced 100 disjoint verified cells spanning ALL [90,110]MHz; Fractions of saved binary64 source and a 65–75dps `mpmath.iv` real-lift π/exp/sin/PL convolution yield `epsilon_joint>1.00002725311896199895582` for ALL b and ALL declared ≤150fs clock shapes. The weakest cell is [100.8203125,100.859375]MHz; its nominal sparse numerator 1.0028281642090691 loses bandwidth ≤.000160415575799 and clock ≤.002640495512585, leaving >1.00002725. This is a **directed under the stated multiprecision interval-arithmetic implementation** exclusion of ONE saved source candidate under ONE declared correlated E, NOT full continuous-L/source roots, unqualified hardware, or any future-work diameter. Strongest full-record ordinary can use precisely this witness too; a single channel or independent eta cannot be substituted.

**Exact limits of clock/noise phase.** The lower bound above fixes the common sine mode's phase relative to CAL start H0; if the same mode is instead evaluated at physically warped timestamps, its extra support is ≤2pi25MHz·A·max(.02/.30558,.05/.0401), and using A≤130fs preserves a narrow directed all-b margin epsilon>1.0000017913. With an unqualified arbitrary sine phase, the particular worst-cell dual's projection is no longer tiny; phase-independent interval exclusion must be separately reoptimized and certified. At +400fs sinusoidal common time warp the P52 candidate was explicitly feasible (epsilon≈.999585) under the earlier model. One calibrated mid-CAL fiducial bounds an endpoint-anchored single sine-bow amplitude; for a broad clock Lipschitz class |delta'|≤24.9ppm over 60ns, four exact interior timestamps spaced 12ns force |delta|≤149.4fs, while five with ±25fs timestamp error spaced10ns force ≤149.5fs. A common clock skew cannot be inferred from V/I interchannel alignment. Marker counts certify this sufficient CLOCK envelope, not a minimal experiment to identify all physical Goal27 worlds. Retain all original CAL samples, command, source law, and joint E for the strongest ordinary.

**Scientific decision:** no real source numerical-error outer, full 4927×50 L4.50 checkpoint or licensed correlated sensor E was supplied. Candidate-specific support changed; the original Goal27 full-source future signed-work diameter remains without a certified nonzero shrink.

## 2026-10-18 P54: reported candidate-array calculation for unknown phase plus a smooth clock (source provenance unverified)

**Evidence status: session-reported candidate-input calculation, not an independently verified archived counterexample.** The session record describes a proposed Pro18F same-full-4927-digital-command/own-PREP L=4.50nH raw H4801 V/I candidate and a Pro18E exposed 4801x2 synthetic observation yD, and cites archive SHA256 `afcd9f4553e675efcf7384dd12a69dfd4788670e0dd1fc5964bc9e758340d108`. That exact archive and a manifest binding the raw ports, timestamps, RC seed, yD and replay script are absent from the pinned remote tree; the local candidate NPZ files do not by themselves establish that identity. Therefore the compatibility calculations below are retained as conditional diagnostics for the reported candidate arrays, not as independently verified compatibility with the named original archive. The session report says P53 excludes the candidate under a narrower phase-locked 25MHz correlated E, while allowing an unknown common phase may change the result. The reported candidate model uses gains in [.9,1.1], arbitrary offsets, inherited first-order exact-PL current RC seed zeta, shared record-wide 25MHz mode amplitudes `eta_s,eta_c` with `sqrt(eta_s^2+eta_c^2)<=1`, and the same warped sampling timestamp for both channels. Residual budgets are 0.30558V and 0.0401A, individually scaled by epsilon, with common increasing timestamps.

**Reported candidate-array feasible-pair parameters (not independently replayable from this snapshot).** The session record gives a single bow `delta_i=250fs sin(pi*(H_i-H0)/(Hend-H0))`, endpoint zero, and delta-array SHA256 `37cddd706fb1287b233b985eb4b6a8bb6319541503dfc39c7805401a831c88ed`. It reports maximum adjacent-clock slew **13.089968455406973ppm**, below the named 24.9ppm Lipschitz class, and candidate parameters at cutoff b=100.1495MHz: `gV=.9949897191142523, betaV=.20892947953196117V, gI=1.0131364500255347, betaI=.046140443893637625A, zeta=-.07339737325731134A, eta_s=-.0744693929394445, eta_c=-.05738734110715958`, with shared modal coefficient norm ~0.094016 <1. The session reports max epsilon_V=**0.9996770643730928** and epsilon_I=**0.9996773213368112** from a binary64 calculation, and directed upper max epsilon_V<**0.999677064376301**, epsilon_I<**0.999677321336855** from a 75-digit interval re-evaluation of all 9602 residuals. Those calculation records and exact source inputs are not committed in the current tree, so neither replay is independently reproducible here. Retain the figures only as conditional diagnostics for the reported candidate arrays; do not cite them as verified original-archive compatibility. The observation law has no qualified measured hardware errors and no full 4927x50 validated state/root history.


**Reported narrow timing-family exclusion (candidate provenance unverified).** The session report considers the same unknown shared 25MHz sin/cos phase with amplitudes in [-1,1]^2, gains/offsets, first-order RC initial and all H4801 samples, under a single endpoint-anchored sinusoidal clock coordinate `delta_i=a sin(pi(H_i-H0)/60ns)` with **|a|<=150fs**. It reports 151 rational sparse dual LPs, 76 dyadic bandwidth cells covering [90,110]MHz, and outward 65–70dps finite-PL RC/slope/phase/bandwidth envelopes yielding **epsilon>1.00001596083454776139** for the stated candidate and clock family. The weakest cell is reported as [6385/64,25545/256]MHz. The raw inputs, generated LP receipts and interval envelopes are absent from the pinned remote tree, so this is not independently replayable from the current snapshot. Treat it as a reported candidate-specific exclusion conditional on those arrays, not a verified original-archive result. Its excess supports at most the as-yet-unqualified raw source-error scale max(rhoV/.30558V, rhoI/.0401A)<1.45098496e−5, i.e. rhoV<4.43392microV and rhoI<0.581845microA. A single TRUE physical midpoint timestamp whose observed offset is nominal with ±150fs calibration would bound this one amplitude and provide one possible PRETARGET repair, provided the 1D clock-shape hypothesis, sensor loading, correlated E and all-source legality are independently established. The session-reported smooth+250fs candidate-array calculation would make ±250fs insufficient for that candidate if its input identity and residual receipts are confirmed; the arbitrary-shape+130fs witness is likewise only reported in the session record. No certified original Goal27 diameter shrink.

**The earlier 130fs case is not needed for this refutation.** Worker2 also generated a feasible irregular <=130fs common-clock witness (full scaled max<0.999671, but 20,800ppm slew), so merely capping per-sample timing amplitude is weaker than enforcing temporal clock regularity. The reported smooth 250fs bow obeys the named 24.9ppm class in the candidate calculation; absent its source manifest and replay receipt, the conclusion that a +/-250fs midpoint sync readout fails to exclude the original archived source remains conditional on that candidate identity. Numerical one-parameter profiling locates the approximate sine-bow transition at 211–212fs (`epsilon(211fs)≈1.000000548`, `epsilon(212fs)≈.9999922535`) for a selected optimizer; this is NOT a directed uniform all-b or all-source minimal required timestamp precision. New observation/synchronization proposals must be compared with strongest full4801 ordinary given the identical auxiliary data and same source constraints. The original Goal27 legal full-source compatible future signed-work diameter still has **ZERO CERTIFIED reduction**. A sensor/clock qualification and 50D L4.50 whole-source root envelope are indispensable before upgrading any candidate exclusion or inclusion.

**Local-only Pro18F artifact inventory (2026-10-18; no numerical replay).** A read-only inventory found candidate files under `pro_runs/20261010_pro18_goal_adequacy_frontier/artifacts/run_F/pro18f_source/`: `pro18f_phase2_CAL_arrays.npz` (165,292 bytes; SHA256 `8d1528d0d42736bc74a0530f89d98b04b78886bc9b4e467d211e4e12fc08b2b7`), `pro18f_joint_original_arrays.npz` (1,998,221 bytes; SHA256 `9a57ac8c8af93f24c228acf2f63e2738dcae4c7fb5e9139b72886d6d052f315c`), and `pro18f_cal2_observation.npz` (96,651 bytes; SHA256 `cd4819ca2cc156bc1b660b3502fa76cc302f9bf6a3b3f6111ac21c56ac5bbea7`). The exact archive cited above (SHA256 `afcd9f4553e675efcf7384dd12a69dfd4788670e0dd1fc5964bc9e758340d108`) was not found in the local ZIP filename inventory, and no committed manifest maps these candidate arrays to the complete H4801 raw V/I, timestamps, RC initial state, yD and replay script. They are candidate evidence only, not substitutes for the cited source package. The remote Math tree still lacks the corresponding raw inputs and generated receipt, so the recorded 9602-residual/151-LP result is not independently reproducible from that snapshot.


## 2026-10-18 P55: minimum extra CAL observation is defined only against the full joint nuisance contract

**Information repair is not noiseless source algebra.** D17 establishes a prospective one-timestamp original-C PRETARGET grounded-sl source-row separation: an assumed L4.16/L4.50 pair with the SAME true RAW i36 sequence must differ by 0.936640441365 V at source CAL index3221. The correct pairwise raw-current/grounded-sl-observation inequality is `2*eta_sl +732.8(V/A)*epsilon_I,pair + 6e-8V < .936640441365V`, where epsilon_I,pair is a bound on the true two-world RAW current mismatch at EACH of the two adjacent source times, not a postfilter residual, and the 6e-8V assumes each source real/solver coil row has separately qualified <=3e-8V residual. This improves the information-target specification but does **not** establish a feasible second own-PREP source root, or how one uncalibrated new node probe interacts with the original full 4801x2 E. The strongest full-record ordinary gets this *same* extra sample and synchronization.

**Adversarial raw-vs-observed check.** Existing P54 jointly models unknown shared-phase 25MHz sin/cos, common warped clock, independent gains/offsets, first-order RC current bandwidth and seed. An I-channel postfilter normalized residual of .0401 A does NOT imply the needed epsilon_I,pair <=1.278mA raw BE step slope without a certified inverse/clock/sensor error outer. Conversely, D13's ideal two-time source-load-current threshold 11.074microA for ΔL=.34nH assumes exactly shared RAW V/I. A favorable hypothetical direct raw voltage ambiguity ±.30558V per world already creates >223.302microA source-coil forcing uncertainty at the named L4.50 max-current-swing CAL pair, over 5.04 times its 44.297microA ideal signal; the best original-H sample would require effective raw V ambiguity <~60.865mV even with zero new-probe noise. Because original P54 uses gain/offset/filter correlation rather than arbitrary independent raw errors, this is a **negative control on blanket sufficiency**, not a theorem ruling out all correlated-observation repair.

**Decisional gate:** Before claiming any Goal27 future-work diameter shrink, independently qualify a source-valid full 4927x50 candidate/history and joint sensor error outer that maps original observed V/I, true RAW current steps, common phase/clock/RC seed and any new grounded-sl or load-current reading. Then run a same-full-information ordinary and compute a uniform future signed-work range. Current original full-source `diameter reduction certified = 0 nJ`. P54's phase-free 250fs candidate-array calculation remains recorded as a session-reported result, but compatibility with the named original archive is not independently verifiable from the pinned artifacts. The source H841 goal coefficients in D16 and hybrid real-lift S-L26/S-L27 are necessary route inputs, not future labels or unconditional CAL identifiability.
