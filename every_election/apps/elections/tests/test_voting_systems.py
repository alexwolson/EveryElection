from django.test import TestCase
from elections.models import ElectedRole
from elections.utils import ElectionBuilder
from organisations.tests.factories import OrganisationFactory

from .base_tests import BaseElectionCreatorMixIn


class TestElectoralSystems(BaseElectionCreatorMixIn, TestCase):
    def test_canadian_municipal_fptp(self):
        """
        Canadian municipal elections use FPTP by default
        """

        # Elections without organisations don't have voting systems
        election_id = ElectionBuilder(
            self.election_type1, "2017-05-04"
        ).build_election_group()
        assert election_id.voting_system is None

        # Canadian municipal election is FPTP
        on_org = OrganisationFactory(territory_code="ON")
        ElectedRole.objects.create(
            election_type=self.election_type1,
            organisation=on_org,
            elected_title="City Councillor",
            elected_role_name="Councillor for Test City",
        )

        election_id = (
            ElectionBuilder(self.election_type1, "2017-05-04")
            .with_organisation(on_org)
            .build_election_group()
        )

        assert election_id.voting_system == "FPTP"
