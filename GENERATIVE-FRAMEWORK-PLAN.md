# Generative Framework Implementation Plan

**Created**: 2026-01-05
**Status**: In Progress

---

## Overview

This plan addresses two tracks:
1. **Product Consistency** - Complete remaining consistency items across all products
2. **Generative Framework Gaps** - Close gaps between design documents and implementation

---

## Track 1: Product Consistency (3 Items) ✅ COMPLETE

### 1.1 Database Index Names ✅
**Status**: ✅ Complete
**Commit**: 89c31515

Added migration 1.6 to drop legacy `idx_*_scenario` indexes (replaced by `idx_*_cohort`).

### 1.2 MemberSim/RxMemberSim MCP Audit ✅
**Status**: ✅ Complete
**Commit**: 89c31515

Updated state servers in both packages to use "Cohort" terminology.

### 1.3 TrialSim MCP Server ✅
**Status**: ✅ Complete
**Commit**: 89c31515

Created full MCP server integration with generation and state tools.

---

## Track 2: Generative Framework Gaps

### 2.1 MCP Tools for Profile Management ✅
**Status**: ✅ Already Implemented
**Tests**: 19 passing

Existing implementation in `packages/core/src/healthsim/mcp/profile_server.py`:
- build_profile, save_profile, load_profile, list_profiles
- list_profile_templates, execute_profile
- list_journey_templates, get_journey_template

### 2.2 Cross-Product Integration
**Status**: 🔄 In Progress
**Effort**: Medium-Large

Connect generation across product domains:
- [ ] Implement `CrossDomainSync` class in core
- [ ] Add identity correlation (same person across MemberSim/PatientSim/RxMemberSim)
- [ ] Add event triggers (enrollment triggers eligibility, claim triggers encounter)
- [ ] Create cross-domain journey templates
- [ ] Add integration tests

### 2.3 Journey Validation Framework
**Status**: ⬜ Not Started
**Effort**: Small-Medium

Enhance journey execution validation:
- [ ] Add journey specification validation (before execution)
- [ ] Add timeline validation (after execution)
- [ ] Add cross-event consistency checks
- [ ] Create validation report format

### 2.4 TrialSim SDTM Export
**Status**: ⬜ Not Started
**Effort**: Medium

Implement CDISC SDTM format export for TrialSim.

### 2.5 PopulationSim Reference Data Integration
**Status**: ⬜ Not Started
**Effort**: Medium

Connect PopulationSim reference data to generation framework.

---

## Execution Order

| Phase | Items | Estimated Sessions | Status |
|-------|-------|-------------------|--------|
| **Phase A** | 1.1, 1.2, 1.3 | 1-2 sessions | ✅ Complete |
| **Phase B** | 2.1 (MCP Tools) | 1-2 sessions | ✅ Already Done |
| **Phase C** | 2.2 (Cross-Product) | 2-3 sessions | 🔄 In Progress |
| **Phase D** | 2.3, 2.4, 2.5 | 2-3 sessions | ⬜ Pending |

---

## Progress Tracking

### Session Log

| Date | Items Completed | Tests Status | Commits |
|------|-----------------|--------------|---------|
| 2026-01-05 | Track 1 complete, 2.1 verified | 1,369 passing | 89c31515 |
| | | | |

---

*End of Plan*
