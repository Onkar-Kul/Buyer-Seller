from django.urls import path

from seller.views import SellerListAPIView, SellerRetrieveUpdateDestroyAPIView, SellerDashboardView, \
    SellerPurchaseRequestListView, SellerUpdatePurchaseRequestStatusView

urlpatterns = [
    path('list/', SellerListAPIView.as_view(), name='seller-list'),
    path('seller-kpi-card/', SellerDashboardView.as_view(), name='seller-kpi-card'),
    path('all-sale-request-list/', SellerPurchaseRequestListView.as_view(), name='seller-sale-request-list'),
    path('<int:pk>/', SellerRetrieveUpdateDestroyAPIView.as_view(), name='seller-retrieve-update-delete'),
    path('sale-request-status-update/<int:pk>/', SellerUpdatePurchaseRequestStatusView.as_view(),
         name='seller-sale-request-status-update'),

]
