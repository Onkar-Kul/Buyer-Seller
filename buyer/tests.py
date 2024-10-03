from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from buyer.models import PurchaseRequest
from rest_framework_simplejwt.tokens import AccessToken


class BuyersAPITestCase(APITestCase):
    def setUp(self):
        # Create a superadmin user
        self.superadmin_user = User.objects.create_user(
            email='superadmin@example.com',
            name='Test User',
            password='password123',
            role='Superadmin',
        )
        self.superadmin_user.is_active = True
        self.superadmin_user.save()

        # Create a buyer user
        self.buyer_user = User.objects.create_user(
            email='buyer@example.com',
            name='Test User Buyer',
            password='password123',
            role='Buyer'
        )
        self.buyer_user.is_active = True
        self.buyer_user.save()

        # Create a buyer user
        self.seller_user = User.objects.create_user(
            email='seller@example.com',
            name='Test User Seller',
            password='password123',
            role='Seller'
        )
        self.seller_user.is_active = True
        self.seller_user.save()

        # Create an access token for the superadmin user
        self.superadmin_token = AccessToken.for_user(self.superadmin_user)
        self.buyer_token = AccessToken.for_user(self.buyer_user)

        # Create a purchase request for testing
        self.purchase_request = PurchaseRequest.objects.create(
            seller=self.seller_user,
            buyer=self.buyer_user,
            description='Test Purchase',
            total_amount=100.00,
            status='In-Process'
        )

    def test_list_buyers_as_superadmin(self):
        url = reverse('buyer-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superadmin_token}')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Buyers retrieved successfully', response.data['message'])
        self.assertIsInstance(response.data['data'], list)

    def test_list_buyers_unauthorized(self):
        url = reverse('buyer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_buyer(self):
        url = reverse('buyer-retrieve-update-delete', kwargs={'pk': self.buyer_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superadmin_token}')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Buyer retrieved successfully', response.data['message'])
        self.assertEqual(response.data['data']['id'], self.buyer_user.id)

    def test_update_buyer(self):
        url = reverse('buyer-retrieve-update-delete', kwargs={'pk': self.buyer_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superadmin_token}')

        response = self.client.put(url, data={
            'email': 'updated_buyer@example.com',
            'name': 'Updated Buyer',
            'role': 'Buyer',
            'is_active': True
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Buyer updated successfully', response.data['message'])
        self.buyer_user.refresh_from_db()
        self.assertEqual(self.buyer_user.email, 'updated_buyer@example.com')

    def test_soft_delete_buyer(self):
        url = reverse('buyer-retrieve-update-delete', kwargs={'pk': self.buyer_user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superadmin_token}')

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Buyer deleted successfully', response.data['message'])
        self.buyer_user.refresh_from_db()
        self.assertFalse(self.buyer_user.is_active)

    def test_create_purchase_request(self):
        url = reverse('buyer-purchase-request')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.buyer_token}')

        response = self.client.post(url, data={
            'seller': self.seller_user.id,
            'description': 'New Purchase Request',
            'total_amount': 150.00
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Purchase Request created successfully', response.data['message'])

    def test_create_purchase_request_validation_errors(self):
        url = reverse('buyer-purchase-request')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.buyer_token}')  # Use stored buyer token

        # Test without seller
        response = self.client.post(url, data={
            'description': 'New Purchase Request',
            'total_amount': 150.00
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field is required.', response.data['seller'])  # Adjusted assertion message

        # Test without description
        response = self.client.post(url, data={
            'seller': self.seller_user.id,
            'total_amount': 150.00
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(any('Description is required.' in str(err) for err in response.data['description']))

        # Test without total_amount
        response = self.client.post(url, data={
            'seller': self.seller_user.id,
            'description': 'New Purchase Request'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(any('Total amount is required.' in str(err) for err in response.data.get('total_amount', [])))

    def test_buyer_dashboard(self):
        url = reverse('buyer-kpi-card')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.buyer_token}')  # Use stored buyer token

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Buyer KPI dashboard retrieved successfully', response.data['message'])
        self.assertIn('total_purchases', response.data['data'])
