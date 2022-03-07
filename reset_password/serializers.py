from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate

# reset password
from rest_auth import serializers as rest_serializer
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

UserModel = get_user_model()

# this class is need to keep the html email
class ResetPasswordSerializer(rest_serializer.PasswordResetSerializer):
    # pass
    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'email_template_name': '../templates/registration/password_reset_email.txt',
            'html_email_template_name': '../templates/registration/password_reset_email.html', #override to set html email
            'request': request,
        }
        self.reset_form.save(**opts)


# class ChangePasswordSerializer(rest_serializer.PasswordChangeSerializer):
    # pass

# class TestConfirmSerializer(rest_serializer.PasswordResetConfirmSerializer):

#    pass