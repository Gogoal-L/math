> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/325.md).

# The complete Crouzeix conjecture

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [A direct proof of the complete Crouzeix inequality](../F325-B_complete_Crouzeix_direct.pdf)
- [The complete Crouzeix theorem: optimal similarity and a common positive boundary representation](../F325-A_complete_Crouzeix_structural.pdf)

## Scope

The complete Crouzeix inequality bounds a matrix-valued polynomial evaluated at a matrix by its maximum norm on the numerical range. The formalized result proves the bound with constant $2$ for every positive matrix and coefficient size, every polynomial degree, and arbitrary complex coefficients. It also proves that no smaller universal constant works. Normality of the matrix and nonempty interior of its numerical range are not assumed.

The formalization proves the complete Crouzeix inequality with sharp constant two for every bounded operator on an arbitrary complex Hilbert space. For every matrix-valued polynomial, its operator evaluation has norm at most twice its supremum norm on the numerical range. The same bound holds for finite matrix-valued functions holomorphic near the closure of the numerical range and for rational functions with poles outside that closure. No separability assumption is required.

For finite matrices in a bounded convex domain with regular real-analytic Jordan boundary, the structural result gives an attained optimal similarity with condition number at most two and one continuous positive boundary density of mass the identity representing every matrix-valued analytic test. The linked supporting statements include numerical-range geometry and finite-compression identities.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Complete Crouzeix inequality and sharpness | [DirectCrouzeix.lean](F325_DirectCrouzeix.lean) |
| Complete polynomial inequality and sharpness | [CompleteCrouzeix.lean](F325_CompleteCrouzeix.lean) |
| Optimal similarity and boundary representation | [StructuralCrouzeix.lean](F325_StructuralCrouzeix.lean) |
| Complete sharp Crouzeix theorem on arbitrary Hilbert spaces | [CrouzeixHilbert.lean](F325_CrouzeixHilbert.lean) |
| Numerical-range geometry and finite-compression support | [HilbertCrouzeix.lean](F325_HilbertCrouzeix.lean) |
