from django.urls import path
from products.views import  CommentView

urlpatterns = [
    path('/comments/<int:course_id>', CommentView.as_view())
]