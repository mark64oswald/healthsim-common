# [Skill Name]
[Brief description of what this skill provides - one or two sentences]

## Metadata
- **Type**: [domain-knowledge | scenario-template | format-spec | validation-rules]
- **Version**: 1.0
- **Author**: [Your name or team]
- **Tags**: [comma, separated, tags]

## Purpose
[Detailed explanation of when and why to use this skill. Include:
- What scenarios this skill is designed for
- What problems it solves
- How it should be used in practice]

<!-- For scenario-template skills, include Parameters and Generation Rules -->

## Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| param_name | range | 40-70 | [Description of what this parameter controls] |
| severity | enum | moderate | [Allowed values: mild, moderate, severe] |
| enabled | boolean | true | [Description of boolean parameter] |

<!--
Parameter types:
- range: Numeric range (e.g., "60-85", "2.0-4.5")
- enum: Fixed set of values (list in description)
- boolean: true/false
- integer: Whole number
- string: Free text
-->

## Generation Rules

### Demographics
- Age: {{age_range}}
- Gender: weighted(male: 0.6, female: 0.4)
- Race: any

### Conditions
**Primary Diagnosis**:
- [ICD-10 code] ([Description])

**Comorbidities** ([probability]%):
- [ICD-10 code] ([Description])

### Vital Signs
**Temperature**: [range] °F ([interpretation])
**Heart Rate**: [range] bpm ([interpretation])
**Respiratory Rate**: [range] /min ([interpretation])
**Blood Pressure**: [range]/[range] mmHg ([interpretation])
**SpO2**: [range]% ([interpretation])

### Laboratory
**[Category Name]**:
- [Test Name]: [range] [unit] ([interpretation])

### Medications
**[Category Name]**:
- [Drug name] [dose] [route] [frequency] ([indication])

### Timeline
1. **[Time Point]**: [Event description]
2. **[Time Point]**: [Event description]

<!-- For domain-knowledge skills, include Knowledge section instead -->

## Knowledge

### [Subsection Name]
[Information about this topic]

### Clinical Concepts
- **[Term]**: [Definition]

### Terminology
- **[Acronym]**: [Full name and explanation]

### Diagnostic Criteria
1. [Criterion description]
2. [Criterion description]

<!-- For format-spec skills, include Format section -->

## Format

### Structure
[Description of format structure]

### Required Fields
- [Field name]: [Description and requirements]

### Encoding Rules
- [Rule description]

<!-- For validation-rules skills, include Rules section -->

## Rules

### Rule: [Rule Name]
- **Code**: RULE_001
- **Severity**: error | warning | info
- **Condition**: [When this rule applies]
- **Check**: [What to validate]
- **Message**: [Error message template]

<!-- Optional: Variations for scenario-template skills -->

## Variations

### Variation: [Variation Name]
[Description of what this variation changes]
- [Parameter]: [override value]
- Add: [additional elements]

<!-- Optional: Examples showing expected usage -->

## Examples

### Example 1: [Use Case Name]
```
User: [What the user would say]
Expected:
- [Expected outcome 1]
- [Expected outcome 2]
```

### Example 2: [Another Use Case]
```
User: [Another usage example]
Expected:
- [Expected outcome]
```

<!-- Optional: External references -->

## References
- [Link to clinical guideline, terminology source, etc.]
- [Citation to medical reference]

<!-- Optional: Other skills this depends on -->

## Dependencies
- skills/[category]/[skill-name].md
- skills/[category]/[another-skill].md

<!-- Or if no dependencies: -->
## Dependencies
None - this is a standalone skill.

---

## Template Notes

**Delete this section when creating your skill!**

### Quick Start
1. Replace `[Skill Name]` with your skill's name
2. Fill in Metadata section with appropriate values
3. Write a clear Purpose section
4. Choose the appropriate sections for your skill type:
   - **scenario-template**: Parameters, Generation Rules, Variations
   - **domain-knowledge**: Knowledge
   - **format-spec**: Format
   - **validation-rules**: Rules
5. Add Examples to show usage
6. Delete this Template Notes section

### Parameter Types Guide
- **range**: "60-85" or "2.0-4.5" - use for numeric ranges
- **enum**: List allowed values in description, default should be one of them
- **boolean**: true or false - use for on/off options
- **integer**: Whole number like 5, 10, 100
- **string**: Free text like "pneumonia" or "moderate"

### Template Variables
Use `{{parameter_name}}` to reference parameters in Generation Rules.

### Probability Notation
- Exact: "80%" or "0.8"
- Descriptive: "likely (> 70%)", "rare (< 10%)"
- Weighted: "weighted(option1: 0.6, option2: 0.4)"

### Best Practices
- **Be Specific**: Use exact ranges and values, not vague terms
- **Include Units**: Always specify units (mg/dL, bpm, mmHg, etc.)
- **Explain Why**: Add clinical context in parentheses
- **Use Standards**: Reference ICD-10, LOINC, RxNorm when applicable
- **Test Your Skill**: Include examples that demonstrate all features
