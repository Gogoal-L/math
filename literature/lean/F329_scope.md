> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/329.md).

# A counterexample to metric-entropy duality

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Counterexamples to the duality conjecture for metric entropy](../F329_metric_entropy_duality_counterexample.pdf)

## Scope

Metric-entropy duality predicts a universal comparison between covering numbers of convex bodies and their polars. The formalized result disproves such a comparison: for every $a,b\ge1$, there is an origin-symmetric convex body $K$ in a positive finite dimension with $\log N(K,B_\infty)>b\log N(B_\infty^\circ,a^{-1}K^\circ)$, where $N$ is the least number of translates in a finite cover. A further construction makes the dual-to-primal logarithmic entropy ratio tend to zero as the dimension grows.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Counterexample to metric-entropy duality | [MetricEntropyDuality.lean](F329_MetricEntropyDuality.lean) |
