"""
Canadian Election Metadata

Defines election types, voting systems, and other metadata for Canadian elections.
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
    # Add other systems as needed (e.g., STV, PR, etc.)
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
