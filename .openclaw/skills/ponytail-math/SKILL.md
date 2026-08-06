---
name: ponytail-math
description: "Reduce repeated definitions in mathematical writing while preserving notation, scope, hypotheses, and legitimate redefinitions."
homepage: https://github.com/DietrichGebert/ponytail
license: MIT
---

# Ponytail Math

Define each mathematical object once per scope. Reuse it thereafter. Shorter
writing is the result; preserving meaning is the constraint.

## Classify before cutting

Keep an internal ledger of each term or symbol's meaning and scope while
writing. Do not print the ledger unless asked.

| Role | Test | Treatment |
|---|---|---|
| **First definition** | Introduces new mathematical content in the visible scope. | State it once, including every necessary domain, quantifier, hypothesis, and dependence. |
| **Notation declaration** | Assigns a symbol or name to an object already defined. | Declare the notation once; do not present it as a new concept. |
| **Reminder** | Recalls an earlier definition without changing it. | Use only when distance or ambiguity warrants it; keep it shorter than the original and cite it when possible. |
| **Local definition** | Introduces a meaning inside a proof, example, case, or other bounded scope. | Use it only inside that scope. A later outer-scope definition may be a genuine first definition there. |
| **Legitimate redefinition** | Changes meaning because the scope, hypotheses, domain, convention, or parameterization changed. | Make the changed context explicit. Never silently overwrite the earlier meaning. |

## Definition ladder

For every apparent definition, stop at the first matching case:

1. The same meaning is already available in the current scope: use it without
   restating it.
2. The reader may reasonably lose the reference: add a short reminder, not a
   second definition.
3. Only a symbol or abbreviation is new: write a notation declaration.
4. The meaning is new in this scope: write the first definition at first use.
5. The meaning intentionally changes: state the new scope or changed condition,
   then redefine it explicitly.

Do not front-load definitions that are never used. Do not delete a definition
merely because its term appeared earlier: appearance, notation, and definition
are different events.

## Editing pass

When revising existing text:

1. Locate the first complete definition in each scope.
2. Preserve it and every clause needed for correctness.
3. Delete later verbatim restatements, or turn them into reminders when the
   reader needs orientation.
4. Keep notation declarations, local definitions, and explicit legitimate
   redefinitions distinct.
5. If two passages may differ mathematically, keep both until their equivalence
   is established.

## Correctness boundary

Never shorten away a domain or codomain, quantifier, hypothesis, dependency,
exceptional case, convention, or scope boundary that changes the statement.
Do not merge concepts because their names or formulas look similar. Treat an
overloaded symbol as a new declaration when its scope or meaning changes.

When uncertain whether a repetition is redundant, preserve it and flag the
ambiguity. A slightly repetitive correct definition is better than a concise
false one.

## Examples

Repeated definition:

> A sequence is Cauchy if ... . Later: Recall that a sequence is Cauchy if ... .

Prefer:

> A sequence is Cauchy if ... . Later: For the Cauchy sequence defined above, ... .

Notation is not a second definition:

> Let \(C(X)\) denote the already-defined space of continuous functions on \(X\).

Local scope may reuse a symbol:

> In this proof, set \(r=\lVert x\rVert\). After the proof, that local meaning expires.

Legitimate redefinition must announce the change:

> For this section only, "graph" means a finite simple graph.

## Output

For writing tasks, return the revised mathematical text without a definition
ledger or change log unless requested. For review tasks, identify each later
occurrence as `delete`, `reminder`, `notation`, `local`, or `redefine`, and cite
the first controlling definition.
