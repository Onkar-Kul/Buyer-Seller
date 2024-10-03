from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User


class UserRegistrationTests(APITestCase):
    """
    Test case for user registration.
    """

    def setUp(self):
        self.registration_url = reverse('user-registration')

    def test_user_registration_success(self):
        """
        Test successful user registration.
        """
        data = {
            'email': 'testuser@yopmail.com',
            'name': 'Test User',
            'role': 'Buyer',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['msg'], 'Registration Successful')

        # Verify that the user was created
        user = User.objects.get(email=data['email'])
        self.assertIsNotNone(user)

    def test_user_registration_failure_email_exists(self):
        """
        Test registration failure if email already exists.
        """
        User.objects.create_user(email='testuser@yopmail.com', role='Buyer', password='testpass123', password2='testpass123',
                                 name='Test User')
        data = {
            'email': 'testuser@yopmail.com',
            'name': 'Another Test User',
            'role': 'Buyer',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user with this email address already exists.', response.data['email'])

    def test_user_registration_failure_password_mismatch(self):
        """
        Test registration failure if password and password2 do not match.
        """
        data = {
            'email': 'mismatched@yopmail.com',
            'name': 'Mismatched User',
            'role': 'Buyer',
            'password': 'testpass123',
            'password2': 'differentpass123',  # Different password
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check for non-field errors related to password mismatch
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'], ["Password and Confirm Password doesn't match"])

    def test_user_registration_failure_invalid_data(self):
        """
        Test registration failure with invalid data (e.g., invalid email format).
        """
        data = {
            'email': 'invalidemail',  # Invalid email
            'name': 'Invalid User',
            'role': 'Buyer',
            'password': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], ['Enter a valid email address.'])

    def test_user_registration_failure_empty_inputs(self):
        """
        Test registration failure with empty fields.
        """
        data = {
            'email': '',
            'name': '',
            'role': '',
            'password': '',
            'password2': '',
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('email', response.data)
        self.assertIn('This field may not be blank.', response.data['email'])

        self.assertIn('name', response.data)
        self.assertIn('This field may not be blank.', response.data['name'])

        self.assertIn('role', response.data)
        self.assertEqual(response.data['role'], ['"" is not a valid choice.'])

        self.assertIn('password', response.data)
        self.assertIn('This field may not be blank.', response.data['password'])

        self.assertIn('password2', response.data)
        self.assertIn('This field may not be blank.', response.data['password2'])


class UserLoginTests(APITestCase):
    """
    Test case for user login.
    """

    def setUp(self):
        self.login_url = reverse('user-login')
        self.user_data = {
            'email': 'testuser@yopmail.com',
            'password': 'testpass123',
            'role': 'Buyer',
            'name': 'Test User',
        }
        # Create a user for login tests
        self.user = User.objects.create_user(**self.user_data)

    def test_user_login_success(self):
        """
        Test successful user login.
        """
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['msg'], 'Login Success')

    def test_user_login_failure_invalid_credentials(self):
        """
        Test login failure with invalid credentials.
        """
        data = {
            'email': 'wronguser@yopmail.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('non_field_errors', response.data['errors'])
        self.assertEqual(response.data['errors']['non_field_errors'], ['Email or Password is not Valid'])

    def test_user_login_failure_missing_fields(self):
        """
        Test login failure with missing email and password.
        """
        data = {
            'email': '',
            'password': '',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)

        self.assertIn('This field may not be blank.', response.data['email'])
        self.assertIn('This field may not be blank.', response.data['password'])
