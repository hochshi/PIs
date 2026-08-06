---
name: ponytail-math
description: "Remove low-value mathematical names and aliases while preserving useful notation, scope, hypotheses, and legitimate redefinitions."
homepage: https://github.com/DietrichGebert/ponytail
license: MIT
---

# Ponytail Math

Every new name or symbol must earn the indirection it creates. Define an object
only when naming it makes the surrounding mathematics easier to understand.
Shorter writing is the result; preserving meaning is the constraint.

## Definition utility gate

Before introducing a name, compare its benefit with its reader cost:

- **Benefit:** repeated expression complexity removed, a central concept exposed,
  or standard notation that makes later reasoning easier to recognize.
- **Cost:** the definition itself, remembering the symbol, looking it up, possible
  collisions, and another layer between the reader and the formula.

Keep the definition only when the benefit is clearly greater. Do not invent a
numeric score; make the comparison from the actual text and uses.

Default to inlining when a proposed name:

- is used once, or only in the immediately following line;
- abbreviates a short expression or a one-step transformation;
- is merely an alias of an existing object, such as a rescaling or shift;
- uses an arbitrary letter that does not suggest its meaning or relation; or
- creates a chain of definitions the reader must mentally expand.

A definition can earn its place when it names a central object used throughout,
replaces a genuinely long repeated expression, exposes proof structure, matches
standard mathematical notation, or is needed to state a result cleanly. Prefer
notation that reveals relationships, such as \(\bar N\) for an average derived
from \(N\), over an unrelated letter such as \(M\).

## Classify before cutting

Keep an internal ledger of each term or symbol's meaning and scope while
writing. Do not print the ledger unless asked.

| Role | Test | Treatment |
|---|---|---|
| **Unnecessary definition** | Its name or symbol costs at least as much mental work as inlining the expression. | Remove the definition and substitute the expression at its uses. |
| **First definition** | Introduces new mathematical content in the visible scope. | State it once, including every necessary domain, quantifier, hypothesis, and dependence. |
| **Notation declaration** | Assigns a symbol or name to an object already defined. | Declare the notation once; do not present it as a new concept. |
| **Reminder** | Recalls an earlier definition without changing it. | Use only when distance or ambiguity warrants it; keep it shorter than the original and cite it when possible. |
| **Local definition** | Introduces a meaning inside a proof, example, case, or other bounded scope. | Use it only inside that scope. A later outer-scope definition may be a genuine first definition there. |
| **Legitimate redefinition** | Changes meaning because the scope, hypotheses, domain, convention, or parameterization changed. | Make the changed context explicit. Never silently overwrite the earlier meaning. |

## Definition ladder

For every apparent definition, stop at the first matching case:

1. The proposed name fails the definition utility gate: inline it. A new value
   or meaning does not automatically justify a new name.
2. The same meaning is already available in the current scope: use it without
   restating it.
3. The reader may reasonably lose the reference: add a short reminder, not a
   second definition.
4. Only a symbol or abbreviation is new and it passes the utility gate: write a
   notation declaration.
5. The meaning is new in this scope and naming it passes the utility gate: write
   the first definition at first use.
6. The meaning intentionally changes: state the new scope or changed condition,
   then redefine it explicitly.

Do not front-load definitions that are never used. Do not delete a definition
merely because its term appeared earlier: appearance, notation, and definition
are different events.

## Editing pass

When revising existing text:

1. Count and inspect the actual uses of every introduced name.
2. Inline definitions that fail the utility gate, starting with aliases of
   aliases and short one-use expressions.
3. Locate the first complete definition of each remaining concept in each scope.
4. Preserve it and every clause needed for correctness.
5. Delete later verbatim restatements, or turn them into reminders when the
   reader needs orientation.
6. Keep notation declarations, local definitions, and explicit legitimate
   redefinitions distinct.
7. If two passages may differ mathematically, keep both until their equivalence
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

Low-value derived alias:

> \(N=\sum_i x_i\), and define \(M=\frac1nN\).

If \(M\) has few uses, prefer:

> \(N=\sum_i x_i\), so the average is \(\frac1nN\).

Here \(M\) is an **unnecessary definition**: the short substitution is easier
than remembering an unrelated symbol. If the average is central and repeatedly
used, meaningful conventional notation such as \(\bar x\) may instead earn a
definition.

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
occurrence as `unnecessary`, `delete`, `reminder`, `notation`, `local`, or
`redefine`, and cite the reason or first controlling definition.
