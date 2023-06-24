from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import StudentTokenObtainPairSerializer, LoginViewAsStudent,\
    StudentDetails, StudentDetailView, DailyReportView

from .views import(
# MentorSendExercise,
# GetPostedExerciseOfMentor,
StudentPanelSendExercise,
GetPostedExerciseOfStudent,
# MentorCreateExam,
# GetMentorExerciseStatus,
GetStudentExerciseStatus,
# MentorStudentExerciseList,
# AddGradeView,
# AddGradeView,
# GradeListView,
# GetAllExam,
# GetOnePostedExerciseOfMentor,
StudentGetExam,
# ExamStatusList,
GradeView
)




urlpatterns = [
    # path('login/', StudentTokenObtainPairSerializer.as_view()),
    path('login2/', TokenObtainPairView.as_view(serializer_class=StudentTokenObtainPairSerializer)),
    path('login/', LoginViewAsStudent.as_view()),
    path('detail/', StudentDetails.as_view()),
    path('detail2/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Report
    path('create-report/', DailyReportView.as_view()),

    # student-exercise
    path('send-answer-student/<int:id>/', StudentPanelSendExercise.as_view(), name='exercises_create_student'),
    path('get-answer-student/<int:id>/', GetPostedExerciseOfStudent.as_view(), name='exercises_list_student'),
    path('student-status/', GetStudentExerciseStatus.as_view(), name='student_status'),
   
#   student
    path('send-answer-exam/<int:id>/', StudentGetExam.as_view()),
    path('grade-exam/<int:exam_id>/', GradeView.as_view()),

]