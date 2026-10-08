> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/365.md).

# Joint metric and connection recovery from one boundary patch

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Nonuniqueness for Bounded Measurable Scalar Conductivities in Three Dimensions](../F365-C_rough_scalar_conductivity_nonuniqueness.pdf)

## Scope

The Calderón inverse problem asks whether boundary measurements determine an interior conductivity. The formalized result gives nonuniqueness for bounded measurable scalar conductivities on the ball $B(0,3)\subset\mathbb R^3$: two uniformly positive conductivities differ on a set of positive volume, equal $1$ near the boundary, and have the same full weak Dirichlet-to-Neumann operator. Weak solutions exist uniquely for every boundary trace.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Scalar conductivity nonuniqueness | [Conductivity.lean](F365_Conductivity.lean) |
