from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate

from dj_rest_auth.registration.serializers import RegisterSerializer

from users.models import User, ContactUs


class UserSerializer(serializers.ModelSerializer):
    """
        user serializer
    """
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class RegistrationSerializer(RegisterSerializer):
    """
        registration with allauth, and social login
    """
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=False, write_only=True)
    country = serializers.CharField(required=False, write_only=True)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
    state = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(
        choices=['Male', 'Female', 'Other'],
        style={'base_template': 'radio.html'}
    )
    education = serializers.CharField(write_only=True)
    password1  = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        """
        Validates the password length + authenticity and dob format
        """
        pw  = data.get('password1')
        pw2 = data.get('password2')
        dob = data.get('dob')
        phone = get_user_model().objects.filter(phone__iexact=data.get('phone'))
        if phone.exists():
            raise serializers.ValidationError({
                "errors": _("The phone number already exists.")
            })
        if not dob:
            raise serializers.ValidationError({'dob':'Give us a dob'})
        if pw != pw2:
            raise serializers.ValidationError({'password':'Password must match.'})
        return data

    def get_cleaned_data(self):
        super(RegistrationSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone': self.validated_data.get('phone', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        user.last_name = first_name
        user.last_name = last_name
        user.phone = self.cleaned_data.get('phone')
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'surname', 'state', 'phone', 'address', 'dob', 'total_questions',
        'total_upvotes', 'total_downvotes', 'total_answers', 'ts_rank']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'user', 'device_type', 'subject', 'message', 'spare']