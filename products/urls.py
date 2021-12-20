from django.urls import path

from .views import OrderView, CommentView

urlpatterns = [
    path('/<int:course_id>/order', OrderView.as_view()),
    path('/<int:course_id>/comments', CommentView.as_view())
]