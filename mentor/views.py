from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import datetime

from django.contrib.auth import authenticate, login

from .serializers import MentorSerializer, MyTokenObtainPairSerializer, LoginViewAsMentorSerializer
from .models import Mentor

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import(
     Exercise,
     Exam,
     Grade,
)

from .serializers import (
    ExerciseSerializer,
    ExamSerializer,
    ExamStatusHomeSerializer,
    GradeSerializer,

   
)
from student.serializers import AnswerSerializer
from ceo.models import Course
from student.models import Student, Answer, AnswerExam
from mentor.models import Mentor
from rest_framework.exceptions import ValidationError



class LoginViewAsMentor(generics.CreateAPIView):
    serializer_class = LoginViewAsMentorSerializer

    def create(self, request, *args, **kwargs):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        mentor = authenticate(request, username=username, password=password)

        if mentor is not None:

            login(request, mentor)
            return Response(self.get_serializer(mentor).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class MentorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def get_object(self):
        user_id = self.request.user.id
        return Mentor.objects.get(user=user_id)


class MyTokenObtainPairView(TokenObtainPairView):
    # Set the serializer class used for token generation
    serializer_class = MyTokenObtainPairSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'refresh_token': token.get_refresh_token(),
        }, status=status.HTTP_200_OK)
    



# exercise
class MentorSendExercise(APIView):

   #   authentication_classes = [JWTAuthentication]
    def post(self, request, course_id):
        serializer = ExerciseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor = Mentor.objects.get(user=request.user)
        student_names = serializer.validated_data.pop('student_name', [])
        send_to_all = serializer.validated_data.pop('send_to_all', False)

        if send_to_all:
            students =  Student.objects.filter(course=course_id)
            send_to_all = True
        else:
            student_ids = [student.id for student in student_names]
            students = Student.objects.filter(id__in=student_ids, course=course_id)
            for student_id in student_ids:
                if not Student.objects.filter(id=student_id, course=course_id).exists():
                    raise ValidationError(f"Student with id {student_id} is not enrolled in the course {course_id}")
            send_to_all = False

        exercises = []
        for student in students:

            exercise = serializer.save(
                mentor=mentor,
                send_to_all=send_to_all,
            )
            exercise.student_name.add(student)
            exercises.append(exercise)

        response_data = []
        for exercise in exercises:
            response_data.append(serializer.to_representation(exercise))
        return Response(response_data, status=status.HTTP_201_CREATED)



class GetPostedExerciseOfMentor(APIView):
#   authentication_classes = [JWTAuthentication]
    def get(self, request,  student_id):
        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)
        exercises = Exercise.objects.filter(mentor=mentor, student_name=student)
        serializer = ExerciseSerializer(instance=exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetOnePostedExerciseOfMentor(APIView):
#   authentication_classes = [JWTAuthentication]
    def get(self, request,  student_id, id ):
        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)
        exercises = Exercise.objects.filter(mentor=mentor, student_name=student, id=id)
        serializer = ExerciseSerializer(instance=exercises, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#get answer-exercise of student
class MentorStudentExerciseList(APIView):
 #   authentication_classes = [JWTAuthentication]
    def get(self, request,  student_id):

        mentor = Mentor.objects.get(user=request.user)
        student = Student.objects.get(id=student_id)
        exercises = Answer.objects.filter(mentor=mentor, student=student, is_done_exercise=True)
        for exercise in exercises:
            exercise.is_seen_by_mentor = True
            exercise.save()
        serializer = AnswerSerializer(exercises, many=True)
        return Response(serializer.data)


class GetMentorExerciseStatus(APIView):
 #   authentication_classes = [JWTAuthentication]

    def get(self, request, student_id):
        mentor = Mentor.objects.get(user=request.user)
        
        student = Student.objects.get(id=student_id)

        exercises_viewed = Answer.objects.filter(mentor=mentor,  student=student, is_seen_by_mentor=True)
        exercises_not_viewed = Answer.objects.filter(mentor=mentor,  student=student, is_seen_by_mentor=False)
        num_exercises_viewed = exercises_viewed.count()
        num_exercises_not_viewed = exercises_not_viewed.count()
        return Response({'num_exercises_viewed': num_exercises_viewed, 'num_exercises_not_viewed': num_exercises_not_viewed})
    



#exam

class MentorCreateExam(APIView):
    
    def post(self, request, course_id):
        serializer = ExamSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mentor = Mentor.objects.get(user=request.user)
        student_names = serializer.validated_data.pop('student_name', [])
        send_to_all = serializer.validated_data.pop('send_to_all', False)

        if send_to_all:
            # students = Student.objects.all()
            students =  Student.objects.filter(course=course_id)
            send_to_all = True
        else:
            student_ids = [student.id for student in student_names]
            students = Student.objects.filter(id__in=student_ids, course=course_id)
            for student_id in student_ids:
                if not Student.objects.filter(id=student_id, course=course_id).exists():
                    raise ValidationError(f"Student with id {student_id} is not enrolled in the course {course_id}")
            send_to_all = False

        

        exams = []
        for student in students:
            exam_number_count = Exam.objects.filter(student_name=student).count()
            exam = serializer.save(
                mentor=mentor,
                send_to_all=send_to_all,
                exam_number=exam_number_count + 1,
                course_name_id=course_id
            )
            # exam.student_name.set([student])
            exam.student_name.add(student)
            exams.append(exam)

        response_data = []
        for exam in exams:
            response_data.append(serializer.to_representation(exam))
        return Response(response_data, status=status.HTTP_201_CREATED)


class GetAllExam(APIView):
    def get_object(self, exam_id):
        mentor = Mentor.objects.get(user=self.request.user)
        return Exam.objects.filter(id=exam_id, mentor=mentor)

    def get(self, request, exam_id, format=None):
        exams = self.get_object(exam_id)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)



class AddGradeView(APIView):
    # def get_object(self, id):
    #     mentor = Mentor.objects.get(user=self.request.user)
    #     return AnswerExam.objects.filter(id=id, mentor=mentor)

    # def get(self, request, id, format=None):
        
    #     answer = self.get_object(id)
    #     serializer = AnswerExamSerializer(answer)
    #     return Response(serializer.data)

    def post(self, request, exam_id, student_id):
        mentor = Mentor.objects.get(user=request.user)
        exam = Exam.objects.get(id=exam_id, mentor=mentor)
        student = Student.objects.get(id=student_id)

        # Check if the student has submitted an answer to the exam
        if not AnswerExam.objects.filter(student=student, exam=exam).exists():
            return Response({'detail': 'This student has not submitted an answer for this exam.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the exam has already been graded for this student
        if Grade.objects.filter(exam=exam, student_name=student).exists():
            return Response({'detail': 'This exam has already been graded for this student.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GradeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(mentor=mentor, exam=exam, student_name=[student])
        return Response(serializer.data, status=status.HTTP_201_CREATED)








class GradeListView(APIView):
   
    def get(self, request, exam_id):
        mentor = Mentor.objects.get(user=request.user)
        exam = Exam.objects.filter(id=exam_id, mentor=mentor)
        grades = Grade.objects.all()

        if exam:
            grades = Grade.objects.filter(mentor=mentor)
            serializer = GradeSerializer(grades, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




class ExamStatusList(generics.ListAPIView):
    queryset = Exam.objects.filter(is_deleted=False)
    serializer_class = ExamStatusHomeSerializer

    def get(self, request, *args, **kwargs):
        exams = self.get_queryset()
        serializer = self.get_serializer(exams, many=True)
        status_list = []
        for exam in exams:
            status = self.get_exam_status(exam)
            status_list.append({
                'exam_id': exam.id,
                'exam_name': exam.exam_name,
                'status': status,
                'start_time': exam.start_time,
                'end_time': exam.end_time

            })
        return Response(status_list)

    def get_exam_status(self, exam):
        # Get the current datetime in UTC timezone
        current_datetime = datetime.datetime.now(datetime.timezone.utc)
        # Add 3.5 hours to the current datetime
        now = current_datetime + datetime.timedelta(hours=3, minutes=30)
        # print(now)
        if exam.start_time <= now < exam.end_time:
            return 'Holding'
        elif exam.end_time <= now:
            return 'Completed'
        else:
            return 'Not held'
