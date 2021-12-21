from django.urls import path

from .views import KakaoSignInView
from users.views import MypageView


urlpatterns = [
    path('/kakaosignin', KakaoSignInView.as_view()),
    path('/Mypage',MypageView.as_view())
]