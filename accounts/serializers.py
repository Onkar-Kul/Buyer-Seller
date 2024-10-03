from rest_framework import serializers

from accounts.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """
        This Serializer used for registering a new user.

        This serializer handles user creation with email, name, password, and password confirmation.
        It ensures that the password and password confirmation match before creating the user.

        Attributes:
            email: Email of user
            name: Full name of user
            role: User's Role
            password: user's password
            password2 (str): Confirmation of the user's password.

    """
    password2 = serializers.CharField(write_only=True, max_length=255)

    class Meta:
        model = User
        fields = ['email', 'name', 'role', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """
                validate method for the password and password confirmation match.

                Args:
                    attrs (dict): The data passed for validation.

                Returns:
                    dict: The validated data.

                Raises:
                    serializers.ValidationError: If the passwords do not match.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return super(UserCreateSerializer, self).validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
           This Serializer user authentication.

           This serializer used for user login.

           Attributes:
               email: Email of user
               password: user's password

       """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']
