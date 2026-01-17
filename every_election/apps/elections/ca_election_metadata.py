"""
Canadian Election Metadata

Defines election types, voting systems, ID requirements, and other metadata
for Canadian elections.
"""

# Valid Canadian election types
CA_ELECTION_TYPES = {
    "federal": {
        "name": "Federal",
        "can_have_divs": True,
        "default_voting_system": "FPTP",  # First Past the Post
        "subtypes": [],
    },
    "provincial": {
        "name": "Provincial",
        "can_have_divs": True,
        "default_voting_system": "FPTP",
        "subtypes": [],
    },
    "territorial": {
        "name": "Territorial",
        "can_have_divs": True,
        "default_voting_system": "FPTP",
        "subtypes": [],
    },
    "municipal": {
        "name": "Municipal",
        "can_have_divs": True,
        "default_voting_system": "FPTP",
        "subtypes": [],
    },
}

# Canadian province and territory codes (ISO 3166-2:CA)
PROVINCE_TERRITORY_CODES = {
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "NS": "Nova Scotia",
    "NT": "Northwest Territories",
    "NU": "Nunavut",
    "ON": "Ontario",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon",
}

# Voting systems used in Canada
CA_VOTING_SYSTEMS = {
    "FPTP": {
        "name": "First Past the Post",
        "description": "Single member plurality voting system",
    },
    "AV": {
        "name": "Alternative Vote",
        "description": "Ranked choice voting system (used in some municipal elections)",
    },
    "STV": {
        "name": "Single Transferable Vote",
        "description": "Multi-member proportional representation system",
    },
}

# Canadian voter ID requirements
# Canadian elections require voters to prove identity and address
# See Elections Canada: https://www.elections.ca/content.aspx?section=vot&dir=ids&document=index&lang=e
CA_ID_REQUIREMENTS = {
    "federal": {
        "name": "Federal Election ID",
        "description": "One piece of government-issued photo ID with name and address, "
                       "or two pieces of ID (one with name, one with address)",
    },
    "provincial": {
        "name": "Provincial Election ID",
        "description": "Requirements vary by province - typically similar to federal requirements",
    },
    "territorial": {
        "name": "Territorial Election ID",
        "description": "Requirements vary by territory",
    },
    "municipal": {
        "name": "Municipal Election ID",
        "description": "Requirements vary by municipality - typically similar to provincial requirements",
    },
}

# Major Canadian municipalities (to start with)
MAJOR_MUNICIPALITIES = [
    "toronto",
    "vancouver",
    "montreal",
    "calgary",
    "edmonton",
    "ottawa",
    "winnipeg",
    "quebec-city",
    "hamilton",
    "kitchener",
]
