---
name: pi-math
description: Reduce low-value definitions and audit mathematical notation without changing meaning. Use when writing or editing proofs, papers, lecture notes, specifications, equations, or other mathematical prose; distinguish first definitions, notation declarations, reminders, local scope, and legitimate redefinitions.
---

# PI Math

Optimize in this order:

1. Preserve mathematical correctness.
2. Resolve undefined symbols, collisions, scope errors, and unit conflicts.
3. Among correct alternatives, minimize introduced notation and indirection.

Do not repair an undefined symbol by automatically defining it. Use this order:

1. remove or inline it;
2. reuse existing notation;
3. explain the expression in prose;
4. introduce a definition only when repeated use or conceptual importance earns it.

A symbol normally fails the utility test when it is used once, abbreviates a
short expression or one-step transformation, aliases another name, or creates
a definition chain. Keep conventional notation and names that expose a central
object or replace a genuinely long repeated expression.

## Workflow

Draft the mathematical text directly. Resolve paths relative to this
`SKILL.md`, save the draft to a temporary Markdown file, and run:

```bash
python3 scripts/audit_math.py <draft.md>
```

Treat the JSON as candidate evidence, not mathematical truth. Repair confirmed
findings using the order above. Do not increase the number of introduced
symbols merely to clear an audit warning. Run the audit once more and return
only the revised mathematical text unless the user asked for a review.

If the script cannot run, perform the same checks manually. In either case:

- permit a definition immediately after its first equation;
- recognize binders and unambiguous standard notation;
- keep local definitions inside their scope;
- make legitimate redefinitions explicit;
- preserve domains, quantifiers, hypotheses, dependencies, conventions, and
  exceptional cases needed for correctness; and
- flag genuine ambiguity instead of inventing notation to hide it.

For review tasks, report confirmed findings as `undefined`, `collision`,
`unit-conflict`, `inline`, `reminder`, `notation`, `local`, or `redefine`.
