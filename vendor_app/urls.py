from django.urls import path
from .views import vendor, purchase, auth
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('vendors/', view=vendor.Vendors.as_view({'get':'get'}), name='vendorsView'),
    path('vendors/<str:id>', view=vendor.Vendors.as_view({'get':'get'}), name='vendorsView'),
    path('vendors/<str:id>/performance', view=vendor.Vendors.as_view({'get' : 'get'}), name='vendorsView'),
    path('vendors/<str:id>/purchase_orders', view=vendor.Vendors.as_view({'get' : 'get_purchases'}), name='vendorsView'),
    path('purchase_orders/', view=purchase.PurchaseOrders.as_view(), name='purchaseOrdersView'),
    path('purchase_orders/<str:po_number>', view=purchase.PurchaseOrders.as_view(), name='purchaseOrdersView'),
    path('register/', auth.register, name='registerView'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist')
]