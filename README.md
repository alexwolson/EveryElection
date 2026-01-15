# EveryElection
[![Build Status](https://circleci.com/gh/DemocracyClub/EveryElection.svg?style=svg)](https://circleci.com/gh/DemocracyClub/EveryElection) [![Coverage Status](https://coveralls.io/repos/github/DemocracyClub/EveryElection/badge.svg?branch=master)](https://coveralls.io/github/DemocracyClub/EveryElection?branch=master) ![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

For recording every election in Canada

> **Note**: This is a Canadian adaptation of EveryElection, originally designed for UK elections. The system has been adapted to support Canadian federal, provincial, territorial, and municipal elections.

## Domain Model

### Elections

The elections table stores a list of election objects, each with a semantic ID.

Election IDs sometimes have a parent, and are sometimes a "group ID".

There are two types of group ID:

1. `[type].[date]`, for example `federal.2025-04-28` will be the group for all federal elections happening on 2025-04-28.
2. `[type].[jurisdiction].[date]`, for example `provincial.ontario.2022-06-02` is the Ontario provincial elections.

Finally an ID is made _per ballot paper_ using `[type].[jurisdiction].[division].[date]` for example `federal.toronto-centre.2025-04-28`.

[See the Canadian election ID format specification](docs/ca-election-ids.md) for more information.

![Graph](docs/graph.png)
