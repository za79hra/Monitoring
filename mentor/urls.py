from django.urls import path

from .views import(
MyTokenObtainPairView,
LoginViewAsMentor,
MentorDetailView,
MentorSendExercise,
GetPostedExerciseOfMentor,
GetOnePostedExerciseOfMentor,
GetMentorExerciseStatus,
)




urlpatterns = [
    path('login/', LoginViewAsMentor.as_view()),
    path('detail2/<int:pk>/', MentorDetailView.as_view()),
    path('login2/', MyTokenObtainPairView.as_view()),

    # mentor-exercise
    path('send-exercise/<int:course_id>/', MentorSendExercise.as_view(), name='send_exercise_mentor'),
    path('get-exercises-student/<int:student_id>/', GetPostedExerciseOfMentor.as_view(), name='get_exercise_mentor'),
    path('get-exercises-student/<int:student_id>/<int:id>/', GetOnePostedExerciseOfMentor.as_view(), name='get_exercise_mentor1'),
    path('menotr-status/<int:student_id>/', GetMentorExerciseStatus.as_view(), name='get_status_mentor'),
]