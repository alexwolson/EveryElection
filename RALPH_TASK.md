---
task: Adapt EveryElection for Canada
test_command: "pytest every_election/apps/elections/tests/test_ca_election_ids.py -v"
---

# Task: Adapt EveryElection for Canada

Adapt the EveryElection Django application from UK-specific implementation to support Canadian elections at all levels (Federal, Provincial/Territorial, and Municipal).

## Requirements

The system needs to be adapted for:
1. Canadian election ID format (replacing UK's `uk-election-ids`)
2. Canadian geographic data sources (postal codes, boundaries, electoral districts)
3. Canadian election types and organizations
4. Canadian election timetables and voting systems
5. Canadian-specific terminology and UI text

## Success Criteria

1. [x] Canadian Election ID System implemented (`CaIdBuilder` with hierarchical IDs)
2. [x] Election metadata updated (federal, provincial, territorial, municipal types)
3. [x] `ElectionBuilder` uses Canadian ID system instead of UK
4. [x] All tests updated to use Canadian election types and examples
5. [ ] Replace UK postcode lookup with Canadian postal code geocoding
6. [ ] Replace UK boundary imports with Canadian boundary sources (Elections Canada, provincial sources)
7. [ ] Update Organisation model for Canadian organization types
8. [ ] Update geographic constants (GSS codes → Canadian identifiers)
9. [ ] Update election timetables (replace `uk-election-timetables` with Canadian calendar)
10. [ ] Create Canadian data import commands (federal ridings, provincial districts, municipal boundaries)
11. [ ] Remove UK-specific dependencies (`uk-election-ids`, `uk-election-timetables`, `uk-geo-utils`)
12. [ ] Update all templates and UI text for Canadian terminology

## Completed Work

### Phase 1: Canadian Election ID System ✅

- Created `ca_election_ids.py` with `CaIdBuilder` class
- Created `ca_election_metadata.py` with Canadian election types
- Updated `ElectionBuilder` to use `CaIdBuilder`
- Updated all utility functions to use `CA_ELECTION_TYPES`
- Created comprehensive test suite (`test_ca_election_ids.py`)
- Updated all existing tests to use Canadian election types
- Created documentation (`docs/ca-election-ids.md`)
- Updated README.md with Canadian context

**Examples of Canadian Election IDs:**
- `federal.2025-04-28` - Federal general election
- `federal.toronto-centre.by.2024-06-24` - Federal by-election
- `provincial.ontario.2022-06-02` - Ontario provincial election
- `provincial.ontario.toronto-danforth.2022-06-02` - Provincial riding election
- `municipal.toronto.2022-10-24` - Toronto municipal election

## Next Steps

1. Replace UK postcode system with Canadian postal code geocoding
2. Import Canadian boundary data (federal ridings, provincial districts, municipalities)
3. Update Organisation model structure for Canadian types
4. Implement Canadian election timetable calculator
5. Update all remaining UK-specific code paths

## Example Usage

```python
from elections.utils import ElectionBuilder
from elections.models import ElectionType
from datetime import date

# Federal election
election_type = ElectionType.objects.get(election_type="federal")
builder = ElectionBuilder(election_type, date(2025, 4, 28))
election = builder.build_election_group()
# election.election_id == "federal.2025-04-28"

# Provincial election with division
election_type = ElectionType.objects.get(election_type="provincial")
builder = ElectionBuilder(election_type, date(2022, 6, 2))
builder.with_organisation(ontario_org)
builder.with_division(toronto_danforth_division)
ballot = builder.build_ballot(group)
# ballot.election_id == "provincial.ontario.toronto-danforth.2022-06-02"
```

---

## Ralph Instructions

1. Work on the next incomplete criterion (marked [ ])
2. Check off completed criteria (change [ ] to [x])
3. Run tests after changes
4. Commit your changes frequently
5. When ALL criteria are [x], output: `<ralph>COMPLETE</ralph>`
6. If stuck on the same issue 3+ times, output: `<ralph>GUTTER</ralph>`
