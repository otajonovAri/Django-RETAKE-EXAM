"""Ishlab chiqish uchun admin foydalanuvchi yaratadi.

`createsuperuser` interaktiv savol beradi; bu buyruq esa bir marta ishga
tushirilsa yetadi va qayta ishga tushirilganda xato bermaydi (idempotent).

Qiymatlarni `.env` orqali o'zgartirish mumkin:
    DJANGO_ADMIN_USERNAME, DJANGO_ADMIN_EMAIL, DJANGO_ADMIN_PASSWORD
"""

import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

DEFAULT_USERNAME = "admin"
DEFAULT_EMAIL = "admin@example.com"
DEFAULT_PASSWORD = "admin12345"


class Command(BaseCommand):
    help = "Ishlab chiqish uchun admin (superuser) foydalanuvchi yaratadi."

    def add_arguments(self, parser):
        parser.add_argument("--username", default=None)
        parser.add_argument("--email", default=None)
        parser.add_argument("--password", default=None)
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="Foydalanuvchi mavjud bo'lsa, parolini yangilaydi.",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        username = (
            options["username"]
            or os.getenv("DJANGO_ADMIN_USERNAME")
            or DEFAULT_USERNAME
        )
        email = options["email"] or os.getenv("DJANGO_ADMIN_EMAIL") or DEFAULT_EMAIL
        password = (
            options["password"]
            or os.getenv("DJANGO_ADMIN_PASSWORD")
            or DEFAULT_PASSWORD
        )

        if not settings.DEBUG and password == DEFAULT_PASSWORD:
            self.stderr.write(
                self.style.ERROR(
                    "DEBUG=False bo'lganda standart parol ishlatilmaydi. "
                    "DJANGO_ADMIN_PASSWORD ni belgilang yoki --password bering."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Admin yaratildi: {username} / {password}")
            )
        elif options["reset_password"]:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Parol yangilandi: {username} / {password}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"«{username}» allaqachon mavjud. Parolni almashtirish uchun: "
                    "python manage.py createadmin --reset-password"
                )
            )

        if settings.DEBUG:
            self.stdout.write(
                "Kirish: http://127.0.0.1:8000/admin/  |  "
                "Swagger: http://127.0.0.1:8000/api/docs/"
            )
