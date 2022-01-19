from getpass import getpass, getuser

from django.core.management.base import CommandError
from django.contrib.auth.management.commands import createsuperuser

from oauth_proxy.models import CompassUser


class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        newuser = CompassUser()
        try:
            newuser.username = self.get_username()
            password1 = getpass("Enter Password: ") or None
            if not password1:
                raise CommandError("Password not provided")
            password2 = getpass("Enter Password again: ") or None
            if not password1 == password2:
                raise CommandError("Passwords did not match")
            newuser.set_password(password1)
            newuser.email = input("Enter email address: ") or None
            newuser.member_number = self.gen_non_compass_member_number()
            newuser.is_staff = True
            newuser.is_superuser = True
            newuser.save()

        except (KeyboardInterrupt, EOFError) as e:
            del newuser
            print(flush=True)
            raise CommandError("Exited before saving the user")
        except Exception as e:
            raise CommandError(e)

    @classmethod
    def get_username(cls) -> str:
        prompt = "Enter Username"
        username = getuser()
        if username:
            prompt += f" [{username}]"
        prompt += ": "
        in_user = input(prompt).strip()

        if in_user:
            username = in_user

        if not username:
            raise CommandError("Username not provided")
        return username

    @classmethod
    def gen_non_compass_member_number(cls) -> int:
        lowest_user: CompassUser = (
            CompassUser.objects.all().order_by("member_number").first()
        )
        if not lowest_user:
            return -1
        if lowest_user.member_number > 0:
            return -1
        return lowest_user.member_number - 1
