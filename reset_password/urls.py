from django.urls import path, include
from . import views
from reset_password import views as view_pass
from django.contrib.auth import views as auth_views
from . import serializers



urlpatterns = [
    # users
    # path('reset-password-sent/', view_pass.RestPasswordView.as_view()), #working
    # path('reset-password-sent/', view_pass.RestPasswordView.as_view(),
    # {
        # 'template_name': '../templates/registration/reset_password.html',
        # 'email_template_name': 'email/password_reset/password_reset.txt',
        # 'html_email_template_name': 'email/password_reset/password_reset.html',
        # 'subject_template_name': 'email/password_reset/password_reset_subject.txt'
    # },

    # path('reset-password-sent/', views.SendPassEmail.as_view()),


             # template_name= '../templates/registration/reset_password.html',
            # email_template_name= '../templates/registration/password_reset_email.txt',
            # html_email_template_name = '../templates/registration/password_reset_email.html',
            # subject_template_name= '../templates/registration/password_reset_subject.txt',
             
    path('reset-password-sent/', view_pass.SendPassEmail.as_view()),
    # password_reset_request
    # path('reset-password/<uidb64>/<token>/', view_pass.ResetPasswordConfirmView.as_view(template_name='/templates/registration/password_reset_form.html'),name='password_reset_confirm'),#'
    # path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='../templates/registration/password_reset_complete.html'),name='password_reset_complete'),#
    
    # path("password_reset/", view_pass.password_reset_request, name="password_reset") #email message config

    # path('reset-password-sent/', view_pass.RestPasswordView.as_view()),
    path('reset-password/<uidb64>/<token>', view_pass.ResetPasswordConfirmView.as_view(template_name='../templates/reset/password_reset_form.html'),name='password_reset_confirm'),#template_name='../templates/registration/password_reset_form.html'
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='../templates/reset/password_reset_complete.html'),name='password_reset_complete'),
    
]

