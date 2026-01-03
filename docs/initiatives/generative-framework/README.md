# HealthSim Generative Framework Initiative

**Status**: Planning Complete, Ready for Implementation  
**Started**: January 3, 2026  
**Target Completion**: 16-20 sessions

## Overview

The Generative Framework enables conversation-driven generation of healthcare data at scale. It separates the creative process of specification building from the mechanical process of execution.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Profile** | Population characteristics (demographics, clinical, coverage) |
| **Distribution** | Statistical tools for value selection |
| **Journey** | Event sequences over time |
| **Event** | Discrete occurrences (encounter, claim, prescription) |
| **Timing** | Event scheduling (fixed, range, protocol window) |
| **Trigger** | Cross-domain connections (encounter → claim) |

## Documents

| Document | Description |
|----------|-------------|
| [Implementation Plan](../GENERATIVE-FRAMEWORK-IMPLEMENTATION-PLAN.md) | Master plan with 16-20 sessions |
| [Conceptual Model](./conceptual-model.html) | Architecture and visual diagrams (TBD) |
| [Design Decisions](./design-decisions.md) | Key architectural decisions (TBD) |
| [Profile Builder Spec](./profile-builder-spec.md) | 4-phase conversation flow (TBD) |

## Phase Overview

1. **Phase 0**: Foundation & Cleanup (2-3 sessions)
2. **Phase 1**: Generation Skills Foundation (4-5 sessions)
3. **Phase 2**: Template Library (3-4 sessions)
4. **Phase 3**: Integration & Polish (4-5 sessions)
5. **Phase 4**: Release (2 sessions)

## Quick Start

Once implemented, generation will work like this:

```
User: "200 Medicare diabetics with claims for demo"

Claude: (Using Profile Builder) I'll help you create a specification for 200 Medicare 
diabetic members. Let me ask a few questions:

- Age distribution: Should I use typical Medicare (65-85) or younger disabled?
- Geographic focus: Any specific state or region?
- Severity mix: Controlled vs poorly controlled diabetes?

[Conversation continues to build specification]
[Executor generates 200 members + claims per specification]
```

## Related Documents in Claude Project

The following design documents exist in the Claude Project and should be consulted:

- `HEALTHSIM-GENERATIVE-FRAMEWORK-CONCEPTS.md` - Core concepts and patterns
- `HEALTHSIM-GENERATIVE-FRAMEWORK-DECISIONS.md` - Design decision points
- `HEALTHSIM-PROFILE-BUILDER-SPECIFICATION.md` - Profile builder details
- `HEALTHSIM-GENERATIVE-TAXONOMY.md` - Mental model reference
- `healthsim-conceptual-model.html` - Visual architecture document

---

*This folder will be populated as implementation progresses.*
