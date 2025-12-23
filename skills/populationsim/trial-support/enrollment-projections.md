---
name: enrollment-projections
description: >
  Project clinical trial enrollment timelines based on population data and
  site capacity. Models enrollment curves, identifies acceleration opportunities,
  and supports contingency planning. Triggers: "enrollment projection", "how
  long to enroll", "enrollment timeline", "enrollment rate".
---

# Enrollment Projections Skill

## Overview

The enrollment-projections skill models clinical trial enrollment timelines using population feasibility data, site capacity, and historical enrollment patterns. It provides realistic projections with confidence intervals to support trial planning.

**Primary Use Cases**:
- Enrollment timeline planning
- Site activation sequencing
- Contingency planning
- Resource allocation

---

## Trigger Phrases

- "How long to enroll [N] subjects?"
- "Enrollment projection for [trial]"
- "When will we complete enrollment?"
- "Enrollment timeline for [condition] trial"
- "Project enrollment rate for [site network]"

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `target_enrollment` | int | Yes | - | Total subjects needed |
| `sites` | array/object | Yes | - | Site details or count |
| `condition` | string | Yes | - | Target condition |
| `geography` | string | No | - | Geographic scope |
| `start_date` | date | No | today | Enrollment start |
| `ramp_period_months` | int | No | 3 | Site activation ramp |

---

## Enrollment Models

### Linear Model (Simple)
```
Monthly enrollment = Sites × Rate per site
Time = Target ÷ Monthly enrollment
```

### Ramp-Up Model (Realistic)
```
Month 1-2: 25% of steady-state
Month 3-4: 50% of steady-state
Month 5-6: 75% of steady-state
Month 7+: 100% steady-state
```

### S-Curve Model (Detailed)
```
Incorporates:
- Staggered site activation
- Competition effects
- Seasonal variation
- Pool depletion
```

---

## Site Enrollment Rates by Type

| Site Type | Monthly Range | Median | Factors |
|-----------|---------------|--------|---------|
| Large Academic | 3-8 | 5 | High capacity, competition |
| Regional Academic | 2-5 | 3 | Moderate capacity |
| Large Community | 1-3 | 2 | Lower awareness |
| Small Community | 0.5-1.5 | 1 | Limited resources |
| Network/Consortium | 5-15 | 8 | Aggregated sites |

### Condition-Specific Adjustments

| Condition | Adjustment | Reason |
|-----------|------------|--------|
| Common chronic (DM, HTN) | 1.0x | Baseline |
| Moderate prevalence (HF, COPD) | 0.8x | Smaller pool |
| Rare disease (<1%) | 0.3-0.5x | Limited patients |
| Oncology | 0.6x | Strict criteria, competition |
| Healthy volunteers | 1.5-2.0x | Easier recruitment |

---

## Output Schema

```json
{
  "enrollment_projection": {
    "trial_parameters": {
      "target_enrollment": 500,
      "condition": "E11",
      "condition_name": "Type 2 Diabetes",
      "phase": "Phase 3",
      "sites_planned": 25
    },
    
    "site_network": {
      "total_sites": 25,
      "by_type": {
        "academic": 8,
        "community": 17
      },
      "by_region": {
        "northeast": 6,
        "southeast": 7,
        "midwest": 5,
        "southwest": 4,
        "west": 3
      },
      "total_monthly_capacity": {
        "steady_state": 62,
        "range": [45, 80]
      }
    },
    
    "activation_schedule": {
      "month_1": { "sites": 5, "cumulative": 5 },
      "month_2": { "sites": 8, "cumulative": 13 },
      "month_3": { "sites": 7, "cumulative": 20 },
      "month_4": { "sites": 5, "cumulative": 25 }
    },
    
    "enrollment_curve": {
      "model": "ramp_up",
      "monthly_projections": [
        { "month": 1, "enrolled": 8, "cumulative": 8 },
        { "month": 2, "enrolled": 18, "cumulative": 26 },
        { "month": 3, "enrolled": 28, "cumulative": 54 },
        { "month": 4, "enrolled": 38, "cumulative": 92 },
        { "month": 5, "enrolled": 48, "cumulative": 140 },
        { "month": 6, "enrolled": 55, "cumulative": 195 },
        { "month": 7, "enrolled": 60, "cumulative": 255 },
        { "month": 8, "enrolled": 62, "cumulative": 317 },
        { "month": 9, "enrolled": 62, "cumulative": 379 },
        { "month": 10, "enrolled": 62, "cumulative": 441 },
        { "month": 11, "enrolled": 59, "cumulative": 500 }
      ]
    },
    
    "timeline_summary": {
      "enrollment_start": "2025-01-15",
      "50_pct_milestone": "2025-06-15",
      "enrollment_complete": "2025-11-20",
      "total_duration_months": 10.2,
      "confidence_interval": {
        "optimistic": 8.5,
        "expected": 10.2,
        "pessimistic": 13.8
      }
    },
    
    "risk_factors": {
      "screen_failure_rate": {
        "assumed": 0.40,
        "impact_if_higher": "+2 months at 50% SF"
      },
      "site_activation_delays": {
        "assumed_delay_pct": 0.20,
        "impact": "+1.5 months if 30% delayed"
      },
      "competition": {
        "competing_trials": 3,
        "impact": "Moderate - factored into rates"
      },
      "seasonal_effects": {
        "holiday_impact": "-15% Nov-Dec",
        "summer_impact": "-10% Jun-Aug"
      }
    },
    
    "scenarios": {
      "optimistic": {
        "assumptions": "Fast activation, low SF, high engagement",
        "duration_months": 8.5,
        "probability": 0.15
      },
      "expected": {
        "assumptions": "Baseline rates, normal ramp",
        "duration_months": 10.2,
        "probability": 0.60
      },
      "pessimistic": {
        "assumptions": "Slow ramp, high SF, site issues",
        "duration_months": 13.8,
        "probability": 0.25
      }
    },
    
    "recommendations": [
      "Front-load academic site activation for faster ramp",
      "Plan for 15% screen failure rate buffer",
      "Consider 2-3 backup sites for contingency",
      "Avoid holiday period for enrollment close"
    ]
  },
  
  "metadata": {
    "model_version": "enrollment_v2.1",
    "generated_at": "2024-12-23T10:00:00Z"
  }
}
```

---

## Examples

### Example 1: Phase 3 Diabetes Trial

**Request**: "Project enrollment for 800 subjects in a diabetes trial with 40 sites"

**Response**:

**Phase 3 Diabetes Enrollment Projection**

**Parameters**:
- Target: 800 subjects
- Sites: 40 (12 academic, 28 community)
- Condition: Type 2 Diabetes

**Site Capacity**:
| Type | Sites | Rate/Site | Monthly |
|------|-------|-----------|---------|
| Academic | 12 | 4/mo | 48 |
| Community | 28 | 1.5/mo | 42 |
| **Total** | 40 | - | **90/mo** |

**Enrollment Timeline**:

```
Subjects
800 ─┼───────────────────────────────●
     │                          ●●●●
600 ─┼                     ●●●●
     │                ●●●●
400 ─┼           ●●●●
     │      ●●●●
200 ─┼  ●●●
     │●●
  0 ─┼──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬─
     0  1  2  3  4  5  6  7  8  9 10
                  Months
```

| Milestone | Date | Subjects |
|-----------|------|----------|
| First Subject | Month 1 | 15 |
| 25% (200) | Month 3 | 200 |
| 50% (400) | Month 5 | 400 |
| 75% (600) | Month 7 | 600 |
| 100% (800) | Month 10 | 800 |

**Duration**: **10 months** (CI: 8-13 months)

---

### Example 2: Rare Disease Trial

**Request**: "Enrollment projection for rare NASH trial: 200 subjects, 15 sites"

**Response**:

**NASH Trial Enrollment Projection**

**Challenge**: Lower prevalence + strict criteria

**Adjusted Rates**:
| Site Type | Standard Rate | NASH Adjusted |
|-----------|---------------|---------------|
| Academic | 4/mo | 1.5/mo |
| Community | 1.5/mo | 0.5/mo |

**Network Capacity**:
- 15 sites × 1.0 avg = **15/month steady-state**

**Timeline**:
| Month | Monthly | Cumulative |
|-------|---------|------------|
| 1-2 | 4 | 8 |
| 3-4 | 8 | 24 |
| 5-6 | 12 | 48 |
| 7-8 | 14 | 76 |
| 9-10 | 15 | 106 |
| 11-12 | 15 | 136 |
| 13-14 | 15 | 166 |
| 15-16 | 15 | 196 |
| 17 | 4 | 200 |

**Duration**: **17 months** (CI: 14-22 months)

**Risk**: High screen failure typical for NASH (50-60%)

**Recommendations**:
- Add 5 backup sites
- Implement central screening support
- Consider adaptive design for early futility

---

### Example 3: Accelerated Oncology Trial

**Request**: "How fast can we enroll 150 subjects for a lung cancer trial?"

**Response**:

**Lung Cancer Trial Accelerated Enrollment**

**Baseline Projection** (Standard approach):
- 20 sites, 0.8/site/mo = 16/month
- Duration: ~12 months

**Accelerated Options**:

| Strategy | Additional Investment | Time Saved |
|----------|----------------------|------------|
| Add 10 sites | $500K | 3 months |
| Increase site payments | $200K | 1.5 months |
| Central screening | $150K | 1 month |
| Patient advocacy partnership | $100K | 2 months |
| **Combined** | **$950K** | **5-6 months** |

**Accelerated Timeline**:
- Baseline: 12 months
- With investment: **6-7 months**

**Monthly Enrollment Comparison**:
| Scenario | Month 3 | Month 6 | Complete |
|----------|---------|---------|----------|
| Standard | 25 | 75 | Month 12 |
| Accelerated | 45 | 120 | Month 7 |

---

## Enrollment Acceleration Strategies

### Site-Level
| Strategy | Impact | Cost |
|----------|--------|------|
| More sites | +20-40% | High |
| Higher per-patient payments | +10-15% | Moderate |
| Dedicated coordinators | +15-25% | Moderate |
| EMR alerts | +10-20% | Low |

### Patient-Level
| Strategy | Impact | Cost |
|----------|--------|------|
| Patient advocacy | +10-20% | Low |
| Social media outreach | +5-15% | Low |
| Travel reimbursement | +10-15% | Moderate |
| Telehealth visits | +5-10% | Low |

### Operational
| Strategy | Impact | Cost |
|----------|--------|------|
| Central lab | +5-10% | Moderate |
| Mobile phlebotomy | +5-10% | Moderate |
| Rapid site activation | +15-20% | Low |

---

## Validation Rules

### Input Validation
- Target enrollment > 0
- Sites > 0
- Valid condition

### Output Validation
- [ ] Cumulative enrollment reaches target
- [ ] Monthly rates match site capacity
- [ ] Timeline includes ramp-up period
- [ ] Scenarios span reasonable range

---

## Related Skills

- [site-feasibility.md](site-feasibility.md) - Site capacity input
- [diversity-planning.md](diversity-planning.md) - May impact timeline
- [chronic-disease-prevalence.md](../health-patterns/chronic-disease-prevalence.md) - Prevalence rates
