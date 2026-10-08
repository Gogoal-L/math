> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/098.md).

# Compact counterexamples to bi-Lipschitz dimension reduction

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [A doubling Hilbert subset with no finite-dimensional bi-Lipschitz embedding](../F098_doubling_Hilbert_embedding_obstruction.pdf)

## Scope

The formalized result gives a doubling subset of real $\ell_2$, with doubling constant at most $76800$, that admits no bi-Lipschitz embedding into any finite-dimensional Euclidean space at any finite distortion. A companion gives one universal doubling constant such that every infinite-dimensional real Banach space contains a compact doubling subset with no bi-Lipschitz embedding into any finite-dimensional normed space.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Doubling Hilbert subset without finite-dimensional embedding | [DoublingHilbert.lean](F098_DoublingHilbert.lean) |
| Compact counterexamples in infinite-dimensional Banach spaces | [CompactBanach.lean](F098_CompactBanach.lean) |
