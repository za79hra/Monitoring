# Generated by Django 4.1.7 on 2023-06-19 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Mentor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=35)),
                ("last_name", models.CharField(max_length=35)),
                ("date_of_birth", models.DateField()),
                ("phone_number", models.CharField(max_length=13, unique=True)),
                ("identity_code", models.CharField(max_length=10, unique=True)),
                (
                    "personality",
                    models.CharField(
                        choices=[
                            ("INTP", "INTP"),
                            ("INTJ", "INTJ"),
                            ("ENTJ", "ENTJ"),
                            ("ENTP", "ENTP"),
                            ("INFJ", "INFJ"),
                            ("INFP", "INFP"),
                            ("ENFJ", "ENFJ"),
                            ("ENFP", "ENFP"),
                            ("ISTJ", "ISTJ"),
                            ("ISFJ", "ISFJ"),
                            ("ESTJ", "ESTJ"),
                            ("ESFJ", "ESFJ"),
                            ("ISTP", "ISTP"),
                            ("ISFP", "ISFP"),
                            ("ESTP", "ESTP"),
                            ("ESFP", "ESFP"),
                        ],
                        max_length=15,
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_images/"
                    ),
                ),
                ("created_at", models.DateField(auto_now_add=True)),
                ("modified_at", models.DateField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mentor_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
