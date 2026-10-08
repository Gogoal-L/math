> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/289.md).

# Strong Kadison–Kastler stability and its spatial boundaries

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Universal strong Kadison–Kastler stability](../F289-A_strong_Kadison_Kastler_stability.pdf)

## Scope

The formalization proves the strong Kadison–Kastler conjecture uniformly. For every $\varepsilon>0$, there is a $\delta>0$ such that any two unital von Neumann algebras on the same complex Hilbert space at Kadison–Kastler distance below $\delta$ are conjugate by a unitary $u$ with $\lVert u-1\rVert<\varepsilon$. The tolerance depends only on $\varepsilon$, uniformly over the algebras, their representations, and the Hilbert space.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Universal near-identity unitary conjugacy for close von Neumann algebras | [StrongKadisonKastler.lean](F289_StrongKadisonKastler.lean) |
