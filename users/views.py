from django.shortcuts import render
from users import serializers, models, permissions
from rest_framework import viewsets, filters,generics, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import response
from rest_framework import status #, viewsets
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from random import randint
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from datetime import datetime
import re





# Create your views here.


class UserViewset(generics.ListAPIView):
    """ this class is use for creating and updating users """

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all() # just tell django we gonna use CREATE, UPDATE, RETRIEVE LIST ETC.
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.ModifyOwnProfile,)
    permission_classes = [IsAuthenticated]
    # filter_backends = (filters.SearchFilter, )
    # search_fields = ('email', 'first_name', 'last_name',)
    # token, created = Token.objects.get_or_create(user=user)
    # response.Response({"token": token.key})
    
class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.User.objects.all()
    permission_classes = (permissions.ModifyOwnProfile,)

class Register(views.APIView):

    permission_classes = [AllowAny]


    def post(self, request, *args, **kwargs):

        loginObj = LoginUserApiView()
        if request.method == 'POST':
            serializer = serializers.UserSerializer(data=request.data)
            
            if serializer.is_valid():
                # print('User: {}'.format(serializer))
                user = serializer.save()
                # user = models.User.objects.create_user(
                #     serializer.validated_data['first_name'],
                #     serializer.validated_data['last_name'],
                #     serializer.validated_data['email'],
                #     serializer.validated_data['password'],
                #     # serializer.validated_data['provider'], 
                # )
                token = Token.objects.create(user=user)
                signup_date = loginObj.getRegisterDate(user.date_joined)
                return response.Response(
                    {
                    'id': user.id,#serializer.data.get('id'),
                    'first_name': user.first_name,#serializer.data.get('first_name'),
                    'last_name' : user.last_name,#serializer.data.get('last_name'),
                    'email' : user.email,#serializer.data.get('email'),
                    'token': token.key,
                    'phone_no': user.phone_no,
                    'provider': user.provider,
                    'date_joined': signup_date,
                },
                status=status.HTTP_201_CREATED
                )
            return response.Response({'message': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class SocialLogin(views.APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        loginObj = LoginUserApiView()

        if request.method == 'POST':
            serializer = serializers.UserSocialSerializer(data=request.data)
            # print('Test')
            user_queryset = models.User.objects.all()
            data = request.data
            email = data.get('email')
            password = data.get('email')

            if serializer.is_valid():

                # print('Ser: {}'.format(serializer))
                
                user = serializer.save()
                # user = models.User.objects.create(
                #     serializer.validated_data['first_name'],
                #     serializer.validated_data['last_name'],
                #     serializer.validated_data['email'],
                #     serializer.validated_data['provider'], 
                #     password = serializer.validated_data['password'],
                # )
                # print('User Test: {}'.format(user))
                # print('Provider: {}'.format(user.provider))
                # print('Email: {}'.format(user.email))
                token = Token.objects.create(user=user)
                signup_date = loginObj.getRegisterDate(user.date_joined)
                return response.Response(
                    {
                    'id': user.id,#serializer.data.get('id'),
                    'first_name': user.first_name,#serializer.data.get('first_name'),
                    'last_name' : user.last_name,#serializer.data.get('last_name'),
                    'email' : user.email,#serializer.data.get('email'),
                    'token': token.key,
                    'phone_no': user.phone_no,
                    'provider': user.provider,
                    'date_joined': signup_date,
                },
                status=status.HTTP_201_CREATED
                )
            # else:
            elif user_queryset.filter(email=email).exists():

                # print('test')
                # print('email: {}'.format(email))
                # print('pass: {}'.format(password))
                user = auth.authenticate(username=email, password=password)
                # print('User: {}'.format(user))
                # print('pass: {}'.format(user))
                if user is not None:
                    # print('pass1')
                    token, created = Token.objects.get_or_create(user=user)
                    signup_date = loginObj.getRegisterDate(user.date_joined)
                    return response.Response(
                    {
                        'id': user.id,#serializer.data.get('id'),
                        'first_name': user.first_name,#serializer.data.get('first_name'),
                        'last_name' : user.last_name,#serializer.data.get('last_name'),
                        'email' : user.email,#serializer.data.get('email'),
                        'token': token.key,
                        'phone_no': user.phone_no,
                        'provider': user.provider,
                        'date_joined': signup_date,
                    },
                    status=status.HTTP_200_OK
                    )
                else:
                    return response.Response({'message': 'Unable to authenticate user.'},status=status.HTTP_400_BAD_REQUEST)

            else:
                return response.Response({'message': serializer.errors},status=status.HTTP_404_NOT_FOUND)
        else:
            return response.Response({'message': 'Invalid request.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
  
class LoginUserApiView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def getRegisterDate(self, signup_date):
        # format date
        old_dt_format = '%Y-%m-%d %H:%M:%S'
        new_dt_format = "%Y-%m-%d"
        dt_joined_str = str(signup_date)
        regx_dt_str = re.compile(re.escape('.')+'.*') # remove everything after '.'
        mod_dt_joined_str = regx_dt_str.sub('', dt_joined_str) #set blank after get text the desire text
        format_dt_joined_str = datetime.strptime(mod_dt_joined_str, old_dt_format).strftime(new_dt_format) #format time 

        return format_dt_joined_str

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # signup_date = str()
        signup_date = self.getRegisterDate(user.date_joined)
        # format date
        # old_dt_format = '%Y-%m-%d %H:%M:%S'
        # new_dt_format = "%Y-%m-%d %H:%M"
        # dt_joined_str = str(user.date_joined)
        # regx_dt_str = re.compile(re.escape('.')+'.*') # remove everything after '.'
        # mod_dt_joined_str = regx_dt_str.sub('', dt_joined_str) #set blank after get text the desire text
        # format_dt_joined_str = datetime.strptime(mod_dt_joined_str, old_dt_format).strftime(new_dt_format) #format time 

        
     
        # print('date join: {}'.format(format_dt_joined_str))


        token, created = Token.objects.get_or_create(user=user)
        return response.Response({
              'id': user.id,
              'first_name': user.first_name,
              'last_name' : user.last_name,
              'email' : user.email,
              'token': token.key,
              'provider': user.provider,
              'date_joined': signup_date,#user.date_joined,
        })

class LogoutUserView(views.APIView):

    permission_classes = [AllowAny]

    def post(self, request,*args, **kwargs):
        logout(request)
        return response.Response(
            {
                "message" : "User was logged out successfully."
            },
            status=status.HTTP_200_OK

        )

class SendEmail():

    def send_email(self, request, context, user, subject, template_name):

        # print("email top")
        subject = subject
        # print('Context1: {}'.format(context))
        text_content = render_to_string(template_name+'.txt', context, request=request)
        print("email middle test")
        html_content = render_to_string(template_name+'.html', context, request=request)

        # print("email middle: ")
        from_email = settings.EMAIL_HOST_USER
        # print('Email: {}'.format(from_email))
        # print('Email address: {}'.format(user))
        to = [user, ]#to some admin user
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

class ConfirmEmailView(views.APIView):
    serializer_class = serializers.ConfirmEmailSerializer
    permission_classes = [AllowAny]

    def generater(self):
        """ generate random code verification code """
        list_no = []
        for rand in range(6):
            random_no = randint(0,6)
            list_no.append(random_no)
            print("Random: {}".format(rand))
        
        print("Random List: {}".format(list_no))

        return list_no

    

    
    def post(self, request, *args, **kwargs):
        serializer_class = serializers.ConfirmEmailSerializer(data=request.data,)
        code_serializer = serializers.ConfirmEmailCodeSerializer
        queryset = models.ConfirmEmail.objects.all()
        user_queryset = models.User.objects.all()


        # user = request.user
        if serializer_class.is_valid():
            user = serializer_class.data.get('user')


            code = self.generater()
            string = ''.join(map(str, code)) 
            print(code_serializer)
            context = {
                'user': user,
                "string": string 
            }

            if not queryset.filter(user=user).exists() and not user_queryset.filter(email=user):
                models.ConfirmEmail.objects.create(user=user, code=string)
                send_mail = SendEmail()
                send_mail.send_email(request, context, user, 'Verify user account.','users/email_confirm_template')

            elif user_queryset.filter(email=user):
                return response.Response({"message": "User already a registered."}, status=status.HTTP_403_FORBIDDEN)

            else:

                return response.Response({'message': 'Code was already sent to user.'}, status=status.HTTP_403_FORBIDDEN)

        else:
            return response.Response({'message': 'Invalid email. Please enter a valid email.'}, status=status.HTTP_400_BAD_REQUEST)


        return response.Response({'message': 'Confirmation code sent.'}, status=status.HTTP_200_OK)

class ConfirmEmailCodeView(views.APIView):
    serializer_class = serializers.ConfirmEmailCodeSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        code_serializer = serializers.ConfirmEmailCodeSerializer(data=request.data)
        queryset = models.ConfirmEmail.objects.all()

        if code_serializer.is_valid():
            ser_user = code_serializer.data.get('user')
            ser_code = code_serializer.data.get('code')

            # user = request.user
            
            if not queryset.filter(user=ser_user, code=ser_code).exists():
                return response.Response({'message': 'Code invalid try again.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                queryset.filter(user=ser_user).delete()
                return response.Response({'message': 'Code accepted. Email was verified succesfully.'}, status=status.HTTP_200_OK)

        else:

            # return response.Response({'message': 'Invalid user input.'})
            return response.Response(code_serializer.errors)

