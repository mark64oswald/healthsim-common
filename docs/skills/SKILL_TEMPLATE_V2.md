# [Skill Name]

_Brief one-sentence description of what this skill enables._

## For Claude

Use this skill when the user [describes when to apply this skill]. This skill teaches you [what clinical/domain knowledge it provides] so you can generate [what kinds of patients/scenarios].

You should apply this knowledge when:
- [Specific user request pattern 1]
- [Specific user request pattern 2]
- [Specific clinical scenario 1]
- [When user mentions specific keywords]

This skill provides [summary of knowledge types: e.g., vital sign patterns, medication regimens, temporal progressions, etc.].

## Purpose

[2-3 paragraphs explaining what this skill enables from a clinical/educational perspective]

This skill supports:
- [Use case 1]
- [Use case 2]
- [Use case 3]

Designed for [target audience or training scenarios].

## When to Use This Skill

Apply this skill when the user mentions:

**Direct Keywords**:
- "[keyword 1]", "[keyword 2]", "[keyword 3]"
- "[medical term 1]", "[medical term 2]"
- "[abbreviation]" (Explanation of abbreviation)

**Clinical Scenarios**:
- [Description of scenario type 1]
- [Description of scenario type 2]
- "[Example user phrasing]"

**Implicit Indicators**:
- Requests for [related concept]
- Mentions of [associated condition]
- [Situational cue]

**Co-occurring Mentions**:
- Often paired with: [related conditions, settings, or treatments]
- Frequently includes: [keywords that appear together]
- May mention: [optional related concepts]

## Domain Knowledge

### [Major Concept 1]

[Narrative explanation of the first major concept. Teach Claude the clinical pattern, not just list facts.]

**Why this matters for generation**: [Explain how Claude should apply this knowledge when creating patients]

#### [Sub-concept if needed]

[More specific details. Use narrative style to explain relationships and patterns.]

**Key Clinical Pattern**: [Describe a recognizable pattern Claude should remember]

### [Major Concept 2]

[Continue with additional major concepts...]

### [Common Patterns Section]

When [condition], you typically see:
- [Observable pattern 1] - [why it occurs]
- [Observable pattern 2] - [clinical significance]
- [Observable pattern 3] - [relationship to other findings]

**Typical presentation**: [Narrative description of how this presents]

### [Laboratory/Diagnostic Patterns]

**[Test Category]**:
- [Test name]: [range] ([interpretation])
  - [Why this value range] - [clinical meaning]
  - [What affects this value]

**Pattern Recognition**: [Describe how multiple lab values relate to each other]

### [Medication Patterns]

**[Medication Class or Indication]**:
```
[Medication 1]: [Dose] [Route] [Frequency]
  - Indication: [When/why used]
  - Timing: [When in course of treatment]
  - Monitoring: [What to watch]

[Medication 2]: [Dose] [Route] [Frequency]
  - Alternative to [Medication 1] when [condition]
  - Duration: [How long]
```

**Selection Logic**: [Explain how to choose between medications based on patient factors]

### [Temporal Progression Patterns]

[Describe how the condition evolves over time]

**Typical Timeline**:
```
[Timepoint 1] ([Time description]):
  - [What's happening clinically]
  - [Observable changes]
  - [Interventions at this point]

[Timepoint 2] ([Time description]):
  - [Progression or response]
  - [New findings]
  - [Treatment changes]
```

**Why this matters for generation**: If creating a patient at [early/middle/late] stage, their presentation should match the corresponding timepoint.

## Generation Guidelines

### How to Apply This Knowledge

**When the user says**: "[Common user request phrasing]"

**Claude should**:
1. [First decision or inference]
2. [Second decision or inference]
3. [Third decision or inference]
4. [Fourth decision or inference]

**Key Generation Rules**:

#### Demographics Considerations
- [Age patterns for this condition]
- [Gender considerations if relevant]
- [Risk factors to consider including]
- [Population-specific notes]

#### Clinical Feature Coherence

**[Feature 1]-[Feature 2] Relationship**: [Describe how these should correlate]
- [Example of appropriate correlation]
- [Warning about implausible combinations]

**[Feature 3]-[Feature 4] Relationship**: [Describe expected pattern]

#### [Domain-Specific] Selection Logic

```python
# Pseudocode showing Claude's reasoning process
if [condition 1]:
    [select option A]
    [implication for other features]
elif [condition 2]:
    [select option B]
    [different implications]

if [severity marker]:
    add([additional feature needed for this severity])
```

#### Clinical Coherence Checks

Before finalizing a patient with [this condition], verify:
- [ ] [Check 1 description]
- [ ] [Check 2 description]
- [ ] [Check 3 description]
- [ ] [Check 4 description]
- [ ] [Check 5 description]

### Variation Strategies

**[Dimension 1]: [Mild vs Severe]**:
- Mild: [defining features of mild presentation]
- Moderate: [defining features of moderate presentation]
- Severe: [defining features of severe presentation]

**[Dimension 2]: [Typical vs Atypical]**:
- Typical: [classic presentation features]
- Atypical: [unusual presentation features, when they occur]

**[Dimension 3]: [Complicated vs Uncomplicated]**:
- Uncomplicated: [straightforward course]
- Complicated: [complications that can develop, how they manifest]

## Parameters

Parameters customize generation through natural language. Frame these as conversations with the user.

| Parameter | Natural Language Description | Type | Default | Claude's Interpretation |
|-----------|------------------------------|------|---------|------------------------|
| [param1] | [Question to user about this aspect] | enum: [opt1], [opt2], [opt3] | [default] | [How Claude interprets each option and what it affects] |
| [param2] | [Question to user] | range | [default] | [What this range controls in generation] |
| [param3] | [Question to user] | enum: [opt1], [opt2] | [default] | [Impact on patient features] |
| [param4] | [Question to user] | boolean | [default] | [What changes if true vs false] |

**How Claude Uses Parameters**:
- `[param1]=[value]` → [specific generation behavior]
- `[param2]=[value]` → [different specific behavior]
- `[param3]=[value]` → [another specific behavior]

## Example Requests and Interpretations

### Example 1: [Basic/Straightforward Request]

**User says**: "[Example user phrasing]"

**Claude interprets**:
- [Inference 1 with reasoning]
- [Inference 2 with reasoning]
- [Inference 3 with reasoning]
- [Setting/context determination]

**Key features Claude generates**:
- Demographics: [age range and relevant characteristics]
- Vital signs: [specific values with reasoning]
- Labs: [specific values with clinical meaning]
- Diagnosis: [ICD-10 code] ([description])
- Medications: [specific medications with reasoning]
- [Other relevant features]

### Example 2: [Severity-Specific Request]

**User says**: "[Example showing severity cue]"

**Claude interprets**:
- [How Claude recognizes severity signal]
- [What severity level is implied]
- [What additional features are required]

**Key features Claude generates**:
- [How features differ from Example 1 due to severity]
- [Specific severity-appropriate values]
- [Additional interventions needed at this severity]

### Example 3: [Source/Type-Specific Request]

**User says**: "[Example with specific subtype]"

**Claude interprets**:
- [How Claude identifies the specific subtype]
- [What makes this subtype different]
- [Specific features associated with this subtype]

**Key features Claude generates**:
- [Subtype-specific demographics]
- [Subtype-specific symptoms/signs]
- [Subtype-specific labs or tests]
- [Subtype-appropriate treatment]

### Example 4: [Temporal/Progression Request]

**User says**: "[Example asking for evolution over time]"

**Claude interprets**:
- [Understanding of temporal request]
- [What pattern of change is expected]
- [Timeline parameters]

**Key features Claude generates**:
```
[Timepoint 1]:
  [Values at first timepoint]
  [Clinical state]

[Timepoint 2]:
  [How values changed]
  [Progression note]

[Timepoint 3]:
  [Further changes]
  [Intervention or outcome]
```

### Example 5: [Atypical/Special Case Request]

**User says**: "[Example with unusual presentation cue]"

**Claude interprets**:
- [Recognition of atypical flag]
- [What makes presentation atypical]
- [Special considerations]

**Key features Claude generates**:
- [How features differ from typical]
- [Absence of expected findings]
- [Presence of unusual findings]
- [Why this presentation occurs (e.g., elderly, immunocompromised)]

## Related Skills

Complementary skills Claude might need:

- **[skill/path.md]** - [Brief description of how it relates]
- **[skill/path.md]** - [Brief description of how it relates]
- **[skill/path.md]** - [Brief description of how it relates]

## Metadata

- **Type**: [domain-knowledge | scenario-template | format-spec | validation-rules]
- **Version**: 2.0
- **Format**: Claude-Optimized (v2.0)
- **Author**: [Your name or team]
- **Tags**: [tag1, tag2, tag3, tag4]
- **Created**: [YYYY-MM-DD]
- **Updated**: [YYYY-MM-DD]

## References

**Clinical Guidelines**:
- [Guideline name and year]
- [Guideline name and year]

**Evidence**:
- [Key studies or evidence sources]

**Tools/Calculators**:
- [Clinical decision tools referenced]

---

## Template Usage Notes

**Delete this section in actual skills**

When creating a skill from this template:

1. **Replace all [bracketed placeholders]** with actual content
2. **Delete sections** that don't apply (e.g., if no temporal progression, remove that section)
3. **Focus on narrative style** in Domain Knowledge - teach patterns, not schemas
4. **Include 3-5 diverse examples** showing different interpretations
5. **Test your skill** by seeing if Claude can answer: "When should I use this skill?" and "What does a typical patient look like?"

**Section priorities** (what to emphasize):
1. "For Claude" + "When to Use" - Critical for discoverability
2. "Domain Knowledge" - Core teaching section
3. "Example Requests" - Shows Claude how to interpret
4. "Generation Guidelines" - Ensures coherent output
5. Everything else - Helpful but secondary

**Voice and tone**:
- Write "For Claude" and "When to Use" in second person ("Use this when you...")
- Write "Domain Knowledge" as teaching/explanatory ("Sepsis occurs when...")
- Write "Examples" showing reasoning ("Claude interprets this as...")
- Use "Why this matters for generation" to connect knowledge to practice
