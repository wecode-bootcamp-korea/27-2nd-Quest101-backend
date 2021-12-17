from django.urls import path

from .views import ProductView

urlpatterns=[
    path('/detail/<int:course_id>', ProductView.as_view())
]