from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from pdp.models import Circle, UserAccount


class Command(BaseCommand):
    help = (
        "Checks and creates UserAccount and associated Circle for Users without them."
    )

    def handle(self, *args, **kwargs):
        # Fetching all users
        users = User.objects.all()

        for user in users:
            # Check if user has a UserAccount and associated Circle
            user_account = UserAccount.objects.filter(user=user).first()

            if not user_account:
                name = (
                    f"{user.first_name} {user.last_name}"
                    if user.first_name and user.last_name
                    else user.username
                )
                circle = Circle.objects.create(name=name, user=user)
                UserAccount.objects.create(user=user, circle=circle)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created UserAccount and"
                        f" Circle for user {user.username}"
                    )
                )
            elif not user_account.circle:
                name = (
                    f"{user.first_name} {user.last_name}"
                    if user.first_name and user.last_name
                    else user.username
                )
                circle = Circle.objects.create(name=name, user=user)
                user_account.circle = circle
                user_account.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created Circle for user {user.username}"
                    )
                )
