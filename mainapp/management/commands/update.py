
from django.core.management.base import BaseCommand
from authapp.models import ShopUser, ShopUserProfile

class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            users = ShopUser.objects.all()
            for user in users:
                users_profile = ShopUserProfile.objects.create(user=user)
                users_profile.save()