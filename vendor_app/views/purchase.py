from rest_framework.views import APIView
from vendor_app.models import PurchaseOrder
from vendor_app.Serializers import PurchaseOrderSerializer
from rest_framework.response import Response
from vendor_app.Signals import po_change_signal
from copy import deepcopy
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class PurchaseOrders(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, **kwargs):
        if 'id' in kwargs:
            purchaseOrder = PurchaseOrder.objects.get(po_number=kwargs['po_number'])
            serializer = PurchaseOrderSerializer(purchaseOrder)
        else:
            purchaseOrders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchaseOrders, many=True)
            
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PurchaseOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def put(self, request, format=None, **kwargs):
        purchaseOrder = PurchaseOrder.objects.get(po_number=kwargs['po_number'])
        serializer = PurchaseOrderSerializer(instance=purchaseOrder, data=request.data)
        serializer.is_valid(raise_exception=True)
        prevInstance = deepcopy(purchaseOrder)
        newInstance = serializer.update(instance=purchaseOrder, validated_data=serializer.validated_data)
        po_change_signal.send(sender=PurchaseOrder, prevInstance=prevInstance, newInstance=newInstance)
        return Response(serializer.data)
        
    def delete(self, request, format=None, **kwargs):
        purchaseOrder = PurchaseOrder.objects.get(po_number=kwargs['po_number'])
        purchaseOrder.delete()
        return Response('Deleted Successfully!')
