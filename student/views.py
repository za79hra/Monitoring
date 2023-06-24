from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, generics, viewsets

from rest_framework.permissions import IsAuthenticated

from django.http import Http404



from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login

from .models import Student, Payment
# from ceo.models import Admin
from .serializers import StudentSerializer, StudentTokenObtainPairSerializer,\
    LoginViewAsStudentSerializer, ReportSerializer, PaymentSerializer

from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

from .models import(
     Answer,
     AnswerExam
)

from .serializers import (
    AnswerSerializer, 
    AnswerExamSerializer
   
)
from mentor.serializers import ExerciseSerializer, ExamSerializer, ExamStatusHomeSerializer, GradeSerializer
from ceo.models import Course
from student.models import Student
from mentor.models import Mentor, Exam, Exercise, Grade



class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentTokenObtainPairSerializer


class LoginViewAsStudent(generics.CreateAPIView):
    serializer_class = LoginViewAsStudentSerializer
    def create(self, request, *args, **kwargs):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's built-in function
        student = authenticate(request, username=username, password=password)

        # Check if authentication was using
        if student is not None:
            # Log the user in using Django's built-in function
            login(request, student)
            return Response(self.get_serializer(student).data, status=status.HTTP_200_OK)

            # serializer = LoginViewAsStudentSerializer(student)
            # token, _ = Token.objects.get_or_create(user=student)

            # return redirect('detail', pk=student.pk)
            # else:
            #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            # Return a success response with the user's information
            # return Response(serializer.data, status=status.HTTP_200_OK)



        else:
            # Return an error response if authentication failed
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class StudentDetails(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = StudentSerializer(request.user, many=True, context={'request': request})
        return Response(serializer.data)


class StudentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        return Student.objects.get(user=user_id)

# {"username": "student_09109232094", "password": "0020064586"}


class DailyReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.create(serializer.validated_data)
        return Response({
            'message': "Report Created successfully",
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer






#student-exercise

class StudentPanelSendExercise(APIView):
#   authentication_classes = [JWTAuthentication]


    def get_object(self, id):
        mentor = Student.objects.get(user=self.request.user)
        return Exercise.objects.filter(id=id, student_name=mentor)

    def get(self, request, id, format=None):
        exercise = self.get_object(id)
        serializer = ExerciseSerializer(exercise, many=True)
        return Response(serializer.data)
    

    def post(self,request, id):
        student = Student.objects.get(user=request.user)

        exercise =Exercise.objects.get(id=id, student_name=student)

        # print(student.course)
        course = student.course
        mentor = course.mentor
        exercise = Exercise.objects.get(id=id, student_name=student)

        # Check if the student has already answered the exercise
        if Answer.objects.filter(student=student, exercise=exercise, is_done_exercise=True).exists():
            return Response({'detail': 'You have already answered this exercise.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the course object has the id attribute
        if not hasattr(course, 'id'):
            course = Course.objects.get(pk=course.pk)

        serializer = AnswerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(student=student, mentor=mentor,course=course, exercise=exercise)   
        instance.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GetPostedExerciseOfStudent(APIView):
   #   authentication_classes = [JWTAuthentication]

    def get(self, request, id):
  
        student = Student.objects.get(user=request.user)
        exercises_done = Answer.objects.filter(student=student)
        exercise=Exercise.objects.filter(id=id)
        exercises_done.update(is_done_exercise=False)
        serializer = AnswerSerializer(instance=exercises_done, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetStudentExerciseStatus(APIView):
#   authentication_classes = [JWTAuthentication]
 
    def get(self, request, *args, **kwargs):

        student = Student.objects.get(user=request.user)
        exercises_done = Answer.objects.filter(student=student, is_done_exercise=True)
        exercises_not_done = Answer.objects.filter(student=student, is_done_exercise=False)
        num_exercises_done = exercises_done.count()
        num_exercises_not_done = exercises_not_done.count()
        return Response({'num_exercises_done': num_exercises_done, 'num_exercises_not_done': num_exercises_not_done})




#student-exam

class StudentGetExam(APIView):
#   authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        student = Student.objects.get(user=self.request.user)
        return Exam.objects.filter(id=id, student_name=student)

    def get(self, request, id, format=None):
        exams = self.get_object(id)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)

    def post(self,request, id):
        student = Student.objects.get(user=request.user)

        exam =Exam.objects.get(id=id, student_name=student)
        course = student.course
        mentor = course.mentor

        # Check if the student has already answered the exercise
        if AnswerExam.objects.filter(student=student, exam=exam).exists():
            return Response({'detail': 'You have already answered this exercise.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the course object has the id attribute
        if not hasattr(course, 'id'):
            course = Course.objects.get(pk=course.pk)

        serializer = AnswerExamSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(student=[student], mentor=mentor,course=course, exam=exam)   
    
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class GradeView(APIView):
   
    def get(self, request, exam_id):
        student = Student.objects.get(user=request.user)
        try:
            grade = Grade.objects.get(exam_id=exam_id, student_name=student)
            serializer = GradeSerializer(grade)
            return Response(serializer.data)
        except Grade.DoesNotExist:
            return Response({'detail': 'Grade not found.'}, status=status.HTTP_404_NOT_FOUND)
      


