from rest_framework.response import Response
from vendor_app.Serializers import VendorSerializer, PurchaseOrderSerializer
from rest_framework.views import APIView
from vendor_app.models import Vendor, PurchaseOrder
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.viewsets import ViewSet
    
class Vendors(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format = None, **kwargs):
        if 'id' in kwargs:
            vendor = Vendor.objects.get(vendor_code=self.kwargs['id'])
            serializer = VendorSerializer(vendor)
        else:
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            
        return Response(serializer.data)
    
    def get_purchases(self, request, format=None, **kwargs):
        vendor = Vendor.objects.get(vendor_code=kwargs['id'])
        purchases = PurchaseOrder.objects.filter(vendor=vendor)
        serializer = PurchaseOrderSerializer(purchases, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def put(self, request, format=None, **kwargs):
        vendor = Vendor.objects.get(vendor_code=kwargs['id'])
        serializer = VendorSerializer(instance=vendor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, format=None, **kwargs):
        vendor = Vendor.objects.get(vendor_code=self.kwargs['id'])
        vendor.delete()
        return Response()