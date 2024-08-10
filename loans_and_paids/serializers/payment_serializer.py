from rest_framework import serializers
from ..models import Payment, PaymentDetail

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ['amount', 'loan']

class PaymentSerializer(serializers.ModelSerializer):
    payment_details = PaymentDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = ['external_id', 'total_amount', 'status', 'paid_at', 'loan', 'payment_details']
