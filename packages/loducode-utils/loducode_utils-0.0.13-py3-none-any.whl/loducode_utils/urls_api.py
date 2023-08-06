
from django.urls import path

from .views_api import ObtainCustomAuthToken, LogoutView, ForgetPasswordView

app_name = 'loducode_utils'

urlpatterns = [
    path('token/', ObtainCustomAuthToken.as_view(), name="token" ),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('forget/', ForgetPasswordView.as_view(), name="logout")
]
