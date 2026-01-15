import pytest
from elections.tests.factories import ElectionFactory, ElectionTypeFactory
from elections.utils import get_voter_id_requirement


@pytest.mark.django_db
class TestGetVoterIdRequirements:
    default_election_id = "municipal.test-city.2024-01-01"

    def test_get_voter_id_requirement_canada(self):
        """
        TODO: Implement Canadian voter ID requirements.
        For now, Canadian elections return None (no ID requirement).
        """
        election = ElectionFactory(election_id=self.default_election_id)
        election.division.territory_code = "ON"
        # Currently returns None as Canadian voter ID requirements are not yet implemented
        assert get_voter_id_requirement(election) is None

    def test_get_voter_id_requirement_no_division(self):
        election = ElectionFactory(election_id=self.default_election_id)
        election.division = None
        assert get_voter_id_requirement(election) is None
