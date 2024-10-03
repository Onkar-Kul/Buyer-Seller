from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from buyer.models import PurchaseRequest
from rest_framework_simplejwt.tokens import RefreshToken


class SellerAPITestCase(APITestCase):

    def setUp(self):
        # Create a superadmin user
        self.superadmin_user = User.objects.create_user(
            email='superadmin@example.com', name='Super Admin', password='password', role='Superadmin'
        )
        # Create a seller user
        self.seller_user = User.objects.create_user(
            email='seller@example.com', name='Seller User', password='password', role='Seller'
        )
        # Create a buyer user
        self.buyer_user = User.objects.create_user(
            email='buyer@example.com', name='Buyer User', password='password', role='Buyer'
        )
        # Create purchase requests
        self.purchase_request = PurchaseRequest.objects.create(
            buyer=self.buyer_user,
            seller=self.seller_user,
            description='Test Purchase Request',
            total_amount=500.0,
            status='In-Process'
        )

        # Generate tokens for users
        self.superadmin_token = str(RefreshToken.for_user(self.superadmin_user).access_token)
        self.seller_token = str(RefreshToken.for_user(self.seller_user).access_token)

    def authenticate(self, user_token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')


class SellerListAPIViewTest(SellerAPITestCase):

    def test_seller_list_superadmin(self):
        """
        Ensure the superadmin can list all sellers.
        """
        self.authenticate(self.superadmin_token)
        url = reverse('seller-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Sellers retrieved successfully")
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_seller_list_unauthorized(self):
        """
        Ensure unauthorized access is denied for listing sellers.
        """
        url = reverse('seller-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SellerRetrieveUpdateDestroyAPIViewTest(SellerAPITestCase):

    def test_seller_retrieve_superadmin(self):
        """
        Ensure the superadmin can retrieve a seller.
        """
        self.authenticate(self.superadmin_token)
        url = reverse('seller-retrieve-update-delete', kwargs={'pk': self.seller_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Seller retrieved successfully")
        self.assertEqual(response.data['data']['email'], self.seller_user.email)

    def test_seller_update_superadmin(self):
        """
        Ensure the superadmin can update a seller.
        """
        self.authenticate(self.superadmin_token)
        url = reverse('seller-retrieve-update-delete', kwargs={'pk': self.seller_user.id})
        response = self.client.put(url, data={'name': 'Updated Seller', 'email': self.seller_user.email,
                                              'role': 'Seller'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Seller')
        self.assertEqual(response.data['message'], "Seller updated successfully")

    def test_seller_delete_superadmin(self):
        """
        Ensure the superadmin can soft-delete a seller.
        """
        self.authenticate(self.superadmin_token)
        url = reverse('seller-retrieve-update-delete', kwargs={'pk': self.seller_user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Seller deleted successfully")

    def test_seller_retrieve_unauthorized(self):
        """
        Ensure unauthorized access is denied for retrieving a seller.
        """
        url = reverse('seller-retrieve-update-delete', kwargs={'pk': self.seller_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SellerPurchaseRequestListViewTest(SellerAPITestCase):

    def test_seller_purchase_request_list(self):
        """
        Ensure the seller can view their purchase requests.
        """
        self.authenticate(self.seller_token)
        url = reverse('seller-sale-request-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['buyer']['email'], self.buyer_user.email)

    def test_seller_purchase_request_list_unauthorized(self):
        """
        Ensure unauthorized access is denied for listing purchase requests.
        """
        url = reverse('seller-sale-request-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SellerUpdatePurchaseRequestStatusViewTest(SellerAPITestCase):

    def test_update_purchase_request_status(self):
        """
        Ensure the seller can update the status of their purchase requests.
        """
        self.authenticate(self.seller_token)
        url = reverse('seller-sale-request-status-update', kwargs={'pk': self.purchase_request.id})
        response = self.client.patch(url, data={'status': 'Approved'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Sale Request status updated successfully')
        self.purchase_request.refresh_from_db()
        self.assertEqual(self.purchase_request.status, 'Approved')

    def test_update_purchase_request_status_invalid(self):
        """
        Ensure invalid status updates return an error.
        """
        self.authenticate(self.seller_token)
        url = reverse('seller-sale-request-status-update', kwargs={'pk': self.purchase_request.id})
        response = self.client.patch(url, data={'status': 'InvalidStatus'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('"InvalidStatus" is not a valid choice.', str(response.data))

    def test_update_purchase_request_status_unauthorized(self):
        """
        Ensure unauthorized access is denied for updating purchase request status.
        """
        url = reverse('seller-sale-request-status-update', kwargs={'pk': self.purchase_request.id})
        response = self.client.patch(url, data={'status': 'Approved'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
