> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/374.md).

# Sharp one-third stability of Brenier maps

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Sharp One-Third Stability of Brenier Maps](../F374_Brenier_one_third_stability.pdf)

## Scope

The formalization proves one-third Hölder stability of Brenier maps from the uniform measure on a compact convex body with nonempty interior in $\mathbb R^d$, for every $d\ge2$. For targets supported in one fixed nonempty compact set, the $L^2$ distance between the unique quadratic optimal maps is at most a constant times the one-third power of the targets' $2$-Wasserstein distance. The constant is uniform over those targets.

It also proves optimality of the exponent: on a fixed cube, pairs of three-atom target measures violate every analogous bound with exponent greater than $1/3$. In particular, the conjectured uniform square-root estimate fails.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| One-third stability of Brenier maps and sharpness | [Brenier.lean](F374_Brenier.lean) |
