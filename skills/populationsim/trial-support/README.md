---
name: populationsim-trial-support
description: >
  Trial support skills for PopulationSim. Use for clinical trial feasibility
  assessment, site selection, enrollment projections, and diversity planning.
  Leverages population data to inform trial design and execution.
---

# Trial Support Skills

## Overview

Trial support skills apply PopulationSim's population intelligence to clinical trial planning and execution. They help sponsors and sites make data-driven decisions about trial feasibility, site selection, enrollment timelines, and diversity requirements.

**Key Capability**: Transform population health data into actionable trial planning intelligence.

---

## Skills in This Category

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [site-feasibility.md](site-feasibility.md) | Assess site-level feasibility | "site feasibility", "can this site enroll", "population at site" |
| [enrollment-projections.md](enrollment-projections.md) | Project enrollment timelines | "enrollment projection", "how long to enroll", "enrollment rate" |
| [diversity-planning.md](diversity-planning.md) | Plan for diverse enrollment | "diversity requirements", "minority enrollment", "representative sample" |

---

## Integration with TrialSim

PopulationSim trial support provides upstream intelligence that feeds TrialSim:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│   PopulationSim     │     │   PopulationSim     │     │     TrialSim        │
│   Geographic +      │────▶│   Trial Support     │────▶│   Synthetic Trial   │
│   Health Patterns   │     │   (Feasibility)     │     │   Execution         │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
         │                           │                           │
         ▼                           ▼                           ▼
    Population Data           Site Feasibility            DM/DS Domains
    Disease Prevalence        Enrollment Rates            Subject Records
    Demographics              Diversity Plans             Trial Events
```

---

## Key Concepts

### Eligible Population Cascade

```
Total Population (Geography)
         │
         ▼ Apply age filter
    Age-Eligible Population
         │
         ▼ Apply condition prevalence
    Condition-Present Population
         │
         ▼ Apply severity/staging criteria
    Meets Clinical Criteria
         │
         ▼ Apply exclusions
    Potentially Eligible
         │
         ▼ Apply access/willingness factors
    Realistically Recruitable
         │
         ▼ Apply screening success rate
    Expected Enrolled
```

### Enrollment Funnel Metrics

| Stage | Typical Rate | Range |
|-------|--------------|-------|
| Aware → Interested | 15-25% | 5-40% |
| Interested → Screened | 40-60% | 20-80% |
| Screened → Eligible | 30-50% | 15-70% |
| Eligible → Enrolled | 60-80% | 40-95% |
| **Overall Conversion** | 3-8% | 1-15% |

### Screen Failure Reasons

| Reason | Typical % | Notes |
|--------|-----------|-------|
| Inclusion not met | 35% | Condition severity |
| Exclusion met | 25% | Comorbidities, meds |
| Lab abnormalities | 15% | Often unexpected |
| Consent withdrawal | 12% | Before randomization |
| Other | 13% | Logistics, lost to f/u |

---

## Trial Type Considerations

### Phase 1 (Healthy Volunteers)
```yaml
population: General healthy adults
key_factors:
  - Proximity to site (urban preferred)
  - No significant medical history
  - Flexible schedule
typical_enrollment: 20-80 subjects
site_requirement: Phase 1 unit
```

### Phase 2 (Proof of Concept)
```yaml
population: Patients with target condition
key_factors:
  - Condition prevalence in catchment
  - Access to specialist care
  - Prior treatment history
typical_enrollment: 100-300 subjects
site_requirement: Specialty centers
```

### Phase 3 (Pivotal)
```yaml
population: Broad patient population
key_factors:
  - Large catchment area
  - Diverse demographics
  - Community and academic sites
typical_enrollment: 300-3000+ subjects
site_requirement: Mixed site network
```

### Phase 4 (Post-Market)
```yaml
population: Real-world patients
key_factors:
  - Representative of treated population
  - Community practices
  - EHR integration for follow-up
typical_enrollment: 1000-10000+ subjects
site_requirement: Community networks
```

---

## Diversity Requirements

### FDA Guidance (2024)

The FDA now requires:
- Diversity Action Plans for Phase 3 trials
- Enrollment goals reflecting disease epidemiology
- Justification for any under-representation

### Key Demographics for Reporting

| Category | Minimum Reporting |
|----------|-------------------|
| Sex | Male, Female |
| Age | Pediatric, Adult, Elderly |
| Race | White, Black, Asian, AIAN, NHPI, Multiple |
| Ethnicity | Hispanic/Latino, Not Hispanic |
| Geography | Urban, Suburban, Rural |

### Disease-Specific Diversity Targets

| Condition | Key Disparity | Recommended Target |
|-----------|---------------|-------------------|
| Diabetes | Hispanic, Black | 35-40% minority |
| Heart Failure | Black | 25-30% Black |
| Alzheimer's | Black, Hispanic | 30-35% minority |
| Lung Cancer | Black, Rural | 20-25% each |
| Lupus | Black, Female | 40%+ Black, 90%+ Female |

---

## Output Integration

### → Site Selection

Trial support outputs inform site network design:
- Identify high-potential sites
- Balance geography and diversity
- Set site-level enrollment targets

### → Protocol Design

Population analysis informs protocol decisions:
- Realistic eligibility criteria
- Achievable enrollment timeline
- Diversity-enabling design elements

### → TrialSim Generation

Feasibility data feeds synthetic trial generation:
- Site distribution modeling
- Realistic screening/enrollment ratios
- Demographically accurate subject pools

---

## Data Sources

| Source | Use |
|--------|-----|
| CDC PLACES | Disease prevalence by geography |
| Census ACS | Demographics, socioeconomics |
| CMS Claims | Healthcare utilization patterns |
| NPPES | Provider/site locations |
| Clinical Literature | Condition-specific enrollment rates |

---

## Related Skills

- [Geographic Intelligence](../geographic/README.md) - Population foundations
- [Health Patterns](../health-patterns/README.md) - Disease prevalence
- [Cohort Definition](../cohorts/README.md) - Target population specs
- TrialSim Skills - Downstream trial execution
