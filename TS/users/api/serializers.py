import ast
import json
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate

from dj_rest_auth.registration.serializers import RegisterSerializer

from users.models import *


class UserSerializer(serializers.ModelSerializer):
    """
        user serializer
    """
    state = serializers.SerializerMethodField('get_state_details')
    country = serializers.SerializerMethodField('get_country_details')

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def get_country_details(self, obj):
        country = CountrySerializers(obj.country)
        return country.data

    def get_state_details(self, obj):
        serializer = StateOnlyRetrieveSerializers(obj.state)
        return serializer.data

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


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Incorrect credential')
            raise exceptions.ValidationError({
                "errors": msg
            })

        return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = get_user_model().objects.get(email__iexact=email).get_username()
                except get_user_model().DoesNotExist:
                    pass

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('This account has been suspended, contact admin to proceed.')
                raise exceptions.ValidationError({
                    "errors": msg
                })

        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError({
                "errors": msg
            })

            # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError({
                        "errors": _('Please verify your email before you can login')
                    })

        attrs['user'] = user
        return attrs


class RegistrationSerializer(RegisterSerializer):
    """
        registration with allauth, and social login
    """
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    username = serializers.CharField(required=True, write_only=True)
    country = serializers.IntegerField(write_only=True, required=False)
    state = serializers.IntegerField(write_only=True, required=False)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    phone = serializers.CharField(required=True, write_only=True)
    address = serializers.CharField(write_only=True, required=False)
    city = serializers.CharField(write_only=True, required=False)
    dob = serializers.CharField(write_only=True, required=False)
    gender = serializers.ChoiceField(
        choices=['Male', 'Female', 'Other'],
        style={'base_template': 'radio.html'},
        required=False
    )
    education = serializers.CharField(write_only=True, required=False)
    password1  = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        """
        Validates the password length + authenticity and dob format
        """
        pw  = data.get('password1')
        pw2 = data.get('password2')
        city = data.get('city')
        dob = data.get('dob')

        phone = get_user_model().objects.filter(phone=data.get('phone'))
        if phone.exists():
            raise serializers.ValidationError({
                "errors": _("The phone number already exists.")
            })
        if len(data.get('phone')) < 9:
            raise serializers.ValidationError({'errors': 'Incorrect phone number, check and retry'})
        if len(data.get('phone')) > 11:
            raise serializers.ValidationError({'errors': 'You have exceeded the amount number'})
        if len(city) > 100:
            raise serializers.ValidationError({'errors': 'You have exceeded the character limit'})
        if len(dob) > 25:
            raise serializers.ValidationError({'errors': 'Maximum is about 25 characters'})
        if pw != pw2:
            raise serializers.ValidationError({'errors': 'Password must match.'})
        return data

    def get_cleaned_data(self):
        super(RegistrationSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
            'full_name': self.validated_data.get('full_name', ''),
            # 'first_name': self.validated_data.get('first_name', ''),
            # 'last_name': self.validated_data.get('last_name', ''),
            'dob': self.validated_data.get('dob', ''),
            'phone': self.validated_data.get('phone', ''),
            'country': self.validated_data.get('state', ''),
            'state': self.validated_data.get('state', ''),
            'city': self.validated_data.get('city', ''),
            'gender': self.validated_data.get('gender', ''),
            'address': self.validated_data.get('address', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        # first_name = self.cleaned_data.get('first_name')
        # last_name = self.cleaned_data.get('last_name')
        full_name = self.cleaned_data.get('full_name')
        username = self.cleaned_data.get('username')
        country = Countries.objects.filter(id=self.cleaned_data.get('country')).first()
        state = StateProvidence.objects.filter(id=self.cleaned_data.get('state')).first()
        # user.last_name = first_name
        # user.last_name = last_name
        user.full_name = f"{full_name}"
        user.username = f"{username}"
        user.dob = self.cleaned_data.get('dob')
        user.gender = self.cleaned_data.get('gender')
        user.city = self.cleaned_data.get('city')
        user.phone = self.cleaned_data.get('phone')
        user.country = country
        user.state = state
        user.address = self.cleaned_data.get('address')
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


class CountryStateSerializers(serializers.ModelSerializer):
    """
        Retrieve countries and states
    """
    regions = serializers.SerializerMethodField('get_regions')

    class Meta:
        model = Countries
        fields = ['id', 'flag', 'dial', 'title', 'code', 'regions']

    def get_regions(self, obj):
        serializer = StateProvidence.objects.filter(country__exact=obj.id).values('id', 'country', 'name')
        return serializer


class CountrySerializers(serializers.ModelSerializer):

    class Meta:
        model = Countries
        fields = ['id', 'flag', 'dial', 'title', 'code']


class StateOnlyRetrieveSerializers(serializers.ModelSerializer):
    """
        retrieve all class for state
    """
    class Meta:
        model = StateProvidence
        fields = ['id', 'country', 'name']