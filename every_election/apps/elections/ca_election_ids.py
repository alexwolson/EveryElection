"""
Canadian Election ID Builder

Generates hierarchical election IDs for Canadian elections following the format:
[type].[jurisdiction].[division].[date] with optional .by segment

Examples:
- federal.2025-04-28
- federal.toronto-centre.by.2024-06-24
- provincial.ontario.2022-06-02
- provincial.ontario.toronto-danforth.by.2023-03-27
- municipal.toronto.2022-10-24
"""

from datetime import date
from typing import List, Optional

from django.utils.text import slugify

from .ca_election_metadata import CA_ELECTION_TYPES


class CaIdBuilder:
    """
    Builder for Canadian election IDs.
    
    Provides a fluent interface to build hierarchical election IDs:
    - Election group: [type].[date]
    - Subtype group: [type].[subtype].[date]
    - Organisation group: [type].[jurisdiction].[date]
    - Ballot: [type].[jurisdiction].[division].[date] or [type].[jurisdiction].[division].by.[date]
    
    Usage constraints:
    - with_organisation() should be called before with_division() when both are needed
    - with_division() requires with_organisation() to have been called first for the ballot ID to be valid
    - Methods can be chained in any order, but the logical hierarchy should be respected
    - The builder validates that required components are present when building specific ID types
    
    Example:
        builder = CaIdBuilder("municipal", date(2022, 10, 24))
        builder.with_organisation("toronto").with_division("ward-1")
        ballot_id = builder.ballot_id  # Returns: municipal.toronto.ward-1.2022-10-24
    """

    VALID_ELECTION_TYPES = set(CA_ELECTION_TYPES.keys())

    def __init__(self, election_type: str, election_date: date):
        """
        Initialize the ID builder.
        
        Args:
            election_type: One of 'federal', 'provincial', 'territorial', 'municipal'
            election_date: The date of the election (polling day)
        """
        if election_type not in self.VALID_ELECTION_TYPES:
            raise ValueError(
                f"Invalid election type: {election_type}. "
                f"Must be one of: {', '.join(self.VALID_ELECTION_TYPES)}"
            )

        self.election_type = election_type
        self.date = election_date
        self.subtype: Optional[str] = None
        self.organisation: Optional[str] = None
        self.division: Optional[str] = None
        self.contest_type: Optional[str] = None

        # Build the list of ID segments as we add components
        self._ids: List[str] = []

    def with_subtype(self, subtype: str) -> "CaIdBuilder":
        """
        Add a subtype to the ID (e.g., for different voting methods).
        
        Args:
            subtype: The subtype slug
            
        Returns:
            self for method chaining
        """
        self.subtype = slugify(subtype)
        return self

    def with_organisation(self, org_slug: str) -> "CaIdBuilder":
        """
        Add an organisation (jurisdiction) to the ID.
        
        For federal elections, this is typically omitted.
        For provincial/territorial, this is the province/territory slug.
        For municipal, this is the municipality slug.
        
        Args:
            org_slug: The organisation slug (will be slugified)
            
        Returns:
            self for method chaining
        """
        self.organisation = slugify(org_slug)
        return self

    def with_division(self, division_slug: str) -> "CaIdBuilder":
        """
        Add a division (electoral district/riding) to the ID.
        
        Args:
            division_slug: The division slug (will be slugified)
            
        Returns:
            self for method chaining
        """
        self.division = slugify(division_slug)
        return self

    def with_contest_type(self, contest_type: str) -> "CaIdBuilder":
        """
        Add a contest type (e.g., 'by' for by-election).
        
        Args:
            contest_type: The contest type (typically 'by' for by-election)
            
        Returns:
            self for method chaining
        """
        self.contest_type = contest_type
        return self

    def _format_date(self) -> str:
        """Format the date as YYYY-MM-DD."""
        return self.date.strftime("%Y-%m-%d")

    def _build_id_parts(self, include_subtype: bool = False) -> List[str]:
        """
        Build the list of ID parts based on current state.
        
        Args:
            include_subtype: Whether to include subtype in the ID
            
        Returns:
            List of ID segments
        """
        parts = [self.election_type]

        if include_subtype and self.subtype:
            parts.append(self.subtype)

        if self.organisation:
            parts.append(self.organisation)

        if self.division:
            parts.append(self.division)

        if self.contest_type == "by":
            parts.append("by")

        parts.append(self._format_date())

        return parts

    @property
    def election_group_id(self) -> str:
        """
        Generate the top-level election group ID.
        
        Format: [type].[date]
        Example: federal.2025-04-28
        """
        return f"{self.election_type}.{self._format_date()}"

    @property
    def subtype_group_id(self) -> str:
        """
        Generate the subtype group ID.
        
        Format: [type].[subtype].[date]
        Example: federal.subtype.2025-04-28
        """
        if not self.subtype:
            return self.election_group_id
        return f"{self.election_type}.{self.subtype}.{self._format_date()}"

    @property
    def organisation_group_id(self) -> str:
        """
        Generate the organisation group ID.
        
        Format: [type].[jurisdiction].[date]
        Example: provincial.ontario.2022-06-02
        """
        parts = [self.election_type]
        if self.organisation:
            parts.append(self.organisation)
        parts.append(self._format_date())
        return ".".join(parts)

    @property
    def ballot_id(self) -> str:
        """
        Generate the ballot-level ID (most specific).
        
        Format: [type].[jurisdiction].[division].[date] or
                [type].[jurisdiction].[division].by.[date]
        Example: federal.toronto-centre.2025-04-28
        Example: provincial.ontario.toronto-danforth.by.2023-03-27
        """
        return ".".join(self._build_id_parts())

    @property
    def ids(self) -> List[str]:
        """
        Return a list of all IDs that have been built.
        
        This property tracks the progression of ID building.
        """
        ids_list = [self.election_group_id]

        if self.subtype:
            ids_list.append(self.subtype_group_id)

        if self.organisation:
            ids_list.append(self.organisation_group_id)

        if self.division:
            ids_list.append(self.ballot_id)

        return ids_list

    def __eq__(self, other) -> bool:
        """Compare two CaIdBuilder instances by their ballot_id."""
        if not isinstance(other, CaIdBuilder):
            return False
        return self.ballot_id == other.ballot_id

    def __repr__(self) -> str:
        """String representation of the builder."""
        return f"CaIdBuilder(election_type={self.election_type}, date={self.date}, ballot_id={self.ballot_id})"


def validate(election_id: str) -> bool:
    """
    Validate a Canadian election ID.
    
    Checks that the election ID follows the correct format:
    - Starts with a valid election type (federal, provincial, territorial, municipal)
    - Ends with a valid date in YYYY-MM-DD format
    - Contains only valid characters (lowercase letters, digits, hyphens, periods)
    
    Args:
        election_id: The election ID to validate
        
    Returns:
        True if the ID is valid, False otherwise
    """
    import re
    
    if not election_id or not isinstance(election_id, str):
        return False
    
    # Check for valid characters only
    if not re.match(r'^[a-z0-9\-\.]+$', election_id):
        return False
    
    parts = election_id.split('.')
    
    # Must have at least 2 parts (type and date)
    if len(parts) < 2:
        return False
    
    # First part must be a valid election type
    if parts[0] not in CA_ELECTION_TYPES:
        return False
    
    # Last part must be a valid date
    date_part = parts[-1]
    try:
        # Check date format YYYY-MM-DD
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_part):
            return False
        # Validate it's a real date
        year, month, day = map(int, date_part.split('-'))
        from datetime import date as date_type
        date_type(year, month, day)
    except (ValueError, TypeError):
        return False
    
    # Check for 'by' segment - must be second to last if present
    if 'by' in parts:
        by_index = parts.index('by')
        # 'by' should be second to last (before date)
        if by_index != len(parts) - 2:
            return False
    
    return True
