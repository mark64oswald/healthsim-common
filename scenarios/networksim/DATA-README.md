# NetworkSim Data Package

**Version**: 2.0  
**Last Updated**: December 27, 2025  
**Location**: `healthsim.duckdb` (network schema)

---

## Overview

NetworkSim v2.0 is a data-driven network analytics product built on real healthcare provider data. Unlike v1.0's synthetic generation, v2.0 queries actual NPPES, CMS, and HRSA datasets for authentic provider lookups, network analysis, and cross-product analytics.

**Key Feature**: Geographic enrichment enables cross-schema JOINs with PopulationSim demographic data for healthcare access analysis.

---

## Database Schema: `network`

### Tables Summary

| Table | Records | Description |
|-------|---------|-------------|
| **providers** | 8.9M | Active US healthcare providers (NPPES) |
| **facilities** | 77K | Hospitals and healthcare facilities (CMS POS) |
| **hospital_quality** | 5.4K | Hospital quality ratings (CMS Hospital Compare) |
| **physician_quality** | 1.5M | Physician performance metrics (CMS Physician Compare) |
| **ahrf_county** | 3.2K | County-level workforce data (HRSA AHRF) |

**Total Size**: ~1.2 GB  
**Geographic Coverage**: 97.77% of providers have county FIPS codes  
**Counties Covered**: 3,213 (exceeds PopulationSim's 3,143)

---

## Table Schemas

### `network.providers` (8,925,672 records)

Primary table containing all active US healthcare providers from NPPES.

**Key Columns**:
- `npi` (VARCHAR): 10-digit National Provider Identifier (PRIMARY KEY)
- `entity_type_code` (VARCHAR): '1' = Individual, '2' = Organization
- `first_name`, `last_name` (VARCHAR): Individual provider names
- `organization_name` (VARCHAR): Organization legal name
- `credential` (VARCHAR): Credentials (MD, DO, RN, etc.)
- `gender` (VARCHAR): Gender code
- `practice_address_1`, `practice_city`, `practice_state`, `practice_zip` (VARCHAR): Practice location
- `taxonomy_1` - `taxonomy_4` (VARCHAR): Healthcare provider taxonomy codes
- `county_fips` (VARCHAR): **5-digit county FIPS** (enables PopulationSim JOINs)
- `phone` (VARCHAR): Practice phone number
- `created_at` (TIMESTAMP): Import timestamp

**Geographic Enrichment**: 97.77% of providers have county FIPS codes assigned via ZIP→County crosswalk.

**Indexes**:
- PRIMARY KEY on `npi`
- INDEX on `practice_state`
- INDEX on `county_fips`
- INDEX on `taxonomy_1`

---

### `network.facilities` (77,302 records)

Healthcare facilities from CMS Provider of Services file.

**Key Columns**:
- `ccn` (VARCHAR): CMS Certification Number (PRIMARY KEY)
- `name` (VARCHAR): Facility name
- `city`, `state`, `zip` (VARCHAR): Location
- `type` (VARCHAR): Facility type (Hospital, Nursing Home, etc.)
- `subtype` (VARCHAR): Facility subtype
- `beds` (INTEGER): Licensed bed count
- `phone` (VARCHAR): Contact phone
- `created_at` (TIMESTAMP): Import timestamp

---

### `network.hospital_quality` (5,421 records)

Hospital quality ratings from CMS Hospital Compare.

**Key Columns**:
- `facility_id` (VARCHAR): CMS facility identifier (PRIMARY KEY)
- `facility_name` (VARCHAR): Hospital name
- `city_town`, `state` (VARCHAR): Location
- `hospital_overall_rating` (VARCHAR): 1-5 star rating
- `hospital_overall_rating_footnote` (VARCHAR): Rating notes
- `created_at` (TIMESTAMP): Import timestamp

---

### `network.physician_quality` (1,478,309 records)

Physician performance metrics from CMS Physician Compare.

**Key Columns**:
- `npi` (VARCHAR): National Provider Identifier (PRIMARY KEY)
- `mips_score` (DECIMAL): Merit-based Incentive Payment System score
- `board_certified` (BOOLEAN): Board certification status
- `medicare_beneficiaries` (INTEGER): Number of Medicare patients
- `created_at` (TIMESTAMP): Import timestamp

**Foreign Key**: `npi` → `network.providers.npi`

---

### `network.ahrf_county` (3,235 records)

Area Health Resources File county-level workforce data.

**Key Columns**:
- `county_fips` (VARCHAR): 5-digit county FIPS (PRIMARY KEY)
- `county_name` (VARCHAR): County name
- `primary_care_phys` (INTEGER): Number of primary care physicians
- `pcp_per_100k` (DECIMAL): Primary care physicians per 100K population
- `hpsa_primary_care` (BOOLEAN): Health Professional Shortage Area status
- `created_at` (TIMESTAMP): Import timestamp

---

## Cross-Schema Integration

### Join Keys

**Geographic Joins (PopulationSim)**:
```sql
-- Join providers with CDC health indicators
SELECT 
    p.countyname,
    p.diabetes_crudeprev,
    COUNT(n.npi) as provider_count
FROM population.places_county p
LEFT JOIN network.providers n ON p.countyfips = n.county_fips
GROUP BY p.countyname, p.diabetes_crudeprev;
```

**Social Vulnerability Analysis**:
```sql
-- Healthcare access in high-vulnerability counties
SELECT 
    s.county,
    s.rpl_themes as vulnerability_score,
    COUNT(n.npi) as provider_count,
    s.e_totpop as population
FROM population.svi_county s
LEFT JOIN network.providers n ON s.stcnty = n.county_fips
WHERE s.rpl_themes >= 0.75  -- Top quartile vulnerability
GROUP BY s.county, s.rpl_themes, s.e_totpop;
```

---

## Data Sources

### Primary Sources

| Data | Source | Update Frequency |
|------|--------|------------------|
| NPPES Provider Registry | [CMS NPPES](https://npiregistry.cms.hhs.gov/) | Monthly |
| Provider of Services | [CMS Data](https://data.cms.gov/) | Quarterly |
| Hospital Compare | [CMS Data](https://data.cms.gov/) | Quarterly |
| Physician Compare | [CMS Data](https://data.cms.gov/) | Quarterly |
| AHRF County Data | [HRSA Data](https://data.hrsa.gov/) | Annual |

### Supporting Data

- **ZIP→County Crosswalk**: [HUD USPS](https://www.huduser.gov/portal/datasets/usps_crosswalk.html)
- **Healthcare Provider Taxonomy**: [NUCC Taxonomy](https://www.nucc.org/)

---

## Data Quality Metrics

**Test Suite**: `scenarios/networksim/tests/test_data_quality.py`

### Current Metrics (Session 4 Validation)

✅ **Provider Data**:
- Total providers: 8,925,672
- NPI format: 100% valid (10 digits)
- Duplicate NPIs: 0
- Entity type: 100% valid (1 or 2)
- State coverage: 97 states/territories

✅ **Geographic Enrichment**:
- County FIPS coverage: 97.77% (exceeds 95% target)
- County FIPS format: 100% valid (5 digits)
- Counties covered: 3,213

✅ **Cross-Product Integration**:
- PopulationSim JOIN: 3,023 counties matched
- SVI JOIN: 3,045 counties matched
- Multi-schema queries: <1 second

✅ **Facility & Quality**:
- Facilities: 77,302
- Hospital quality records: 5,421
- Physician quality records: 1,478,309

**Test Command**:
```bash
cd scenarios/networksim
python3 -m pytest tests/test_data_quality.py -v
```

---

## Usage Examples

### Provider Search by Specialty
```sql
SELECT npi, first_name, last_name, practice_city, practice_state
FROM network.providers
WHERE taxonomy_1 = '207Q00000X'  -- Family Medicine
AND practice_state = 'CA'
LIMIT 100;
```

### Hospital Quality Lookup
```sql
SELECT facility_name, city_town, state, hospital_overall_rating
FROM network.hospital_quality
WHERE state = 'NY'
AND hospital_overall_rating IN ('4', '5')
ORDER BY facility_name;
```

### Healthcare Desert Analysis
```sql
SELECT 
    s.county,
    s.state,
    s.e_totpop as population,
    COUNT(p.npi) as provider_count,
    ROUND(1000.0 * COUNT(p.npi) / NULLIF(s.e_totpop, 0), 2) as providers_per_1000
FROM population.svi_county s
LEFT JOIN network.providers p ON s.stcnty = p.county_fips
WHERE s.e_totpop > 0
GROUP BY s.county, s.state, s.e_totpop
HAVING COUNT(p.npi) < 10
ORDER BY s.e_totpop DESC;
```

---

## Refresh Procedures

### Monthly NPPES Refresh

1. Download latest NPPES file (first Sunday of month)
2. Filter to active US providers
3. Run geographic enrichment
4. Validate with test suite
5. Replace `network.providers` table

**Script**: `scenarios/networksim/scripts/filter_nppes.py`

### Quarterly CMS Updates

1. Download updated POS, Hospital Compare, Physician Compare files
2. Process and import to staging tables
3. Validate data quality
4. Swap staging→production

---

## Maintenance Notes

### Known Data Characteristics

**Missing County FIPS** (2.23%):
- Primarily military/overseas addresses (APO, FPO, DPO)
- Some PO Box-only addresses
- Territories with incomplete ZIP data

**Physician Quality Coverage**:
- Only providers participating in Medicare programs
- ~17% of total provider base

**Facility Quality Ratings**:
- Only hospitals participating in Medicare/Medicaid
- ~7% of total facility base

---

## Version History

### v2.0 (December 2025)
- ✅ Real NPPES data (8.9M providers)
- ✅ Geographic enrichment (97.77% coverage)
- ✅ Cross-schema integration with PopulationSim
- ✅ Comprehensive test suite (18 tests)
- ✅ CMS quality metrics integrated

### v1.0 (2024)
- Synthetic generation via Skills
- No real provider data
- Archived: `skills/networksim/archive/v1/`

---

## Support

**Issues**: [GitHub Issues](https://github.com/mark64oswald/healthsim-workspace/issues)  
**Documentation**: `docs/NETWORKSIM-ARCHITECTURE.md`  
**Tests**: `scenarios/networksim/tests/`

---

**Last Validated**: December 27, 2025  
**Next Refresh**: January 2026 (NPPES monthly update)
