> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/229.md).

# Exact three- and four-state reconstruction thresholds and four-state tree capacity

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [The exact reconstruction threshold for the three-state symmetric channel](../F229_three_state_reconstruction.pdf)

## Scope

The formalization proves the supercritical direction of reconstruction for the symmetric three-state broadcast channel, whose parameter satisfies $-1/2\le\lambda\le1$. On a regular $b$-ary tree, reconstruction holds when $b\lambda^2>1$; on an observed Poisson Galton–Watson tree of mean $d$, it holds when $d\lambda^2>1$. In each case the root-estimation advantage converges to a positive limit, with the Poisson advantage averaged over trees and spins.

The selected statements cover reconstruction above the Kesten–Stigum threshold. Non-reconstruction at or below the threshold and the stochastic-block-model consequences in the paper are outside them.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Supercritical reconstruction on regular and Poisson trees | [ThreeStateSupercritical.lean](F229_ThreeStateSupercritical.lean) |
| Three-state reconstruction above the Kesten–Stigum threshold | [ThreeStateTreeClauses.lean](F229_ThreeStateTreeClauses.lean) |
