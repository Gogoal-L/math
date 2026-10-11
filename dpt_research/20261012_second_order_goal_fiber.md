# Second-order goal recovery along a regular nonlinear observation fiber

**Date:** 2026-10-12. **Status:** independent, source-aware deterministic derivation, analytical falsifiers, executable linear-algebra auditor and synthetic tests. **Not** a new universal mathematical theorem, native SiC replay, proof of hardware noise or post-hoc score promotion.

Companion: [DPT Math main MAP](../DPT_MATH_RESEARCH_MAP.md) equations M40–M49; [fiber_goal_curvature.py](../dpt_tools/fiber_goal_curvature.py); [12 tests](../dpt_tools/test_fiber_goal_curvature.py).

## A. Prior work and exact conceptual separation

- J. N. Neuberger, A. Alexanderian, B. van Bloemen Waanders, *Goal oriented optimal design of infinite-dimensional Bayesian inverse problems using quadratic approximations* (arXiv:2411.07532v1, 2024), [primary full text](https://arxiv.org/html/2411.07532): the **quadratic goal Hessian** contributes to a Bayesian-Gaussian goal-oriented sensor-selection criterion (Gq-optimality). The work reports stronger designs than linearized c-optimality in its own studied PDE examples. It **does not** prove the deterministic minimax fiber formula below.
- S. Zhong, W. Shen, T. Catanach, X. Huan, *Goal-Oriented Bayesian Optimal Experimental Design for Nonlinear Models Using Markov Chain Monte Carlo*, [SIAM/ASA Journal on Uncertainty Quantification, DOI 10.1137/24M1649344](https://doi.org/10.1137/24M1649344): considers QoI expected information gain for **nonlinear observation and QoI models**, estimated by nested Monte Carlo. Bayesian information gain is distinct from the **hard bounded-error radius** derived here.
- The constrained Hessian / Lagrange-multiplier restriction to a regular level set follows classical implicit-function calculus. No originality claim is attached to that identity. The contribution **for this project** is the explicitly scoped goal-minimax coefficient, third-derivative gap, future-command Hessian pullback, and executable DPT-boundary/falsifier chain.
- Independent power-device metrology caution: Tiwari et al., *Design considerations and laboratory testing of power circuits for parallel operation of silicon carbide MOSFETs*, 2015, [Chalmers record / DOI 10.1109/EPE.2015.7309165](https://research.chalmers.se/en/publication/237572): measured current and overvoltage can reflect probe and inductor artifacts. The goal/observation definitions and sensor nuisance terms cannot be inferred from a mathematical Hessian test.

## B. What is held fixed

Let $h_0$ belong to a single **source-reachable** history/state manifold in a specified DPT reference. Let $O:\mathbb R^n\to\mathbb R^m$ be the exact **external pretarget observation**, and let $G_w:\mathbb R^n\to\mathbb R$ be the prescribed scalar goal **after a frozen, legally executed future command word** $w$. Assume both are $C^3$ on an adequately small chart with **no guard/branch changes**.

Assume $DO(h_0)$ has full row rank $m\le n$. Let $Z\in\mathbb R^{n\times (n-m)}$ have orthonormal columns spanning $\ker DO(h_0)$. The local level set $O(h)=O(h_0)$ is a smooth $(n-m)$-dimensional manifold by the submersion theorem. We consider a **specific chart-ball of legal states**, not all independent ambient perturbations:

$$
h(v)=h_0+Zv+Uq(v),\quad
\|v\|_2\le r,\quad
DO(h_0)U=I_m,\quad
q(0)=Dq(0)=0.
\tag{C1}
$$

Here $U$ is an exact right inverse and $q(v)$ is fixed by $O(h(v))=O(h_0)$. The domain claim explicitly includes that the entire chosen compact chart-ball is physically legal. A tangent vector alone cannot prove that.

If $DG_w(h_0)Z\ne0$, a **first-order** obstruction already exists and the second-order-only claim below is not the leading one. Focus on the apparently reassuring case $DG_w(h_0)Z=0$. Because $DO$ is surjective, this is equivalent to a unique multiplier $\lambda$ with

$$
DG_w(h_0)=\lambda^\top DO(h_0).
\tag{C2}
$$

## C. Correct constrained Hessian, with full derivation

Differentiate the exact fiber constraint twice at $v=0$:

$$
DO(h_0)\,D^2h(0)[a,a]
+D^2O(h_0)[Za,Za]=0.
\tag{C3}
$$

Differentiate $G_w(h(v))$ twice, and apply (C2)–(C3):

$$
\begin{aligned}
D^2(G_w\circ h)(0)[a,a]
&=D^2G_w(h_0)[Za,Za]\\
&\quad+DG_w(h_0)\,D^2h(0)[a,a]\\
&=D^2G_w(h_0)[Za,Za]\\
&\quad-\lambda^\top D^2O(h_0)[Za,Za].
\end{aligned}\tag{C4}
$$

Therefore the **actual fiber Hessian** in orthonormal tangent coordinates is

$$
Q_w=Z^\top\left(
D^2G_w(h_0)-\sum_{j=1}^{m}\lambda_jD^2O_j(h_0)
\right)Z.
\tag{C5}
$$

This object cannot in general be replaced by $Z^\top D^2G_w Z$: the observation map may curve in exactly the same source directions as the goal. Orthogonal changes of tangent coordinates conjugate $Q_w$ and leave its eigenvalues and minimax coefficient invariant. **An arbitrary nonlinear reparameterization with non-orthonormal coordinates does not preserve the eigenvalues** without also transforming the declared norm ball.

## D. The leading local deterministic minimax radius is exactly a Hessian spectral range

Set $\widetilde g(v)=G_w(h(v))$. Under (C2) its first derivative vanishes at the origin. Taylor's theorem gives, with a real **supremum bound M on the third derivative of the composite exact-fiber function $\widetilde g$** on the chart-ball,

$$
\widetilde g(v)
=G_w(h_0)+\tfrac12 v^\top Q_wv+\mathcal E_3(v),
\quad |\mathcal E_3(v)|\le \frac M6\|v\|_2^3.
\tag{C6}
$$

The actual source third-derivative bound is **not** the raw ambient $D^3G_w$ alone; it includes nonlinear observation-fiber curvature and the future command $T_w$, with correct physical scaling.

At the *fixed observation* $O(h_0)$, all legal histories $h(v)$ have identical external data, so an optimal scalar decoder returns the midpoint of the range of $\widetilde g(v)$; its error equals half the range diameter. For the quadratic part, diagonalize the real symmetric $Q_w$, and define

$$
s_+=\max(0,\lambda_{\max}(Q_w)),
\qquad s_-=\min(0,\lambda_{\min}(Q_w)).
\tag{C7}
$$

Because the tangent domain is a **ball**, the center $v=0$ is feasible, so the maximum and minimum of the quadratic form are exactly $\tfrac12r^2s_+$ and $\tfrac12r^2s_-$ (not simply $r^2\lambda_{\max}/2$ when $Q_w$ is negative definite). Thus

$$
\boxed{R_2(r)=\frac{r^2}{4}(s_+-s_-).}
\tag{C8}
$$

If two functions differ uniformly by at most $\delta$, each of their maxima and minima differs by at most $\delta$, hence their half-range minimax radii differ by at most $\delta$. Set $\delta=Mr^3/6$ to obtain the **two-sided, sharp-to-leading-order conditional bound**

$$
\boxed{
\max(0,R_2(r)-Mr^3/6)
\le R_{\rm fiber}(r)
\le R_2(r)+Mr^3/6.
}
\tag{C9}
$$

This is **exact for quadratic goals on quadratic fibers with vanishing composite third derivative**. It makes the earlier MAP M32 example an instance rather than the whole method. Since the global admissible observation fiber may be larger than the chosen chart ball, the lower bound in (C9) transfers to the **whole** admissible class, but the upper bound does not unless the whole compatible class is covered.

Even if bounded sensor noise enlarges the compatibility class, zero-error observations remain allowed in the standard bounded-noise model; the lower bound survives. The upper bound must then account for *all compatible noisy states* separately, e.g. with a certified nonlinear readout-gain budget.

## E. Three exact counterexamples and what each rejects

**(E1) Observation curvature creates hidden goal variation.**
Take $O(x,y)=x+y^2$ and $G(x,y)=x$, at $(0,0)$. Then
$DO=DG=(1,0)$, but $D^2O|_y=2$, $D^2G|_y=0$. The exact observation fiber is $x=-y^2$. Thus $Q=-2$, and within the legal local chart $|y|\le r$,

$$
\boxed{R_{\rm fiber}(r)=r^2/2,\quad\text{despite }DG|_{\ker DO}=0.}
\tag{C10}
$$

A naive Hessian-of-goal-only audit would falsely report zero. The relative Hessian correctly reports a nonzero $r^2$ obstruction.

**(E2) Observation curvature cancels goal curvature.**
Keep $O=x+y^2$ but set $G=x+y^2=O$. The goal is **already exactly measured**, so $R_{\rm fiber}=0$ (for exact observation). Here $D^2G|_y=2$ is positive, but $Q=2-2=0$. A naive Hessian-of-goal-only audit would falsely report a nonzero ambiguity.

**(E3) A new nonlinear sensor can be valuable despite zero Jacobian.**
Start with $O(x,y)=x$ on $|y|\le r$, and choose $G(y)=y^2$. A *hypothetically legal pretarget* calibration sensor reading $P=y^2+e$, with deterministic $|e|\le\epsilon$, is sufficient to estimate this particular goal. At the nominal center $DP(0)=0$, so first-order sensor-rank testing says the candidate adds nothing. Nevertheless, direct compatible-interval analysis gives

$$
\boxed{R_{\rm after\ P}=\min(\epsilon,r^2/2).}
\tag{C11}
$$

Proof: all goal values q lie in $[0,r^2]$. Given a possible sensor reading p, the compatible q interval is $[0,r^2]\cap[p-\epsilon,p+\epsilon]$. Its longest possible diameter is $\min(r^2,2\epsilon)$, so the optimal midpoint decoder has radius exactly half this diameter.

For a **future** DPT work goal, measuring future work before the future command is not available. $P=y^2$ here is an abstract proxy available *before* the future target; real acquisition proposals must show a physical CAL observable with this information structure. It also does not recover the **sign** of y, so it would not recover a signed future goal G=y.

A fourth caution: if $Q=0$ but $\widetilde g(v)=\alpha v^3$, the leading $r^2$ term vanishes yet exact minimax radius is $|\alpha|r^3$ on $[-r,r]$. Therefore **second-order zero is not nonlinear goal sufficiency** without a higher-order/remainder contract.

## F. Dynamic goal Hessian pullback across legal ordered commands

For a single smooth legal source update $x_+=f_u(x)$ and a scalar future goal $g_+$ defined on its output, denote the source Jacobian $J_u=Df_u(x)$ and component Hessians $H_{u,j}=D^2(f_u)_j(x)$. Define $g(x)=g_+(f_u(x))$. Then the exact source derivative transport is

$$
\begin{aligned}
Dg(x)&=J_u^\top Dg_+(x_+),\\
D^2g(x)
&=J_u^\top D^2g_+(x_+)J_u\\
&\quad+\sum_j [Dg_+(x_+)]_jH_{u,j}.
\end{aligned}\tag{C12}
$$

The second line is critical. A **linear final engineering goal** has zero terminal Hessian, but nonlinear dynamics can generate nonzero Hessian relative to the *earlier history*. Repeat (C12) from the last command back toward preparation, using **each stage's legally reached source point**. This is not simply multiplication of all single-stage Jacobians or arbitrary commutation of commands.

An exact two-command check: first $f_A(x,y)=(x+\alpha y^2,y)$, then $f_B(X,Y)=(X,Y+\beta X^2)$, and finally $G_{\rm final}(X',Y')=Y'$. The precommand goal is

$$
\widetilde G(x,y)=y+\beta(x+\alpha y^2)^2.
\tag{C13}
$$

Direct differentiation and two uses of (C12) both yield

$$
D^2\widetilde G=
\begin{pmatrix}
2\beta &4\alpha\beta y\\
4\alpha\beta y&4\alpha\beta(x+\alpha y^2)+8\alpha^2\beta y^2
\end{pmatrix}.
\tag{C14}
$$

The automated tool uses [pullback_goal_derivatives](../dpt_tools/fiber_goal_curvature.py) and an independent analytic polynomial oracle in its tests. Unlike F129's full relation-alphabet exponential theorem, this is ordinary finite-dimensional calculus used for finite **source-qualified** command words.

The rank and curvature check for a future command now uses $DG_w$ and $D^2G_w$ pulled back to the **same preparation coordinates** as $DO,D^2O$ and evaluated under the **same reference**. A change of stage guard/event winner may invalidate the smooth source map; then a piecewise or nonsmooth goal bound, not (C12), is needed.

## G. Best physical next discriminating experiment, not a paper claim

For a single 150-V Pro18B/C actual-law reference or the distinct original R1 at 100 V:

1. Fix source law, terminal/window definitions for future signed work, peak VDS value and event time, and a legal preparation/command set. Document all directly acquired pretarget VDS/current/gate/CAL data, sensor nuisance and units.
2. Produce a regular, source-reachable observation center with a nonzero **legal fiber chart**. Differentiate the *actual* external observation and *same-reference* future goal, including command curvature via (C12). Rescale states so the declared Euclidean tangent radius has a physical interpretation.
3. If $DG_wZ$ is nonzero, first-order predicted ambiguity dominates; otherwise compute **relative** $Q_w$. Obtain legal source re-shooting of two histories with identical/qualified near-identical observations along the predicted extreme eigen-directions.
4. Compare *prospective* goal gaps to $R_2\pm Mr^3/6$ only if M was actually bounded on the entire chart. Compare against a strong ordinary based on recorded full command, valid direct switching regression and source-based one-Newton; test separately whether prediction improves for work, peak and event-time.
5. If Q is small or zero, check higher-order and finite-noise ambiguity before claiming sufficient information. If true CAL changes the physical state, use the withheld-vs-observed CAL comparison with the *same* CAL-executed future physics (see main MAP M28–M29).

**Risk/falsifier:** the source observation may fail the rank/regularity condition, the legal chart may collapse at a mode guard, a physical CAL proxy may be unavailable, or a well-specified ordinary may already reach the target tolerances. Those outcomes bound the role of this second-order object rather than invalidate the conditional calculus.

## H. Verification and hard limits

- The executable matrix auditor [fiber_goal_curvature.py](../dpt_tools/fiber_goal_curvature.py) checks full-row-rank, tangent goal-gradient factorization, Hessian symmetry, relative Q eigenvalues, r²/4 radius, and outputs a numeric interval **only** when a uniform composed-fiber third derivative bound M is supplied.
- [12 tests](../dpt_tools/test_fiber_goal_curvature.py) include exact linear-goal hidden nonlinear observation, cancellation, positive/negative Hessian modes, 120 synthetic cubic exact-fiber cases, invalid regularity, and a two-stage command-pullback polynomial oracle. They prove software behavior on these fixtures, not a universal theorem or source physical truth.
- Assumed $C^3$ charts and uniform M do **not** follow from one finite-difference Hessian or a green MathJax syntax check. For the actual device, derive local derivatives and uniform bounds from the source residual (implicit differentiation/validated interval calculations), correct prepared state and legal guard branches.


## I. Direct implicit source-law bridge: adjoint Hessian without forming explicit f

**Why this matters for the actual DPT project.** The supplied *IH2662 DPT Research Design V6* §4.7 and §6.5 describe a coupled backward-Euler source residual with current/previous diode stored charge, conduction, network and thermal equations. Other stages use trapezoidal source updates. The future-goal Hessian (C12) cannot be assumed known: computing derivatives of an explicit multi-stage update f may be costly or misleading if source signs/current-before-next conventions are wrong. The following formula supplies a pointwise **exact implicit** route, without claiming the whole source has been differentiated yet.

Fix one legal command u and a regular source pair (z,x) satisfying F(z,x;u)=0. For clarity both z and x have n coordinates (a real BE evaluator must map its own actual coordinate chart and time step). Let

$$
A=F_z,\qquad B=F_x,\qquad J=-A^{-1}B,\qquad A J+B=0.
\tag{C15}
$$

The implicit function theorem gives z=f(x) near that root when A is invertible. Let g(z) be the goal after this step and solve the **source adjoint**

$$
A^\top\lambda=\nabla g(z).
\tag{C16}
$$

For any old-state tangent vectors a,b, define complete residual directions $\widetilde a=(Ja,a)$ and $\widetilde b=(Jb,b)$, in the concatenated coordinates (next z, previous x). Differentiate F(f(x),x;u)=0 twice:

$$
A\,D^2 f[a,b]+D^2F(z,x;u)[\widetilde a,\widetilde b]=0.
\tag{C17}
$$

The second derivative of the postcommand scalar goal, **including current/previous coupling**, is then

$$
\boxed{
\begin{aligned}
D(g\circ f)&=J^\top\nabla g,\\
D^2(g\circ f)[a,b]
&=(Ja)^\top D^2g(z)(Jb)\\
&\quad-\lambda^\top D^2F[\widetilde a,\widetilde b].
\end{aligned}
}\tag{C18}
$$

The minus sign arises from the source residual differentiation. **It does not equal simply $J^\top D^2g\,J$** except when the source residual has zero second variation on the legal directions (or the adjoint kills it).

The weighted source Hessian includes four physically distinct blocks $F_{zz},F_{zx},F_{xz},F_{xx}$. In particular **retaining only $F_{zz}$ misses old charge, preparation memory and cross derivatives**, even if g is linear. The code [implicit_goal_hessian.py](../dpt_tools/implicit_goal_hessian.py) accepts precisely these full derivatives in concatenated [z,x] order and returns both gradient and Hessian in previous-state coordinates. A matrix-free source implementation would use adjoint-weighted Hessian-vector products to avoid materializing F2.

### Sharp ordinary counterexample: current–previous mixed Hessian alone

For an exact scalar nonlinear discrete source equation

$$
F(z,x)=z+\kappa zx-x=0,\qquad
z=f(x)=\frac{x}{1+\kappa x},\quad 1+\kappa x\ne0,
\tag{C19}
$$

take a *linear* terminal goal g(z)=z. Here $F_{zz}=F_{xx}=0$, but $F_{zx}=F_{xz}=\kappa$, and exact differentiation gives

$$
\frac{d}{dx}g(f(x))=\frac{1}{(1+\kappa x)^2},
\quad
\frac{d^2}{dx^2}g(f(x))
=-\frac{2\kappa}{(1+\kappa x)^3}.
\tag{C20}
$$

A Hessian transport that kept only $F_{zz}$ and $F_{xx}$ would incorrectly report **zero source curvature**, despite the exact nonzero result. This mechanism is not a claim that a vendor SiC branch has precisely z+κzx; it is an **adversarial analytic circuit-like residual** showing why the cross-block cannot be dropped from the *general* method.

### Actual V6 diode law: curvature formula and scope

For fixed temperature/emission thermal scale a>0, fixed τ>0, and known time step h>0, the actual V6 BE diode-residual component is (up to the declared source sign conventions)

$$
F_D=i_b-I_s(e^{v_n/a}-1)
-\frac{\tau I_s}{h_n}\bigl(e^{v_n/a}-e^{v_{n-1}/a}\bigr).
\tag{C21}
$$

Its **isolated diode current/charge contribution** has second derivative entries

$$
\begin{aligned}
(F_D)_{v_nv_n}
&=-\frac{I_se^{v_n/a}}{a^2}(1+\tau/h_n),\\
(F_D)_{v_{n-1}v_{n-1}}
&=+\frac{\tau I_s e^{v_{n-1}/a}}{h_na^2}.
\end{aligned}\tag{C22}
$$

Even this simple model contributes with **opposite signs** at current and previous steps; dropping previous stored charge violates its source law. Further mixed derivatives can arise from the rest of the full coupled BE residual (and from T-dependence of Is and a), so the stand-alone diode entries are **not** a complete DPT Hessian. Under uniformly bounded source/goal operators on a shared legal chart, (C18) immediately provides a conditional estimate

$$
\|D^2(g\circ f)\|
\le\|J\|^2\|D^2g\|
+\|\lambda\|\,\|D^2F\|(1+\|J\|^2).
\tag{C23}
$$

The numerical Jacobian/adjoint condition number must be included in error propagation; if F_z becomes near singular, a pointwise float Hessian need not have a useful finite-radius uniform bound.

**Independent verification:** analytic tests for (C19)–(C20), an implicit nonlinear current+previous scalar residual, a two-state quadratic command, and 200 random exactly specified quadratic maps represented through an invertible implicit residual all matched the source-free explicit chain rule. This validates the algebra and program on those fixtures, not the actual Wolfspeed/TRAP/BE vendor source.

**Source-level acquisition required to close the loop:** actual executable F(z,x;u) and correct frozen command; measured source-consistent preparation/state chart; analytic/AD/validated finite-interval F_z,F_x,F_zz,F_zx,F_xx; goal g(z) or full stage work/readout including guard/event terms; and uniform implicit invertibility and third-derivative bounds on one physically legal history fiber. These feed (C5)–(C9) to decide the engineering goal radius *without* claiming recoverability of all parasitic inductances.
