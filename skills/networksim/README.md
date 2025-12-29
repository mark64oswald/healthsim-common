# NetworkSim

> Access real provider reference data and generate synthetic healthcare provider entities including providers, facilities, pharmacies, and network configurations.

## What NetworkSim Does

NetworkSim is the **provider network** component of HealthSim. It provides two complementary capabilities:

1. **Reference Data Access** - Query 8.9 million real US healthcare providers from the NPPES registry stored in DuckDB
2. **Synthetic Generation** - Generate synthetic provider entities with valid-format NPIs for testing and demos

When other HealthSim products need a provider for an encounter, a pharmacy for a prescription, or a facility for a claim, NetworkSim provides the appropriate entity - either from real data or synthetically generated.

## Quick Start

### Query Real Providers (from NPPES)

```
Find cardiologists in Houston, TX
How many primary care physicians are in San Diego County?
Show me hospitals in Phoenix with more than 300 beds
```

### Generate Synthetic Providers

```
Generate a cardiologist for this patient's encounter
Generate a 200-bed acute care hospital
Generate a specialty pharmacy for oncology medications
```

See [hello-healthsim examples](../../hello-healthsim/examples/networksim-examples.md) for detailed examples.

## Data Architecture

NetworkSim reference data is stored in the unified HealthSim DuckDB database under the `network` schema:

| Table | Records | Description |
|-------|---------|-------------|
| `network.providers` | 8,925,672 | All US healthcare providers from NPPES |
| `network.facilities` | ~35,000 | Medicare-certified facilities from CMS POS |
| `network.hospital_quality` | ~4,500 | Hospital quality metrics from CMS |
| `network.physician_quality` | ~1.2M | Physician quality data from CMS |
| `network.ahrf_county` | ~3,200 | County healthcare resources from HRSA |

**Data Source**: CMS NPPES (National Plan and Provider Enumeration System) - public domain, updated monthly.

### Provider Table Structure

Key columns in `network.providers`:

| Column | Description |
|--------|-------------|
| `npi` | 10-digit National Provider Identifier |
| `entity_type_code` | 1=Individual, 2=Organization |
| `first_name`, `last_name` | Provider name (individuals) |
| `organization_name` | Organization name (type 2) |
| `primary_taxonomy_code` | Healthcare Provider Taxonomy Code |
| `city`, `state`, `zip_code` | Practice location |
| `credential_text` | Credentials (MD, DO, NP, etc.) |

## Key Capabilities

| Capability | Description | Data Source |
|------------|-------------|-------------|
| **Provider Lookup** | Find providers by NPI, specialty, location | DuckDB (real data) |
| **Geographic Analysis** | Provider distribution by county/state | DuckDB (real data) |
| **Specialty Search** | Find providers by taxonomy code | DuckDB (real data) |
| **Synthetic Providers** | Generate test providers with valid NPI format | On-demand generation |
| **Synthetic Facilities** | Generate hospitals, ASCs, clinics | On-demand generation |
| **Synthetic Pharmacies** | Generate retail, mail-order, specialty pharmacies | On-demand generation |
| **Network Patterns** | HMO, PPO, tiered network structures | Reference knowledge |

## When to Use Each Approach

### Use Real Data (Query) When:

- You need actual provider NPIs for validation
- You're analyzing provider distribution by geography
- You need realistic specialty mix for a region
- You're building network adequacy reports
- You need to verify a provider exists

### Use Synthetic Generation When:

- You're creating test data for demos
- You need reproducible synthetic scenarios
- Real provider data isn't relevant to your use case
- You want to avoid any association with real providers
- You're building tutorials or training materials

## Example Queries

### Find Providers by Specialty and Location

```sql
SELECT npi, first_name, last_name, credential_text, city
FROM network.providers
WHERE state = 'CA'
  AND primary_taxonomy_code = '207RC0000X'  -- Cardiovascular Disease
  AND city = 'SAN FRANCISCO'
LIMIT 10;
```

### Count Providers by State

```sql
SELECT state, COUNT(*) as provider_count
FROM network.providers
WHERE entity_type_code = '1'  -- Individuals only
GROUP BY state
ORDER BY provider_count DESC
LIMIT 10;
```

### Find Hospitals with Quality Metrics

```sql
SELECT p.organization_name, p.city, p.state, h.overall_rating
FROM network.providers p
JOIN network.hospital_quality h ON p.npi = h.facility_id
WHERE p.state = 'TX'
  AND h.overall_rating >= 4
ORDER BY h.overall_rating DESC;
```

## Integration with Other Products

| Product | NetworkSim Provides | Example |
|---------|---------------------|---------|
| **PatientSim** | Attending, referring, PCP | Cardiologist NPI for heart failure encounter |
| **MemberSim** | Billing provider, network status | In-network vs OON for adjudication |
| **RxMemberSim** | Dispensing pharmacy | Pharmacy NPI for prescription fill |
| **TrialSim** | Site, investigator | PI credentials for trial site |

## Reference Knowledge

NetworkSim also provides domain knowledge about how provider networks work:

| Topic | Description |
|-------|-------------|
| Network Types | HMO, PPO, EPO, POS structures and trade-offs |
| Plan Structures | Cost sharing, benefit design, tiered networks |
| Pharmacy Benefits | PBM concepts, formulary tiers, specialty pharmacy |
| Network Adequacy | Access standards, provider-to-member ratios |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | (default) | API testing, integration |
| CSV | "as CSV" | Analytics, spreadsheets |

## Skills Reference

For complete generation parameters, examples, and validation rules, see:

- **[SKILL.md](SKILL.md)** - Full skill reference with all capabilities
- **[../../SKILL.md](../../SKILL.md)** - Master skill file (cross-product routing)

## Related Documentation

- [hello-healthsim NetworkSim Examples](../../hello-healthsim/examples/networksim-examples.md)
- [Data Architecture Guide](../../docs/data-architecture.md) - Database schema details
- [Architecture Guide](../../docs/HEALTHSIM-ARCHITECTURE-GUIDE.md) - Overall system architecture
- [Code Systems Reference](../../references/code-systems.md) - Taxonomy codes

---

*NetworkSim provides access to real NPPES provider data for queries and analytics, plus synthetic generation for test data.*
