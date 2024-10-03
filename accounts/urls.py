from django.urls import path

from accounts.views import UserRegistrations, UserLoginView, UserLogoutView, get_current_user

urlpatterns = [
    path('registration/', UserRegistrations.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('me/', get_current_user, name='get_current_user'),

]
