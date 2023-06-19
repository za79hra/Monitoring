from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels


from mentor.models import Mentor

from multiselectfield import MultiSelectField


class Course(models.Model):
    HOLDING = (
        ('Online', 'Online'),
        ('In person', 'In person')
    )

    DAYS_OF_WEEK_CHOICES = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]

    name = models.CharField(max_length=60)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_of_course')
    start_at = models.DateField()
    duration = models.PositiveSmallIntegerField(default=6)
    days_of_week = MultiSelectField(choices=DAYS_OF_WEEK_CHOICES, max_choices=2, max_length=7)
    class_time = models.TimeField()
    how_to_hold = models.CharField(max_length=15, choices=HOLDING)
    short_brief = models.CharField(max_length=70)

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DailyNote(models.Model):
    objects = jmodels.jManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notes')
    daily_note = models.TextField()
    created_at = jmodels.jDateField(auto_now_add=True)
    modified_at = jmodels.jDateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)