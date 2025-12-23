---
name: site-feasibility
description: >
  Assess clinical trial site feasibility using population data. Estimates
  eligible patient population, expected enrollment capacity, and site
  characteristics. Triggers: "site feasibility", "can this site enroll",
  "eligible population at site", "site assessment".
---

# Site Feasibility Skill

## Overview

The site-feasibility skill assesses clinical trial enrollment potential for specific sites or geographic areas. It combines population health data with trial criteria to estimate eligible patient pools and expected enrollment rates.

**Primary Use Cases**:
- Site selection for new trials
- Enrollment target setting
- Site network optimization
- Feasibility questionnaire validation

---

## Trigger Phrases

- "Assess feasibility for [site/geography]"
- "Can [area] enroll for a [condition] trial?"
- "Eligible population for [trial] in [geography]"
- "Site feasibility for [location]"
- "How many [condition] patients in [area]?"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `geography` | string | Yes | - | Site location (city, county, metro) |
| `condition` | string | Yes | - | Primary condition (ICD-10 or name) |
| `age_range` | array | No | [18, 100] | Age eligibility |
| `exclusions` | array | No | [] | Key exclusion conditions |
| `catchment_radius` | int | No | 50 | Miles from site |
| `site_type` | string | No | "academic" | "academic", "community", "network" |

---

## Feasibility Cascade

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Total Population in Catchment                   │
│         (Census data for geography + radius)            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: Age-Eligible Population                         │
│         (Apply age range filter)                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: Condition-Present Population                    │
│         (Apply disease prevalence rate)                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: Severity-Appropriate Population                 │
│         (Apply staging/severity criteria)               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: Exclusions Applied                              │
│         (Remove patients with exclusionary conditions)  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 6: Access-Adjusted Population                      │
│         (Healthcare access, insurance, transportation)  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ Step 7: Realistically Recruitable                       │
│         (Awareness, interest, site capacity factors)    │
└─────────────────────────────────────────────────────────┘
```

---

## Site Type Factors

| Factor | Academic | Community | Network |
|--------|----------|-----------|---------|
| Catchment radius | 75-100 mi | 25-50 mi | Varies |
| Patient awareness | Higher | Lower | Variable |
| Screening capacity | High | Moderate | High |
| Competition for patients | High | Low | Moderate |
| Diversity potential | Moderate | High | High |
| Monthly enrollment | 2-5/mo | 0.5-2/mo | 3-8/mo |

---

## Output Schema

```json
{
  "feasibility_assessment": {
    "site": {
      "name": "Houston Methodist Hospital",
      "type": "academic",
      "location": {
        "city": "Houston",
        "state": "TX",
        "coordinates": [29.7109, -95.3994]
      },
      "catchment_radius_miles": 50
    },
    
    "trial_criteria": {
      "condition": "E11",
      "condition_name": "Type 2 Diabetes",
      "age_range": [40, 75],
      "key_inclusions": ["A1c 7.5-10.5%", "On metformin"],
      "key_exclusions": ["N18.5", "N18.6", "B18"],
      "exclusion_names": ["CKD Stage 5", "ESRD", "Chronic Hepatitis"]
    },
    
    "population_cascade": {
      "step_1_total_population": {
        "value": 4850000,
        "description": "Total population within 50 miles"
      },
      "step_2_age_eligible": {
        "value": 1842000,
        "pct_of_prior": 0.38,
        "description": "Age 40-75"
      },
      "step_3_condition_present": {
        "value": 235800,
        "pct_of_prior": 0.128,
        "prevalence_used": 0.128,
        "description": "Diagnosed diabetes"
      },
      "step_4_severity_appropriate": {
        "value": 94300,
        "pct_of_prior": 0.40,
        "description": "A1c 7.5-10.5%, on metformin"
      },
      "step_5_exclusions_applied": {
        "value": 75400,
        "pct_of_prior": 0.80,
        "exclusion_rates": {
          "N18.5_N18.6": 0.08,
          "B18": 0.02,
          "other": 0.10
        },
        "description": "After exclusions"
      },
      "step_6_access_adjusted": {
        "value": 60300,
        "pct_of_prior": 0.80,
        "factors": {
          "has_insurance": 0.92,
          "has_transportation": 0.88,
          "english_proficient": 0.85
        },
        "description": "Can access trial site"
      },
      "step_7_realistically_recruitable": {
        "value": 9000,
        "pct_of_prior": 0.15,
        "factors": {
          "awareness_potential": 0.30,
          "interest_rate": 0.50,
          "site_capacity_factor": 1.0
        },
        "description": "Realistically recruitable"
      }
    },
    
    "enrollment_estimate": {
      "recruitable_pool": 9000,
      "screening_to_enrollment_rate": 0.35,
      "expected_enrolled": 3150,
      "confidence_interval": [2200, 4100],
      "confidence_level": "moderate"
    },
    
    "monthly_capacity": {
      "screening_capacity": 20,
      "expected_enrollment": 7,
      "range": [4, 10],
      "limiting_factor": "site_staff_capacity"
    },
    
    "demographics_of_eligible": {
      "age": {
        "mean": 58.4,
        "range": [40, 75]
      },
      "sex": {
        "male": 0.48,
        "female": 0.52
      },
      "race_ethnicity": {
        "white_nh": 0.28,
        "black": 0.22,
        "hispanic": 0.40,
        "asian": 0.08,
        "other": 0.02
      }
    },
    
    "feasibility_rating": {
      "score": 82,
      "rating": "high",
      "interpretation": "Strong feasibility for enrollment target",
      "strengths": [
        "Large diabetic population",
        "Diverse demographics",
        "Academic center resources"
      ],
      "challenges": [
        "Competitive trial market",
        "Language barriers (14% limited English)"
      ]
    },
    
    "recommendations": [
      "Target Hispanic community outreach",
      "Partner with community health centers",
      "Consider bilingual coordinators"
    ]
  },
  
  "metadata": {
    "data_sources": ["Census_2022", "CDC_PLACES_2024", "NPPES"],
    "generated_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Examples

### Example 1: Diabetes Trial Site

**Request**: "Assess site feasibility for a diabetes trial at Cleveland Clinic"

**Response**:

**Cleveland Clinic Diabetes Trial Feasibility**

**Site Profile**:
- Type: Large Academic Medical Center
- Catchment: 75-mile radius
- Catchment Population: 4.2M

**Eligibility Cascade**:
| Step | Population | % of Prior |
|------|------------|------------|
| Total Population | 4,200,000 | - |
| Age 40-75 | 1,596,000 | 38% |
| Has Diabetes | 191,500 | 12.0% |
| Target Severity | 76,600 | 40% |
| After Exclusions | 61,300 | 80% |
| Access-Adjusted | 52,100 | 85% |
| Recruitable | 7,800 | 15% |

**Enrollment Estimate**:
- Recruitable Pool: 7,800
- Screen-to-Enroll: 35%
- Expected Enrolled: **2,730** (CI: 1,900-3,500)

**Monthly Capacity**:
- Screening: 25/month
- Enrollment: **8-10/month**

**Demographics of Eligible**:
| Group | Rate |
|-------|------|
| White NH | 62% |
| Black | 24% |
| Hispanic | 8% |
| Asian | 4% |

**Feasibility Rating**: **HIGH (85/100)**

---

### Example 2: Rare Disease Site Network

**Request**: "Feasibility for NASH trial sites in Texas"

**Response**:

**Texas NASH Trial Site Feasibility**

**Condition**: K75.81 (NASH), F2-F3 Fibrosis
**Sites Evaluated**: Houston, Dallas, San Antonio, Austin

| Site | Catchment Pop | NASH Eligible | Monthly Enroll |
|------|---------------|---------------|----------------|
| Houston Methodist | 4.8M | 4,200 | 3-5 |
| UT Southwestern | 5.2M | 4,500 | 4-6 |
| UT Health SA | 2.4M | 2,100 | 2-3 |
| Dell Medical | 2.1M | 1,800 | 1-2 |

**Network Total**:
- Combined Eligible: 12,600
- Combined Monthly: 10-16/month
- 12-Month Projection: 120-190 enrolled

**Diversity Profile** (Combined):
| Group | % | Count at n=150 |
|-------|---|----------------|
| White NH | 52% | 78 |
| Hispanic | 32% | 48 |
| Black | 10% | 15 |
| Asian | 6% | 9 |

**Recommendation**: Strong network with diversity potential. Consider adding El Paso for additional Hispanic representation.

---

### Example 3: Community Site Assessment

**Request**: "Can a community practice in rural Kentucky enroll for a COPD trial?"

**Response**:

**Rural Kentucky COPD Trial Feasibility**

**Site**: Community Pulmonology Practice, Pikeville, KY
**Site Type**: Community Specialty
**Catchment**: 30 miles (limited by terrain)

**Population Cascade**:
| Step | Population | Notes |
|------|------------|-------|
| Total | 82,000 | Rural, aging population |
| Age 45-80 | 31,200 | 38% (older skew) |
| Has COPD | 5,300 | **17%** (high prevalence) |
| Moderate-Severe | 2,650 | 50% |
| After Exclusions | 2,120 | 80% |
| Recruitable | 320 | 15% |

**Enrollment Estimate**:
- Expected Enrolled: **110** (over trial duration)
- Monthly Capacity: **1-2/month**

**Considerations**:
| Factor | Assessment |
|--------|------------|
| COPD Prevalence | Very High (17% vs 6% national) |
| Transportation | Challenge (28% >30 min drive) |
| Insurance | 42% Medicare, 18% Medicaid |
| Competition | Low (only pulm practice) |

**Feasibility Rating**: **MODERATE (62/100)**

**Recommendation**: Viable site with high disease prevalence offsetting small population. Recommend NEMT support for transportation-challenged patients.

---

## Validation Rules

### Input Validation
- Geography must be mappable
- Condition must be valid ICD-10 or recognized name
- Age range must be valid [min, max]

### Output Validation
- [ ] Cascade percentages decrease at each step
- [ ] Enrollment estimates within reasonable range
- [ ] Demographics sum to ~100%
- [ ] Monthly capacity matches site type norms

---

## Related Skills

- [county-profile.md](../geographic/county-profile.md) - Geographic data
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Prevalence rates
- [enrollment-projections.md](enrollment-projections.md) - Timeline estimates
- [diversity-planning.md](diversity-planning.md) - Diversity targets
