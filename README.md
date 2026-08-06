# PIs

A skill-only plugin containing domain-specific principal investigators.

The first skill, **PI-math**, removes low-value mathematical definitions and
verifies that every semantic symbol in an equation is defined in scope. Future
skills can be added beside it under `plugins/pis/skills/`.

No application, service, runtime, hook, or dependency is included.

## Install

Import the marketplace from `hochshi/math-ponytail` at ref
`agent/minimal-math-plugin`, install **PIs**, and start a new chat.

- ChatGPT: select **PIs** from the `@` menu.
- Codex: invoke `$pi-math`.

Local Codex installation does not automatically install the plugin in ChatGPT.
