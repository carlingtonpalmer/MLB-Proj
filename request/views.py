from django.shortcuts import render
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import views, generics
from rest_framework import response, status


from . import models, serializers

# Create your views here.



class SendEmail():
    # recipient email func
    def to_email(self, subject, text_content, from_email, to_user, html_content):
        to = [to_user]#to some admin user or recipient pickup@mylaundrybucket.com
        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = 'html'

            # send email 
            msg.send(fail_silently=False)
        except:
            return response.Response({'message': 'Unable to send email at this time please try again later.'}, status=status.HTTP_502_BAD_GATEWAY)
    
    # send email
    def send_email(self, request, context, user, subject, template_name):

        
        subject = subject
        text_content = render_to_string(template_name+'.txt', context, request=request)
        html_content = render_to_string(template_name+'.html', context, request=request)

        from_email = settings.EMAIL_HOST_USER
        to = from_email
        if(template_name == 'request/email_request_template'):
            self.to_email(subject, text_content, from_email, to, html_content)
            
        else:
            user_email = str(request.user)
            self.to_email(subject, text_content, from_email, user_email, html_content)


class RequestView(views.APIView):

    serializer_class = serializers.RequestSerializer

    # send user a confirmation email
    def user_comfirm_email(self, request, context, user):
        send_mail = SendEmail()
        send_mail.send_email(request, context, user, 'Requesting Pickup Confirmation','request/email_confirmation_template')

    # send request to admin mlb team    
    def post(self, request, *args, **kwargs):

        request_serializer = serializers.RequestSerializer(data=request.data)


        if request_serializer.is_valid():

            user = request.user
            request_type = request_serializer.data['request_type']
            pickup = request_serializer.data['pickup']
            dropoff = request_serializer.data['dropoff']

            context = ({
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'phone_no': user.phone_no,
            'request_type': request_type,
            'pickup': pickup,
            'dropoff': dropoff,
        })


            # email function
            send_mail = SendEmail()
            send_mail.send_email(request, context, user, 'Requesting pickup!!!','request/email_request_template')
            self.user_comfirm_email(request, context, user) #send email to user
            # self.send_email(request, context, user)

            return response.Response(request_serializer.data, status=status.HTTP_201_CREATED)
        else:

            return response.Response({"message" : "Unable to process request. Try again later."}, status=status.HTTP_400_BAD_REQUEST)
    
