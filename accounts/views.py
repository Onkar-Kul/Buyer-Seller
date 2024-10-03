from django.contrib.auth import authenticate
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserCreateSerializer, UserLoginSerializer


# Create your views here.
# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrations(APIView):
    """
        API view for user registration.

        This view handles the registration of new users by processing a POST request
        with user details and creating a new user if the data is valid.
    """

    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
        API view for user login.

        This view handles the user login by processing a POST request with email and password,
        authenticating the user, and returning a token if authentication is successful.

    """

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        """
            Args:
                request (Request): The request object containing the user credentials.

            Returns:
                Response: A response containing the authentication token and a success message
                with status code 200 if login is successful. Otherwise, a response with an error
                message and status code 404 is returned.

            Raises:
                ValidationError: If the data provided is invalid.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'msg': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure the user is authenticated
def get_current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
    })
