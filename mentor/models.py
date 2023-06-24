from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')

    PERSONALITIES = (
        ('INTP', 'INTP'), ('INTJ', 'INTJ'), ('ENTJ', 'ENTJ'), ('ENTP', 'ENTP'),
        ('INFJ', 'INFJ'), ('INFP', 'INFP'), ('ENFJ', 'ENFJ'), ('ENFP', 'ENFP'),
        ('ISTJ', 'ISTJ'), ('ISFJ', 'ISFJ'), ('ESTJ', 'ESTJ'), ('ESFJ', 'ESFJ'),
        ('ISTP', 'ISTP'), ('ISFP', 'ISFP'), ('ESTP', 'ESTP'), ('ESFP', 'ESFP'),
    )

    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=13, editable=True, unique=True)
    identity_code = models.CharField(max_length=10, unique=True)
    personality = models.CharField(max_length=15, choices=PERSONALITIES)
    avatar = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'personality']

    def __str__(self):
        # return f"{self.id} - {self.first_name} {self.last_name}"
        return f"{self.first_name} - {self.phone_number} - {self.date_of_birth}"
    




class Exercise(models.Model):

    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exercise_model')
    course_name = models.ForeignKey("ceo.Course", on_delete=models.CASCADE, related_name='course_name')
    student_name = models.ManyToManyField("student.Student", related_name='assigned_exercises')
    send_to_all = models.BooleanField(default=False)
    exercise_name = models.CharField(max_length=200)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.exercise_name
    


#exam

class Exam(models.Model):
    course_name = models.ForeignKey("ceo.Course", on_delete=models.CASCADE, related_name='course')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_exam')
    student_name = models.ManyToManyField("student.Student", related_name='assigned_exam')
    send_to_all = models.BooleanField(default=False)
    exam_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    exam_number = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


    def __str__(self):
        return {self.exam_name}


class Grade(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='mentor_grade')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_grade')
    score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(20.0)])
    opinion = models.TextField(max_length=200)
    student_name = models.ManyToManyField("student.Student", related_name='grade')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.score}"