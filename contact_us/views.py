from django.shortcuts import render
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import views, generics
from rest_framework import response, status


from . import models, serializers

# Create your views here.



class SendEmail():

    def send_email(self, request, context, user, subject, template_name):

        # print("email top")
        subject = subject
        # print('Context1: {}'.format(context))
        text_content = render_to_string(template_name+'.txt', context, request=request)
        # print("email middle test {}".format(template_name))
        html_content = render_to_string(template_name+'.html', context, request=request)

        # print("email middle: ")
        from_email = settings.EMAIL_HOST_USER
        # print('Email: {}'.format(from_email))
        # print('Email address: {}'.format(user))
        to = [from_email, ]#to some admin user or recipient 'pickup@mylaundrybucket.com'
        try:
            # print("email try")
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = 'html'

            # send email 
            msg.send(fail_silently=False)

        except:
            # return response.Response({'message': 'Unable to send email at this time please try again later.'})
            return response.Response({'message': 'Unable to send email at this time please try again later.'}, status=status.HTTP_502_BAD_GATEWAY)


class ContactUsView(views.APIView):

    serializer_class = serializers.ContactUsSerializer

    def post(self, request, *args, **kwargs):

        contact_serializer = serializers.ContactUsSerializer(data=request.data)


        if contact_serializer.is_valid():

            user = request.user
            title = contact_serializer.data['title']
            details = contact_serializer.data['details']

            context = ({
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'phone_no': user.phone_no,
            'title': title,
            'details': details,
            
        })


            # email function
            send_mail = SendEmail()
            send_mail.send_email(request, context, user, 'User has made a contact!!!','contact/email_contact_template')
            # self.send_email(request, context, user)
# /Users/carlington/Documents/Point GM Project/MLB/contact_us/template/contact/email_contact_template.html
            return response.Response(contact_serializer.data, status=status.HTTP_201_CREATED)
        else:

            return response.Response({"message" : "Unable to process request. Try again later."}, status=status.HTTP_400_BAD_REQUEST)
    
