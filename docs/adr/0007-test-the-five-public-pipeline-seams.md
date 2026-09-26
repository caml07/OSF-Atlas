---
status: accepted
---

# Test the five public pipeline seams

TDD is centered on five behavioral seams: Collector, StructuralParser, KnowledgeResolver, Renderer, and Validator. Tests exercise observable behavior through these interfaces rather than internal regexes or helper functions, keeping the suite stable while the implementation evolves.
