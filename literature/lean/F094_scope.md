> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/094.md).

# Subpolynomial dimension reduction in <i>L</i><sub><i>p</i></sub>

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Subpolynomial dimension reduction in $L_p$](../F094_Lp_subpolynomial_dimension_reduction.pdf)

## Scope

For $p>1$, $p\ne2$, the formalization bounds the least dimension needed to embed every $n$-point subset of real $L_p$ with distortion $D$. For each fixed $D>1$, there is a constant $C=C(p,D)$ such that this dimension lies between $\log n/\log(1+2D)$ and $\exp(C(\log n)^{\gamma(p)})$ for every $n\ge2$, where $\gamma(p)=2-p$ for $p<2$ and $1-2/p$ for $p>2$. At distortion $1$ and $n\ge9$, it lies between $\lfloor(n-1)/4\rfloor^2$ and $\binom n2$. The least dimension is attained, and its logarithm divided by $\log n$ tends to $0$ for $D>1$ and to $2$ for $D=1$.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Dimension reduction in $L_p$ | [SubpolynomialLp.lean](F094_SubpolynomialLp.lean) |
