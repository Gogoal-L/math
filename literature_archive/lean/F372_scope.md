> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/372.md).

# Global uniqueness in smooth isotropic elasticity

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Global Uniqueness for the Smooth Isotropic Elasticity Inverse Problem](../F372_smooth_isotropic_elasticity_uniqueness.pdf)

## Scope

The formalization proves global uniqueness in the three-dimensional static isotropic elasticity inverse problem. On a bounded connected smooth domain, let two pairs of smooth real Lamé moduli satisfy $\mu>0$ and $3\lambda+2\mu>0$ on the closure. If their full displacement-to-traction maps agree, then both Lamé moduli agree throughout the domain. The selected statement is uniqueness; it does not supply a reconstruction algorithm.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Global uniqueness of smooth isotropic Lamé moduli | [ElasticityUniqueness.lean](F372_ElasticityUniqueness.lean) |
