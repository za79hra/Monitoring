# Generated by Django 4.1.7 on 2023-06-24 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ceo", "0001_initial"),
        ("student", "0001_initial"),
        ("mentor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exercise",
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
                ("send_to_all", models.BooleanField(default=False)),
                ("exercise_name", models.CharField(max_length=200)),
                ("caption", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "course_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_name",
                        to="ceo.course",
                    ),
                ),
                (
                    "mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mentor_exercise_model",
                        to="mentor.mentor",
                    ),
                ),
                (
                    "student_name",
                    models.ManyToManyField(
                        related_name="assigned_exercises", to="student.student"
                    ),
                ),
            ],
        ),
    ]
