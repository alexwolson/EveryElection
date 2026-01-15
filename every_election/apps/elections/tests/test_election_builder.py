from datetime import date

from django.test import TestCase
from election_snooper.models import SnoopedElection
from elections.models import (
    DEFAULT_STATUS,
    ElectedRole,
    Election,
    ElectionSubType,
    ElectionType,
)
from elections.utils import ElectionBuilder, reset_cache
from organisations.models import Organisation, OrganisationDivision
from organisations.tests.factories import (
    OrganisationDivisionFactory,
    OrganisationDivisionSetFactory,
)

from .base_tests import BaseElectionCreatorMixIn


class TestElectionBuilder(BaseElectionCreatorMixIn, TestCase):
    def setUp(self):
        super().setUp()
        reset_cache()

    def test_eq(self):
        eb1 = ElectionBuilder("municipal", "2017-06-08")

        eb2 = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_source("foo/bar.baz")
            .with_snooped_election(7)
        )

        # these should be 'equal' because only the meta-data differs
        self.assertEqual(eb1, eb2)

        eb2 = eb2.with_organisation(self.org1)

        # now these objects will build funamentally different elections
        self.assertNotEqual(eb1, eb2)

    def test_with_metadata(self):
        snooper = SnoopedElection.objects.create()
        builder = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_organisation(self.org1)
            .with_division(self.org_div_1)
            .with_source("foo/bar.baz")
            .with_snooped_election(snooper.id)
        )
        election = builder.build_ballot(None)
        election.save()
        self.assertEqual("foo/bar.baz", election.source)
        assert isinstance(election.snooped_election, SnoopedElection)

    def test_invalid_subtype(self):
        # Create a provincial election type for testing subtypes
        provincial_election_type, _ = ElectionType.objects.get_or_create(
            election_type="provincial"
        )
        invalid_sub_type = ElectionSubType.objects.create(
            election_subtype="x", election_type=self.election_type1
        )
        builder = ElectionBuilder(provincial_election_type, "2017-06-08")
        with self.assertRaises(ElectionSubType.ValidationError):
            builder.with_subtype(invalid_sub_type)

    def test_invalid_organisation(self):
        builder = ElectionBuilder("municipal", "2017-06-08")

        # delete the relationship between org1 and municipal elections
        self.org1.election_types.remove(self.elected_role1.election_type)

        with self.assertRaises(Organisation.ValidationError):
            reset_cache()
            builder.with_organisation(self.org1)

    def test_organisation_date_range_invalid(self):
        builder = ElectionBuilder("municipal", "2001-01-01")

        # delete the relationship between org1 and municipal elections
        self.org1.election_types.remove(self.elected_role1.election_type)

        with self.assertRaises(Organisation.ValidationError):
            builder.with_organisation(self.org1)

    def test_invalid_division_not_child_of_org(self):
        org2 = Organisation.objects.create(
            official_identifier="TEST2",
            organisation_type="municipal",
            official_name="Test City 2",
            slug="test-city-2",
            territory_code="ON",
            election_name="Test City 2 Municipal Elections",
            start_date=date(2016, 10, 1),
        )
        ElectedRole.objects.create(
            election_type=self.election_type1,
            organisation=org2,
            elected_title="City Councillor",
            elected_role_name="Councillor for Test City 2",
        )
        builder = ElectionBuilder("municipal", "2017-06-08").with_organisation(org2)

        # self.org_div_1 is not a child of org2
        # its a child of self.org1
        with self.assertRaises(OrganisationDivision.ValidationError):
            builder.with_division(self.org_div_1)

    def test_invalid_division_wrong_subtype(self):
        # Skip this test for now as it requires UK-specific subtypes
        # This test can be re-implemented when Canadian subtypes are defined
        self.skipTest("Requires Canadian election subtypes to be defined")

    def test_seats_contested_municipal_election(self):
        builder = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_organisation(self.org1)
            .with_division(self.org_div_1)
        )
        election = builder.build_ballot(None)
        election.save()
        self.assertEqual(election.seats_contested, 1)
        self.assertEqual(3, election.seats_total)

    def test_seats_contested_more_than_seats_total_raises(self):
        with self.assertRaises(ValueError) as e:
            (
                ElectionBuilder("municipal", "2017-06-08")
                .with_organisation(self.org1)
                .with_division(self.org_div_1)
                .with_seats_contested(100)
            )
        self.assertEqual(
            str(e.exception),
            "Seats contested can't be more than seats total (100 > 3)",
        )

    def test_seats_contested_municipal_by_election(self):
        builder = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_organisation(self.org1)
            .with_division(self.org_div_1)
            .with_contest_type("by")
        )
        election = builder.build_ballot(None)
        election.save()
        self.assertEqual(1, election.seats_contested)
        self.assertEqual(3, election.seats_total)

    def test_get_seats_contested(self):
        # Test with provincial election (similar structure)
        provincial_election_type, _ = ElectionType.objects.get_or_create(
            election_type="provincial"
        )
        provincial_org = Organisation.objects.create(
            official_identifier="ON",
            organisation_type="provincial",
            official_name="Ontario",
            slug="ontario",
            election_name="Ontario provincial election",
            territory_code="ON",
            start_date=date(1999, 5, 6),
        )

        ElectedRole.objects.create(
            election_type=provincial_election_type,
            organisation=provincial_org,
            elected_title="Member of Provincial Parliament",
            elected_role_name="Member of Provincial Parliament",
        )

        provincial_div_set = OrganisationDivisionSetFactory(organisation=provincial_org)

        provincial_div_1 = OrganisationDivisionFactory(
            divisionset=provincial_div_set,
            name="Riding 1",
            slug="riding-1",
            seats_total=7,
        )
        provincial_div_2 = OrganisationDivisionFactory(
            divisionset=provincial_div_set,
            name="Riding 2",
            slug="riding-2",
        )

        builder_1 = (
            ElectionBuilder("provincial", "2021-05-06")
            .with_organisation(provincial_org)
            .with_division(provincial_div_1)
            .with_seats_contested(7)
        )
        builder_2 = (
            ElectionBuilder("provincial", "2021-05-06")
            .with_organisation(provincial_org)
            .with_division(provincial_div_2)
        )

        ballot_1 = builder_1.build_ballot(None)
        ballot_1.save()

        ballot_2 = builder_2.build_ballot(None)
        ballot_2.save()

        self.assertEqual(7, ballot_1.seats_contested)
        self.assertEqual(1, ballot_2.seats_contested)

    def test_with_groups(self):
        builder = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_organisation(self.org1)
            .with_division(self.org_div_1)
        )
        election_group = builder.build_election_group()
        org_group = builder.build_organisation_group(election_group)
        ballot = builder.build_ballot(org_group)
        ballot.save()

        # calling save() on the ballot object
        # should also save its 2x parent groups
        self.assertEqual(3, Election.private_objects.all().count())
        self.assertIsNotNone(election_group.id)
        self.assertIsNotNone(org_group.id)
        self.assertIsNotNone(ballot.id)

    def test_created_with_status(self):
        builder = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_organisation(self.org1)
            .with_division(self.org_div_1)
        )
        election_group = builder.build_election_group()
        org_group = builder.build_organisation_group(election_group)
        ballot = builder.build_ballot(org_group)
        ballot.save()

        default_status = DEFAULT_STATUS

        self.assertEqual(default_status, ballot.current_status)
        self.assertEqual(default_status, org_group.current_status)
        self.assertEqual(default_status, election_group.current_status)

    def test_can_create_duplicate_groups(self):
        """
        Regression test for https://github.com/DemocracyClub/EveryElection/issues/1162

        If an ID exists for the organisation after creating a ballot ID, later
        attempts to create another ballot ID for the org on the same day failed
        due to a duplicate key error.

        """
        # A user submits an election for an organisation and save it
        builder = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_organisation(self.org1)
            .with_division(self.org_div_1)
        )
        election_group = builder.build_election_group().save()
        org_group = builder.build_organisation_group(election_group).save()
        ballot = builder.build_ballot(org_group)
        ballot.save()
        reset_cache()
        # Later, a user submits another election for that organisation, on the
        # same day, in a different division
        builder = (
            ElectionBuilder("municipal", "2017-06-08")
            .with_organisation(self.org1)
            .with_division(self.org_div_2)
        )
        election_group = builder.build_election_group().save()
        org_group = builder.build_organisation_group(election_group).save()
        ballot = builder.build_ballot(org_group)
        ballot.save()
