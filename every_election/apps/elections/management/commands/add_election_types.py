from django.core.management.base import BaseCommand
from elections.models import ElectionSubType, ElectionType
from elections.ca_election_metadata import CA_ELECTION_TYPES


class Command(BaseCommand):
    """
    Management command to add Canadian election types to the database.
    
    Creates/updates ElectionType records for: federal, provincial, territorial, municipal
    """
    
    help = "Add Canadian election types to the database"

    def handle(self, *args, **options):
        for type_name, info in CA_ELECTION_TYPES.items():
            election_type, created = ElectionType.objects.update_or_create(
                election_type=type_name,
                defaults={"name": info["name"]},
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} election type: {type_name}")
            
            for subtype in info.get("subtypes", []):
                sub, sub_created = ElectionSubType.objects.update_or_create(
                    election_type=election_type,
                    election_subtype=subtype["election_subtype"],
                    defaults={"name": subtype["name"]},
                )
                sub_action = "Created" if sub_created else "Updated"
                self.stdout.write(f"  {sub_action} subtype: {subtype['election_subtype']}")
