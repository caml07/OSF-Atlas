# OSF Atlas Documentation

This directory records the design of the local Obsidian Soundfields Atlas before and during implementation.

## Reference

- [[architecture]] — system shape, module boundaries, data flow, ownership, rebuild rules
- [[ux]] — intended Obsidian reading and research experience
- [[graph]] — graph visibility, node types, filtering, and relationship behavior
- [[collector]] — collector/parser CLI and ingestion lifecycle
- [[vault-agent-skill]] — draft design for the future vault-local agent skill
- [[plan-v3]] — approved implementation sequence and final senior review

## Decisions

Durable decisions live in [[adr/]].

## Status

Planning is complete and **Milestone 0 (vault scaffold)** is implemented.

The Atlas, Bases, Graph defaults, Properties schema, templates, local visual
layer, and final project folders now follow the approved architecture.

Collector/parser code and corpus ingestion remain pending; those sections of the
documentation describe the implementation contract for the next milestones.
