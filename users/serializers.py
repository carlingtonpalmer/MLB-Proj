from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    """ use to serialze a user model or object"""
    #when using modelserializer you use meta class to configure the serializer to point to a specific model

    class Meta:
        model = models.User
        fields = ['id','first_name', 'last_name', 'email', 'password', 'phone_no', 'provider','date_joined']

        extra_kwargs = {
            'password' : {
                'write_only': True,
                'style' : {'input_type' : 'password'}
                }
        }

    def create(self, validated_data):
        """ override this create default user function to use the custom create_user method from user manager.
        One of the reason for this to ensure that password is hash etc """

        user = models.User.objects.create_user(
            validated_data['first_name'],
            validated_data['last_name'],
            validated_data['email'],
            validated_data['provider'], 
            password = validated_data['password'],            

        )
        user = models.User.objects.filter(pk=user.id).first()
        
        return user


class UserSocialSerializer(serializers.ModelSerializer):
    """ use to serialze a user model or object"""
    #when using modelserializer you use meta class to configure the serializer to point to a specific model

    class Meta:
        model = models.User
        fields = ['id','first_name', 'last_name', 'email', 'password', 'phone_no', 'provider','date_joined']

        extra_kwargs = {
            'password' : {
                'write_only': True,
                'style' : {'input_type' : 'password'}
                }
        }

    def create(self, validated_data):
        """ override this create default user function to use the custom create_user method from user manager.
        One of the reason for this to ensure that password is hash etc """

        user = models.User.objects.create_user(
            validated_data['first_name'],
            validated_data['last_name'],
            validated_data['email'],
            validated_data['provider'], 
            password = validated_data['password'],            

        )
        user = models.User.objects.filter(pk=user.id).first()
        
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('email', 'password')



class UserUpdateSerializer(serializers.ModelSerializer):
    """ Allow a single user to update profile """

    class Meta:
        model = models.User
        fields = ['id','first_name', 'last_name', 'email', 'phone_no','date_joined']
        read_only_fields = ['id','first_name', 'last_name', 'email', 'date_joined']
        
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

         # return the user model
        user = models.User.objects.filter(pk=user.id).first()

        return user


class ConfirmEmailSerializer(serializers.ModelSerializer):
    """ use as a email serialize to send email """
    class Meta:
        model = models.ConfirmEmail
        fields = ('user',)

class ConfirmEmailCodeSerializer(serializers.ModelSerializer):
    """ use to confirm code sent to user with the assigned email address """
    class Meta:
        model = models.ConfirmEmail
        fields = ('user','code')

