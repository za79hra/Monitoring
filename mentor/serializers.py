import re

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User

from Monitoring.utils import *

from .models import Mentor, Exercise, Exam, Grade


class MentorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = JalaliDateField()
    jalali_date_of_birth = serializers.CharField(required=False, allow_blank=True, max_length=10)
    phone_number = serializers.CharField(required=True)
    identity_code = serializers.CharField(required=True, write_only=True)
    personality = serializers.ChoiceField(choices=Mentor.PERSONALITIES, required=True)
    avatar = serializers.ImageField(required=False)

    def create(self, validated_data: dict) -> Mentor:
        try:
            with transaction.atomic():
                username = f"mentor_{validated_data['phone_number']}"
                user = User.objects.create(username=username)

                user.set_password(validated_data['identity_code'])
                user.save()
                jalali_date = validated_data.pop('jalali_date_of_birth', None)
                if not jalali_date:
                    raise serializers.ValidationError({'jalali_date_of_birth': 'This field is required.'})
                validated_data['date_of_birth'] = convert_jalali_to_gregorian(jalali_date)

                mentor = Mentor.objects.create(user=user, **validated_data)
                return mentor
        except IntegrityError:
            raise serializers.ValidationError('Phone number already exists')

    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'jalali_date_of_birth', 'date_of_birth', 'phone_number', 'identity_code',
                  'personality', 'avatar')
        read_only_fields = ['id', 'first_name', 'last_name', 'identity_code', 'jalali_date_of_birth', 'date_of_birth'
                                                                                                      'personality']

    def validate_phone_number(self, value: str) -> str:

        if value.startswith('+98') and len(value) == 13 and str(value[1:]).isnumeric():
            value = '0' + str(value[3:])
            return value

        elif value.startswith('09') and len(value) == 11:
            return value

        elif not value.startswith('+98') or not value.startswith('0'):
            raise serializers.ValidationError('Invalid phone number format')
        elif Mentor.objects.filter(username=value).exists():
            raise serializers.ValidationError("A mentor with this phone_number is exist")
        return value

    def validate_first_name(self, value: str) -> str:
        persian_regex = '^[\u0600-\u06FF\s]+$'
        if not re.match(persian_regex, value):
            raise serializers.ValidationError("First name must be written in Persian.")
        elif not re.search('[^a-zA-Z]', value):
            raise serializers.ValidationError('First name must not contain signs or numbers.')
        if re.search('[\u06F0-\u06F9]', value):
            raise serializers.ValidationError('First name must not contain Persian numbers.')
        return value

    def validate_last_name(self, value: str) -> str:
        persian_regex = '^[\u0600-\u06FF\s]+$'
        if not re.match(persian_regex, value):
            raise serializers.ValidationError("Last name must be written in Persian.")
        elif not re.search('[^a-zA-Z]', value):
            raise serializers.ValidationError('Last name must not contain signs or numbers.')
        if re.search('[\u06F0-\u06F9]', value):
            raise serializers.ValidationError('Last name must not contain Persian numbers.')
        return value

    def validate_identity_code(self, value: str) -> str:
        if not value.isnumeric():
            raise serializers.ValidationError('Identity code must be numeric.')
        if re.search('[^0-9]', value):
            raise serializers.ValidationError('Identity code must not contain letters or signs.')
        return value

    def validate_avatar(self, value):
        max_size = 11 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('Avatar size must be less than 11 MB.')
        if not value.name.lower().endswith('.jpeg') and not value.name.lower().endswith('.jpg'):
            raise serializers.ValidationError('Avatar must be in JPEG/JPG format.')
        return value

    def update(self, instance, validated_data):
        # Remove the fields from the validated data
        validated_data.pop('id')
        validated_data.pop('first_name')
        validated_data.pop('last_name')
        validated_data.pop('date_of_birth')
        validated_data.pop('identity_code')
        validated_data.pop('personality')

        if 'phone_number' in validated_data:
            instance.phone_number = validated_data['phone_number']
            validated_data.pop('phone_number')

        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
            validated_data.pop('avatar')

        return super().update(instance, validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Add any additional fields you want to include in the token
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        # ... any other fields you want to include
        return token


class LoginViewAsMentorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = Mentor
        fields = ('username', 'password')



# exercise
class ExerciseSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='MentorStudentExerciseList')
    class Meta:
        model = Exercise
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']
     

    def validate(self, data):
    
        mentor = self.context['request'].user
        data['mentor'] = mentor
        return data

#exam
class ExamSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Exam
        fields = '__all__'
        # fields = ['mentor', 'exam_name', 'exam_date', 'description', 'created_at', 'modified_at', 'is_deleted']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted', 'course_name']



class GradeSerializer(serializers.ModelSerializer):
    student_first_name = serializers.CharField(source='student_name.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student_name.last_name', read_only=True)
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    mentor_name = serializers.CharField(source='mentor.name', read_only=True)
    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at', 'is_deleted', 'exam', 'mentor', 'student_name']


class ExamStatusHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'
        # fields = ['exam_name', 'exam_date', 'status', 'score', 'exam_number']
        read_only_fields = ['created_at', 'modified_at', 'is_deleted']