# Canadian Election ID Format Specification

## Overview

This document describes the format for Canadian election IDs used in EveryElection. The format follows a hierarchical structure similar to the UK system but adapted for Canadian electoral structures.

## Format Structure

Canadian election IDs follow this pattern:

```
[type].[jurisdiction].[division].[date]
```

With an optional `.by` segment for by-elections:

```
[type].[jurisdiction].[division].by.[date]
```

## Components

### Type

The election type, one of:
- `federal` - Federal elections (House of Commons)
- `provincial` - Provincial legislature elections
- `territorial` - Territorial legislature elections
- `municipal` - Municipal/regional elections

### Jurisdiction

The jurisdiction identifier (slugified):
- **Federal**: Omitted (single federal parliament)
- **Provincial/Territorial**: Province or territory slug (e.g., `ontario`, `quebec`, `british-columbia`)
- **Municipal**: Municipality slug (e.g., `toronto`, `vancouver`, `montreal`)

### Division

The electoral district/riding identifier (slugified):
- Federal: Riding name (e.g., `toronto-centre`, `vancouver-quadra`)
- Provincial: Provincial riding/district name
- Territorial: Territorial district name
- Municipal: Ward or district name (e.g., `ward-10`, `district-5`)

### Date

The polling day in ISO format: `YYYY-MM-DD`

### By-Election Indicator

Optional `.by` segment inserted before the date for by-elections.

## Hierarchical Structure

Election IDs are organized hierarchically:

1. **Election Group**: `[type].[date]`
   - Example: `federal.2025-04-28`

2. **Subtype Group** (if applicable): `[type].[subtype].[date]`
   - Example: `federal.subtype.2025-04-28`

3. **Organisation Group**: `[type].[jurisdiction].[date]`
   - Example: `provincial.ontario.2022-06-02`

4. **Ballot**: `[type].[jurisdiction].[division].[date]` or `[type].[jurisdiction].[division].by.[date]`
   - Example: `federal.toronto-centre.2025-04-28`
   - Example: `provincial.ontario.toronto-danforth.by.2023-03-27`

## Examples

### Federal Elections

```
federal.2025-04-28
```
Federal general election on April 28, 2025

```
federal.toronto-centre.by.2024-06-24
```
Federal by-election in Toronto Centre on June 24, 2024

### Provincial Elections

```
provincial.ontario.2022-06-02
```
Ontario provincial general election on June 2, 2022

```
provincial.ontario.toronto-danforth.by.2023-03-27
```
Ontario by-election in Toronto-Danforth on March 27, 2023

```
provincial.quebec.2022-10-03
```
Quebec provincial general election on October 3, 2022

### Territorial Elections

```
territorial.yukon.2021-04-12
```
Yukon territorial election on April 12, 2021

### Municipal Elections

```
municipal.toronto.2022-10-24
```
Toronto municipal election on October 24, 2022

```
municipal.toronto.ward-10.2022-10-24
```
Toronto ward 10 election on October 24, 2022

```
municipal.vancouver.2022-10-15
```
Vancouver municipal election on October 15, 2022

## Slugification Rules

All jurisdiction and division names are automatically slugified:
- Spaces become hyphens
- Special characters are removed or converted
- Accented characters are converted to ASCII equivalents
- Uppercase is converted to lowercase

Examples:
- "British Columbia" → `british-columbia`
- "Québec City" → `quebec-city`
- "Toronto-Danforth" → `toronto-danforth`
- "Ward 10" → `ward-10`

## Usage

### Programmatic Generation

```python
from datetime import date
from elections.ca_election_ids import CaIdBuilder

# Federal election
builder = CaIdBuilder("federal", date(2025, 4, 28))
election_id = builder.election_group_id  # "federal.2025-04-28"

# Provincial election with division
builder = CaIdBuilder("provincial", date(2022, 6, 2))
builder.with_organisation("ontario")
builder.with_division("toronto-danforth")
ballot_id = builder.ballot_id  # "provincial.ontario.toronto-danforth.2022-06-02"

# By-election
builder = CaIdBuilder("federal", date(2024, 6, 24))
builder.with_division("toronto-centre")
builder.with_contest_type("by")
by_election_id = builder.ballot_id  # "federal.toronto-centre.by.2024-06-24"
```

### Using ElectionBuilder

```python
from elections.utils import ElectionBuilder
from elections.models import ElectionType

election_type = ElectionType.objects.get(election_type="federal")
builder = ElectionBuilder(election_type, date(2025, 4, 28))
election = builder.build_election_group()
```

## Validation

- Election type must be one of: `federal`, `provincial`, `territorial`, `municipal`
- Date must be in valid YYYY-MM-DD format
- Jurisdiction and division names are automatically slugified
- By-election indicator is only added when `contest_type` is `"by"`

## Differences from UK System

1. **Election Types**: Uses Canadian-specific types (federal, provincial, territorial, municipal) instead of UK types (local, parl, sp, etc.)

2. **Jurisdiction Structure**: 
   - Federal elections don't include jurisdiction in the ID (single federal parliament)
   - Provincial/territorial elections include province/territory slug
   - Municipal elections include municipality slug

3. **No GSS Codes**: Canadian system uses slugs instead of GSS (Government Statistical Service) codes

4. **Province/Territory Codes**: Uses standard ISO 3166-2:CA codes (AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT) for reference, but slugs in IDs

## Future Considerations

- Support for school board elections
- Support for Indigenous governance elections
- Handling of special election types (referendums, plebiscites)
- Support for multi-day elections or advance polling periods
