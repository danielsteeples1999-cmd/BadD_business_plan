# BAD-D // Market Forge

This repository holds the Market Forge operating guidance, experiment method, priority queue, and JSON Schema contracts. The linked files are authoritative; this README is a navigation guide rather than a second source of project guidance.

## Recommended reading order

1. [Mission and operating guidance](CLAUDE_NOW.md) — mission, evidence labels, human-control boundaries, and the research and execution loops.
2. [Experiment protocol](EXPERIMENT_PROTOCOL.md) — the decision-question, evidence-gathering, measurement, and review steps.
3. [Market priority queue](MARKET_PRIORITY_QUEUE.md) — the ordered `MARKET-001`–`MARKET-018` work items and the rule against automating distribution before validation.
4. **Contract schemas**
   - [Market result schema](contracts/market-result.schema.json) — the Draft 2020-12 contract for experiment status, evidence, findings, unknowns, and next action.
   - [Pricing model schema](contracts/pricing-model.schema.json) — the Draft 2020-12 contract for pricing scenarios and assumptions.
