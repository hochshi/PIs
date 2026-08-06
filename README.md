# PIs

A skill-only plugin containing domain-specific principal investigators.

The first skill, **PI-math**, removes low-value mathematical definitions and
audits equation symbols, definition chains, collisions, and unit conventions.
Its dependency-free audit reports candidates; PI-math confirms them from the
mathematical context and prefers inlining or reuse over adding notation.

No application, service, MCP server, hook, or third-party dependency is included.

## Install

Import the marketplace from `hochshi/math-ponytail` at ref
`agent/minimal-math-plugin`, install **PIs**, and start a new chat.

- ChatGPT: select **PIs** from the `@` menu.
- Codex: invoke `$pi-math`.

Local Codex installation does not automatically install the plugin in ChatGPT.
