"""
Canadian Organisation Constants

This module contains constants related to Canadian electoral geography
and organisation structures.
"""

# Canadian Province and Territory Codes (ISO 3166-2:CA)
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

# Provincial/Territorial legislature slugs
PROVINCIAL_LEGISLATURES = {
    "alberta": "AB",
    "british-columbia": "BC",
    "manitoba": "MB",
    "new-brunswick": "NB",
    "newfoundland-and-labrador": "NL",
    "nova-scotia": "NS",
    "ontario": "ON",
    "prince-edward-island": "PE",
    "quebec": "QC",
    "saskatchewan": "SK",
}

TERRITORIAL_LEGISLATURES = {
    "northwest-territories": "NT",
    "nunavut": "NU",
    "yukon": "YT",
}

# Fields to include in PMTiles feature attributes
PMTILES_FEATURE_ATTR_FIELDS = [
    "id",
    "source",
    "division_id",
    "division__name",
    "division__official_identifier",
]

# TODO: Add Canadian boundary/division types when implementing boundary imports
# This will need to map Canadian electoral district types to their geographic data sources
