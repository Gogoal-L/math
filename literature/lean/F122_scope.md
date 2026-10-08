> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/122.md).

# Quantitative trace-reconstruction bounds with a uniform decoder

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Quantitative lower bounds for trace reconstruction](../F122-B_trace_reconstruction_lower_bound.pdf)

## Scope

The formalization proves superpolynomial sample lower bounds for exact worst-case reconstruction of binary words from independent deletion traces, with unrestricted computation and any fixed positive success probability. For every fixed deletion probability $q\in(0,1)$, sample complexity grows faster than every fixed power of the word length; the minimum total-variation distance between two one-trace laws decays faster than every inverse power.

More quantitatively, along sequences with $q^3\log n\to\infty$, the required number of samples is at least $n^{c\log(q^3\log n)}$ eventually for every fixed $0<c<1/(4\log2)$. All logarithms are natural.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Quantitative and superpolynomial sample lower bounds for trace reconstruction | [TraceReconstruction.lean](F122_TraceReconstruction.lean) |
