# NetworkSim Master Skill

**Description**: Provider network data queries and analytics using real NPPES provider data, CMS facility data, and quality metrics integrated with PopulationSim demographics

**Version**: 2.0.0  
**Status**: Active (Phase 3 - Advanced Analytics)  
**Data Scale**: 8.9M providers, 60K+ facilities, 5.4K hospitals with quality ratings

---

## Overview

NetworkSim enables authentic provider network analysis through real NPPES and CMS data embedded in HealthSim's DuckDB database. Query 8.9 million providers, analyze network adequacy against regulatory standards, and identify healthcare deserts by integrating provider access with health needs and social vulnerability.

**Core Capabilities**:
- Search providers by specialty, location, credentials (8.9M records)
- Validate NPIs with Luhn algorithm checksums
- Assess network adequacy (CMS MA, NCQA, Medicaid MCO standards)
- Generate network rosters (CSV/JSON/Excel export)
- Identify healthcare deserts (access + health burden + vulnerability)
- Quality-based filtering (CMS star ratings, credentials)

**Cross-Product Integration**:
- PopulationSim demographics (county-level JOINs)
- Social Vulnerability Index (SVI) - equity analysis
- CDC PLACES health indicators - disease burden correlation
- Quality metrics - Hospital Compare star ratings

---

## Skill Categories

### Query Skills (6 skills) ✅

**Search & Discovery:**
- **[provider-search](query/provider-search.md)**: Search 8.9M providers by specialty, location, credentials
- **[facility-search](query/facility-search.md)**: Search hospitals, nursing homes, clinics by type and geography
- **[pharmacy-search](query/pharmacy-search.md)**: Search retail, specialty, and mail-order pharmacies

**Analysis & Validation:**
- **[npi-validation](query/npi-validation.md)**: Validate NPIs with Luhn algorithm checksums
- **[network-roster](query/network-roster.md)**: Generate provider rosters in multiple formats (CSV/JSON/Excel)
- **[provider-density](query/provider-density.md)**: Calculate providers per 100K population with HRSA benchmarks
- **[coverage-analysis](query/coverage-analysis.md)**: Assess network coverage against CMS/NCQA standards

**Quality Filtering:**
- **[hospital-quality-search](query/hospital-quality-search.md)**: Filter hospitals by CMS star ratings (1-5 scale)
- **[physician-quality-search](query/physician-quality-search.md)**: Validate physician credentials (MD, DO, NP, PA)

### Analytics Skills (2 skills) 🎯

**Advanced Analysis:**
- **[network-adequacy-analysis](analytics/network-adequacy-analysis.md)**: Comprehensive adequacy assessment (time/distance, ratios, specialty coverage)
- **[healthcare-deserts](analytics/healthcare-deserts.md)**: Identify underserved areas (access + health needs + vulnerability)

### Integration Skills (Planned) 📋

**Cross-Product Patterns:**
- population-network-integration: Link demographics with provider access
- health-equity-analysis: Disparity identification and intervention prioritization
- value-based-network-design: Quality-tier network optimization

---

## Quick Start Examples

### Find Cardiologists in Houston
```
"Find cardiologists in Houston, Texas"
```
→ Uses provider-search skill  
→ Returns providers with taxonomy 207RC00 (Cardiovascular Disease)

### Assess Network Adequacy for California
```
"Assess primary care network adequacy for California against CMS standards"
```
→ Uses network-adequacy-analysis skill  
→ Compares actual PCPs vs required (1:1,200 ratio)

### Identify Healthcare Deserts
```
"Show me the most critical healthcare deserts in Texas"
```
→ Uses healthcare-deserts skill  
→ Combines low provider access + high health needs + social vulnerability

### Generate Provider Roster
```
"Create a network roster for primary care providers in San Diego County, export to CSV"
```
→ Uses network-roster skill  
→ Generates CSV with NPI, name, specialty, location, credentials

---

## Regulatory Standards Supported

### CMS Medicare Advantage
- Provider-to-enrollee ratios (1:1,200 PCPs, 1:2,000 OB/GYN, etc.)
- Time/distance access standards (urban/suburban/rural)
- Essential specialty requirements
- Network adequacy reporting

### NCQA Health Plan Accreditation
- 13 essential specialty categories
- Geographic distribution requirements
- Provider credential standards
- Quality metrics integration

### HRSA Provider Benchmarks
- 60-80 providers per 100K population (primary care)
- Health Professional Shortage Area (HPSA) criteria
- Medically Underserved Area (MUA) designation

### State Medicaid MCO
- Varies by state (stricter standards in some states)
- Essential Community Provider (ECP) requirements
- Network adequacy by county/region

---

## Data Sources & Quality

### Provider Data (8.9M records)
- **Source**: NPPES (National Plan and Provider Enumeration System)
- **Update Frequency**: Monthly CMS releases
- **Coverage**: All active US healthcare providers with NPIs
- **Quality**: 97.77% county FIPS coverage (3,213 counties)

### Facility Data (60K+ facilities)
- **Source**: CMS Provider of Services (POS) file
- **Types**: Hospitals (01), Nursing Homes (05), Clinics, Dialysis Centers
- **Quality Metrics**: Hospital Compare star ratings (5,421 hospitals)

### Demographics (PopulationSim)
- **SVI**: Social Vulnerability Index (3,144 counties)
- **PLACES**: CDC health indicators (3,143 counties)
- **Census**: Population, age, race/ethnicity distributions

---

## Performance Benchmarks

| Query Type | Target | Actual | Status |
|------------|--------|--------|--------|
| Provider search | <100ms | 13.8ms | ✅ Excellent |
| NPI validation | <50ms | 18.8ms | ✅ Excellent |
| Provider density | <100ms | 46.9ms | ✅ Good |
| Network adequacy | <300ms | ~200ms | ✅ Good |
| Healthcare deserts | <500ms | ~400ms | ✅ Good |

**Database Size**: 1.7GB (healthsim.duckdb)  
**Query Optimization**: Indexed on county_fips, taxonomy_1, practice_state

---

## Usage Patterns

### Health Plan Operations
- Network development (geography + specialty + quality)
- Regulatory compliance reporting (CMS MA, NCQA)
- Provider recruitment prioritization
- Member directory generation

### Analytics & Strategy
- Market analysis and competitive intelligence
- Healthcare desert identification
- Equity analysis (vulnerable populations)
- Value-based network optimization

### Quality Improvement
- Provider scorecards (quality metrics)
- Performance management (low/high performers)
- Star rating optimization
- Cost-quality efficiency analysis

---

## Cross-Product Integration Examples

### NetworkSim + PopulationSim
```sql
-- Provider access in vulnerable communities
SELECT 
    sv.county,
    sv.rpl_themes as svi_percentile,
    COUNT(DISTINCT p.npi) as provider_count
FROM ref_svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
WHERE sv.rpl_themes > 0.75  -- Most vulnerable
GROUP BY sv.county, sv.rpl_themes
ORDER BY provider_count ASC;
```

### Healthcare Deserts Analysis
```sql
-- Low access + high disease burden
SELECT 
    sv.county,
    COUNT(p.npi) as providers,
    pl.diabetes_prevalence,
    sv.poverty_rate
FROM ref_svi_county sv
LEFT JOIN network.providers p ON sv.stcnty = p.county_fips
LEFT JOIN ref_places_county pl ON sv.stcnty = pl.locationid
WHERE COUNT(p.npi) * 100000.0 / sv.e_totpop < 40  -- Low density
  AND pl.diabetes_prevalence > 12  -- High disease
GROUP BY sv.county;
```

---

## Development Status

### Phase 1: Data Infrastructure ✅ (Sessions 1-4)
- [x] NPPES data import (8.9M providers)
- [x] Geographic enrichment (97.77% county FIPS coverage)
- [x] Quality metrics integration (CMS Hospital Compare)
- [x] Test framework establishment (18 tests passing)

### Phase 2: Query Skills ✅ (Sessions 5-7)
- [x] Search skills (provider, facility, pharmacy)
- [x] Analysis skills (NPI validation, roster, density, coverage)
- [x] Quality skills (hospital ratings, physician credentials)
- [x] 9 skills total, 4,069 lines documentation

### Phase 3: Advanced Analytics 🎯 (Sessions 8-12)
- [x] Network adequacy analysis (Session 8)
- [x] Healthcare deserts identification (Session 8)
- [ ] Specialty distribution analysis (Session 9)
- [ ] Provider demographics analysis (Session 9)
- [ ] Cross-product integration patterns (Sessions 10-12)

**Overall Progress**: 66% (8 of 12 sessions complete)

---

## Related Documentation

- **[Master Plan](../../scenarios/networksim/NETWORKSIM-V2-MASTER-PLAN.md)**: Complete implementation roadmap
- **[Architecture](../../docs/NETWORKSIM-ARCHITECTURE.md)**: Database design and data flows
- **[Data Guide](../../scenarios/networksim/DATA-ARCHITECTURE.md)**: Table schemas and relationships
- **[Session Summaries](../../scenarios/networksim/)**: Detailed session logs

---

## Support & Maintenance

**Data Updates**:
- NPPES: Monthly refresh from CMS
- Hospital Quality: Quarterly updates from Hospital Compare
- Demographics: Annual updates from Census/CDC

**Performance Monitoring**:
- Query performance benchmarks
- Database size tracking
- Index optimization

**Quality Assurance**:
- NPI validation (Luhn checksums)
- County FIPS completeness
- Taxonomy code validation

---

*Last Updated: December 27, 2025*  
*Version: 2.0.0*  
*Status: Active Development (Phase 3)*
