# PopulationSim

> Access real population health data and generate evidence-based cohort specifications grounded in CDC, Census, and SDOH sources.

## What PopulationSim Does

PopulationSim is the **data intelligence** layer of HealthSim. Unlike other products that generate synthetic data, PopulationSim provides **access to real, embedded population statistics** from CDC PLACES, Social Vulnerability Index, and Area Deprivation Index.

This grounds all HealthSim data generation in evidence—when you generate a diabetic patient in Harris County, TX, the prevalence rates, comorbidities, and demographics reflect actual population data, not generic national averages.

## Quick Start

**Data lookup:**
```
What is the diabetes prevalence in Harris County, TX?
Show health indicators for San Diego County
```

**Geographic profiling:**
```
Profile census tract 06073010802 for SDOH factors
Compare health outcomes across Los Angeles County census tracts
```

**Cohort specification:**
```
Build a cohort for a Phase III diabetes trial in the Midwest
Generate demographic distribution for a Medicare population in Florida
```

See [hello-healthsim examples](../../hello-healthsim/examples/populationsim-examples.md) for detailed examples with expected outputs.

## Key Capabilities

| Capability | Description | Skill Reference |
|------------|-------------|-----------------|
| **Data Lookup** | Query embedded CDC/Census data | [data-access/data-lookup.md](data-access/data-lookup.md) |
| **County Profiles** | Comprehensive county health reports | [geographic/county-profile.md](geographic/county-profile.md) |
| **Tract Analysis** | Neighborhood-level health patterns | [geographic/census-tract-analysis.md](geographic/census-tract-analysis.md) |
| **SDOH Analysis** | Vulnerability and deprivation scoring | [sdoh/svi-analysis.md](sdoh/svi-analysis.md) |
| **Cohort Builder** | Evidence-based population specifications | [cohorts/cohort-specification.md](cohorts/cohort-specification.md) |
| **Trial Support** | Feasibility, site selection, diversity | [trial-support/](trial-support/) |

## Embedded Data (v2.0)

PopulationSim embeds **148 MB of real population data** covering 100% of US geographies:

| Data Source | Coverage | Records | Key Measures |
|-------------|----------|---------|--------------|
| CDC PLACES 2024 | All US counties + tracts | 86,665 | 40 health measures (diabetes, obesity, BP meds, etc.) |
| CDC SVI 2022 | All US counties + tracts | 87,264 | 16 vulnerability indicators |
| HRSA ADI 2023 | All US block groups | 242,336 | Area Deprivation Index |

## Data Categories

### Health Measures (CDC PLACES)
| Category | Examples |
|----------|----------|
| Chronic Disease | Diabetes, obesity, coronary heart disease, stroke, COPD, CKD, cancer |
| Health Behaviors | Smoking, binge drinking, physical inactivity, sleep <7 hours |
| Prevention | Mammography, colonoscopy, dental visit, flu shot, core preventive services |
| Health Status | Fair/poor health, mental health not good, physical health not good |

### Social Vulnerability (CDC SVI)
| Theme | Indicators |
|-------|------------|
| Socioeconomic | Below 150% poverty, unemployed, housing cost burden, no health insurance, no high school diploma |
| Household Composition | Age 65+, age 17 and younger, civilian with disability, single-parent households, English language proficiency |
| Minority Status | Minority population, speaks English "less than well" |
| Housing/Transportation | Multi-unit structures, mobile homes, crowding, no vehicle, group quarters |

## Integration with Other Products

PopulationSim **grounds generation** across all HealthSim products:

| Product | Integration | Effect |
|---------|-------------|--------|
| **PatientSim** | Demographics, conditions | Real prevalence rates, comorbidity correlations |
| **MemberSim** | Utilization, risk | Actuarially realistic member panels |
| **RxMemberSim** | Adherence patterns | SDOH-adjusted medication adherence |
| **TrialSim** | Feasibility, diversity | Evidence-based site selection |

**Example:**
```
# Without PopulationSim:
"Generate 10 diabetic patients" → Generic 10.2% national prevalence

# With PopulationSim v2.0:
"Generate 10 diabetic patients in Harris County, TX" →
  - Uses actual 12.1% diabetes rate from CDC PLACES
  - Applies 72% minority population from SVI
  - Includes real comorbidity correlations
  - Tracks data provenance in output
```

## Output Types

| Output | Purpose | Use Case |
|--------|---------|----------|
| Data Query Results | Raw data from embedded sources | Research, analysis |
| Geographic Profile | Comprehensive area health report | Planning, assessment |
| Cohort Specification | Evidence-based population definition | Trial design, product development |
| Cross-Product Integration | Grounding data for other products | Realistic data generation |

## Skills Reference

For complete parameters, examples, and data dictionaries, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all capabilities
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)
- **[data/README.md](data/README.md)** - Data package documentation

## Related Documentation

- [hello-healthsim PopulationSim Examples](../../hello-healthsim/examples/populationsim-examples.md)
- [Data Package Documentation](data/README.md)
- [Cross-Product Integration Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md#83-cross-product-integration)

---

*PopulationSim provides access to public CDC/Census data. Individual-level data is synthetic.*
