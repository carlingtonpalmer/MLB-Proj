from rest_framework import generics
from django.contrib.auth import views as auth_views

# reset password
from rest_auth import views as rest_view
from . import serializers
from rest_framework import response, status


# newly imported
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# just for reset password override
# from django.core.urlresolvers import reverse


# Create your views here.

class RestPasswordView(rest_view.PasswordResetView):

	
    pass
    # def test():
    #     # html_email_template_name="../templates/registration/password_reset_email1.html"
    #     email_template_name='../templates/registration/password_reset_email.txt'
    #     # email_template_name = "main/password/password_reset_email.txt"
class SendPassEmail(rest_view.PasswordResetView): #rest_view.PasswordResetView
	
	def password_reset(request, is_admin_site=False,
                #    template_name='registration/password_reset_form.html',
                   email_template_name='../templates/registration/password_reset_email.html',
                   subject_template_name='../templates/registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name='../templates/registration/password_reset_email.html'):
		if post_reset_redirect is None:
			post_reset_redirect = reverse('password_reset_done')
		else:
			post_reset_redirect = resolve_url(post_reset_redirect)
		if request.method == "POST":
			form = password_reset_form(request.POST)
			if form.is_valid():
				opts = {
					'use_https': request.is_secure(),
					'token_generator': token_generator,
					'from_email': from_email,
					'email_template_name': email_template_name,
					'subject_template_name': subject_template_name,
					'request': request,
					'html_email_template_name': html_email_template_name,
				}
				if is_admin_site:
					opts = dict(opts, domain_override=request.get_host())
				form.save(**opts)
				return HttpResponseRedirect(post_reset_redirect)
		else:
			form = password_reset_form()
		context = {
			'form': form,
			'title': _('Password reset'),
		}
		if extra_context is not None:
			context.update(extra_context)
		return TemplateResponse(request, template_name, context,
								current_app=current_app)

	# pass
    # def password_reset_request(request):

    #     if request.method == "POST":
    #     # 	password_reset_form = PasswordResetForm(request.POST)
    #         print('testing')
    #     return response.Response({"message":'test'}, status=status.HTTP_200_OK)
		# return response.Response({"message": 'Test'}, status=status.HTTP_400_BAD_REQUEST)
			# if password_reset_form.is_valid():
			
				# data = password_reset_form.cleaned_data['email']
	# 		associated_users = User.objects.filter(Q(email=data)|Q(username=data))
	# 		if associated_users.exists():
	# 			for user in associated_users:
	# 				subject = "Password Reset Requested"
	# 				email_template_name = "main/password/password_reset_email.txt"
	# 				c = {
	# 				"email":user.email,
	# 				'domain':'127.0.0.1:8000',
	# 				'site_name': 'Website',
	# 				"uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
	# 				"user": user,
	# 				'token': default_token_generator.make_token(user),
	# 				'protocol': 'http',
	# 				}
	# 				email = render_to_string(email_template_name, c)
	# 				try:
	# 					send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
	# 				except BadHeaderError:
	# 					return HttpResponse('Invalid header found.')
	# 				return redirect ("/password_reset/done/")
	# password_reset_form = PasswordResetForm()
	# # return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})
	# return render(request=request, template_name="../templates/registration/password_reset_sent.html", context={"password_reset_form":password_reset_form})
    
class ChangePasswordView(rest_view.PasswordChangeView):
    pass

# class ResetPasswordConfirmView(rest_view.PasswordResetConfirmView):
#     pass

class ResetPasswordConfirmView(auth_views.PasswordResetConfirmView):
    pass

class ResetPasswordCompleteView(auth_views.PasswordResetCompleteView):
    pass

