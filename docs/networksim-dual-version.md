# NetworkSim Dual-Version Architecture

**Purpose**: Explains the relationship between NetworkSim (public) and NetworkSim-Local (private)

---

## Overview

NetworkSim exists in two versions to address different needs:

| Aspect | NetworkSim (Public) | NetworkSim-Local (Private) |
|--------|---------------------|----------------------------|
| **Repository** | healthsim-workspace (public) | networksim-local (private) |
| **Purpose** | Synthetic provider/network generation | Real provider data lookup |
| **Data Source** | Claude generates on-demand | NPPES/CMS registry data |
| **NPIs** | Valid format, but synthetic | Actual registered NPIs |
| **Use Case** | Demos, tutorials, testing | Research, validation, enrichment |
| **Integration** | Full HealthSim ecosystem | Loosely coupled utility |

---

## Why Two Versions?

### NetworkSim (Public)

The public version serves the core HealthSim mission: **generate realistic synthetic healthcare data through conversation**. It:

- Generates synthetic providers with realistic attributes
- Creates network patterns (HMO, PPO, tiered networks)
- Produces valid-format NPIs that aren't real
- Integrates seamlessly with PatientSim, MemberSim, TrialSim
- Appears in hello-healthsim, demos, and tutorials
- Contains no large data files (purely generative)

**Location**: `/skills/networksim/` in healthsim-workspace

### NetworkSim-Local (Private)

The private version provides access to **real provider data** for scenarios where synthetic isn't sufficient:

- Queries actual NPPES registry (~9M providers)
- Returns real NPIs for validation or enrichment
- Provides geographic distribution analysis
- Enables "real-world" research scenarios
- Data files too large for GitHub (~9GB raw, ~1.7GB database)
- Kept separate to avoid accidental public exposure

**Location**: `/Users/markoswald/Developer/projects/networksim-local/`

---

## Data Comparison

### NetworkSim (Public) Generates:

```json
{
  "npi": "1234567890",          // Valid format, synthetic
  "entity_type": "individual",
  "name": {
    "first": "Sarah",
    "last": "Chen",
    "credential": "MD"
  },
  "specialty": "Internal Medicine",
  "taxonomy_code": "207R00000X",
  "address": {
    "city": "San Francisco",
    "state": "CA",
    "zip": "94102"
  }
}
```

### NetworkSim-Local Returns:

```json
{
  "npi": "1679576722",          // Real registered NPI
  "entity_type": 1,
  "provider_last_name": "SMITH",
  "provider_first_name": "JOHN",
  "provider_credential_text": "MD",
  "healthcare_provider_taxonomy_code_1": "207R00000X",
  "provider_business_practice_location_address_city_name": "SAN FRANCISCO",
  "provider_business_practice_location_address_state_name": "CA",
  "provider_business_practice_location_address_postal_code": "941021234"
}
```

---

## When to Use Each

### Use NetworkSim (Public) When:

- Generating demo data for presentations
- Creating test scenarios for development
- Building tutorials and documentation
- Any public-facing content
- Integration with other HealthSim products
- You need consistent, reproducible synthetic data

### Use NetworkSim-Local (Private) When:

- Validating against real provider distributions
- Research requiring actual NPI lookups
- Geographic analysis of real provider networks
- Enriching synthetic data with real attributes
- Verifying specialty codes and taxonomy mappings
- Building features that will eventually use real data

---

## Integration Patterns

### Pattern 1: Pure Synthetic (Public Only)

For demos, tutorials, and testing:

```
User Request: "Generate a cardiologist in California"
     ↓
NetworkSim (Public): Generates synthetic provider
     ↓
PatientSim: Uses provider in encounter
     ↓
MemberSim: Creates claim with provider NPI
```

### Pattern 2: Real Data Enrichment (Private + Public)

For research or validation:

```
Step 1: Query NetworkSim-Local
     ↓
     "Find 5 real cardiologists in San Francisco"
     ↓
     Returns actual NPIs: [1679576722, 1234567893, ...]

Step 2: Use real NPI in synthetic scenario
     ↓
     PatientSim encounter uses real NPI
     ↓
     MemberSim claim references real provider
```

### Pattern 3: Distribution Analysis (Private Only)

For geographic/specialty research:

```sql
-- NetworkSim-Local query
SELECT 
    practice_state,
    COUNT(*) as provider_count,
    COUNT(*) FILTER (taxonomy_code LIKE '207R%') as internists
FROM providers
WHERE entity_type = 1
GROUP BY practice_state
ORDER BY provider_count DESC;
```

---

## File Organization

### NetworkSim (Public) - healthsim-workspace

```
skills/networksim/
├── README.md                  # Product overview
├── SKILL.md                   # Skill reference
├── developer-guide.md         # Implementation details
│
├── reference/                 # Domain knowledge
│   ├── network-types.md
│   ├── plan-structures.md
│   └── ...
│
├── synthetic/                 # Generation skills
│   ├── synthetic-provider.md
│   ├── synthetic-network.md
│   └── ...
│
├── patterns/                  # Network patterns
│   ├── hmo-network-pattern.md
│   └── ...
│
└── integration/               # Cross-product skills
    ├── provider-for-encounter.md
    └── ...
```

### NetworkSim-Local (Private) - separate repo

```
networksim-local/
├── README.md                  # Overview and setup
├── SKILL.md                   # Skill reference
├── developer-guide.md         # Technical details
├── networksim-local.code-workspace
│
├── data/                      # LOCAL ONLY - gitignored
│   ├── README.md              # Data documentation (committed)
│   ├── nppes/                 # Raw NPPES files
│   ├── taxonomy/              # Taxonomy reference
│   └── networksim-local.duckdb
│
├── setup/                     # Setup scripts (committed)
│   ├── setup-all.py
│   ├── download-nppes.py
│   ├── build-database.py
│   └── validate-db.py
│
├── skills/                    # Query skills (committed)
│   ├── provider-lookup.md
│   ├── geographic-search.md
│   └── ...
│
└── queries/                   # SQL templates (committed)
    └── provider-queries.sql
```

---

## Repository Separation

### Why Separate Repositories?

1. **Size**: Raw NPPES data is ~9GB, far exceeding GitHub limits
2. **Privacy**: Private repo prevents accidental public exposure
3. **Independence**: Can update data without affecting main workspace
4. **Flexibility**: Different update cadences (NPPES monthly vs code as-needed)

### What's Committed vs Local-Only

| Component | In Git | Local Only |
|-----------|--------|------------|
| README.md, SKILL.md | ✅ | |
| Setup scripts | ✅ | |
| Skill definitions | ✅ | |
| Query templates | ✅ | |
| .gitignore | ✅ | |
| data/README.md | ✅ | |
| Raw CSV files | | ✅ |
| DuckDB database | | ✅ |
| Download archives | | ✅ |

---

## Future Roadmap

### Near-Term

1. Both versions operational and documented
2. Clear guidance on when to use each
3. Minimal coupling between public/private

### Medium-Term

1. **Download Scripts Distribution**: Provide setup scripts to interested users
2. **Pre-Built Database Option**: Host processed DuckDB on CDN for faster setup
3. **API Layer**: Optional REST API for NetworkSim-Local queries

### Long-Term (SaaS Consideration)

1. **Hosted Real Data**: Cloud-hosted NPPES database
2. **Subscription Tiers**: Filter by state, specialty, or full access
3. **Automatic Updates**: Monthly refresh without user intervention
4. **Integration API**: Direct integration with HealthSim products

---

## Quick Reference

### NetworkSim (Public) - Synthetic Generation

```
Location:   healthsim-workspace/skills/networksim/
Repo:       https://github.com/mark64oswald/healthsim-workspace
Workspace:  healthsim.code-workspace
Purpose:    Generate synthetic providers and networks
```

### NetworkSim-Local (Private) - Real Data

```
Location:   /Users/markoswald/Developer/projects/networksim-local/
Repo:       https://github.com/mark64oswald/networksim-local (private)
Workspace:  networksim-local.code-workspace
Purpose:    Query real NPPES provider registry
Data Size:  ~1.7GB (DuckDB), ~9GB (raw)
```

---

*Last Updated: December 2025*
