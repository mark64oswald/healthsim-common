"""TrialSim-specific event handlers for the journey engine.

This module provides handlers for TrialSim clinical trial events that can be registered
with the core JourneyEngine. Handlers generate the appropriate outputs
(screenings, visits, adverse events, etc.) when events are executed.

The handlers wrap the core healthsim.generation.handlers.TrialSimHandlers class
and provide a consistent interface matching MemberSim and RxMemberSim patterns.
"""

from typing import Any

from healthsim.generation.journey_engine import (
    JourneyEngine,
    TrialEventType,
    TimelineEvent,
    create_journey_engine,
)
from healthsim.generation.handlers import TrialSimHandlers as CoreTrialSimHandlers


# Re-export the core handlers class for direct access if needed
TrialSimHandlers = CoreTrialSimHandlers


def screening_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle screening visit events.
    
    Generates screening records with inclusion/exclusion criteria results.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_screening(subject, event, context)


def randomization_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle randomization events.
    
    Assigns subjects to treatment arms and generates randomization records.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_randomization(subject, event, context)


def withdrawal_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle subject withdrawal events.
    
    Generates withdrawal/discontinuation records.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_withdrawal(subject, event, context)


def scheduled_visit_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle scheduled study visit events.
    
    Generates visit records with procedures and assessments.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_scheduled_visit(subject, event, context)


def unscheduled_visit_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle unscheduled study visit events.
    
    Generates unscheduled visit records (e.g., AE follow-up).
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_unscheduled_visit(subject, event, context)


def adverse_event_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle adverse event reporting.
    
    Generates AE records with severity, causality assessment.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_adverse_event(subject, event, context)


def serious_adverse_event_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle serious adverse event reporting.
    
    Generates SAE records with expedited reporting requirements.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_serious_adverse_event(subject, event, context)


def protocol_deviation_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle protocol deviation events.
    
    Generates protocol deviation records.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_protocol_deviation(subject, event, context)


def dose_modification_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle dose modification events.
    
    Generates dose adjustment records.
    """
    handlers = CoreTrialSimHandlers(context.get("seed"))
    return handlers.handle_dose_modification(subject, event, context)


def milestone_handler(
    subject: Any,
    event: TimelineEvent,
    context: dict[str, Any],
) -> dict[str, Any]:
    """Handle milestone events.
    
    Milestones are non-transactional markers in a subject's trial journey.
    """
    subject_id = _get_subject_id(subject)
    return {
        "type": "milestone",
        "subject_id": subject_id,
        "milestone_name": event.event_name,
        "milestone_date": event.scheduled_date.isoformat(),
        "parameters": event.result.get("parameters", {}) if event.result else {},
    }


def _get_subject_id(subject: Any) -> str:
    """Extract subject ID from various entity formats."""
    if isinstance(subject, dict):
        return subject.get("subject_id", subject.get("id", "unknown"))
    return getattr(subject, "subject_id", getattr(subject, "id", "unknown"))


def register_trial_handlers(engine: JourneyEngine, seed: int | None = None) -> None:
    """Register all TrialSim event handlers with a journey engine.
    
    Args:
        engine: JourneyEngine instance to register handlers with
        seed: Random seed for reproducibility
    """
    # Use the core handlers class for registration
    handlers = CoreTrialSimHandlers(seed)
    handlers.register_all(engine)
    
    # Also register milestone handler
    engine.register_handler("trialsim", "milestone", milestone_handler)


def create_trial_journey_engine(seed: int | None = None) -> JourneyEngine:
    """Create a JourneyEngine pre-configured with TrialSim handlers.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        JourneyEngine with all TrialSim handlers registered
        
    Example:
        >>> engine = create_trial_journey_engine(seed=42)
        >>> timeline = engine.create_timeline(subject, "subject", journey_spec)
        >>> results = engine.execute_timeline(timeline, subject)
    """
    engine = create_journey_engine(seed)
    register_trial_handlers(engine, seed)
    return engine
