from django.dispatch import Signal, receiver
from vendor_app.models import PurchaseOrder, Vendor
from datetime import datetime
from rest_framework.exceptions import ValidationError
from vendor_app.Serializers import VendorSerializer, VendorPerformanceHistorySerializer
from datetime import datetime

po_change_signal = Signal()

@receiver(signal=po_change_signal)
def updateMetrics(sender, **kwargs):
    
    # existing instance
    prevInstance = kwargs['prevInstance']
    # new instance to be updated with
    newInstance = kwargs['newInstance']
    
    data = {}
    addMetricsToPerformanceHistory = False
    
    if (prevInstance.acknowledgment_date is None or prevInstance.acknowledgment_date!=newInstance.acknowledgment_date) and isinstance(newInstance.acknowledgment_date, datetime):
        averageResponseTime = PurchaseOrder.getAverageResponseTime(purchaseOrder=newInstance)
        data['average_response_time'] = averageResponseTime
        addMetricsToPerformanceHistory = True
    
    if (prevInstance.status == PurchaseOrder.PENDING or prevInstance.status == PurchaseOrder.CANCELLED) and newInstance.status == PurchaseOrder.COMPLETED:
        onTimeDeliveryRate = PurchaseOrder.getOnTimeDeliveryRate(purchaseOrder=newInstance)
        data['on_time_delivery_rate'] = onTimeDeliveryRate
        addMetricsToPerformanceHistory = True
        
    if isinstance(newInstance.quality_rating, float) and prevInstance.quality_rating!=newInstance.quality_rating:
        qualityRatingAverage = PurchaseOrder.getQualityRatingAverage(purchaseOrder=newInstance)
        data['quality_rating_avg']= qualityRatingAverage
        addMetricsToPerformanceHistory = True
    
    if (prevInstance.status!=newInstance.status):
        fulfillmentRate = PurchaseOrder.getFulfillmentRate(purchaseOrder=newInstance)
        data['fulfillment_rate'] = fulfillmentRate
        addMetricsToPerformanceHistory = True
        
    vendor = Vendor.objects.get(vendor_code = newInstance.vendor.vendor_code)
    vendorSerializer = VendorSerializer(instance=vendor, data=data, partial=True)
    vendorSerializer.is_valid(raise_exception=True)
    vendorSerializer.save()
    
    vendor = Vendor.objects.get(vendor_code = newInstance.vendor.vendor_code)
    performance_data = {
        'vendor' : vendor.vendor_code,
        'date' : datetime.now(),
        'on_time_delivery_rate' : vendor.on_time_delivery_rate,
        'quality_rating_avg' : vendor.quality_rating_avg,
        'average_response_time' : vendor.average_response_time,
        'fulfillment_rate' : vendor.fulfillment_rate
    }
    
    if addMetricsToPerformanceHistory:
        vendorPerformanceHistorySerializer = VendorPerformanceHistorySerializer(data=performance_data)
        vendorPerformanceHistorySerializer.is_valid(raise_exception=True)
        vendorPerformanceHistorySerializer.save()