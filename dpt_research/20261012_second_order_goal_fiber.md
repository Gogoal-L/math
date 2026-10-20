# Second-order goal recovery along a regular nonlinear observation fiber

**Date:** 2026-10-12. **Status:** independent, source-aware deterministic derivation, analytical falsifiers, executable linear-algebra auditor and synthetic tests. **Not** a new universal mathematical theorem, native SiC replay, proof of hardware noise or post-hoc score promotion.

Companion: [DPT Math transfer MAP](../DPT_MATH_RESEARCH_MAP.md) (legacy M40–M49 below); [fiber_goal_curvature.py](../dpt_tools/fiber_goal_curvature.py); [12 tests](../dpt_tools/test_fiber_goal_curvature.py).

## A. Prior work and exact conceptual separation

- J. N. Neuberger, A. Alexanderian, B. van Bloemen Waanders, *Goal oriented optimal design of infinite-dimensional Bayesian inverse problems using quadratic approximations* (arXiv:2411.07532v1, 2024), [primary full text](https://arxiv.org/html/2411.07532): the **quadratic goal Hessian** contributes to a Bayesian-Gaussian goal-oriented sensor-selection criterion (Gq-optimality). The work reports stronger designs than linearized c-optimality in its own studied PDE examples. It **does not** prove the deterministic minimax fiber formula below.
- S. Zhong, W. Shen, T. Catanach, X. Huan, *Goal-Oriented Bayesian Optimal Experimental Design for Nonlinear Models Using Markov Chain Monte Carlo*, [SIAM/ASA Journal on Uncertainty Quantification, DOI 10.1137/24M1649344](https://doi.org/10.1137/24M1649344): considers QoI expected information gain for **nonlinear observation and QoI models**, estimated by nested Monte Carlo. Bayesian information gain is distinct from the **hard bounded-error radius** derived here.
- The constrained Hessian / Lagrange-multiplier restriction to a regular level set follows classical implicit-function calculus. No originality claim is attached to that identity. The contribution **for this project** is the explicitly scoped goal-minimax coefficient, third-derivative gap, future-command Hessian pullback, and executable DPT-boundary/falsifier chain.
- Independent power-device metrology caution: Tiwari et al., *Design considerations and laboratory testing of power circuits for parallel operation of silicon carbide MOSFETs*, 2015, [Chalmers record / DOI 10.1109/EPE.2015.7309165](https://research.chalmers.se/en/publication/237572): measured current and overvoltage can reflect probe and inductor artifacts. The goal/observation definitions and sensor nuisance terms cannot be inferred from a mathematical Hessian test.

## B. What is held fixed

Let $`h_0`$ belong to a single **source-reachable** history/state manifold in a specified DPT reference. Let $`O:\mathbb R^n\to\mathbb R^m`$ be the exact **external pretarget observation**, and let $`G_w:\mathbb R^n\to\mathbb R`$ be the prescribed scalar goal **after a frozen, legally executed future command word** $`w`$. Assume both are $`C^3`$ on an adequately small chart with **no guard/branch changes**.

Assume $`DO(h_0)`$ has full row rank $`m\le n`$. Let $`Z\in\mathbb R^{n\times (n-m)}`$ have orthonormal columns spanning $`\ker DO(h_0)`$. The local level set $`O(h)=O(h_0)`$ is a smooth $`(n-m)`$-dimensional manifold by the submersion theorem. We consider a **specific chart-ball of legal states**, not all independent ambient perturbations:

**(C1)**

```math
\begin{aligned}
h(v)&=h_0+Zv+Uq(v),\\
\|v\|_2&\le r,\quad DO(h_0)U=I_m,\\
q(0)&=0,\quad Dq(0)=0.
\end{aligned}
```

Here $`U`$ is an exact right inverse and $`q(v)`$ is fixed by $`O(h(v))=O(h_0)`$. The domain claim explicitly includes that the entire chosen compact chart-ball is physically legal. A tangent vector alone cannot prove that.

If $`DG_w(h_0)Z\ne0`$, a **first-order** obstruction already exists and the second-order-only claim below is not the leading one. Focus on the apparently reassuring case $`DG_w(h_0)Z=0`$. Because $`DO`$ is surjective, this is equivalent to a unique multiplier $`\lambda`$ with

**(C2)**

```math
DG_w(h_0)=\lambda^\top DO(h_0).
```

## C. Correct constrained Hessian, with full derivation

Differentiate the exact fiber constraint twice at $`v=0`$:

**(C3)**

```math
DO(h_0)\,D^2h(0)[a,a]
+D^2O(h_0)[Za,Za]=0.
```

Differentiate $`G_w(h(v))`$ twice, and apply (C2)–(C3):

**(C4)**

```math
\begin{aligned}
D^2(G_w\circ h)(0)[a,a]
&=D^2G_w(h_0)[Za,Za]\\
&\quad+DG_w(h_0)\,D^2h(0)[a,a]\\
&=D^2G_w(h_0)[Za,Za]\\
&\quad-\lambda^\top D^2O(h_0)[Za,Za].
\end{aligned}
```

Therefore the **actual fiber Hessian** in orthonormal tangent coordinates is

**(C5)**

```math
Q_w=Z^\top\left(
D^2G_w(h_0)-\sum_{j=1}^{m}\lambda_jD^2O_j(h_0)
\right)Z.
```

This object cannot in general be replaced by $`Z^\top D^2G_w Z`$: the observation map may curve in exactly the same source directions as the goal. Orthogonal changes of tangent coordinates conjugate $`Q_w`$ and leave its eigenvalues and minimax coefficient invariant. **An arbitrary nonlinear reparameterization with non-orthonormal coordinates does not preserve the eigenvalues** without also transforming the declared norm ball.

## D. The leading local deterministic minimax radius is exactly a Hessian spectral range

Set $`\widetilde g(v)=G_w(h(v))`$. Under (C2) its first derivative vanishes at the origin. Taylor's theorem gives, with a real **supremum bound M on the third derivative of the composite exact-fiber function $`\widetilde g`$** on the chart-ball,

**(C6)**

```math
\widetilde g(v)
=G_w(h_0)+\tfrac12 v^\top Q_wv+\mathcal E_3(v),
\quad |\mathcal E_3(v)|\le \frac M6\|v\|_2^3.
```

The actual source third-derivative bound is **not** the raw ambient $`D^3G_w`$ alone; it includes nonlinear observation-fiber curvature and the future command $`T_w`$, with correct physical scaling.

At the *fixed observation* $`O(h_0)`$, all legal histories $`h(v)`$ have identical external data, so an optimal scalar decoder returns the midpoint of the range of $`\widetilde g(v)`$; its error equals half the range diameter. For the quadratic part, diagonalize the real symmetric $`Q_w`$, and define

**(C7)**

```math
s_+=\max(0,\lambda_{\max}(Q_w)),
\qquad s_-=\min(0,\lambda_{\min}(Q_w)).
```

Because the tangent domain is a **ball**, the center $`v=0`$ is feasible, so the maximum and minimum of the quadratic form are exactly $`\tfrac12r^2s_+`$ and $`\tfrac12r^2s_-`$ (not simply $`r^2\lambda_{\max}/2`$ when $`Q_w`$ is negative definite). Thus

**(C8)**

```math
\boxed{R_2(r)=\frac{r^2}{4}(s_+-s_-).}
```

If two functions differ uniformly by at most $`\delta`$, each of their maxima and minima differs by at most $`\delta`$, hence their half-range minimax radii differ by at most $`\delta`$. Set $`\delta=Mr^3/6`$ to obtain the **two-sided, sharp-to-leading-order conditional bound**

**(C9)**

```math
\boxed{
\max(0,R_2(r)-Mr^3/6)
\le R_{\rm fiber}(r)
\le R_2(r)+Mr^3/6.
}
```

This is **exact for quadratic goals on quadratic fibers with vanishing composite third derivative**. It makes the earlier MAP M32 example an instance rather than the whole method. Since the global admissible observation fiber may be larger than the chosen chart ball, the lower bound in (C9) transfers to the **whole** admissible class, but the upper bound does not unless the whole compatible class is covered.

Even if bounded sensor noise enlarges the compatibility class, zero-error observations remain allowed in the standard bounded-noise model; the lower bound survives. The upper bound must then account for *all compatible noisy states* separately, e.g. with a certified nonlinear readout-gain budget.

## E. Three exact counterexamples and what each rejects

**(E1) Observation curvature creates hidden goal variation.**
Take $`O(x,y)=x+y^2`$ and $`G(x,y)=x`$, at $`(0,0)`$. Then
$`DO=DG=(1,0)`$, but $`D^2O|_y=2`$, $`D^2G|_y=0`$. The exact observation fiber is $`x=-y^2`$. Thus $`Q=-2`$, and within the legal local chart $`|y|\le r`$,

**(C10)**

```math
\boxed{R_{\rm fiber}(r)=r^2/2,\quad\text{despite }DG|_{\ker DO}=0.}
```

A naive Hessian-of-goal-only audit would falsely report zero. The relative Hessian correctly reports a nonzero $`r^2`$ obstruction.

**(E2) Observation curvature cancels goal curvature.**
Keep $`O=x+y^2`$ but set $`G=x+y^2=O`$. The goal is **already exactly measured**, so $`R_{\rm fiber}=0`$ (for exact observation). Here $`D^2G|_y=2`$ is positive, but $`Q=2-2=0`$. A naive Hessian-of-goal-only audit would falsely report a nonzero ambiguity.

**(E3) A new nonlinear sensor can be valuable despite zero Jacobian.**
Start with $`O(x,y)=x`$ on $`|y|\le r`$, and choose $`G(y)=y^2`$. A *hypothetically legal pretarget* calibration sensor reading $`P=y^2+e`$, with deterministic $`|e|\le\epsilon`$, is sufficient to estimate this particular goal. At the nominal center $`DP(0)=0`$, so first-order sensor-rank testing says the candidate adds nothing. Nevertheless, direct compatible-interval analysis gives

**(C11)**

```math
\boxed{R_{\rm after\ P}=\min(\epsilon,r^2/2).}
```

Proof: all goal values q lie in $`[0,r^2]`$. Given a possible sensor reading p, the compatible q interval is $`[0,r^2]\cap[p-\epsilon,p+\epsilon]`$. Its longest possible diameter is $`\min(r^2,2\epsilon)`$, so the optimal midpoint decoder has radius exactly half this diameter.

For a **future** DPT work goal, measuring future work before the future command is not available. $`P=y^2`$ here is an abstract proxy available *before* the future target; real acquisition proposals must show a physical CAL observable with this information structure. It also does not recover the **sign** of y, so it would not recover a signed future goal G=y.

A fourth caution: if $`Q=0`$ but $`\widetilde g(v)=\alpha v^3`$, the leading $`r^2`$ term vanishes yet exact minimax radius is $`|\alpha|r^3`$ on $`[-r,r]`$. Therefore **second-order zero is not nonlinear goal sufficiency** without a higher-order/remainder contract.

## F. Dynamic goal Hessian pullback across legal ordered commands

For a single smooth legal source update $`x_+=f_u(x)`$ and a scalar future goal $`g_+`$ defined on its output, denote the source Jacobian $`J_u=Df_u(x)`$ and component Hessians $`H_{u,j}=D^2(f_u)_j(x)`$. Define $`g(x)=g_+(f_u(x))`$. Then the exact source derivative transport is

**(C12)**

```math
\begin{aligned}
Dg(x)&=J_u^\top Dg_+(x_+),\\
D^2g(x)
&=J_u^\top D^2g_+(x_+)J_u\\
&\quad+\sum_j [Dg_+(x_+)]_jH_{u,j}.
\end{aligned}
```

The second line is critical. A **linear final engineering goal** has zero terminal Hessian, but nonlinear dynamics can generate nonzero Hessian relative to the *earlier history*. Repeat (C12) from the last command back toward preparation, using **each stage's legally reached source point**. This is not simply multiplication of all single-stage Jacobians or arbitrary commutation of commands.

An exact two-command check: first $`f_A(x,y)=(x+\alpha y^2,y)`$, then $`f_B(X,Y)=(X,Y+\beta X^2)`$, and finally $`G_{\rm final}(X',Y')=Y'`$. The precommand goal is

**(C13)**

```math
\widetilde G(x,y)=y+\beta(x+\alpha y^2)^2.
```

Direct differentiation and two uses of (C12) both yield

**(C14)**

```math
D^2\widetilde G=
\begin{pmatrix}
2\beta &4\alpha\beta y\\
4\alpha\beta y&4\alpha\beta(x+\alpha y^2)+8\alpha^2\beta y^2
\end{pmatrix}.
```

The automated tool uses [pullback_goal_derivatives](../dpt_tools/fiber_goal_curvature.py) and an independent analytic polynomial oracle in its tests. Unlike F129's full relation-alphabet exponential theorem, this is ordinary finite-dimensional calculus used for finite **source-qualified** command words.

The rank and curvature check for a future command now uses $`DG_w`$ and $`D^2G_w`$ pulled back to the **same preparation coordinates** as $`DO,D^2O`$ and evaluated under the **same reference**. A change of stage guard/event winner may invalidate the smooth source map; then a piecewise or nonsmooth goal bound, not (C12), is needed.

## G. Best physical next discriminating experiment, not a paper claim

For a single 150-V Pro18B/C actual-law reference or the distinct original R1 at 100 V:

1. Fix source law, terminal/window definitions for future signed work, peak VDS value and event time, and a legal preparation/command set. Document all directly acquired pretarget VDS/current/gate/CAL data, sensor nuisance and units.
2. Produce a regular, source-reachable observation center with a nonzero **legal fiber chart**. Differentiate the *actual* external observation and *same-reference* future goal, including command curvature via (C12). Rescale states so the declared Euclidean tangent radius has a physical interpretation.
3. If $`DG_wZ`$ is nonzero, first-order predicted ambiguity dominates; otherwise compute **relative** $`Q_w`$. Obtain legal source re-shooting of two histories with identical/qualified near-identical observations along the predicted extreme eigen-directions.
4. Compare *prospective* goal gaps to $`R_2\pm Mr^3/6`$ only if M was actually bounded on the entire chart. Compare against a strong ordinary based on recorded full command, valid direct switching regression and source-based one-Newton; test separately whether prediction improves for work, peak and event-time.
5. If Q is small or zero, check higher-order and finite-noise ambiguity before claiming sufficient information. If true CAL changes the physical state, use the withheld-vs-observed CAL comparison with the *same* CAL-executed future physics (see main MAP M28–M29).

**Risk/falsifier:** the source observation may fail the rank/regularity condition, the legal chart may collapse at a mode guard, a physical CAL proxy may be unavailable, or a well-specified ordinary may already reach the target tolerances. Those outcomes bound the role of this second-order object rather than invalidate the conditional calculus.

## H. Verification and hard limits

- The executable matrix auditor [fiber_goal_curvature.py](../dpt_tools/fiber_goal_curvature.py) checks full-row-rank, tangent goal-gradient factorization, Hessian symmetry, relative Q eigenvalues, r²/4 radius, and outputs a numeric interval **only** when a uniform composed-fiber third derivative bound M is supplied.
- [12 tests](../dpt_tools/test_fiber_goal_curvature.py) include exact linear-goal hidden nonlinear observation, cancellation, positive/negative Hessian modes, 120 synthetic cubic exact-fiber cases, invalid regularity, and a two-stage command-pullback polynomial oracle. They prove software behavior on these fixtures, not a universal theorem or source physical truth.
- Assumed $`C^3`$ charts and uniform M do **not** follow from one finite-difference Hessian or a green MathJax syntax check. For the actual device, derive local derivatives and uniform bounds from the source residual (implicit differentiation/validated interval calculations), correct prepared state and legal guard branches.


## I. Direct implicit source-law bridge: adjoint Hessian without forming explicit f

**Why this matters for the actual DPT project.** The supplied *IH2662 DPT Research Design V6* §4.7 and §6.5 describe a coupled backward-Euler source residual with current/previous diode stored charge, conduction, network and thermal equations. Other stages use trapezoidal source updates. The future-goal Hessian (C12) cannot be assumed known: computing derivatives of an explicit multi-stage update f may be costly or misleading if source signs/current-before-next conventions are wrong. The following formula supplies a pointwise **exact implicit** route, without claiming the whole source has been differentiated yet.

Fix one legal command u and a regular source pair (z,x) satisfying F(z,x;u)=0. For clarity both z and x have n coordinates (a real BE evaluator must map its own actual coordinate chart and time step). Let

**(C15)**

```math
A=F_z,\qquad B=F_x,\qquad J=-A^{-1}B,\qquad A J+B=0.
```

The implicit function theorem gives z=f(x) near that root when A is invertible. Let g(z) be the goal after this step and solve the **source adjoint**

**(C16)**

```math
A^\top\lambda=\nabla g(z).
```

For any old-state tangent vectors a,b, define complete residual directions $`\widetilde a=(Ja,a)`$ and $`\widetilde b=(Jb,b)`$, in the concatenated coordinates (next z, previous x). Differentiate F(f(x),x;u)=0 twice:

**(C17)**

```math
A\,D^2 f[a,b]+D^2F(z,x;u)[\widetilde a,\widetilde b]=0.
```

The second derivative of the postcommand scalar goal, **including current/previous coupling**, is then

**(C18)**

```math
\boxed{
\begin{aligned}
D(g\circ f)&=J^\top\nabla g,\\
D^2(g\circ f)[a,b]
&=(Ja)^\top D^2g(z)(Jb)\\
&\quad-\lambda^\top D^2F[\widetilde a,\widetilde b].
\end{aligned}
}
```

The minus sign arises from the source residual differentiation. **It does not equal simply $`J^\top D^2g\,J`$** except when the source residual has zero second variation on the legal directions (or the adjoint kills it).

The weighted source Hessian includes four physically distinct blocks $`F_{zz},F_{zx},F_{xz},F_{xx}`$. In particular **retaining only $`F_{zz}`$ misses old charge, preparation memory and cross derivatives**, even if g is linear. The code [implicit_goal_hessian.py](../dpt_tools/implicit_goal_hessian.py) accepts precisely these full derivatives in concatenated [z,x] order and returns both gradient and Hessian in previous-state coordinates. A matrix-free source implementation would use adjoint-weighted Hessian-vector products to avoid materializing F2.

### Sharp ordinary counterexample: current–previous mixed Hessian alone

For an exact scalar nonlinear discrete source equation

**(C19)**

```math
F(z,x)=z+\kappa zx-x=0,\qquad
z=f(x)=\frac{x}{1+\kappa x},\quad 1+\kappa x\ne0,
```

take a *linear* terminal goal g(z)=z. Here $`F_{zz}=F_{xx}=0`$, but $`F_{zx}=F_{xz}=\kappa`$, and exact differentiation gives

**(C20)**

```math
\frac{d}{dx}g(f(x))=\frac{1}{(1+\kappa x)^2},
\quad
\frac{d^2}{dx^2}g(f(x))
=-\frac{2\kappa}{(1+\kappa x)^3}.
```

A Hessian transport that kept only $`F_{zz}`$ and $`F_{xx}`$ would incorrectly report **zero source curvature**, despite the exact nonzero result. This mechanism is not a claim that a vendor SiC branch has precisely z+κzx; it is an **adversarial analytic circuit-like residual** showing why the cross-block cannot be dropped from the *general* method.

### Actual V6 diode law: curvature formula and scope

For fixed temperature/emission thermal scale a>0, fixed τ>0, and known time step h>0, the actual V6 BE diode-residual component is (up to the declared source sign conventions)

**(C21)**

```math
F_D=i_b-I_s(e^{v_n/a}-1)
-\frac{\tau I_s}{h_n}\bigl(e^{v_n/a}-e^{v_{n-1}/a}\bigr).
```

Its **isolated diode current/charge contribution** has second derivative entries

**(C22)**

```math
\begin{aligned}
(F_D)_{v_nv_n}
&=-\frac{I_se^{v_n/a}}{a^2}(1+\tau/h_n),\\
(F_D)_{v_{n-1}v_{n-1}}
&=+\frac{\tau I_s e^{v_{n-1}/a}}{h_na^2}.
\end{aligned}
```

Even this simple model contributes with **opposite signs** at current and previous steps; dropping previous stored charge violates its source law. Further mixed derivatives can arise from the rest of the full coupled BE residual (and from T-dependence of Is and a), so the stand-alone diode entries are **not** a complete DPT Hessian. Under uniformly bounded source/goal operators on a shared legal chart, (C18) immediately provides a conditional estimate

**(C23)**

```math
\|D^2(g\circ f)\|
\le\|J\|^2\|D^2g\|
+\|\lambda\|\,\|D^2F\|(1+\|J\|^2).
```

The numerical Jacobian/adjoint condition number must be included in error propagation; if F_z becomes near singular, a pointwise float Hessian need not have a useful finite-radius uniform bound.

**Independent verification:** analytic tests for (C19)–(C20), an implicit nonlinear current+previous scalar residual, a two-state quadratic command, and 200 random exactly specified quadratic maps represented through an invertible implicit residual all matched the source-free explicit chain rule. This validates the algebra and program on those fixtures, not the actual Wolfspeed/TRAP/BE vendor source.

**Source-level acquisition required to close the loop:** actual executable F(z,x;u) and correct frozen command; measured source-consistent preparation/state chart; analytic/AD/validated finite-interval F_z,F_x,F_zz,F_zx,F_xx; goal g(z) or full stage work/readout including guard/event terms; and uniform implicit invertibility and third-derivative bounds on one physically legal history fiber. These feed (C5)–(C9) to decide the engineering goal radius *without* claiming recoverability of all parasitic inductances.

---

## J. Goal-oriented sensor ranking with correlated model error (Q1–Q4)

**Result and priority (2026-10-12).** This section develops a source-*conditional*, computationally cheap **Bayesian** comparison among legal pretarget observation designs for future work/peak/event goals. The quadratic data-averaged goal risk is the finite-dimensional form of **Neuberger, Alexanderian and van Bloemen Waanders (2025)**, [original Theorem 3.2 and proof](https://arxiv.org/html/2411.07532). The correlated approximation-error part follows elementary joint-Gaussian conditioning, motivated by **Koval and Nicholson (2025)**, [full article](https://doi.org/10.1007/s10915-025-03008-7), whose original criterion is *parameter A-optimal*, not this particular goal functional. This combination is an explicit diagnostic synthesis rather than a claim to an unprecedented theorem. It is independent of the deterministic minimax fiber radius proved in Sections C–D, and no native SiC source dataset has yet been scored.

### J.1. Exact stochastic input contract and covariance retention

Fix one source reference, prior $`\mathcal N(\mu,P)`$ for the **scaled** vector $`x`$ representing admissible uncertain preparation/parameters on a *declared* chart. A candidate pretarget observation is

```math
y=Hx+d+\varepsilon.
```

Here $`(x,d)`$ is **jointly Gaussian**, with state–discrepancy cross covariance $`C`$, discrepancy covariance $`D`$, and independent measurement noise $`\varepsilon\sim\mathcal N(0,R)`$, where $`R`$ is positive definite. The joint block covariance of $`(x,d)`$ must be positive semidefinite. The mean of $`d`$ can be subtracted as an explicit, **pre-calibrated** offset; it must not be estimated from the unknown target outcome. Dependence between $`x`$ and $`d`$ is NOT ignored. Ordinary parameter covariance trace requires a chosen nondimensionalization/metric, since L in nH and R in ohms cannot be added as an unqualified scalar trace.

The covariance of a candidate's pretarget data, its state–data cross covariance and its Gaussian conditional state covariance are

**(Q1)**

```math
\begin{aligned}
S_y&=HPH^\top+HC+C^\top H^\top+D+R,\\
C_{xy}&=PH^\top+C,\\
S&=P-C_{xy}S_y^{-1}C_{xy}^\top.
\end{aligned}
```

**Proof.** Expand $`\mathrm{Cov}(Hx+d+\varepsilon)`$ bilinearly, keeping both $`HC`$ and $`C^\top H^\top`$. Independence of $`\varepsilon`$ removes its cross terms, but not those of $`x,d`$. Completing the square in the jointly Gaussian density gives the posterior. This is the exact posterior covariance for the *joint Gaussian affine observation model*; even an exact Hessian does not make it correct for an unknown non-Gaussian switched DPT observation law.

### J.2. Nonlinear future goal: exact variance of its quadratic model

For a source-derived future goal $`G`$, choose a Taylor point $`x_*`$ **before** seeing the future target:

```math
G_2(x)=G(x_*)+b^\top(x-x_*)
+\tfrac12(x-x_*)^\top Q(x-x_*).
```

The gradient $`b`$ and symmetric Hessian $`Q`$ must be computed for the same **future command, stage law, and goal units** as the eventual held-out score. Let $`a=b+Q(\mu-x_*)`$. The data-averaged posterior variance of the *quadratic* goal is

**(Q2)**

```math
\begin{aligned}
\Psi_q
&=\mathbb E_y[\mathrm{Var}(G_2(x)\mid y)]\\
&=a^\top S a
+\mathrm{tr}(PQSQ)-\tfrac12\mathrm{tr}[(SQ)^2].
\end{aligned}
```

**Proof independent of posterior sampling.** Conditional on $`y`$, the state is Gaussian with mean $`m_y`$ and covariance $`S`$. The quadratic-form Gaussian fourth-moment identity gives

```math
\mathrm{Var}(G_2\mid y)
=(b+Q(m_y-x_*))^\top S(b+Q(m_y-x_*))
+\tfrac12\mathrm{tr}[(SQ)^2].
```

By the law of total variance for the affine observation, $`m_y`$ is Gaussian with mean $`\mu`$ and covariance $`P-S`$. Averaging the first term yields $`a^\top Sa+\mathrm{tr}(Q(P-S)QS)`$; combining with the last trace gives (Q2). This is the precise finite-dimensional analogue of Neuberger et al.'s Gq-optimality. A first-order goal-only criterion retains only $`a^\top Sa`$, while parameter A-optimality uses $`\mathrm{tr}(S)`$, and Gaussian parameter mutual information ranks $`\frac12\log(\det S_y/\det S_{y\mid x})`$ when the relevant covariance is nondegenerate. For correlated discrepancy, $`S_{y\mid x}=R+D-C^\top P^{-1}C`$ when $`P`$ is invertible; dropping $`C`$ changes both the observation law and the information score.

### J.3. Strict analytical sensor-ranking reversal (not a native SiC sample)

Take $`P=\mathrm{diag}(9,1)`$, $`\mu=x_*=0`$, future goal $`G(x)=x_2^2`$ (so $`b=0,Q=\mathrm{diag}(0,2)`$), and two equally noisy scalar sensors $`H_A=(1,0)`$, $`H_B=(0,1)`$, each with variance $`R=1`$. The posterior covariances are $`S_A=\mathrm{diag}(0.9,1)`$ and $`S_B=\mathrm{diag}(9,0.5)`$. The exact choices are:

| Metric (optimization direction) | Sensor A | Sensor B | Winner |
| --- | ---: | ---: | --- |
| Parameter variance trace $`\mathrm{tr}(S)`$ (minimize) | 1.9 | 9.5 | A |
| Parameter mutual information (maximize, nats) | $`\tfrac12\log10`$ | $`\tfrac12\log2`$ | A |
| Linearized goal variance $`a^\top Sa`$ (minimize) | 0 | 0 | Tie |
| Quadratic-goal data-averaged posterior variance $`\Psi_q`$ (minimize, squared goal units) | **2** | **1.5** | **B** |

Thus the second-order future-goal rule identifies a **25% reduction** from measuring the relevant curvature direction despite an uninformative first-order gradient. This toy is a genuine finite-dimensional analytic falsifier of choosing a sensor by parameter information, and not evidence that a real VDS probe improves 150 V SiC Eoff.

### J.4. Correlated discrepancy can restore or erase information

A second exact example refutes the simplistic idea that “model discrepancy = extra independent noise”. Let $`x\sim\mathcal N(0,1)`$, a nominal uninformative map $`H=0`$, and let the discrepancy equal $`d=x`$. Then $`P=D=C=1`$, independent measurement variance $`R=0.1`$, so (Q1) yields $`S=1/11`$: the *observed discrepancy* carries genuine signal. If one incorrectly sets $`C=0`$ but leaves $`D=1`$, the same nominal $`H=0`$ becomes uninformative and $`S=1`$. For future $`G=x^2`$, the corresponding $`\Psi_q`$ values are $`42/121`$ and $`2`$. This is a conditional Gaussian mathematical case; shared semiconductor sensor filtering, capacitance and drift need **measured and source-supported cross covariances**, not an assumption that every observed error is useful.

A separate adverse case has $`G=x^2`$, $`P=1`$, $`H_A=1,R_A=0.01`$, and $`H_B=0.8,R_B=0.04`$: A wins if its model is exact. Adding uncorrelated discrepancy variance $`D_A=2`$ makes A worse than B under the same goal. Thus a nominal $`G_q`$ ranking can reverse when the source discrepancy uncertainty is admitted. These are design-stability counterexamples, not quantitative bounds on MOSFET switching losses.

### J.5. Invariance and a hard boundary on nonlinear observation

**Coordinate invariance.** Under an invertible reparametrization $`x'=Tx`$, apply
$`P'=TPT^\top`$, $`H'=HT^{-1}`$, $`Q'=T^{-\top}QT^{-1}`$,
$`b'=T^{-\top}b`$, $`C'=TC`$, and $`x_*'=Tx_*`$.
Then $`S'=TST^\top`$, and every scalar in (Q2) is unchanged by matrix multiplication and trace cyclicity. By contrast $`\mathrm{tr}(S')`$ generally differs from $`\mathrm{tr}(S)`$: a raw multi-unit parameter-A ranking has no comparable physical meaning until a specific metric/normalization is frozen. An actual test scales parameter axes by factors 100 and 0.01 and confirms $`G_q`$ invariance but large parameter-trace change.

**Observation-nonlinearity counterexample.** If $`x\sim\mathcal N(0,1)`$, future goal $`G=x^2`$, and a *noise-free* pretarget sensor returns $`y=x^2`$, this sensor predicts the goal exactly. Yet its observation Jacobian at $`x_*=0`$ is $`H=0`$, so the Gaussian *linearized observation* model predicts no reduction of prior goal variance (2). A quadratic GOAL approximation alone cannot repair a missing nonlinear OBSERVATION model. **Zhong, Shen, Catanach and Huan (2026)** study nonlinear-observation nonlinear-QoI expected-information-gain design using nested Monte Carlo/MCMC, [primary full manuscript](https://arxiv.org/html/2403.18072); their method is a more expensive independent rival, with different posterior/utility semantics. When observation curvature or mode changes decide the ranking, use actual nonlinear goal/measurement simulation or bound the observation approximation error instead of trusting $`H`$ alone.

### J.6. Actual SiC physics, strongest rival and minimum owner action

Two additional physical studies motivate a *possible* frequency/history-specific model discrepancy: Nagel et al., **PCIM 2025**, [Evidence of Frequency-dependent SiC Power MOSFET Capacitances in Fast and Slow Switching Transients](https://doi.org/10.30420/566541011) (original accessible abstract); Race et al., **IEEE Transactions on Electron Devices 2024**, [Frequency-Dependent Internal Gate Resistance of SiC Power MOSFETs](https://doi.org/10.1109/TED.2024.3488684) (repository abstract/metadata). The first reports divergent fast/slow turn-off twin agreement and a possible C–V/interface-trap explanation; the second identifies a frequency-dependent internal gate resistance mechanism. **Their full experimental methods and data have not been independently verified in this research round.** Neither source proves that the DPT-R1 device exhibits the same defect, nor supplies a numerical covariance for (Q1).

**Decision question.** Within one 100 V original R1 *or* 150 V accepted 18B/C chart (never pooled), would one *legal* extra pretarget voltage/current/CAL measurement reduce the expected squared prediction error for **one frozen future command and goal** more than the fully recorded-command ordinary, parameter A/D design, and gradient-only goal design, after source-aligned model discrepancy is considered?

**Main handoff inputs:** (1) frozen reference/ports/preparation/ordered command/goal units and scalar tolerance, (2) physically legal candidate pretarget sensors plus acquisition costs and bandwidth/skew specifications, (3) centered/scaled prior mean/covariance, (4) actual future-goal gradient and Hessian on that source-law/timing chart, (5) sensor noise and cross-channel error model, (6) full-law versus approximate-law paired simulations for empirical $`D,C`$ without target leakage, (7) prospective holdout goals and strong complete-command and full-source baselines. Use [goal_ellipsoid_recovery.py](../dpt_tools/goal_ellipsoid_recovery.py) in `--quadratic-design` mode only as a **cheap pre-screen**. If the best candidate flips under plausible $`D,C`$, if the observation is too nonlinear to justify $`H`$, or if the full recorded-command ordinary wins, recommend the lower-cost ordinary or an actual nonlinear acquisition study—not a premature sensor deployment claim.

**Executable evidence.** Existing [goal_ellipsoid_recovery.py](../dpt_tools/goal_ellipsoid_recovery.py) adds exact finite-dimensional joint-Gaussian quadratic-risk calculation and candidate ranking; [test_goal_ellipsoid_recovery.py](../dpt_tools/test_goal_ellipsoid_recovery.py) supplies known-answer rank reversal, independent Monte Carlo conditional-variance verification, cross-covariance necessity, reparametrization invariance, nonlinearity false-negative, discrepancy ranking flip, PSD rejection and CLI replay. A green Actions run establishes implementation behavior and formula rendering within these test cases. This remains **SIDE_VERIFIED / READY_FOR_HANDOFF for a qualified Gaussian chart** and **OPEN_RESEARCH for source-native SiC prediction**, without changing the Main acceptance record.

---

## Legacy MAP derivations: relative observation-fiber Hessian and implicit source pullback (M40–M54)

This source-aware proof record retains M numbering while the independent C-numbered theorem above remains the central formal derivation. The [original historical MAP](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/DPT_MATH_RESEARCH_MAP.md) is frozen.

### 0.11 深挖：真正的二阶可辨识对象是 observation fiber 的相对 Hessian

进一步核对 [Neuberger–Alexanderian–van Bloemen Waanders 2024 原文 §3](https://arxiv.org/html/2411.07532) 后，需要与其 **Bayesian-Gaussian quadratic-goal OED** 区分：它使用二次目标展开和后验方差进行传感器设计；我们这里独立推导的是**确定性、固定观测相容类上的最坏 scalar-goal 半径**。[Zhong et al. 2026 SIAM/ASA](https://doi.org/10.1137/24M1649344) 进一步处理非线性观察和未来 QoI 的 Bayesian information gain，但不提供以下硬误差界。完整证明、强反例、来源与物理接口见 [二阶 goal fiber 专题笔记](dpt_research/20261012_second_order_goal_fiber.md)。

**合法前提：** 在一份固定 source reference 的 pretarget preparation 点 $`h_0`$，外部观测 $`O(h)`$ 和冻结合法未来命令后的标量目标 $`G_w(h)`$ 是 $`C^3`$；$`DO(h_0)`$ 对观测空间满行秩。取 $`Z`$ 的列为 $`\ker DO(h_0)`$ 正交基，且最有趣的一阶“看似足够”情形满足

**(M40)**

```math
DO(h_0)Z=0,\qquad
DG_w(h_0)Z=0
\iff DG_w(h_0)=\lambda^\top DO(h_0).
```

根据正则水平集隐函数定理，若一整个**明确的、source-合法的 chart-ball** 都可达，则存在真正保持同一观测的曲线族 $`h(v)`$：

**(M41)**

```math
O(h(v))=O(h_0),\quad
h(0)=h_0,\quad Dh(0)=Z,\quad \|v\|_2\le r.
```

对观测约束二次微分并消去曲线弯曲的法向加速度，得到真正的目标二阶矩阵：

**(M42)**

```math
\boxed{
Q_w=Z^\top\left[
D^2G_w(h_0)-\sum_j\lambda_jD^2O_j(h_0)
\right]Z.
}
```

**推导：** $`DO\,h''(0)[v,v]+D^2O[Zv,Zv]=0`$，且 $`DG_w=\lambda^\top DO`$，所以 $`D^2(G_w\circ h)(0)=Z^\top(D^2G_w-\lambda^\top D^2O)Z`$。因此**只看 $`D^2G`$ 自身是错的**：非线性 observation 的曲率可以制造、也可以完全抵消未来目标的二阶歧义。

若确有整个合法 chart-ball 上的统一三阶上界 $`M_w`$（它是**真正复合函数 $`G_w\circ h`$** 的三阶导数界，不是单独 goal 的 ambient 三阶导数），Taylor 定理给

**(M43)**

```math
G_w(h(v))=G_w(h_0)+\tfrac12v^\top Q_wv+R_3(v),
\qquad |R_3(v)|\le M_wr^3/6.
```

定义 $`s_+=\max(0,\lambda_{\max}(Q_w))`$、$`s_-=\min(0,\lambda_{\min}(Q_w))`$。球内包括中心 $`v=0`$，二次型的精确最大最小分别是 $`r^2s_+/2,r^2s_-/2`$。固定外部观测时，一个 scalar decoder 必须输出同一数，其 minimax 最优输出是目标范围中点，故

**(M44)**

```math
\boxed{R_2(r)=\frac{r^2}{4}(s_+-s_-).}
```

对每个状态的目标统一扰动不超过 $`M_wr^3/6`$ 时，max 和 min 各移动至多该值。因此可得到**真正双侧的局部目标半径资格**：

**(M45)**

```math
\boxed{
\bigl[R_2(r)-M_wr^3/6\bigr]_+
\le R_{\rm fiber}(r)
\le R_2(r)+M_wr^3/6.
}
```

这里正号 $`[x]_+=\max(x,0)`$。若整个 global observation fiber 比这个 chart-ball 大，(M45) **仅有下界**可直接传递到全域，不能把局部上界命名为全域预测充分性。若 third-derivative 常数尚无严格来源，数值 Hessian 只能提供 $`R_2`$ 的主项诊断。

**两个物理直觉相反、但一阶完全相同的精确反例。** 在二维合法局部 chart $`|y|\le r`$，取 $`O=x+y^2`$。若目标 $`G=x`$，虽然 $`DG=DO`$ 于中心，其精确 observation fiber 为 $`x=-y^2`$，故 $`Q=-2`$ 且

**(M46)**

```math
R_{\rm fiber}(O=x+y^2,G=x)=r^2/2;
\quad R_{\rm fiber}(O,G=O)=0.
```

第二个目标 $`G=O`$ 的 ambient Hessian 并非零，但观测本身已经充分，所以相对 Hessian 正确地抵消了它。

**新增信息甚至可能一阶 Jacobian 为零。** 若旧观测为 $`O=x`$、未来目标为 $`G=y^2`$，一个**假设在 future 之前合法取得的非线性 CAL proxy** $`P=y^2+e,\ |e|\le\epsilon`$，在中心有 $`DP=0`$，却给出准确 deterministic minimax 半径

**(M47)**

```math
\boxed{R_{\rm with\ P}=\min(\epsilon,r^2/2).}
```

证明是：给定读数 $`p`$，相容目标值落在 $`[0,r^2]\cap[p-\epsilon,p+\epsilon]`$，最大区间长度为 $`\min(r^2,2\epsilon)`$。此 toy 不能被误说成工程上能在开关前直接测量未来 work；需要真实合法 CAL 的对应 proxy 与误差资格。它证明 first-order **rank 不是 nonlinear candidate 的完整 acquisition 价值标准**。

**未来命令的二阶曲率如何向 preparation 传播？** 设一步合法光滑更新 $`x_+=f_u(x)`$，后续 goal 为 $`g_+(x_+)`$，$`J_u=Df_u`$，则（所有量在对应实际 stage point 求值）

**(M48)**

```math
\begin{aligned}
D(g_+\circ f_u)&=J_u^\top Dg_+,\\
D^2(g_+\circ f_u)
&=J_u^\top D^2g_+J_u\\
&\quad+\sum_j(Dg_+)_jD^2(f_u)_j.
\end{aligned}
```

即使最后一阶段工程目标 $`g_+`$ 是线性的，**非线性 source command 的第二项仍可制造目标曲率**。这提供一种比把所有历史压成 28-state 直接构造更经济的必要信息审计：沿冻结命令词回传 goal gradient/Hessian，再在**同一 pretarget observation fiber** 上计算 $`Q_w`$。在共同合法 chart-ball、所有目标共同的 pretarget observation 和具名工程容差 $`\tau_j`$ 下，任意预测器至少要承担

**(M49)**

```math
R_{\infty,\mathcal W}\ge
\max_{w,j}
\frac{\bigl[\frac{r^2}{4}(s_{+,w,j}-s_{-,w,j})
-M_{w,j}r^3/6\bigr]_+}{\tau_j}.
```

**可验证代码**：[regular fiber curvature](dpt_tools/fiber_goal_curvature.py) 的 source Hessian/grad 输入及 backward command pullback；[12 项独立测试](dpt_tools/test_fiber_goal_curvature.py) 包括 120 个 cubic exact-fiber 场景和真实多项式两阶段命令的解析 oracle。它们验证数学实现，不代表自动提取了 LTspice/BE/trapezoidal source 的导数或完成了本构全域余项证书。

**对 18B/C 的可证伪选择：** (i) 150-V 同 reference/source 的完整 recorded-command ordinary 是否已经充分；(ii) 若不足，未见 pair 的未来 work/peak 歧义是否能由 $`Q_w`$ 特征方向定量预测；(iii) 合法 CAL 在不混入自身状态干预效应的条件下能否缩小真实 goal fiber，而不只是提高参数 Hessian 的秩；(iv) peak/event guard 换支导致光滑 chart 失效时，退回前面的 sup-norm peak 和分段 work 界。最强科学出口是**源码同域的条件下界 + 非线性有界上界 + 未参与拟合的未来预测**，而不是将这套微分几何称为已有 SiC 全局证书。

---

### 0.12 直接回接实际隐式 source 残差：不必显式构造整套 nonlinear update

上一段 (M48) 需要每个未来命令的状态更新 Hessian，但真实 DPT source evaluator 通常只提供离散隐式节点残差，例如 coupled backward Euler、梯形积分或带 charge/thermal 的求解器。正确的接口不必先全局求出状态转移 $`f_u`$。固定一个**合法命令** $`u`$，令前态 $`x`$、后态 $`z=f_u(x)`$ 满足整套离散 source 方程 $`F(z,x;u)=0`$，并假设真实点处 $`A=F_z`$ 可逆。于是由隐函数定理：

**(M50)**

```math
\begin{aligned}
F(z,x;u)&=0,\qquad A=F_z,\quad B=F_x,\\
J_u:=Df_u&=-A^{-1}B,\qquad A J_u+B=0.
\end{aligned}
```

目标 $`g(z)`$ 若只通过 postcommand 状态计算，则定义当前态 future goal $`G(x)=g(f_u(x))`$，求解 $`A^\top\lambda=\nabla g(z)`$ 得到 adjoint $`\lambda`$。任何前态方向 $`a,b`$ 诱导扩展 source 方向 $`p_a=(J_u a,a)`$、$`p_b=(J_u b,b)`$。连续对源残差**二次微分**并消去 $`D^2f_u`$，给出下式精确 Hessian-vector pairing：

**(M51)**

```math
\boxed{
\begin{aligned}
DG(x)&=J_u^\top\nabla g(z),\\
D^2G(x)[a,b]
&=(J_ua)^\top D^2g(z)(J_ub)\\
&\quad-\lambda^\top D^2F(z,x;u)[p_a,p_b].
\end{aligned}
}
```

**推导：** $`D^2F[(J_ua,a),(J_ub,b)]+A D^2 f_u[a,b]=0`$；代入 $`D^2(g\circ f_u)[a,b]=(J_ua)^\top D^2g(J_ub)+(\nabla g)^\top D^2 f_u[a,b]`$，再用 $`A^\top\lambda=\nabla g`$ 即得第二项的**负号**。实际实现须保留 $`F_{zz},F_{zx},F_{xz},F_{xx}`$ 全部块，尤其**同一步 current/previous charge 的相关性**，不能只对目标和当前态求 Hessian。该式可用求解当前 node Jacobian 与其转置来构造目标二阶方向导数；大规模 source 可采用 Hessian-vector products，而不必显式形成完整三阶存储张量。

**把式子作用到已提供的 V6 二极管 BE 子本构。** 若固定 $`a,I_s,\tau`$，并暂只检查 §4.7 的二极管 charge/conduction 对残差的贡献

**(M52)**

```math
F_{D,n}=i_{b,n}-I_s(e^{v_n/a}-1)
-\frac{\tau I_s(e^{v_n/a}-e^{v_{n-1}/a})}{h_n},
```

则控制电压块的**精确二阶残差导数**为

**(M53)**

```math
\begin{aligned}
\frac{\partial^2 F_{D,n}}{\partial v_n^2}
&=-\frac{I_s e^{v_n/a}}{a^2}
\left(1+\frac{\tau}{h_n}\right),\\
\frac{\partial^2 F_{D,n}}{\partial v_{n-1}^2}
&=+\frac{\tau I_s e^{v_{n-1}/a}}{h_n a^2}.
\end{aligned}
```

这两个项符号相反，且 previous charge 通过 $`1/h_n`$ 放大；**这是跨步 charge history 必须进入目标 Hessian 的精确 source 原因之一**。本式对该 scalar BE diode contribution 的交叉 $`v_n,v_{n-1}`$ 导数为零；但整套网络/器件/热残差的 mixed Hessian、隐式状态求解耦合与 guard 并不必为零。若 $`a=a(T)`$、$`I_s=I_s(T)`$，还要加入温度方向和其交叉偏导。本节不是把 diode branch 当作整个 vendor model。

对于一个合法相容 source 状态邻域，定义 $`\|D^2F\|`$ 为从两项归一化 source 方向到残差向量的双线性算子范数。由 (M51) 和 $`\|[J_u;I]\|_2^2=1+\|J_u\|_2^2`$（此处 $`\|[J_u;I]\|_2^2`$ **实际上等于** $`1+\|J_u\|_2^2`$），得条件目标曲率上界：

**(M54)**

```math
\boxed{
\|D^2G\|
\le \|J_u\|^2\|D^2g\|
+\|\lambda\|\,\|D^2F\|
  \bigl(1+\|J_u\|^2\bigr).
}
```

这帮助确定哪个 source 区域更值得重做有限域证书：$`F_z`$ 接近奇异、$`\|J_u\|`$ 大、指数电荷曲率大时，简单 constant/affine ordinary 的余项可能迅速上升；若 adjoint $`\lambda`$ 与曲率 source rows 正交，**某个工程目标**仍可稳定。这是**带目标投影的物理计算压力测试**，不是绝对的 source 器件精度定理。完整多步 work/peak 还需 stage goal/window boundary 与 guard。V6 的 150-V trapezoidal 与 600-V BE 残差不可混接。

[可执行隐式 source Hessian 工具](dpt_tools/implicit_goal_hessian.py) 实现式 (M50–M51)，输入同点完整 $`F_z,F_x,D^2F,\nabla g,D^2g`$；[独立解析测试](dpt_tools/test_implicit_goal_hessian.py) 包括精确含 $`F_{zx}`$ 交叉项的 rational source、含 $`F_{zz},F_{xx}`$ 的 implicit source，以及 200 个随机解析显式律与隐式残差一致性比较。需要在实际 DPT source 中冻结 reference、nodal 变量单位、求解分支和正确的上一时步 state，才可将输出放进 (M42–M49) 的真实 observation-fiber 计算。

**验证账本：** F119/F129/F132 的上述定理式从钉住的 [openai/math source](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb) 抽出；(M5–M6),(M8–M9),(M13–M22),(M24–M25) 是在具名假设下的独立有限维/分析推导。F119 相关噪声反例有精确有限枚举，F129 二状态 relation context 有全枚举，F132 小局部 grouped witness 有合成审计；[proof-level 细节](dpt_research/20261011_F119_F129_F132_proof_level_DPT_bridge.md)。联合半径工具另经独立的 70 组随机受约束 primal/dual 数值交叉检查（最坏绝对差约 $`9.14\cdot10^{-12}`$，其中 6 个严格容差下的 SciPy line-search status 未成功但最终可行迭代满足 $`10^{-8}`$ 约束容差；非形式证书），以及 analytic/CLI regressions。**没有真实 SiC source replay、没有物理参数/测量噪声资格、没有全部非线性 remainder 的统一证书。**

---

---

## Provenance annex: nonlinear fiber and finite-stage tube

The complete original nonlinear fiber / finite-stage box-tube derivations and critiques are preserved here. The finite-stage tube requires independently justified state/guard/remainder envelopes and is not an automatically validated actual SiC reachable domain. [Immutable original source](https://github.com/Gogoal-L/math/blob/15b3fde162b2f7cb729ec106b847be1ad046d222/dpt_research/20261010_nonlinear_fiber_and_stage_tube.md).

### DPT-R1 mathematical frontier IV: nonlinear goal fibers and finite-stage admissible tubes

**Date:** 2026-10-10. **Authority:** independent mathematical research; no native SiC validation, no S09/S10 budget or owner decision. **Upstream OpenAI Math identity:** [`fd4aeeb2`](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb). The preceding [all-word + solver-fidelity note](20261010_goal_information_solver_fidelity.md) and [ordered goal-error note](20261010_goal_stability_compositional_closure.md) remain valid within their stated model classes.

#### 1. Domain brief: what is now missing?

The MAP records: actual-law prospective 150/600 V command predictions; a qualified local Eth consistent chart with moving-event derivative; source-based K/Q and two-command summary tests; the larger-radius failure of the one-row fixed-Q summary; a well-performing one-Newton competitor. The earlier executable bridge covers *linear* all-word observability, *linear* ordered error transport and a *conditional* smooth implicit-solver bound. Two distinct mathematical gaps remain:

1. **Curved observation fiber:** even when `DG = B DO` and the *tangent* goal-visible hidden dimension is zero, can two admissible histories with exactly the same retained observation have different next-command goals at order `r^2`?
2. **Verified stage domain:** does a qualified Eth tangent and a list of successful trajectories suffice to carry an entire declared preparation neighborhood through subsequent guards/branches? It does not by itself. Can a small but mathematically genuine finite-stage enclosure be constructed?

**Evidence ledger.** Source-backed: the current MAP reports the above *model-level accepted evidence*; F049/F149/F360 and classical nonlinear-observability/DAE results state their own mathematical theorems. Inference: these proof structures suggest concrete tests on DPT `O,G,Eth` and stage intervals. Unknown: actual `D2O,D2G`, physical reachable-fiber tangent, certified BE remainder/guard tubes and real DPT finite-radius sharpness. These unknowns must be supplied by the local controller rather than invented here.

#### 2. Independent proposition A: second-order goal leakage on an observation fiber

Let `U` be an open neighborhood of a physically admissible **history-coordinate** `x0` in `R^n`. Let `O:U -> R^m` and scalar `G:U -> R` be `C^2`, with `1 <= m < n`, and assume `DO(x0)` has full row rank. Here `G` is the *fixed future command and goal*, not an arbitrary post-target readout. Suppose additionally that the first-order factorization **is exact**:

```math
DG(x_0)=b\,DO(x_0),\qquad b\in\mathbb R^{1\times m}.
```

Let `K=ker DO(x0)` and define the *observation-fiber goal Hessian* (quadratic form on `K`):

```math
\boxed{Q_{G\mid O}(v)=v^T\left[D^2G(x_0)-\sum_{i=1}^{m}b_iD^2O_i(x_0)\right]v,\qquad v\in K.}
```

**Claim (elementary local implicit-function consequence).** For any unit `v` in `K`, there is a local `C^2` curve `x(t)` through `x0` such that `O(x(t))=O(x0)`, `x'(0)=v`, and

```math
G(x(t))-G(x_0)=\frac12 Q_{G\mid O}(v)t^2+o(t^2).
```

If `Q(v) != 0`, no exact predictor depending only on the retained `O` can be correct for both `x0` and `x(t)`: the two-point minimax scalar error is at least `|Q(v)|t^2/4+o(t^2)`. Under the *Euclidean metric of the declared scaled history chart*, the greatest absolute second-order coefficient is

```math
\frac12\rho\bigl(K^T[D^2G-\sum_i b_iD^2O_i]K\bigr),
```

where columns of `K` form an orthonormal nullspace basis and `rho` means **maximum absolute eigenvalue**, not the stage-state radius. This is an *asymptotic coefficient*, **not** an unconditional finite-radius error bound. It does not prove the new variable needed for repair is minimal or an external sensor.

**Proof.** The constant-rank (submersion) theorem gives a local observation-level manifold. Pick its curve with prescribed tangent `v`. Twice differentiating `O(x(t))=O(x0)` gives `DO x''(0)+D2O[v,v]=0`. By exact factorization, `DG x''(0)=-b D2O[v,v]`. Twice differentiating the scalar goal yields exactly `Q(v)`. The Taylor expansion and two-point indistinguishability bound follow. Maximizing `|v^T M v|` on the unit sphere in `K` gives the spectral radius of the symmetric restriction `M` by the Rayleigh quotient. QED.

**Constructive tests.** (a) `O(x,y)=x`, `G(x,y)=x+y^2`: at `(0,0)` the first-order nullspace audit passes, yet the equal-observation histories `(0,0)` and `(0,t)` differ by `t^2` in goal. (b) `O(x,y)=x+y^2`, `G=x`: exact fiber `(-t^2,t)`, target difference `-t^2`. (c) `G=O` has zero curvature; (d) `G=x+y^3` also has zero *quadratic* curvature but is *not* sufficient—higher order cannot be dismissed. (e) `G=x+10^-9 y+y^2` fails exact first-order factorization even if a loose numerical tolerance would accept it; its linear leakage dominates for sufficiently small `t`.

**Executable:** [fiber_curvature_audit.py](../dpt_tools/fiber_curvature_audit.py) accepts `DO,DG,D2O,D2G`, verifies declared first-order factorization at a numerical tolerance and differentiability data consistency, returns the maximal hidden curvature and a tangent/second-derivative witness satisfying the level-set constraints. `QUADRATIC_WITNESS` is a **conditional mathematical candidate** dependent on exact identities, not a native DPT claim. `NEAR_FIRST_ORDER_FACTOR` prevents a small residual from masquerading as genuine second-order leakage. Full-row-rank/underflow failure refuses the submersion theorem. Mathematically nonzero curvature smaller than an absolute reporting tolerance may be classified as below threshold; that is no proof of its absence.

**Why DPT cares:** the fixed Q second row becoming important at larger preparation radii could come from `Q_{G|O}` along source-reachable directions; the alternative is a *different command-horizon tangent direction* (earlier `goal_word_quotient.py`), an event branch change, or merely increased numerical error. Distinguish them on the same source/command/goal with native-approved data. In particular the physical reachable preparation set may be a lower-dimensional submanifold. Compute derivatives **in a valid chart of that set** rather than using arbitrary 28-coordinate displacements.

#### 3. Independent proposition B: finite-stage box inclusion with certified envelopes as inputs

Let `B_k=[l_k,u_k]` be stage-valid state boxes in one common physical/scaled chart. For one frozen command sequence suppose **throughout** `B_k` the actual state map admits

```math
x_{k+1}=A_kx_k+b_k+r_k(x_k),\qquad |r_{k,i}(x_k)|\le \epsilon_{k,i}.
```

For any input box `[p,q] subset B_k`, define the interval image by coordinates

```math
\begin{aligned}
L_{k,i}
&=b_{k,i}+\sum_j\min(A_{k,ij}p_j,A_{k,ij}q_j)
-\epsilon_{k,i},\\
U_{k,i}
&=b_{k,i}+\sum_j\max(A_{k,ij}p_j,A_{k,ij}q_j)
+\epsilon_{k,i}.
\end{aligned}
```

**Finite-stage conditional inclusion theorem.** If the initial uncertainty box lies in `B0` and at each step `[L_k,U_k] subset B_{k+1}`, then every physically admissible trajectory satisfying these particular map/remainder contracts remains within the declared stage-valid boxes throughout the specified command sequence. Proof is induction using the exact affine coordinatewise extrema of a box and the separately justified remainder bounds. This is **not** F149 permanence, a uniform infinite-time invariant region, or a complete nonlinear SiC certificate.

**Why a failed check is not a counterexample:** after a stage, a box hull discards correlations. Example `x -> (x_1,x_1)` followed by `z=x_1-x_2` gives true `z=0` but interval hull allows `[-1,1]`. Failure says *the conservative certificate cannot qualify that domain*; it does not prove the physical state escaped.

**Executable:** [stage_box_reachability.py](../dpt_tools/stage_box_reachability.py) accepts ordered affine maps, offsets, initial bounds, stage-valid boxes and **externally certified** componentwise remainder radii. It returns the propagated hull, validated prefix length, first unqualified stage, and the smallest numerical margin to a guard (with a roundoff-level warning). Its `CONDITIONAL_AFFINE_BOX_CHAIN` status means **the exact-algebra containment conditions are met numerically under the supplied contracts**, not that floating-point calculations are verified outward-rounded interval arithmetic. A numerically marginal result requires outward interval evaluation before formal certification. No native evidence is claimed.

**Natural next DPT evidence:** from Sol9 Eth implicit lift, obtain a valid local coordinate continuation; on one frozen preparation tube, derive actual finite-range `A,b` and interval/remainder/guard bounds from the coupled BE equations rather than a single point Jacobian. If the interval hull fails, first preserve physical constraints using a polytope or zonotope before asking for new LTspice; do not react by choosing arbitrary larger boxes.

#### 4. Additional OpenAI Math deep reads and proof transfers

All OpenAI links below are pinned to `fd4aeeb2` and the papers are treated as preprints; selected Lean formalization scopes are recorded individually, not promoted to DPT.

| Family, primary manuscript and exact result | Useful proof idea / challenge | What would make it load-bearing in DPT? |
|---|---|---|
| **F049** [stable coordinate counterexample](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-stable-coordinate-that-is-not-a-coordinate-in-four-variables-October-5-2026/build/source/sections/01-introduction.tex), [explicit stabilization construction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-stable-coordinate-that-is-not-a-coordinate-in-four-variables-October-5-2026/build/source/sections/02-construction.tex) | Exhibits a complex polynomial that becomes a coordinate after adding an auxiliary variable but is not one in the original four variables; even affine-space fibers need not be ambiently straightenable. | Evidence that the proposed Eth/storage representation has a legal *physical* near-identity lift, rather than naming an augmented numerical chart a globally valid physical state. Algebraic counterexample is **not** a counterexample to actual DPT. [Lean selected scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/049.md) includes its explicit four-variable polynomial. |
| **F149** [finite affine trapping proof](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/build/sections/trapping.tex) | Uses finitely many affine barriers/plateaux, sign comparisons and monotonicity to establish trapping and eventual entry in weakly reversible mass-action networks. | Motivates a *different elementary* affine interval-box containment pilot in switching dynamics; F149 network theorems cannot certify it. Its [selected Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/149.md) covers the earlier persistence result, not automatically every stronger October assertion. |
| **F360** [weak-MTW to convex tangent injectivity domains](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Global-Support-and-Convex-Injectivity-Domains-under-Weak-MTW-September-25-2026/build/sections/introduction.tex) | Proves *specific* transverse cost curvature conditions imply global convexity on a Riemannian manifold; strong global inference requires a verified hypothesis, not scattered local tangents. | Suggests asking whether any actual DPT finite-radius valid domain has proven convex/monotonic geometry. Without an analogous condition, use conservative explicit guard boxes instead. [Lean scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/360.md) covers the specified convex-injectivity result. |
| **F334** [smooth metric without a local isometric immersion](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Smooth-Metric-with-No-Local-Isometric-Immersion-into-Three-Space-September-24-2026/build/main.tex) | A smooth metric can have the same *full* Taylor jet as Euclidean at a point and yet fail local smooth realization into 3D. | A sharp analogy for refusing to turn an Eth pointwise Taylor audit into a neighborhood representation without a continuation theorem. The result is about geometry, not DPT circuit states. |
| **F093** [log-Sobolev from subgaussian linear marginals](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-dimension-free-logarithmic-Sobolev-inequality-for-subgaussian-log-concave-measures-September-23-2026/build/sections/01-introduction.tex) | Dimension-free concentration requires a centered **log-concave distribution with all linear marginals subgaussian** as defined in the theorem. | An eventual stochastic noise-certified companion to deterministic radius analysis *only if* the preparation/noise distribution is measured and those hypotheses validated. Not used as an error bar now. No `lean/docs/093.md` was located at the inspected commit. |
| **F377** [infinity-harmonic interior C1-alpha regularity](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Uniform-Interior-C1alpha-Estimates-for-Infinity-Harmonic-Functions-October-4-2026/build/manuscript/sections/01-introduction.tex) | Provides `C^{1,alpha}` for **bounded infinity-harmonic functions**, not generic nonlinear maps. | Reminder that second derivatives must be explicitly available; generic `C1`/Holder systems do not license the Hessian test. WATCH until a valid differentiability model exists. No `lean/docs/377.md` found in this inspection. |

##### Source-audit and closest-prior subtraction

The OpenAI papers do **not** prove our two mathematical propositions. The fiber argument is classical submersion/implicit-function differential geometry and nonlinear observability; compare [Hermann–Krener 1977](https://doi.org/10.1109/TAC.1977.1101601). Stage box inclusion is elementary robust set propagation; compare [Della Rossa–Egidio–Jungers 2023](https://doi.org/10.1137/22M1482226) and [Cinto et al. 2025](https://doi.org/10.1137/24M1715520), which address harder switched-affine stability/controlled invariance questions. [Trenn 2012](https://doi.org/10.1007/978-1-4471-2885-4_6) describes mode consistency projection for linear switched DAEs. Our proposed DPT contribution is the verified **application and diagnostic role of the specific nonlinear observation-fiber curvature and stage-reachable tubes** using actual preparation and hybrid circuit equations. It is not novelty merely to name a Hessian or a box.

#### 5. Short roundtable stress test (simulated, sourced positions; NOT real quotations)

**Moderator's question:** Under the current S09 resource limit, is it more valuable to add an internal state, refine the full solver, or prove a range where the existing reduced state already works?

**Hermann–Krener lens (nonlinear observability; 1977, inference applied to DPT):** The lack of a goal-visible direction in a first-order matrix is a *local rank observation*, not a whole nonlinear input-output equivalence. Ask whether a curved observation fiber gives distinct future outputs for the same summary. The precise derivative and future command matter. [Source](https://doi.org/10.1109/TAC.1977.1101601).

**Trenn lens (switched-DAE mode consistency; 2012, inference applied to DPT):** Before interpreting a hidden direction as a physical mode, establish which variables are algebraic after Eth, which storage is continuous, and whether an implicit stage update is uniquely defined. A tangent in a forbidden or inconsistent DAE chart is not an admissible history. [Source](https://doi.org/10.1007/978-1-4471-2885-4_6).

**Krause lens (robust observation selection; 2008, inference applied to DPT):** Even a mathematically decisive witness is not automatically an economical sensor. Evaluate available readouts, shared prefix, acquisition costs and robustness across multiple actual goals; greedy selection guarantees require the assumptions of the chosen information objective. [Source](https://www.jmlr.org/papers/v9/krause08b.html).

**Round 1 crux:** *Rank deficiency or radius leakage* cannot be diagnosed before defining the legitimate physically reachable fiber. A no-extra-simulation check is: take the same native-qualified Eth/source chart and construct a candidate observation-equal perturbation. The second-order result is meaningful only when this perturbation remains admissible.

**Round 2 crux:** A physically admissible *point* is not a verified *domain*. The affine-box pilot supplies a conservative failure locator; if interval overapproximation fails because of correlated charge constraints, the next mathematics should be a polytope or manifold chart, not a larger solver budget.

```text
valid preparation chart + guard/DAE identities
               |
           JO, DG, Hessians ------> curved-fiber goal witness (lower information boundary)
               |
        qualified stage maps ------> finite-stage box containment (upper domain boundary)
               |                               |
      combined source-specific forecast / repair choice (controller only)
```

**Moderator synthesis:** The strongest two alternative hypotheses are (H1) a genuinely missing, goal-visible preparation direction and (H2) an incorrect/nonuniform stage chart or unqualified approximation region. The two audits discriminate them better than another generic fit refinement. They do not imply that one hypothesis is universally true, and no actual scientist is claimed to have spoken about this SiC project.

#### 6. Controller replay gate and rejection outcomes

1. **Same physical source/branch:** obtain valid preparation-parameter coordinates, recorded fixed commands/goals, and complete `O/G` derivative mapping; exclude future outcome data from prediction inputs.
2. **Curvature attack:** run `fiber_curvature_audit.py` on physically reachable chart derivatives. Compare its predicted hidden tangent with archived finite perturbation/goal contrasts; explicitly test first-order leakage and event-branch conditions. If the Hessians are unavailable or charts nonsmooth, record the missing math contract, not an inferred result.
3. **Finite-stage tube attack:** on a *frozen* valid prefix and command sequence, derive `A_k,b_k`, stage boxes, all-coordinate true residual envelopes and guard domains from actual BE storage/constraint law. Run `stage_box_reachability.py`. If the box fails due to correlation, test an exact constrained reachable set/polytope rather than reclassifying native evidence as invalid.
4. **Decision fork:** a nonzero qualified curvature suggests a **local information repair** candidate. A valid small box and certified small solver residual suggest a **cheaper model/solver** regime. Both failing suggests domain/representation needs repair before any new acquisition. Include full/affine/one-Newton ordinary rivals and the current 600 V path qualification.
5. **Formal acceptance:** no automatic modification of S09 freeze, native model claim, extra LTspice, or active owner lane. The local controller decides which math deltas are scientifically material.

**Evidence status:** analytical theorem(s) independently reconstructed; original OpenAI sources read at theorem/proof-architecture level; 23 synthetic/analytic tests including randomized vertex cross-check, numerical margin guard and CLI/compile checks passed locally; actual DPT source Hessians and stage-valid remainder boxes remain unknown. These tools are reusable mathematical probes and **not** native validations.


## 2026-10-20 Q4: saved N100 window-sensitive rank reversal and prospective condition challenge

**Retrospective, actual saved vendor-model 100 V result; no new native execution.** Local authority locator: /power-semiconductor/run/S03_heldout_recovery/development_scout/native_finite_L_mechanism/prep_response_transfer/current_conditioned_curvature/{forecast_freeze.json,result.json,report.md,analysis.py}. The worker and prime inspected the original saved result.json and its fixed scorer boundaries read-only. Contract: 100 V, B-history T1 1.75–6 us and T2 7–8 us, Rg=7.5 ohm, 25 °C, load 150 uH, L_ext=5.25 nH; recorded external V(D_L,S_L)/I(V_J5_JUMPER), 641-node nonfiltered H=[7.115,7.155] us. Errors are actual minus frozen prediction, in pJ.

| Scorer window/path | Shared-curvature profile | Current-scaled profile |
| --- | ---: | ---: |
| Full H, fine | -1.635193 | +8.868157 |
| Full H, H2 | -1.293533 | +8.546443 |
| Leading [7.115,7.124379] us, fine | -7.858822 | -0.014794 |
| Leading [7.115,7.124379] us, H2 | -7.289456 | +0.145704 |

The error ranking reverses on the *same frozen predictions and equal observation information* when the declared future signed-work functional is changed from full H to the fixed leading subwindow. Full H shared-curvature near-zero work residual results partly from cancellation of leading negative and later positive contributions (source report fine two-cycle core +6.393182 pJ, trailing -0.170401 pJ). This is a concrete **retrospective falsifier of window-uniform dominance**, not a new held-out condition, a hardware L_eff/R_eff recovery or source-wide guarantee. The current-scaled scalar-work ordinary is a distinct comparator and must not be confused with the current-scaled **profile** in this table. Numerical H2-vs-fine differences are path/scorer movements, not a validated TOTAL_ERROR bound.

**One decision-changing future trial.** After Main freezes and qualifies an actual E-history command (T1-on 1.5 us, with the true T1-off/T2 timing), select 100 V, Rg=7.5 ohm, 25 °C, load 150 uH and L_ext=5.25 nH own-PREP, conditioned on **new source-valid E-history 150 uH endpoint records L_ext=5.0 and 5.5 nH**, original E 100 uH mid/endpoint records and no target leakage. Freeze baseline simple scalar-work endpoint/old-history curvature, shared-profile curvature, current-scaled-profile curvature, and the fully recorded-command/full-wave ordinary on the EXACT same CAL/measurement budget. Compare original signed work over Full H plus predeclared disjoint leading/cycle1/cycle2/trailing windows on both fine/H2 paths; require winning margins larger than independently qualified sensor/clock/numerical/model discrepancy bound to claim information improvement. A full-window win alongside a predeclared leading failure is a meaningful NEGATIVE predictive result. The new 150 uH E endpoints, exact command/target event identity, source qualification and frozen TOTAL_ERROR are not available in the remote Math repository: the prospective experiment remains OPEN and is not authorized by this mathematical note to run native jobs or reveal truth.

**Measurement object boundary.** Rproj and Lproj in Original R1 are coefficients of a declared residual-port projection onto (i_res,di_res/dt), which depend on the measurement operator and calibration. The forward model's manipulated L_ext is a coordinate, not automatically measurement-defined package/PCB parasitics. The saved N100 V(D_L,S_L)/J5 work scorer does not supply the residual cut, raw current derivative, joint clock/gain/PREP error or calibrated projection operator needed to certify recovery of that effective object.


**New E150 pretarget numeric challengers (NOT a new-condition source execution or genuine freeze).** Read-only, separately hash-pinned saved vendor-model 100V records have historical signed H-work [fine,H2] in nJ: B100=[62.411894937103,62.387342991745], E100=[69.662348603357,69.641430064909], B150=[28.034528346669,28.006415530245]. Let Delta=W(E100)-W(B100)=[7.250453666254,7.254087073164]nJ and candidate P(k)=W(B150)+k*Delta, for k=1, r, q. Here r=[.668202753730,.668197452468] is the H-grid arithmetic-mean load-current ratio at L5.0, whereas q=[.449185662043,.448911817481] is the B150/B100 L5.25 work ratio. The prospective candidate family is fine [35.284982012924,32.879301452254,31.291328176857]nJ and H2 [35.260502603410,32.853578032515,31.262860942426]nJ. These are arithmetic alternatives, not observed E150 target results or a frozen E150 predictor. Source-valid E150 5.0/5.5nH endpoint CAL, complete exact command/event identity, target blackout, lawful ownPREP, strongest same-data ordinary and TOTAL_ERROR are still missing. Score 1000*(W_target_nJ-P_nJ) pJ only AFTER a legitimate new target. No new native simulation, protected truth or physical effective R/L inference follows.
