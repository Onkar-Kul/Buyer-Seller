from django.urls import path

from user_interface.views import login_page, dashboard

urlpatterns = [
    path('', login_page, name='login_page'),
    path('dashboard/', dashboard, name='dashboard'),
]
