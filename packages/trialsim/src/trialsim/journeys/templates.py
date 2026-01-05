"""TrialSim journey templates.

Pre-built journey specifications for common clinical trial protocols.
These templates can be used directly or customized for specific trial designs.
"""

from healthsim.generation.journey_engine import (
    JourneySpecification,
    EventDefinition,
    DelaySpec,
    EventCondition,
    TrialEventType,
    create_simple_journey,
)


# =============================================================================
# Journey Template Definitions
# =============================================================================

TRIAL_JOURNEY_TEMPLATES = {
    "phase3-oncology-standard": {
        "journey_id": "phase3-oncology-standard",
        "name": "Phase 3 Oncology Standard Protocol",
        "description": "Standard phase 3 oncology trial with 24-week treatment period",
        "products": ["trialsim"],
        "duration_days": 252,  # 36 weeks including follow-up
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "visit_name": "Screening",
                    "visit_number": -1,
                    "pass_rate": 0.75,
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 28},
                "depends_on": "screening",
                "parameters": {
                    "arm_weights": {"Treatment": 0.67, "Placebo": 0.33},
                },
            },
            {
                "event_id": "baseline",
                "name": "Baseline Visit (Day 1)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_name": "Baseline",
                    "visit_number": 1,
                    "procedures": ["vital_signs", "labs", "tumor_assessment"],
                },
            },
            {
                "event_id": "week2",
                "name": "Week 2 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 12, "days_max": 18},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 2",
                    "visit_number": 2,
                    "procedures": ["vital_signs", "labs", "ae_assessment"],
                },
            },
            {
                "event_id": "week4",
                "name": "Week 4 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 25, "days_max": 35},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 4",
                    "visit_number": 3,
                    "procedures": ["vital_signs", "labs"],
                },
            },
            {
                "event_id": "week8",
                "name": "Week 8 Visit (First Tumor Assessment)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56, "days_min": 52, "days_max": 63},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 8",
                    "visit_number": 4,
                    "procedures": ["vital_signs", "labs", "tumor_assessment"],
                },
            },
            {
                "event_id": "week12",
                "name": "Week 12 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 84, "days_min": 77, "days_max": 91},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 12",
                    "visit_number": 5,
                    "procedures": ["vital_signs", "labs"],
                },
            },
            {
                "event_id": "week16",
                "name": "Week 16 Visit (Second Tumor Assessment)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 112, "days_min": 105, "days_max": 119},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 16",
                    "visit_number": 6,
                    "procedures": ["vital_signs", "labs", "tumor_assessment"],
                },
            },
            {
                "event_id": "week24",
                "name": "Week 24 Visit (End of Treatment)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 168, "days_min": 161, "days_max": 175},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 24 / End of Treatment",
                    "visit_number": 7,
                    "procedures": ["vital_signs", "labs", "tumor_assessment", "ecg"],
                },
            },
            {
                "event_id": "followup_30day",
                "name": "30-Day Safety Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 30, "days_min": 28, "days_max": 35},
                "depends_on": "week24",
                "parameters": {
                    "visit_name": "30-Day Follow-up",
                    "visit_number": 8,
                    "procedures": ["vital_signs", "ae_assessment"],
                },
            },
            {
                "event_id": "survival_followup",
                "name": "Survival Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 84, "days_min": 77, "days_max": 98},
                "depends_on": "week24",
                "parameters": {
                    "visit_name": "Survival Follow-up",
                    "visit_number": 9,
                    "procedures": ["survival_status"],
                },
            },
        ],
    },
    
    "phase2-diabetes-dose-finding": {
        "journey_id": "phase2-diabetes-dose-finding",
        "name": "Phase 2 Diabetes Dose-Finding Study",
        "description": "12-week dose-finding study with multiple treatment arms",
        "products": ["trialsim"],
        "duration_days": 112,  # 16 weeks including run-in and follow-up
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "visit_name": "Screening",
                    "pass_rate": 0.70,
                },
            },
            {
                "event_id": "run_in",
                "name": "Run-in Period Start",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 5, "days_max": 14},
                "depends_on": "screening",
                "parameters": {
                    "visit_name": "Run-in Start",
                    "visit_number": -1,
                    "procedures": ["vital_signs", "hba1c", "fasting_glucose"],
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 14},
                "depends_on": "run_in",
                "parameters": {
                    "arm_weights": {
                        "Low Dose": 0.25,
                        "Medium Dose": 0.25,
                        "High Dose": 0.25,
                        "Placebo": 0.25,
                    },
                },
            },
            {
                "event_id": "baseline",
                "name": "Baseline (Day 1)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_name": "Baseline",
                    "visit_number": 1,
                    "procedures": ["vital_signs", "hba1c", "fasting_glucose", "lipid_panel"],
                },
            },
            {
                "event_id": "week2",
                "name": "Week 2 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 12, "days_max": 17},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 2",
                    "visit_number": 2,
                    "procedures": ["vital_signs", "fasting_glucose"],
                },
            },
            {
                "event_id": "week4",
                "name": "Week 4 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 25, "days_max": 32},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 4",
                    "visit_number": 3,
                    "procedures": ["vital_signs", "fasting_glucose"],
                },
            },
            {
                "event_id": "week8",
                "name": "Week 8 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56, "days_min": 52, "days_max": 60},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 8",
                    "visit_number": 4,
                    "procedures": ["vital_signs", "hba1c", "fasting_glucose"],
                },
            },
            {
                "event_id": "week12",
                "name": "Week 12 Visit (End of Treatment)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 84, "days_min": 80, "days_max": 88},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 12 / End of Treatment",
                    "visit_number": 5,
                    "procedures": ["vital_signs", "hba1c", "fasting_glucose", "lipid_panel"],
                },
            },
            {
                "event_id": "followup",
                "name": "2-Week Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 12, "days_max": 18},
                "depends_on": "week12",
                "parameters": {
                    "visit_name": "Follow-up",
                    "visit_number": 6,
                    "procedures": ["vital_signs", "ae_assessment"],
                },
            },
        ],
    },
    
    "phase1-healthy-volunteer": {
        "journey_id": "phase1-healthy-volunteer",
        "name": "Phase 1 Healthy Volunteer PK Study",
        "description": "Single-ascending dose PK study in healthy volunteers",
        "products": ["trialsim"],
        "duration_days": 28,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "visit_name": "Screening",
                    "pass_rate": 0.85,
                },
            },
            {
                "event_id": "admission",
                "name": "Unit Admission (Day -1)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 3, "days_max": 21},
                "depends_on": "screening",
                "parameters": {
                    "visit_name": "Day -1 Check-in",
                    "visit_number": 0,
                    "procedures": ["vital_signs", "labs", "ecg", "physical_exam"],
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "admission",
                "parameters": {
                    "arm_weights": {"Active": 0.75, "Placebo": 0.25},
                },
            },
            {
                "event_id": "dosing",
                "name": "Dosing (Day 1)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_name": "Dosing Day",
                    "visit_number": 1,
                    "procedures": ["dosing", "pk_sample_predose", "pk_sample_0.5h", "pk_sample_1h", "pk_sample_2h", "pk_sample_4h", "pk_sample_8h", "pk_sample_12h"],
                },
            },
            {
                "event_id": "day2",
                "name": "Day 2 (24h PK)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "dosing",
                "parameters": {
                    "visit_name": "Day 2",
                    "visit_number": 2,
                    "procedures": ["vital_signs", "pk_sample_24h", "ae_assessment"],
                },
            },
            {
                "event_id": "day3",
                "name": "Day 3 (48h PK)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "day2",
                "parameters": {
                    "visit_name": "Day 3",
                    "visit_number": 3,
                    "procedures": ["vital_signs", "pk_sample_48h"],
                },
            },
            {
                "event_id": "discharge",
                "name": "Discharge (Day 4)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "day3",
                "parameters": {
                    "visit_name": "Discharge",
                    "visit_number": 4,
                    "procedures": ["vital_signs", "pk_sample_72h", "labs", "physical_exam"],
                },
            },
            {
                "event_id": "followup",
                "name": "Follow-up Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 5, "days_max": 10},
                "depends_on": "discharge",
                "parameters": {
                    "visit_name": "Follow-up",
                    "visit_number": 5,
                    "procedures": ["vital_signs", "ae_assessment"],
                },
            },
        ],
    },
    
    "phase2-cardiology-long-term": {
        "journey_id": "phase2-cardiology-long-term",
        "name": "Phase 2 Cardiology Long-Term Outcomes Study",
        "description": "52-week cardiovascular outcomes study",
        "products": ["trialsim"],
        "duration_days": 420,  # 60 weeks including follow-up
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "visit_name": "Screening",
                    "pass_rate": 0.65,
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 28},
                "depends_on": "screening",
                "parameters": {
                    "arm_weights": {"Treatment": 0.5, "Placebo": 0.5},
                },
            },
            {
                "event_id": "baseline",
                "name": "Baseline Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_name": "Baseline",
                    "visit_number": 1,
                    "procedures": ["vital_signs", "labs", "ecg", "echo"],
                },
            },
            {
                "event_id": "week4",
                "name": "Week 4 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 28, "days_min": 25, "days_max": 35},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 4",
                    "visit_number": 2,
                    "procedures": ["vital_signs", "labs", "ecg"],
                },
            },
            {
                "event_id": "week12",
                "name": "Week 12 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 84, "days_min": 77, "days_max": 91},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 12",
                    "visit_number": 3,
                    "procedures": ["vital_signs", "labs"],
                },
            },
            {
                "event_id": "week26",
                "name": "Week 26 Visit (6 Month)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 182, "days_min": 168, "days_max": 196},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 26",
                    "visit_number": 4,
                    "procedures": ["vital_signs", "labs", "ecg", "echo"],
                },
            },
            {
                "event_id": "week39",
                "name": "Week 39 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 273, "days_min": 259, "days_max": 287},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 39",
                    "visit_number": 5,
                    "procedures": ["vital_signs", "labs"],
                },
            },
            {
                "event_id": "week52",
                "name": "Week 52 Visit (End of Treatment)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 364, "days_min": 350, "days_max": 378},
                "depends_on": "baseline",
                "parameters": {
                    "visit_name": "Week 52 / End of Treatment",
                    "visit_number": 6,
                    "procedures": ["vital_signs", "labs", "ecg", "echo"],
                },
            },
            {
                "event_id": "followup",
                "name": "8-Week Safety Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56, "days_min": 49, "days_max": 63},
                "depends_on": "week52",
                "parameters": {
                    "visit_name": "Follow-up",
                    "visit_number": 7,
                    "procedures": ["vital_signs", "ae_assessment"],
                },
            },
        ],
    },
    
    "rwe-observational": {
        "journey_id": "rwe-observational",
        "name": "Real-World Evidence Observational Study",
        "description": "Non-interventional observational study following routine care",
        "products": ["trialsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "enrollment",
                "name": "Study Enrollment",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "visit_name": "Enrollment",
                    "pass_rate": 0.90,
                },
            },
            {
                "event_id": "baseline_assessment",
                "name": "Baseline Assessment",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "enrollment",
                "parameters": {
                    "visit_name": "Baseline",
                    "visit_number": 1,
                    "procedures": ["demographics", "medical_history", "concomitant_meds"],
                },
            },
            {
                "event_id": "month3",
                "name": "Month 3 Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 90, "days_min": 75, "days_max": 105},
                "depends_on": "baseline_assessment",
                "parameters": {
                    "visit_name": "Month 3",
                    "visit_number": 2,
                    "procedures": ["outcomes_assessment", "healthcare_utilization"],
                },
            },
            {
                "event_id": "month6",
                "name": "Month 6 Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 180, "days_min": 165, "days_max": 195},
                "depends_on": "baseline_assessment",
                "parameters": {
                    "visit_name": "Month 6",
                    "visit_number": 3,
                    "procedures": ["outcomes_assessment", "healthcare_utilization", "pro_survey"],
                },
            },
            {
                "event_id": "month9",
                "name": "Month 9 Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 270, "days_min": 255, "days_max": 285},
                "depends_on": "baseline_assessment",
                "parameters": {
                    "visit_name": "Month 9",
                    "visit_number": 4,
                    "procedures": ["outcomes_assessment", "healthcare_utilization"],
                },
            },
            {
                "event_id": "month12",
                "name": "Month 12 Final Assessment",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 365, "days_min": 350, "days_max": 380},
                "depends_on": "baseline_assessment",
                "parameters": {
                    "visit_name": "Month 12 / Study End",
                    "visit_number": 5,
                    "procedures": ["outcomes_assessment", "healthcare_utilization", "pro_survey", "study_exit"],
                },
            },
        ],
    },
}


def get_trial_journey_template(template_id: str) -> dict | None:
    """Get a trial journey template by ID.
    
    Args:
        template_id: Template identifier (e.g., 'phase3-oncology-standard')
        
    Returns:
        Template dictionary or None if not found
    """
    return TRIAL_JOURNEY_TEMPLATES.get(template_id)


def list_trial_journey_templates() -> list[dict]:
    """List all available trial journey templates.
    
    Returns:
        List of template summaries with id, name, description
    """
    return [
        {
            "id": template_id,
            "name": template.get("name", template_id),
            "description": template.get("description", ""),
            "duration_days": template.get("duration_days", 0),
            "event_count": len(template.get("events", [])),
        }
        for template_id, template in TRIAL_JOURNEY_TEMPLATES.items()
    ]
