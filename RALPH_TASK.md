---
task: Rewrite EveryElection from UK to Canadian election data system
completion_criteria:
  - Remove uk-election-ids, uk-election-timetables, uk-geo-utils dependencies from pyproject.toml
  - Create Canadian election ID builder (ca_election_ids.py) following docs/ca-election-ids.md specification
  - Replace UK election types with Canadian types (federal, provincial, territorial, municipal)
  - Replace UK organisation types with Canadian equivalents (parliament, provincial-legislature, territorial-legislature, municipal-council)
  - Replace UK territory codes (WLS, ENG, NIR, SCT, GBN) with Canadian province/territory codes (AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT)
  - Remove UK-specific constants (GSS codes, police areas, combined authorities, ONSPD postcode data)
  - Update Organisation model ORGTYPES choices for Canadian government bodies
  - Update elections/models.py to remove UK package imports and use Canadian election ID logic
  - Remove UK-specific timetable calculation (get_timetable property) - not needed for Canadian version
  - Remove UK-specific postcode lookup (get_example_postcode, Onspd references) - not needed for Canadian version
  - Update add_election_types management command for Canadian election types
  - Update ElectionBuilder (elections/utils.py) to generate Canadian election IDs
  - Remove or update UK-specific fixtures (onspd.json, boundaryline data)
  - Update API serializers to remove UK-specific fields
  - Update templates to remove UK-specific references (ynr_link, whocivf_link properties)
  - Remove UK-specific organisation constants (POLICE_AREA_NAME_TO_GSS, COMBINED_AUTHORITY_SLUG_TO_GSS, ORG_CURIE_TO_MAPIT_AREA_TYPE, etc.)
  - Update organisation boundary imports to support Canadian data sources (design for future implementation)
  - Update or remove UK-specific tests that reference UK election types, organisations, or geography
  - Ensure all Python imports are updated and no references to removed UK packages remain
  - All existing tests pass (or are appropriately updated/removed for Canadian context)
max_iterations: 30
test_command: "cd /Users/alex/repos/EveryElection && python manage.py test --settings=every_election.settings.testing"
---

# Task: Rewrite EveryElection for Canadian Election Data

Convert this Django-based election tracking system from UK elections to Canadian elections. The UK-specific functionality should be completely removed (not dual-support). Focus on federal, provincial, and territorial elections, with the data model designed to support municipal elections in the future.

## Context

### Current UK Structure (to be removed)
- **UK Packages**: `uk-election-ids`, `uk-election-timetables`, `uk-geo-utils`
- **UK Election Types**: sp (Scottish Parliament), gla (Greater London Authority), naw/senedd (Welsh), nia (Northern Ireland), parl (UK Parliament), europarl, local, mayor, pcc
- **UK Organisation Types**: combined-authority, sp, gla, local-authority, naw, senedd, nia, parl, police-area, europarl
- **UK Territory Codes**: WLS, ENG, NIR, SCT, GBN
- **UK Geography**: GSS codes, ONSPD postcode database, BoundaryLine imports

### Target Canadian Structure
- **Canadian Election Types**: federal, provincial, territorial, municipal (future)
- **Canadian Organisation Types**: parliament, provincial-legislature, territorial-legislature, municipal-council (future)
- **Canadian Province/Territory Codes**: AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT
- **Canadian Election ID Format**: See `docs/ca-election-ids.md` for full specification

### Canadian Election ID Examples
```
federal.2025-04-28                           # Federal general election
federal.toronto-centre.by.2024-06-24         # Federal by-election
provincial.ontario.2022-06-02                # Ontario provincial election
provincial.ontario.toronto-danforth.by.2023-03-27  # Ontario by-election
territorial.yukon.2021-04-12                 # Yukon territorial election
```

## Success Criteria

The task is complete when ALL of the following are true:

- [ ] Remove uk-election-ids, uk-election-timetables, uk-geo-utils dependencies from pyproject.toml
- [ ] Create Canadian election ID builder (ca_election_ids.py) following docs/ca-election-ids.md specification
- [ ] Replace UK election types with Canadian types (federal, provincial, territorial, municipal)
- [ ] Replace UK organisation types with Canadian equivalents (parliament, provincial-legislature, territorial-legislature, municipal-council)
- [ ] Replace UK territory codes (WLS, ENG, NIR, SCT, GBN) with Canadian province/territory codes (AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT)
- [ ] Remove UK-specific constants (GSS codes, police areas, combined authorities, ONSPD postcode data)
- [ ] Update Organisation model ORGTYPES choices for Canadian government bodies
- [ ] Update elections/models.py to remove UK package imports and use Canadian election ID logic
- [ ] Remove UK-specific timetable calculation (get_timetable property) - not needed for Canadian version
- [ ] Remove UK-specific postcode lookup (get_example_postcode, Onspd references) - not needed for Canadian version
- [ ] Update add_election_types management command for Canadian election types
- [ ] Update ElectionBuilder (elections/utils.py) to generate Canadian election IDs
- [ ] Remove or update UK-specific fixtures (onspd.json, boundaryline data)
- [ ] Update API serializers to remove UK-specific fields
- [ ] Update templates to remove UK-specific references (ynr_link, whocivf_link properties)
- [ ] Remove UK-specific organisation constants (POLICE_AREA_NAME_TO_GSS, COMBINED_AUTHORITY_SLUG_TO_GSS, ORG_CURIE_TO_MAPIT_AREA_TYPE, etc.)
- [ ] Update organisation boundary imports to support Canadian data sources (design for future implementation)
- [ ] Update or remove UK-specific tests that reference UK election types, organisations, or geography
- [ ] Ensure all Python imports are updated and no references to removed UK packages remain
- [ ] All existing tests pass (or are appropriately updated/removed for Canadian context)

## Constraints

1. **No dual UK/Canadian support** - Remove UK functionality entirely, don't try to support both
2. **Design for future municipal support** - The data model should accommodate municipal elections even though they're not the initial focus
3. **No postal code lookup needed** - Don't implement Canadian postal code lookup (may be added later)
4. **No timetable calculations needed** - Don't implement Canadian election timetables (may be added later)
5. **Preserve core architecture** - Keep the Election/Organisation/Division model structure, just adapt for Canadian context
6. **Database migrations** - Create appropriate migrations for model changes
7. **Keep tests working** - Update tests to use Canadian data, don't just delete them

## Key Files to Modify

### Dependencies
- `pyproject.toml` - Remove UK packages

### Models
- `every_election/apps/elections/models.py` - Remove UK imports, update ID logic
- `every_election/apps/organisations/models/organisations.py` - Update ORGTYPES
- `every_election/apps/organisations/constants.py` - Replace UK constants

### Election ID Generation
- `every_election/apps/elections/utils.py` - Update ElectionBuilder for Canadian IDs
- Create `every_election/apps/elections/utils/ca_election_ids.py` (new file)

### Management Commands
- `every_election/apps/elections/management/commands/add_election_types.py` - Canadian types

### API
- `every_election/apps/api/serializers.py` - Remove UK-specific fields
- `every_election/apps/api/views.py` - Update as needed

### Tests
- Various test files - Update to use Canadian data

---

## Ralph Instructions

### Before Starting Work
1. Read `.ralph/guardrails.md` for any learned constraints
2. Read `.ralph/progress.md` to understand what has been completed
3. Run `git status` to see current state

### Working Protocol
1. Work on ONE unchecked criterion at a time from the Success Criteria above
2. Make focused, incremental changes
3. Run the test command after significant changes: `python manage.py test --settings=every_election.settings.testing`
4. Commit after completing each criterion with a descriptive message

### After Completing Work
1. Update `.ralph/progress.md` with what was done
2. Check off completed criteria in this file (change `- [ ]` to `- [x]`)
3. Commit all changes including updated state files
4. If stuck or context is running low, commit current progress and stop

### Git Protocol
- Always commit working code
- Use descriptive commit messages that reference the criterion being completed
- If a change breaks tests, fix before committing or revert

### If Tests Fail
1. Read the error message carefully
2. Check if the failure is due to UK-specific code that needs updating
3. Fix the issue or update the test for Canadian context
4. Add any learnings to `.ralph/guardrails.md`
