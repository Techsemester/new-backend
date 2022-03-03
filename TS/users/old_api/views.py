import random

from users.api.serializers import (ContactUsSerializer, ProfileSerializer,
                                   RegistrationSerializer)
from users.models import LoginLogoutFail, User, DeviceId, ResetRequests, OtherRequests
from users.notifications import sendEmail
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def logLoginLogoutFail(user, event, device="Non-Mobile"):
    '''
    Log successful logins and logouts and and failed login attempts
    '''
    try:
        if event == 'login':
            logger = LoginLogoutFail(user=user, login=True, device=device, login_time=timezone.now())
        elif event == 'logout':
            logger = LoginLogoutFail(user=user, logout=True, device=device, logout_time=timezone.now())
        elif event == 'fail':
            logger = LoginLogoutFail(user=user, failed_login =True, device=device, failed_login_time=timezone.now())

        logger.save()
        return True
    except Exception as e:
        print("Logggggg off")
        print(e)
        return False



class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page_number': self.page.number,
            'results': data
        })



class RegisterApiView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = RegistrationSerializer
    permission_classes  = []


class UserUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset            = User.objects.all()
    serializer_class    = ProfileSerializer
    parser_class = (FileUploadParser,)

    def get_object(self):
        """
        This handles the issue of pk in the url
        """
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



@api_view(['POST',])
@permission_classes([])
def loginx(request):
    username = request.data.get('username')
    password = request.data.get('password')
    device_id = request.data.get('device_id')

    #Make explicit if the username exists
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        print(e)
        return Response({'message':"Erm, ..we cannot find that username."}, status=status.HTTP_400_BAD_REQUEST)

    if device_id:
        try:
            user = authenticate(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user)
        except Exception as e:
            user = User.objects.get(username='johndoe')
            logLoginLogoutFail(user, 'fail', device_id)
            msg = 'Unable to log in with provided credentials.'
            return Response({'message':msg}, status=status.HTTP_400_BAD_REQUEST)

        #Create DeviceId model for user if it was not around or inactive
        try:
            device = DeviceId.objects.get(user=user, device_id = device_id)
            if device.active == True:
                pass
            else:
                device.active = True
                device.save()
        except DeviceId.DoesNotExist:
            device = DeviceId(user=user, device_id = device_id)
            device.save()
    else:#It's a browser
        try:
            user = authenticate(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user)
            #Log the login
            logLoginLogoutFail(user, 'login')
        except Exception as e:
            print(e)
            msg = 'Unable to log in with provided credentials.'
            return Response({'message':msg}, status=status.HTTP_400_BAD_REQUEST)

    #Logging the login
    if device_id:
        logLoginLogoutFail(user, 'login', device_id)
    else:
        logLoginLogoutFail(user, 'login')
    return Response({
            'message': 'user token and details',
            'token': token.key,
            'user_id': user.pk,
            'user': user.username,
            'phone': user.phone,
            'surname': user.surname,
            'first_name': user.first_name,
        }, status=status.HTTP_200_OK)




@api_view(['POST',])
@permission_classes(())
def token_request(request):
    """
    request token for password reset
    """
    try:
        l_user = request.data["user"] #or email
    except:
        return Response({'message':'No user information received.'}, status=status.HTTP_400_BAD_REQUEST)

    l_user = l_user.lower()

    try:
        user = User.objects.get(username=l_user)
    except:
        try:
            user = User.objects.get(email=l_user)
        except:
            return Response({'message': l_user + ' does not match any record.'}, status=status.HTTP_400_BAD_REQUEST)

    pin = random.randint(0, 1000000)
    try:
        subject = "Password Reset Token."
        sendEmail(user, subject, "Password Reset", otp=pin)

        #Write to use record
        ResetRequests.objects.create(user = user, token = pin, use_case = 'password reset')
        
        #Add password reset request date here
        return Response({'message':'Token sent to registered email.', 'username' : user.username}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message':'We could not send an email', 'error':e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes(())
def password_reset(request):
    #Find user in resetRequests and get their matching reset otp
    try:
        owner = request.data['username']
        otp = request.data['otp']
        new_password = request.data['password']
        confirm_pw = request.data['confirm_password']
    except:
        return Response({'message':"Field(s) missing. Ensure you are passing 'username', 'otp', 'password' and 'confirm_password'"
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=owner)
    except User.DoesNotExist:
        return Response({'message':'Wrong Username.'}, status=status.HTTP_400_BAD_REQUEST)

    #Get token
    qs = ResetRequests.objects.filter(user=user, token=otp)
    if not qs.exists():
        return Response({'message':'Wrong Token.'}, status=status.HTTP_400_BAD_REQUEST)
    token_request = qs.last()

    timer = token_request.created_at

    #Check token expiry
    if timezone.now() > timer + timezone.timedelta(minutes=10):
        return Response({'message':'Token Expired. Request another please.'}, status=status.HTTP_400_BAD_REQUEST)

    if token_request.consumed:
        return Response({"message":"Pin has been used already"}, status=status.HTTP_400_BAD_REQUEST)

    if new_password == "None":
        return Response({"message":"New Password Not Sent"}, status=status.HTTP_400_BAD_REQUEST)
    checker = [line for line in new_password if line.isdigit()] #make a list ints in password to see if they exist
    if not checker:
        raise Exception({"Passsword":"Password must contain a number"})
    elif confirm_pw == "Nada":
        return Response({"message":"Confirm password was not filled"}, status=status.HTTP_400_BAD_REQUEST)
    if new_password != confirm_pw:
        return Response({"message":"Passwords Do not Match"}, status=status.HTTP_400_BAD_REQUEST)
    elif new_password == user.username or len(new_password) < 6:
        return Response({"message":"Password too weak"}, status=status.HTTP_400_BAD_REQUEST)

    #Attempt password reset
    try:
        user.set_password(new_password)
        user.save()
        info = "Your request to rest to reset your password was executed successfully. If this was not done by you, please let us know immediately."
        sendEmail(user, "Your password has been reset Successful.", "Password Reset Successful", information=info)
        return Response({'message':'Password changed!.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message':'Something bad happened.', 'error': e}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def verify_email(request):
    """
    Request token for email validation
    """
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        otp = request.data.get('otp')
        if not otp:
            return Response({'message':"We cannot find your otp"}, status=status.HTTP_400_BAD_REQUEST)

        #Get token
        qs = ResetRequests.objects.filter(user=user, token=otp, use_case = 'users confirmation')
        if not qs.exists():
            return Response({'message':'Wrong Token.'}, status=status.HTTP_400_BAD_REQUEST)

        #Grab the last token
        token_request = qs.last()
        timer = token_request.created_at

        #Check token expiry
        if timezone.now() > timer + timezone.timedelta(minutes=10):
            return Response({'message':'Token Expired. Request another please.'}, status=status.HTTP_400_BAD_REQUEST)

        #Check whether token has been used.
        if token_request.consumed:
            return Response({"message":"Pin has been used already"}, status=status.HTTP_400_BAD_REQUEST)

        if int(otp) == int(token_request.token):
            #Set user as verified
            user.email_verified = True
            user.save()
            #Set token as consumed
            token_request.consumed = True
            token_request.save()

            #Send Confirmation Mail
            email_subject = "SpendWise - Account Verified."
            email_msg = "Your users has been verified. Welcome to the SpendWise Ecosystem"
            try:
                sendEmail(user, email_subject, "Account Verified", information=email_msg)
                return Response({'message':'User users successfully verified.'}, status=status.HTTP_200_OK)
            except:
                return Response({'message':'We could not send a confirmation email'}, status=status.HTTP_200_OK)


    if request.method == 'GET':
        to = User.objects.get(username=request.user).email
        pin = random.randint(0, 1000000)
        #presumes this link is only reachable cos the user already has an email.
        to = user.email
        try:
            subject = "Account Confirmation."
            message = f"Your Account Confirmation code is {pin}\n\nExpires in 10 minutes."
            sendEmail(user, subject, "Account Confirmation", information=message, otp=pin)

            #Write to user's record
            ResetRequests.objects.create(
                user = user,
                token = pin,
                use_case = 'users confirmation'
            )
            #Add password reset request date here
            return Response({'message':'Token sent to registered email.',
                            'email' : to},
            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'We could not send an email', 'error':e},
                status=status.HTTP_400_BAD_REQUEST)

    #Do the actual verification
    #Verified is alrady possibly True via sms. What happens now?


class ChangePassword(APIView):
    """
    Change Customer password API view
    """

    def post(self, request):

        current_password        = request.data.get("current_password", None)
        new_password            = request.data.get("new_password", None)
        confirm_new_password    = request.data.get("confirm_password", None)

        if not current_password:
            return Response({"error" : "Current_password is needed"}, status=status.HTTP_400_BAD_REQUEST)

        if not new_password or not confirm_new_password:
            return Response({"error" : "Confirm Password and New password is needed"}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 6 or not any(letter.isdigit() for letter in new_password):
            return Response({"error" : "Password must be at least 6 characters and must contain a digit"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_new_password:
            return Response({"error" : "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(current_password):
            return Response({"message" : "Password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        #log it
        log = OtherRequests(user=user)
        log.request_type = 'Change Password'
        log.save()
        return Response({"message" : "Password changed!"}, status=status.HTTP_200_OK)

        # checker = [line for line in value if line.isdigit()] #make a list ints in password to see if they exist
        # if not checker:
        #     raise serializers.ValidationError({"Passsword":"Password must contain a number"})


@api_view(['POST',])
@permission_classes(())
def get_username(request):
    """
    request username to be sent to registered email
    """
    try:
        email = request.data["email"]
    except:
        return Response({'message':'No email information received.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except:
        return Response({'message':'No user with this email exists'}, status=status.HTTP_400_BAD_REQUEST)

    #Get username and send to registered email
    subject = "Your SpendWise Username"
    message = f"Your SpendWise username is '{user.username}'"
    sendEmail(user, subject, "Your Username", information=message)

    #Take note
    log = OtherRequests(user=user)
    log.request_type = 'Username Retrieval'
    log.save()
    return Response({'message':'Username sent to the email.'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_profile(request):
    user = request.user.username
    profile = User.objects.get(username=user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def contact_us(request):
    data = request.data
    data['user'] = request.user.id
    serializer = ContactUsSerializer(data=request.data)
    serializer.is_valid(True)
    serializer.save()
    return Response({'message':'We got your message!'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_phone_email(request):
    user = request.user

    phone = request.data.get("phone")
    email = request.data.get("email")

    if not phone and not email:
        return Response({'message':"We got neither a phone no or email"}, status=status.HTTP_404_NOT_FOUND)

    if phone and email:
        if email != user.email:
            user.email = email
            user.email_verified = False
        if phone != user.phone:
            user.phone = phone
            user.phone_verified = False
        user.save()
        return Response({'message':'Phone number and email updated!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def profile_pic(request):
    user = request.user
    image = request.data['image']
    user.image = image
    user.save()
    return Response({'message':f'Profile pic updated {user.username}!'}, status=status.HTTP_200_OK)
