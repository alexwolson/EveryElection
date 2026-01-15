"""
Tests for Canadian Election ID Builder
"""

from datetime import date

from django.test import TestCase

from elections.ca_election_ids import CaIdBuilder


class TestCaIdBuilder(TestCase):
    def test_federal_election_group_id(self):
        """Test federal election group ID generation."""
        builder = CaIdBuilder("federal", date(2025, 4, 28))
        assert builder.election_group_id == "federal.2025-04-28"

    def test_provincial_election_group_id(self):
        """Test provincial election group ID generation."""
        builder = CaIdBuilder("provincial", date(2022, 6, 2))
        assert builder.election_group_id == "provincial.2022-06-02"

    def test_territorial_election_group_id(self):
        """Test territorial election group ID generation."""
        builder = CaIdBuilder("territorial", date(2023, 10, 3))
        assert builder.election_group_id == "territorial.2023-10-03"

    def test_municipal_election_group_id(self):
        """Test municipal election group ID generation."""
        builder = CaIdBuilder("municipal", date(2022, 10, 24))
        assert builder.election_group_id == "municipal.2022-10-24"

    def test_provincial_with_organisation(self):
        """Test provincial election with organisation (jurisdiction)."""
        builder = CaIdBuilder("provincial", date(2022, 6, 2))
        builder.with_organisation("ontario")
        assert builder.organisation_group_id == "provincial.ontario.2022-06-02"

    def test_provincial_with_division(self):
        """Test provincial election with organisation and division."""
        builder = CaIdBuilder("provincial", date(2022, 6, 2))
        builder.with_organisation("ontario")
        builder.with_division("toronto-danforth")
        assert builder.ballot_id == "provincial.ontario.toronto-danforth.2022-06-02"

    def test_federal_by_election(self):
        """Test federal by-election ID format."""
        builder = CaIdBuilder("federal", date(2024, 6, 24))
        builder.with_division("toronto-centre")
        builder.with_contest_type("by")
        assert builder.ballot_id == "federal.toronto-centre.by.2024-06-24"

    def test_provincial_by_election(self):
        """Test provincial by-election ID format."""
        builder = CaIdBuilder("provincial", date(2023, 3, 27))
        builder.with_organisation("ontario")
        builder.with_division("toronto-danforth")
        builder.with_contest_type("by")
        assert (
            builder.ballot_id
            == "provincial.ontario.toronto-danforth.by.2023-03-27"
        )

    def test_municipal_with_ward(self):
        """Test municipal election with ward."""
        builder = CaIdBuilder("municipal", date(2022, 10, 24))
        builder.with_organisation("toronto")
        builder.with_division("ward-10")
        assert builder.ballot_id == "municipal.toronto.ward-10.2022-10-24"

    def test_slugification(self):
        """Test that organisation and division names are properly slugified."""
        builder = CaIdBuilder("provincial", date(2022, 6, 2))
        builder.with_organisation("British Columbia")
        builder.with_division("Vancouver Quadra")
        assert builder.organisation_group_id == "provincial.british-columbia.2022-06-02"
        assert (
            builder.ballot_id
            == "provincial.british-columbia.vancouver-quadra.2022-06-02"
        )

    def test_subtype_group_id(self):
        """Test subtype group ID generation."""
        builder = CaIdBuilder("federal", date(2025, 4, 28))
        builder.with_subtype("some-subtype")
        assert builder.subtype_group_id == "federal.some-subtype.2025-04-28"

    def test_subtype_without_subtype_returns_election_group(self):
        """Test that subtype_group_id returns election_group_id if no subtype."""
        builder = CaIdBuilder("federal", date(2025, 4, 28))
        assert builder.subtype_group_id == builder.election_group_id

    def test_ids_property(self):
        """Test that ids property returns list of all IDs."""
        builder = CaIdBuilder("provincial", date(2022, 6, 2))
        builder.with_organisation("ontario")
        builder.with_division("toronto-danforth")

        ids = builder.ids
        assert len(ids) == 3
        assert "provincial.2022-06-02" in ids
        assert "provincial.ontario.2022-06-02" in ids
        assert "provincial.ontario.toronto-danforth.2022-06-02" in ids

    def test_invalid_election_type(self):
        """Test that invalid election type raises ValueError."""
        with self.assertRaises(ValueError):
            CaIdBuilder("invalid", date(2025, 4, 28))

    def test_equality(self):
        """Test that two builders with same configuration are equal."""
        builder1 = CaIdBuilder("federal", date(2025, 4, 28))
        builder1.with_division("toronto-centre")

        builder2 = CaIdBuilder("federal", date(2025, 4, 28))
        builder2.with_division("toronto-centre")

        assert builder1 == builder2

    def test_inequality(self):
        """Test that two builders with different configurations are not equal."""
        builder1 = CaIdBuilder("federal", date(2025, 4, 28))
        builder1.with_division("toronto-centre")

        builder2 = CaIdBuilder("federal", date(2025, 4, 28))
        builder2.with_division("vancouver-quadra")

        assert builder1 != builder2

    def test_repr(self):
        """Test string representation of builder."""
        builder = CaIdBuilder("federal", date(2025, 4, 28))
        builder.with_division("toronto-centre")
        repr_str = repr(builder)
        assert "CaIdBuilder" in repr_str
        assert "federal" in repr_str
        assert "2025-04-28" in repr_str

    def test_federal_without_organisation(self):
        """Test that federal elections don't require organisation in ID."""
        builder = CaIdBuilder("federal", date(2025, 4, 28))
        builder.with_division("toronto-centre")
        # Federal elections can have divisions without explicit organisation
        assert builder.ballot_id == "federal.toronto-centre.2025-04-28"

    def test_date_formatting(self):
        """Test that dates are formatted correctly."""
        builder = CaIdBuilder("federal", date(2025, 1, 1))
        assert builder.election_group_id == "federal.2025-01-01"

        builder = CaIdBuilder("federal", date(2025, 12, 31))
        assert builder.election_group_id == "federal.2025-12-31"

    def test_special_characters_in_names(self):
        """Test handling of special characters in names."""
        builder = CaIdBuilder("municipal", date(2022, 10, 24))
        builder.with_organisation("Québec City")
        builder.with_division("Ward 10 - Centre")
        # Should be slugified properly
        assert "quebec-city" in builder.organisation_group_id.lower()
        assert "ward-10" in builder.ballot_id.lower() or "centre" in builder.ballot_id.lower()

    def test_by_election_with_organisation(self):
        """Test by-election with organisation."""
        builder = CaIdBuilder("provincial", date(2023, 3, 27))
        builder.with_organisation("quebec")
        builder.with_division("montreal-riding")
        builder.with_contest_type("by")
        assert (
            builder.ballot_id
            == "provincial.quebec.montreal-riding.by.2023-03-27"
        )

    def test_contest_type_not_by(self):
        """Test that non-by contest types are handled."""
        builder = CaIdBuilder("federal", date(2025, 4, 28))
        builder.with_division("toronto-centre")
        builder.with_contest_type("general")
        # Only "by" is added to the ID
        assert builder.ballot_id == "federal.toronto-centre.2025-04-28"
