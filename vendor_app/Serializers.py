from rest_framework.serializers import ModelSerializer
from .models import Vendor, PurchaseOrder, VendorPerformanceHistory
from rest_framework import serializers
from django.contrib.auth.models import User

class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        
class PurchaseOrderSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        
    def validate_quality_rating(self, value):
        if not 0<=value<=10 and value is not None:
            raise serializers.ValidationError("quality rating should be between 0 and 10")
        return value
    
    def update(self, instance, validated_data):
        changed_fields = []
        for field, value in validated_data.items():
            new_value = value
            old_value = getattr(instance, field)
            if new_value!=old_value:
                changed_fields.append(field)
                
        requiredForDeliveryDate = [validated_data['acknowledgment_date'], validated_data['order_date'], validated_data['issue_date']]
        requiredBeforeOrderDate = [validated_data['acknowledgment_date'], validated_data['expected_delivery_date'], validated_data['issue_date']]
                
        if (validated_data['acknowledgment_date'] is None or validated_data['order_date'] is None) and isinstance(validated_data['quality_rating'], float):
            raise serializers.ValidationError({'quality_rating' : "Please ensure delivery_date and acknowledgment_date are fileled while updating quality_rating"})
        
        if validated_data['order_date'] is not None and any(f is None for f in requiredBeforeOrderDate):
            raise serializers.ValidationError({'order_date' : "issue_date, acknowledgment_date, expected_delivery_date all are required while updating order_date"})
        
        if validated_data['delivery_date'] is not None and any(f is None for f in requiredForDeliveryDate):
            raise serializers.ValidationError({'delivery_date' : "acknowledgment_date, order_date, quality_rating all are required before updating delivery_date"})
            
        if instance.status == PurchaseOrder.COMPLETED and validated_data['status'] == PurchaseOrder.COMPLETED:
            if validated_data['delivery_date'] is None:
                raise serializers.ValidationError({'delivery_date' : "delivery_date required while updating status to 'COMPLETED'"})
        
        if 'status' in changed_fields:
            if (instance.status == PurchaseOrder.PENDING or instance.status == PurchaseOrder.CANCELLED) and validated_data['status'] == PurchaseOrder.COMPLETED:
                if validated_data['delivery_date'] is None:
                    raise serializers.ValidationError({'delivery_date' : "delivery_date required while updating status to 'COMPLETED'"})
                
        if 'delivery_date' in changed_fields:        
            if validated_data['status'] != PurchaseOrder.COMPLETED:
                raise serializers.ValidationError({'status' : "only 'COMPLETED' allowed while updating delivery_date"})
        
        return super().update(instance, validated_data)
    
class UpdateOrderSerializer(PurchaseOrderSerializer):
    class Meta(PurchaseOrderSerializer.Meta):
        model = PurchaseOrder        
        
class VendorPerformanceHistorySerializer(ModelSerializer):
    class Meta:
        model = VendorPerformanceHistory
        fields = '__all__'
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        validated_data.pop('password')
        return validated_data