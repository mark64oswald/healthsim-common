# TrialSim Development Guide

## Purpose

This guide defines the structure, conventions, and phase roadmap for developing TrialSim within the HealthSim workspace. Follow these rules to maintain consistency with other HealthSim products.

---

## Directory Structure

TrialSim uses a **flat structure** matching other HealthSim products (PatientSim, MemberSim, RxMemberSim).

### Correct Structure

    skills/trialsim/
    ├── SKILL.md                      # Product overview and routing
    ├── clinical-trials-domain.md     # Domain knowledge
    ├── recruitment-enrollment.md     # Domain knowledge
    ├── phase3-pivotal.md             # Scenario skill
    ├── phase1-dose-escalation.md     # Scenario skill (future)
    ├── phase2-poc.md                 # Scenario skill (future)
    ├── adaptive-design.md            # Scenario skill (future)
    └── therapeutic-areas/            # Subcategory folder
        ├── oncology-trials.md
        ├── biologics-cgt.md
        └── cardiovascular-trials.md

### Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Domain files | skills/trialsim/clinical-trials-domain.md | skills/trialsim/domain/clinical-trials-domain.md |
| Scenario files | skills/trialsim/phase3-pivotal.md | skills/trialsim/scenarios/phase3-pivotal.md |
| CDISC formats | formats/cdisc-sdtm.md (root level) | skills/trialsim/formats/sdtm.md |
| Subcategories | therapeutic-areas/oncology-trials.md | Allowed (like patientsim/oncology/) |

### DO NOT Create These Subdirectories

- domain/ - Put domain files directly in trialsim/
- skills are organized at the product level
- formats/ - CDISC formats go in root formats/ folder (shared)
- models/ - Not used; schemas defined inline in skills

---

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Product SKILL | SKILL.md | skills/trialsim/SKILL.md |
| Domain skill | {topic}.md | clinical-trials-domain.md |
| Scenario skill | {scenario-name}.md | phase3-pivotal.md |
| Therapeutic area | therapeutic-areas/{area}-trials.md | therapeutic-areas/oncology-trials.md |
| CDISC format | formats/cdisc-{standard}.md | formats/cdisc-sdtm.md |
| Quickstart | hello-healthsim/trialsim-quickstart.md | Single quickstart per product |

---

## YAML Frontmatter Template

Every skill file MUST have YAML frontmatter:

    ---
    name: {skill-name}
    description: "{What this skill does}. Use when user requests: {trigger 1}, {trigger 2}, {trigger 3}."
    ---

### Examples

**Product SKILL:**

    ---
    name: healthsim-trialsim
    description: "Generate realistic clinical trial synthetic data including study definitions, sites, subjects, visits, adverse events, efficacy assessments, and disposition. Use when user requests: clinical trial data, CDISC/SDTM/ADaM datasets, trial scenarios (Phase I/II/III/IV), FDA submission test data, or specific therapeutic areas like oncology or biologics/CGT."
    ---

**Scenario skill:**

    ---
    name: phase3-pivotal-trial
    description: "Generate Phase III pivotal trial data with realistic multi-site enrollment, randomization, visit schedules, safety monitoring, and efficacy endpoints. Use for: Phase 3 trials, pivotal studies, registration trials, NDA/BLA submission data."
    ---

**Domain skill:**

    ---
    name: clinical-trials-domain
    description: "Core domain knowledge for clinical trial data generation including trial phases, CDISC standards, regulatory requirements, safety/efficacy patterns, and cross-product integration. Referenced by all TrialSim scenario skills."
    ---

---

## Link Patterns

### From trialsim/ files

| Target | Pattern |
|--------|---------|
| Same folder | [file.md](file.md) |
| Subcategory | [therapeutic-areas/oncology-trials.md](therapeutic-areas/oncology-trials.md) |
| Root formats | [../../formats/dimensional-analytics.md](../../formats/dimensional-analytics.md) |
| Root references | [../../references/code-systems.md](../../references/code-systems.md) |
| Hello quickstart | [../../hello-healthsim/trialsim-quickstart.md](../../hello-healthsim/trialsim-quickstart.md) |

### From hello-healthsim/

| Target | Pattern |
|--------|---------|
| TrialSim SKILL | [../skills/trialsim/SKILL.md](../skills/trialsim/SKILL.md) |
| TrialSim scenario | [../skills/trialsim/phase3-pivotal.md](../skills/trialsim/phase3-pivotal.md) |

---

## Phase Roadmap

### Phase 1: Foundation Setup - COMPLETE

- [x] Directory structure
- [x] Product SKILL.md
- [x] clinical-trials-domain.md
- [x] recruitment-enrollment.md (placeholder)
- [x] phase3-pivotal.md
- [x] trialsim-quickstart.md
- [x] Master SKILL.md routing
- [x] CHANGELOG.md update

### Phase 2: Core Content

| Phase | Deliverable | Description |
|-------|-------------|-------------|
| 2-B | recruitment-enrollment.md | Full recruitment/screening funnel implementation |
| 2-C | Entity schemas | Canonical JSON schemas for Study, Site, Subject, Visit, AE, etc. |
| 2-D | formats/cdisc-sdtm.md | SDTM domain mappings and generation patterns |
| 2-E | formats/cdisc-adam.md | ADaM dataset derivation patterns |
| 2-F | Site/Investigator patterns | Interim investigator entity, site generation |

### Phase 3: Extended Content

| Phase | Deliverable | Description |
|-------|-------------|-------------|
| 3-G | Additional scenarios | phase1-dose-escalation.md, phase2-poc.md, adaptive-design.md |
| 3-H | Therapeutic areas | therapeutic-areas/oncology-trials.md, biologics-cgt.md |
| 3-I | Database loading | Shared skill in formats/database-loading.md |
| 3-J | Dimensional model | Shared + TrialSim-specific dimensional mappings |

---

## Verification Checklist

Before committing any TrialSim phase:

### Structure

- [ ] No domain/, scenarios/, formats/, or models/ subdirectories created
- [ ] New files placed directly in skills/trialsim/ (unless subcategory)
- [ ] CDISC format files go to root formats/ folder

### Files

- [ ] All files have YAML frontmatter with name and description
- [ ] SKILL.md routing table updated for new skills
- [ ] All internal links use correct relative paths
- [ ] Links tested (no broken references)

### Documentation

- [ ] CHANGELOG.md updated with [TrialSim] prefix
- [ ] hello-healthsim example updated if needed

### Git

- [ ] git status shows expected files
- [ ] Commit message follows pattern: [TrialSim] {description}

---

## Reference: Existing Product Patterns

Check these for consistency guidance:

| Product | Path | Notes |
|---------|------|-------|
| PatientSim | skills/patientsim/ | Has oncology/, pediatrics/ subcategories |
| MemberSim | skills/membersim/ | Flat structure, no subcategories |
| RxMemberSim | skills/rxmembersim/ | Flat structure, no subcategories |
| Shared formats | formats/ | FHIR, HL7v2, X12, NCPDP, dimensional |
| Shared references | references/ | Code systems, validation rules |

---

## Quick Reference Commands

Check trialsim structure:

    ls -la skills/trialsim/

Verify no nested directories (should only show therapeutic-areas/):

    find skills/trialsim -type d

Check frontmatter in all files:

    for f in skills/trialsim/*.md; do head -4 "$f"; echo "---"; done

Grep for broken links:

    grep -r "domain/\|scenarios/" skills/trialsim/*.md
