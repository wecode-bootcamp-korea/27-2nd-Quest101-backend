from django.urls import path

from .views import *

urlpatterns = [
    path('', CoursesView.as_view()),
    path('/<int:course_id>', CourseView.as_view()),
]