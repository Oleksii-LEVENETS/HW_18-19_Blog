from blog_users.models import BlogUser, Profile

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.template.defaultfilters import pluralize

from faker import Faker


class Command(BaseCommand):
    help = "Creating fake Users"  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument(
            "count_of_users",
            type=int,
            choices=range(1, 6),
            help="Enter an integer from 1 to 5 incl. -- the count of fake users.",
        )

    def handle(self, *args, **options):
        fake = Faker()
        list_users = []
        for _ in range(options["count_of_users"]):
            name = fake.name()
            first_name = name.split(" ")[0]
            last_name = name.split(" ")[-1]
            username = first_name.lower() + last_name.lower()
            email = username + "@" + last_name.lower() + ".com"
            password = "QWE!@#qwe123"
            list_users.append(
                BlogUser(
                    username=username,
                    password=make_password(password),
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
            )

        blog_users_created = BlogUser.objects.bulk_create(list_users)

        list_profiles = []
        for user in blog_users_created:
            about_me = f"Two words about me ({user.first_name} {user.last_name}). {fake.text(200)}"
            user = user
            list_profiles.append(
                Profile(
                    about_me=about_me,
                    user=user,
                )
            )

        Profile.objects.bulk_create(list_profiles)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {options['count_of_users']} user{pluralize(options['count_of_users'])}!"
            )
        )
