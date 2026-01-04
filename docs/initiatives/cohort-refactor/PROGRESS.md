# Cohort Refactoring Progress Tracker

**Last Updated:** 2026-01-04 09:45 UTC
**Status:** IN PROGRESS

## Completed Phases

### Phase 1: Database Schema ✅ COMPLETE
| Commit | File | Changes |
|--------|------|---------|
| f480fb6 | schema.py | Tables: cohorts→cohorts, cohort_entities→cohort_entities, cohort_tags→cohort_tags; Columns: cohort_id→cohort_id |
| 1c66f99 | migrations.py | Added v1.5 migration |
| 21f998d | queries.py | Query functions renamed |
| 84716e8 | db/__init__.py | Exports updated |

### Phase 2: State Management ✅ COMPLETE
| Commit | File | Changes |
|--------|------|---------|
| bf488ca | summary.py | SQL table/column renames |
| db09f50 | manager.py | SQL table/column renames |
| 929a019 | auto_persist.py | Fixed cohort_id column references |

**Test Results:** 295 passed, 0 failed

---

## Current Phase: Phase 3 - MCP Server

### 3.1 Tool Renames in healthsim_mcp.py
| Tool | Old Name | New Name | Status |
|------|----------|----------|--------|
| List | healthsim_list_cohorts | healthsim_list_cohorts | ⬜ |
| Load | healthsim_load_cohort | healthsim_load_cohort | ⬜ |
| Save | healthsim_save_cohort | healthsim_save_cohort | ⬜ |
| Delete | healthsim_delete_cohort | healthsim_delete_cohort | ⬜ |
| Summary | healthsim_get_cohort_summary | healthsim_get_cohort_summary | ⬜ |

### 3.2 MCP Tests
| File | Status |
|------|--------|
| test_add_entities.py | ⬜ |
| test_canonical_e2e.py | ⬜ |
| test_canonical_insert.py | ⬜ |
| Other test files | ⬜ |

---

## Remaining Phases

### Phase 4: Skills
- [ ] skills/common/state-management.md
- [ ] Other skill files with cohort references

### Phase 5: Documentation (~80 files)
- [ ] README files
- [ ] Architecture docs
- [ ] Tutorials
- [ ] Examples

### Phase 6: Directory Structure
- [ ] cohorts/saved/ → cohorts/saved/

### Phase 7: Test File Renames
- [ ] Rename test files with "cohort" in name

### Phase 8: Final Validation
- [ ] Full test suite
- [ ] Manual MCP tool testing
- [ ] Search for remaining "cohort" references
