from django.core.management.base import BaseCommand
from authentication.models import Role

class Command(BaseCommand):
    help = 'Create initial roles'

    def handle(self, *args, **kwargs):
        roles = [
            'Admin',
            'Manager',
            'Employee',
            'Finance',
        ]

        for role_name in roles:
            Role.objects.get_or_create(name=role_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created role "{role_name}"'))
