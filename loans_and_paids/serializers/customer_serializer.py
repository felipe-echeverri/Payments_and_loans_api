from rest_framework import serializers
from ..models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['external_id', 'status', 'score', 'preapproved_at']

class CustomerBalanceSerializer(serializers.Serializer):
    external_id = serializers.CharField(max_length=60)
    score = serializers.DecimalField(max_digits=12, decimal_places=2)
    available_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_debt = serializers.DecimalField(max_digits=12, decimal_places=2)