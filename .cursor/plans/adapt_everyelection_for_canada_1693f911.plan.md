---
name: Adapt EveryElection for Canada
overview: Adapt the EveryElection codebase from UK-specific implementation to support Canadian elections at all levels (Federal, Provincial/Territorial, and Municipal), maintaining the same election ID format structure while replacing UK-specific dependencies and data sources with Canadian equivalents.
todos:
  - id: replace_uk_dependencies
    content: Remove UK-specific packages (uk-election-ids, uk-election-timetables, uk-geo-utils) from pyproject.toml and create/identify Canadian equivalents
    status: pending
  - id: create_ca_election_ids
    content: Create or adapt election ID generation system for Canadian elections (federal, provincial, territorial, municipal)
    status: pending
    dependencies:
      - replace_uk_dependencies
  - id: update_organisation_model
    content: Update Organisation model to use Canadian organisation types (federal, provincial, territorial, municipal) and province/territory codes
    status: pending
  - id: replace_postcode_system
    content: Replace UK postcode lookup (Onspd) with Canadian postal code geocoding system in query_helpers.py and managers.py
    status: pending
    dependencies:
      - replace_uk_dependencies
  - id: update_election_timetables
    content: Replace uk_election_timetables with Canadian election calendar logic in Election model get_timetable() method
    status: pending
    dependencies:
      - replace_uk_dependencies
  - id: update_boundary_imports
    content: Replace UK boundary import commands with Canadian boundary sources (Elections Canada, provincial sources, Statistics Canada)
    status: pending
  - id: update_geographic_constants
    content: Replace UK geographic constants (GSS codes, area types) with Canadian identifiers in organisations/constants.py and boundaries/constants.py
    status: pending
  - id: update_api_endpoints
    content: Update API views and filters to handle Canadian postal codes and remove UK-specific validation
    status: pending
    dependencies:
      - replace_postcode_system
  - id: create_canadian_import_commands
    content: Create management commands to import federal ridings, provincial districts, and municipal boundaries from Canadian sources
    status: pending
    dependencies:
      - update_boundary_imports
  - id: update_templates_ui
    content: Update templates and UI text to use Canadian terminology (ridings, postal codes) and remove UK references
    status: pending
  - id: update_tests
    content: Replace UK test data with Canadian examples (postal codes, organisations, election IDs) in all test files
    status: pending
    dependencies:
      - create_ca_election_ids
      - update_organisation_model
      - replace_postcode_system
  - id: update_documentation
    content: Update README, settings, and documentation to reflect Canadian context
    status: pending
---

# Adapting EveryElection for Canada

## Overview

EveryElection is a Django application for recording elections with semantic IDs. Currently built for the UK, it needs to be adapted for Canada's three-tier electoral system (Federal, Provincial/Territorial, Municipal).

## Architecture Understanding

The system uses:

- **Election ID Structure**: Hierarchical IDs like `[type].[organisation].[division].[date] `(e.g., `local.norfolk.diss.2017-05-04`)
- **Core Models**: `Election`, `Organisation`, `OrganisationDivision`, with geographic boundaries
- **UK Dependencies**: `uk-election-ids`, `uk-election-timetables`, `uk-geo-utils` (Onspd postcode database)
- **Data Sources**: BoundaryLine shapefiles, LGBCE data, UK government registers

## Key Changes Required

### 1. Replace UK-Specific Dependencies

**Files to modify:**

- [`pyproject.toml`](pyproject.toml) - Remove UK packages, add Canadian equivalents
- [`every_election/settings/base.py`](every_election/settings/base.py) - Update installed apps

**Actions:**

- Remove: `uk-election-ids`, `uk-election-timetables`, `uk-geo-utils`, `django-localflavor` (GB-specific)
- Create: `ca-election-ids` package (or adapt existing) for Canadian election ID generation
- Create: `ca-election-timetables` for Canadian election calendars
- Replace: UK postcode lookup with Canadian postal code lookup (different format: A1A 1A1)

### 2. Create Canadian Election ID System

**Files to create/modify:**

- [`every_election/apps/elections/utils.py`](every_election/apps/elections/utils.py) - Replace `ElectionBuilder` to use Canadian ID builder
- Create `every_election/apps/elections/ca_election_ids.py` - Canadian election ID logic

**Canadian Election Types:**

- `federal` - House of Commons elections
- `provincial` - Provincial legislature elections (BC, AB, ON, QC, etc.)
- `territorial` - Territorial elections (YT, NT, NU)
- `municipal` - Municipal/regional elections
- `school-board` - School board elections (if applicable)

**Organisation Structure:**

- Federal: Single `parl` organisation
- Provincial: One per province/territory (e.g., `ontario`, `quebec`, `british-columbia`)
- Municipal: Individual municipalities

### 3. Update Organisation Model

**Files to modify:**

- [`every_election/apps/organisations/models/organisations.py`](every_election/apps/organisations/models/organisations.py) - Replace UK organisation types

**Changes:**

- Replace `ORGTYPES` choices:
- Remove: `sp`, `naw`, `senedd`, `nia`, `europarl`, `police-area`, `combined-authority`, `gla`
- Add: `federal`, `provincial`, `territorial`, `municipal`, `school-board`
- Update `territory_code` to use Canadian province/territory codes (AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT)

### 4. Replace Geographic Data Sources

**Files to modify:**

- [`every_election/apps/organisations/boundaries/constants.py`](every_election/apps/organisations/boundaries/constants.py) - Replace UK boundary types
- [`every_election/apps/organisations/constants.py`](every_election/apps/organisations/constants.py) - Remove UK-specific mappings
- [`every_election/apps/elections/query_helpers.py`](every_election/apps/elections/query_helpers.py) - Replace UK postcode lookup

**Canadian Geographic Identifiers:**

- Replace GSS codes with Canadian identifiers (FED codes for federal ridings, provincial codes)
- Use Statistics Canada geographic identifiers
- Replace UK postcode database (Onspd) with Canadian postal code geocoding
- Update boundary import commands for Canadian shapefile sources

### 5. Update Election Timetables

**Files to modify:**

- [`every_election/apps/elections/models.py`](every_election/apps/elections/models.py) - Update `get_timetable()` method (lines 489-520)

**Changes:**

- Replace `uk_election_timetables` with Canadian election calendar logic
- Update territory code mapping:
- Remove: `WLS`, `ENG`, `NIR`, `SCT`, `GBN`
- Add: Canadian province/territory codes
- Adapt timetable calculation for Canadian electoral law

### 6. Update Postcode/Postal Code Lookup

**Files to modify:**

- [`every_election/apps/elections/query_helpers.py`](every_election/apps/elections/query_helpers.py) - Replace `ONSPDPostcodeLookup`
- [`every_election/apps/elections/managers.py`](every_election/apps/elections/managers.py) - Update postcode filtering

**Changes:**

- Replace `GBPostcodeField` with Canadian postal code validation
- Replace `OnspdGeocoder` with Canadian postal code geocoding service
- Canadian postal code format: `A1A 1A1` (letter-number-letter space number-letter-number)

### 7. Update Boundary Import Commands

**Files to modify:**

- [`every_election/apps/organisations/boundaries/management/commands/`](every_election/apps/organisations/boundaries/management/commands/) - All boundary import commands

**Canadian Boundary Sources:**

- Federal: Elections Canada riding boundaries
- Provincial: Individual provincial electoral boundary files
- Municipal: Statistics Canada or provincial sources
- Replace UK BoundaryLine imports with Canadian equivalents

### 8. Update API and Views

**Files to modify:**

- [`every_election/apps/api/views.py`](every_election/apps/api/views.py) - Update postcode parameter handling
- [`every_election/apps/api/filters.py`](every_election/apps/api/filters.py) - Ensure filters work with Canadian data

**Changes:**

- Update postcode validation in API endpoints
- Ensure coordinate-based lookups work with Canadian boundaries

### 9. Update Templates and UI

**Files to modify:**

- [`every_election/templates/`](every_election/templates/) - Update references to UK-specific terms
- [`every_election/apps/core/templates/`](every_election/apps/core/templates/) - Update branding

**Changes:**

- Replace "UK" references with "Canada"
- Update terminology (constituencies → ridings/electoral districts, postcodes → postal codes)
- Update example IDs and references

### 10. Update Settings and Configuration

**Files to modify:**

- [`every_election/settings/base.py`](every_election/settings/base.py) - Remove `uk_geo_utils` from INSTALLED_APPS
- [`README.md`](README.md) - Update documentation
- [`pyproject.toml`](pyproject.toml) - Update description

**Changes:**

- Update `LANGUAGE_CODE` if needed (currently `en-gb`)
- Update `SITE_TITLE` and descriptions
- Remove UK-specific environment variables

### 11. Create Canadian Data Import Commands

**Files to create:**

- `every_election/apps/organisations/management/commands/import_federal_ridings.py`
- `every_election/apps/organisations/management/commands/import_provincial_districts.py`
- `every_election/apps/organisations/management/commands/import_municipalities.py`

**Purpose:**

- Import federal electoral districts (ridings) from Elections Canada
- Import provincial electoral districts
- Import municipal boundaries and organizations

### 12. Update Tests

**Files to modify:**

- All test files in `every_election/apps/elections/tests/`
- All test files in `every_election/apps/organisations/tests/`
- [`fixtures/`](fixtures/) - Replace UK test data with Canadian examples

**Changes:**

- Replace UK postcodes with Canadian postal codes
- Replace UK organisation examples with Canadian equivalents
- Update election ID examples
- Replace UK-specific test fixtures

## Implementation Phases

### Phase 1: Foundation (Core Dependencies)

1. Create/identify Canadian election ID library
2. Create Canadian election timetables library
3. Replace UK postcode utilities with Canadian postal code utilities
4. Update dependencies in `pyproject.toml`

### Phase 2: Models and Data Structure

1. Update `Organisation` model with Canadian types
2. Update `Election` model to use Canadian ID builder
3. Update territory code mappings
4. Create Canadian election type fixtures

### Phase 3: Geographic Data

1. Replace postcode lookup with postal code lookup
2. Update boundary import commands for Canadian sources
3. Import initial Canadian boundary data
4. Update geographic queries

### Phase 4: API and Integration

1. Update API endpoints for Canadian data
2. Update filters and serializers
3. Test API with Canadian examples
4. Update documentation

### Phase 5: UI and Polish

1. Update templates and terminology
2. Update example data and documentation
3. Update tests with Canadian data
4. Final validation and testing

## Data Sources to Identify

- **Elections Canada**: Federal electoral district boundaries and data
- **Provincial Electoral Offices**: Provincial riding boundaries
- **Statistics Canada**: Geographic identifiers, postal code data
- **Municipal Sources**: Municipal boundary data (varies by province)
- **Canadian Postal Code Database**: For geocoding (may need commercial service or open data)

## Notes

- The core Django architecture and database models are largely reusable
- The election ID format structure can remain the same, just with Canadian context
- Geographic data will require significant work to replace UK sources
- Some features (like voter ID requirements) may need to be adapted or removed for Canada
- Consider creating a configuration layer to support multiple countries in the future