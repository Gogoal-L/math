> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/266.md).

# Exactly three mutually unbiased bases in dimension six

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [The maximum number of mutually unbiased bases in dimension six](../F266_dimension_six_MUB_certificate.pdf)
- [Exact Fourier certificates for complex Hadamard matrices of order six](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026.pdf)

## Scope

The paper claims that at most three mutually unbiased orthonormal bases exist in $\mathbb C^6$. The linked formalization proves a weaker family bound: every family in its mutually unbiased bases model has at most five members. It also proves a Fourier character-sum vanishing statement for order-six complex Hadamard matrices not equivalent to the Tao matrix, uniformly over coordinate permutations.

The selected statement does not establish the paper's upper bound of three or its computer-assisted exclusion of four arbitrary bases.

The linked formalization proves a cancellation lemma used in the order-six complex Hadamard analysis. Let $H$ and its entrywise square both be complex Hadamard matrices, and fix two distinct rows. If the cubes of their six entrywise ratios take only two distinct values, then the sum of the row-ratio terms over either specified cube fiber is zero.

This is a supporting Fourier cancellation statement. The paper's full character-sum vanishing theorem and its mutually unbiased bases bound are outside this selected statement.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Order-six Hadamard Fourier vanishing and a five-basis upper bound | [MUBSix.lean](F266_MUBSix.lean) |
| Cube-fiber cancellation for order-six Hadamard row ratios | [HadamardCubeFiber.lean](../../literature_archive/lean/F266_HadamardCubeFiber.lean) |
