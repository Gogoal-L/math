> OpenAI source snapshot at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Local change: attribution and link targets only. Selected scope wording is unchanged. [Original scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/docs/251.md).

# Amenability, unitarizability, and strong Ulam stability

The following describes the scope of the Lean formalization related to the following accompanying paper(s):

- [Unitarizability implies amenability for discrete groups](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Unitarizability-Implies-Amenability-for-Countable-Groups-September-23-2026/paper.pdf)

## Scope

Dixmier's unitarizability problem asks whether a discrete group is amenable exactly when every uniformly bounded Hilbert-space representation is similar to a unitary one. The formalization establishes this equivalence for every discrete group.

For every nonamenable group and every $\varepsilon>0$, it also gives a nonunitarizable representation with uniform operator bound at most $1+\varepsilon$. The Hilbert space can be chosen separable for countable groups; a separate linked statement records a separable witness with uniform bound $101$ in that case.

## Comparator links

| Result | Comparator statement |
| --- | --- |
| Unitarizability for all discrete groups | [DixmierAllDiscrete.lean](F251_DixmierAllDiscrete.lean) |
| Separable nonunitarizable witnesses for countable nonamenable groups | [Dixmier.lean](F251_Dixmier.lean) |
