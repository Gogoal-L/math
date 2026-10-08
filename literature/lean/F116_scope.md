> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/116.md).

# Uniform black-box noncommutative identity testing across characteristics

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [One Rational Matrix Hitting Point for Noncommutative Formulas](../F116-A_noncommutative_hitting_point.pdf)
- [Polynomial Hitting Lists for Noncommutative Rational Formulas](../F116-B_rational_hitting_lists.pdf)

## Scope

The formalization gives one explicit tuple of rational matrices that simultaneously detects every nonzero division-free noncommutative formula with at most $s$ gates in $n$ variables, for $n,s\ge1$. Evaluation at that tuple is a nonzero matrix over every characteristic-zero field.

The selected theorem states this universal hitting property. The paper's deterministic polynomial bit-construction bound and matrix-dimension bound $O(ns^2)$ are not separately asserted in it.

The formalized result constructs polynomial-size hitting lists for noncommutative rational formulas with rational constants, addition, multiplication, and inverse gates. Given the number of variables and a formula-size bound, one deterministic polynomial-time machine outputs rational matrix tuples of a common positive dimension. Every admissible nonzero formula within the size bound evaluates to an invertible matrix on some listed tuple. The matrix dimension, complete binary output length, and running time are all polynomially bounded.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| One rational matrix tuple hitting all bounded-size noncommutative formulas | [FormulaHitting.lean](F116_FormulaHitting.lean) |
| Polynomial hitting lists for rational formulas | [RationalHitting.lean](F116_RationalHitting.lean) |
