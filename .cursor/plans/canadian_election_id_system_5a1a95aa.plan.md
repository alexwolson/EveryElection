---
name: Canadian Election ID System
overview: Create a Canadian election ID generation system to replace uk-election-ids, maintaining the same interface as IdBuilder while using Canadian-specific formats for federal, provincial, territorial, and municipal elections.
todos:
  - id: create_ca_id_builder
    content: "Create CaIdBuilder class in every_election/apps/elections/ca_election_ids.py with same interface as IdBuilder (with_subtype, with_organisation, with_division, with_contest_type, and properties: election_group_id, subtype_group_id, organisation_group_id, ballot_id)"
    status: pending
  - id: implement_id_generation
    content: "Implement ID generation logic in CaIdBuilder: format [type].[jurisdiction].[division].[date] with optional .by segment, using slugification for jurisdiction and division names"
    status: pending
    dependencies:
      - create_ca_id_builder
  - id: create_election_metadata
    content: Create every_election/apps/elections/ca_election_metadata.py with CA_ELECTION_TYPES dictionary defining federal, provincial, territorial, municipal types and their properties
    status: pending
  - id: update_election_builder
    content: Update ElectionBuilder in utils.py to use CaIdBuilder instead of IdBuilder, replace uk_election_ids imports with ca_election_ids
    status: pending
    dependencies:
      - create_ca_id_builder
      - create_election_metadata
  - id: update_utility_functions
    content: Update election_type_has_divisions() and other utility functions in utils.py to use CA_ELECTION_TYPES instead of UK ELECTION_TYPES, mark UK-specific functions (get_voter_id_requirement, get_voting_system) as TODO
    status: pending
    dependencies:
      - create_election_metadata
  - id: create_tests
    content: Create test_ca_election_ids.py with tests for ID generation, hierarchical structure, by-elections, slugification, and edge cases
    status: pending
    dependencies:
      - create_ca_id_builder
  - id: update_existing_tests
    content: Update existing test files (test_election_builder.py, test_create_ids.py) to use Canadian election types and examples instead of UK ones
    status: pending
    dependencies:
      - update_election_builder
  - id: write_documentation
    content: Create docs/ca-election-ids.md documenting the Canadian election ID format, examples, hierarchical structure, and update README.md
    status: pending
    dependencies:
      - create_ca_id_builder
---

# Canadian Election ID System Implementation Plan

## Research Summary

**Key Findings:**

- Canada has no standardized national election ID format (unlike UK's `uk-election-ids`)
- Elections Canada uses unique identifiers for electors, not election events
- Statistics Canada classifies elections as: 1=Federal, 2=Provincial, 3=Municipal
- Canadian elections are identified by jurisdiction, date, and type (general/by-election)
- Provinces use ISO 3166-2 codes (ON, QC, BC, etc.)

**Current UK System:**

- Uses `uk-election-ids.IdBuilder` with fluent interface
- Generates hierarchical IDs: `[type].[org].[division].[date] `with optional `by` segment
- Provides: `election_group_id`, `subtype_group_id`, `organisation_group_id`, `ballot_id`
- Methods: `with_subtype()`, `with_organisation()`, `with_division()`, `with_contest_type()`

## Proposed Canadian ID Format

Following the UK pattern but adapted for Canada:

**Format Structure:**

```
[type].[jurisdiction].[division].[date]
```

Where:

- **type**: `federal`, `provincial`, `territorial`, `municipal`
- **jurisdiction**: 
  - Federal: omitted (single federal parliament)
  - Provincial/Territorial: province code slug (e.g., `ontario`, `quebec`, `british-columbia`)
  - Municipal: municipality slug (e.g., `toronto`, `vancouver`)
- **division**: Electoral district/riding slug (e.g., `toronto-centre`, `vancouver-quadra`)
- **date**: ISO date format `YYYY-MM-DD`
- **by-election**: Optional `.by` segment before date

**Examples:**

- `federal.2025-04-28` - Federal general election
- `federal.toronto-centre.by.2024-06-24` - Federal by-election in Toronto Centre
- `provincial.ontario.2022-06-02` - Ontario provincial general election
- `provincial.ontario.toronto-danforth.by.2023-03-27` - Ontario by-election
- `municipal.toronto.2022-10-24` - Toronto municipal election
- `municipal.toronto.ward-10.2022-10-24` - Toronto ward election

**Hierarchical Structure (matching UK pattern):**

1. **Election Group**: `federal.2025-04-28`
2. **Organisation Group**: `federal.ontario.2025-04-28` (if applicable)
3. **Ballot**: `federal.toronto-centre.2025-04-28`

## Implementation Steps

### Phase 1: Create Canadian ID Builder Module

**File to create:** `every_election/apps/elections/ca_election_ids.py`

**Class to implement:** `CaIdBuilder` (matching `IdBuilder` interface)

**Required Interface:**

```python
class CaIdBuilder:
    def __init__(self, election_type: str, date: date)
    def with_subtype(self, subtype: str) -> 'CaIdBuilder'
    def with_organisation(self, org_slug: str) -> 'CaIdBuilder'
    def with_division(self, division_slug: str) -> 'CaIdBuilder'
    def with_contest_type(self, contest_type: str) -> 'CaIdBuilder'
    
    @property
    def election_group_id(self) -> str
    @property
    def subtype_group_id(self) -> str
    @property
    def organisation_group_id(self) -> str
    @property
    def ballot_id(self) -> str
    @property
    def ids(self) -> list[str]
    
    def __eq__(self, other) -> bool
    def __repr__(self) -> str
```

**Key Implementation Details:**

- Use slugification for jurisdiction and division names (similar to UK system)
- Handle date formatting consistently (YYYY-MM-DD)
- Support `.by` segment for by-elections
- Maintain hierarchical ID generation logic
- Validate election types: `federal`, `provincial`, `territorial`, `municipal`

### Phase 2: Update ElectionBuilder to Use Canadian IDs

**File to modify:** [`every_election/apps/elections/utils.py`](every_election/apps/elections/utils.py)

**Changes:**

1. Replace import: `from uk_election_ids.election_ids import IdBuilder` → `from elections.ca_election_ids import CaIdBuilder`
2. Update line 129: `self.id = IdBuilder(...)` → `self.id = CaIdBuilder(...)`
3. Ensure all `self.id` method calls work with new interface (should be compatible)

**Dependencies to handle:**

- Remove `uk_election_ids.datapackage.ELECTION_TYPES` usage (line 16, 42)
- Remove `IDRequirementsMatcher` and `VotingSystemMatcher` (lines 18-20, 61, 253)
- Create Canadian equivalents or mark as TODO for later phases

### Phase 3: Define Canadian Election Types and Metadata

**File to create:** `every_election/apps/elections/ca_election_metadata.py`

**Content:**

- Define Canadian election types dictionary (replacing `ELECTION_TYPES`)
- Define valid election types and their properties
- Define province/territory codes mapping
- Define voting systems for Canadian elections (First Past the Post, etc.)

**Election Types:**

```python
CA_ELECTION_TYPES = {
    "federal": {
        "name": "Federal",
        "can_have_divs": True,
        # ... other metadata
    },
    "provincial": {
        "name": "Provincial",
        "can_have_divs": True,
    },
    "territorial": {
        "name": "Territorial",
        "can_have_divs": True,
    },
    "municipal": {
        "name": "Municipal",
        "can_have_divs": True,
    },
}
```

### Phase 4: Update Utility Functions

**File to modify:** [`every_election/apps/elections/utils.py`](every_election/apps/elections/utils.py)

**Functions to update:**

1. `election_type_has_divisions()` - Use `CA_ELECTION_TYPES` instead of `ELECTION_TYPES`
2. `get_voter_id_requirement()` - Remove or adapt for Canada (different ID requirements)
3. `get_voting_system()` - Create Canadian voting system matcher

**Temporary approach:**

- Mark UK-specific functions as deprecated/TODO
- Return None or default values where appropriate
- Document what needs Canadian equivalents

### Phase 5: Create Tests

**File to create:** `every_election/apps/elections/tests/test_ca_election_ids.py`

**Test cases:**

1. ID generation for each election type (federal, provincial, territorial, municipal)
2. Hierarchical ID structure (election group → organisation group → ballot)
3. By-election ID format
4. Slugification of jurisdiction and division names
5. Date formatting
6. Edge cases (special characters, long names, etc.)

**Test examples:**

```python
def test_federal_election_id():
    builder = CaIdBuilder("federal", date(2025, 4, 28))
    assert builder.election_group_id == "federal.2025-04-28"

def test_provincial_with_division():
    builder = CaIdBuilder("provincial", date(2022, 6, 2))
    builder.with_organisation("ontario")
    builder.with_division("toronto-danforth")
    assert builder.ballot_id == "provincial.ontario.toronto-danforth.2022-06-02"
```

### Phase 6: Update Existing Tests

**Files to modify:**

- `every_election/apps/elections/tests/test_election_builder.py`
- `every_election/apps/elections/tests/test_create_ids.py`
- Other test files using `ElectionBuilder`

**Approach:**

- Update test fixtures to use Canadian election types
- Replace UK examples with Canadian examples
- Ensure tests still validate the same functionality

### Phase 7: Documentation

**Files to create/update:**

- `docs/ca-election-ids.md` - Canadian election ID format specification
- Update `README.md` with Canadian context
- Add docstrings to `CaIdBuilder` class

**Documentation should include:**

- ID format specification
- Examples for each election type
- Hierarchical structure explanation
- How to generate IDs programmatically

## Technical Considerations

### Slugification

- Use Django's `slugify()` or similar for consistent slug generation
- Handle special characters (accents, hyphens, etc.)
- Ensure uniqueness and readability

### Date Handling

- Always use ISO format: YYYY-MM-DD
- Handle timezone considerations (use UTC or document timezone)
- Validate date ranges (no future dates beyond reasonable limits)

### Backward Compatibility

- Consider keeping UK ID support temporarily for migration
- Add feature flag or configuration to switch between UK/CA systems
- Document migration path

### Validation

- Validate election type is one of: federal, provincial, territorial, municipal
- Validate province/territory codes (AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT)
- Validate date format and ranges
- Validate slug format (alphanumeric, hyphens, underscores)

## Dependencies

**New dependencies needed:**

- None (use Django's built-in utilities)

**Dependencies to remove (later):**

- `uk-election-ids` (after full migration)
- `uk-election-timetables` (separate task)
- `uk-geo-utils` (separate task)

## Success Criteria

1. ✅ `CaIdBuilder` generates valid Canadian election IDs
2. ✅ `ElectionBuilder` works with `CaIdBuilder` without code changes
3. ✅ All existing tests pass (with updated fixtures)
4. ✅ New tests validate Canadian ID format
5. ✅ Documentation explains the format and usage
6. ✅ IDs are hierarchical and match UK pattern structure

## Next Steps After This Plan

1. Implement voting system matcher for Canada
2. Implement election timetable calculator for Canada
3. Update Organisation model for Canadian types
4. Create data import commands for Canadian elections