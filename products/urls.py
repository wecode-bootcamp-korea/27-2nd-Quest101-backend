from django.urls import path

from .views import OrderView, CommentView, LikeView

urlpatterns = [
    path('/order/<int:course_id>', OrderView.as_view()),
    path('/<int:course_id>/comments', CommentView.as_view()),
    path('/like', LikeView.as_view())
]
