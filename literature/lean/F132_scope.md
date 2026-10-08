> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/132.md).

# A superquadratic separation of sensitivity and block sensitivity

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [A superquadratic separation between sensitivity and block sensitivity](../F132_sensitivity_block_sensitivity_separation.pdf)

## Scope

The formalized result disproves a universal quadratic bound of block sensitivity by sensitivity for total Boolean functions. For every integer $d\ge1$, it constructs a nonconstant function with $\mathrm{bs}(f)/s(f)^2\ge2^d/(4(d+2)^2)$, making the ratio unbounded. The formalization also gives a fixed exponent $\alpha>2$ and a sequence with $s(f)^\alpha\le\mathrm{bs}(f,0)$ while the latter tends to infinity; here $\mathrm{bs}(f,0)$ is block sensitivity at the all-zero input.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Superquadratic sensitivity separation | [SensitivitySeparation.lean](F132_SensitivitySeparation.lean) |
