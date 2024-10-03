from django.urls import path

from buyer.views import BuyersListAPIView, BuyerRetrieveUpdateDestroyAPIView, PurchaseRequestListCreateAPIView, \
    BuyerDashboardView

urlpatterns = [
    path('list/', BuyersListAPIView.as_view(), name='buyer-list'),
    path('<int:pk>/', BuyerRetrieveUpdateDestroyAPIView.as_view(), name='buyer-retrieve-update-delete'),
    path('purchase-request/', PurchaseRequestListCreateAPIView.as_view(), name='buyer-purchase-request'),
    path('kpi-card/', BuyerDashboardView.as_view(), name='buyer-kpi-card'),


]
