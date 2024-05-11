from django.db import models
from django.db.models import F, Avg, ExpressionWrapper
from django.core.validators import MinValueValidator
from uuid import uuid4
from datetime import datetime

class Vendor(models.Model):
    name = models.CharField(max_length=255, blank=False)
    contact_details = models.TextField(blank=False)
    address = models.TextField(blank=False)
    vendor_code = models.CharField(primary_key=True, default=uuid4, max_length=36)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.DurationField(null=True)
    fulfillment_rate = models.FloatField(default=0.0)
    
class PurchaseOrder(models.Model):
    po_number = models.CharField(primary_key=True, default=uuid4, max_length=36)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField(null=False)
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    PENDING = "P"
    CANCELLED = "CL"
    COMPLETED = "CP"
    STATUS_CHOICES = {
        (PENDING, "Pending"),
        (CANCELLED, "Cancelled"),
        (COMPLETED, "Completed")
    }
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(blank=False, default=datetime.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def getStatusChoiceValue(self, choice):
        for choice_mapping in self.STATUS_CHOICES:
            if choice_mapping[0]==choice:
                return choice_mapping[1]
        return ""
    
    def getOnTimeDeliveryRate(purchaseOrder):
        try:
            onTimeDeliveries = PurchaseOrder.objects.filter(vendor=purchaseOrder.vendor,delivery_date__lte = F("expected_delivery_date"), status=PurchaseOrder.COMPLETED)
            totalDeliveries = PurchaseOrder.objects.filter(vendor=purchaseOrder.vendor, status=PurchaseOrder.COMPLETED)
            return len(onTimeDeliveries)/len(totalDeliveries)
        except ZeroDivisionError:
            return 0
        except Exception as e:
            return 0
        
    def getAverageResponseTime(purchaseOrder):
        try:
            expression = ExpressionWrapper(F('acknowledgment_date')-F('issue_date'), output_field=models.fields.DurationField())
            responseTime = PurchaseOrder.objects.annotate(response_time=expression).filter(vendor=purchaseOrder.vendor, status = PurchaseOrder.COMPLETED, issue_date__isnull=False, acknowledgment_date__isnull=False).aggregate(Avg('response_time'))
            return responseTime['response_time__avg']
        except Exception as e:
            return 0
        
    def getQualityRatingAverage(purchaseOrder):
        try:
            qualityRatingAverage = PurchaseOrder.objects.filter(vendor=purchaseOrder.vendor,status=PurchaseOrder.COMPLETED).exclude(quality_rating__isnull=True).aggregate(Avg('quality_rating'))
            return qualityRatingAverage['quality_rating__avg']
        except ZeroDivisionError:
            return 0
        except Exception as e:
            return 0
    
    def getFulfillmentRate(purchaseOrder):
        try:
            fulfilledDeliveries = PurchaseOrder.objects.filter(vendor = purchaseOrder.vendor, status = PurchaseOrder.COMPLETED)
            totalDeliveries= PurchaseOrder.objects.filter(vendor = purchaseOrder.vendor)
            return len(fulfilledDeliveries)/len(totalDeliveries)
        except ZeroDivisionError:
            return 0
        except Exception as e:
            return 0
        
class VendorPerformanceHistory(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.DurationField(null=True)
    fulfillment_rate = models.FloatField(default=0.0)
    