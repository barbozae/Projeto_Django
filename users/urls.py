from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import register


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path(
        'password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='users/password_change.html', 
             success_url='/password_change_done/'
             ),
             name='password_change'),
    path(
        'password_change_done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
            ),
            name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]