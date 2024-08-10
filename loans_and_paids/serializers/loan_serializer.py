from rest_framework import serializers
from django.db.models import Sum
from ..models import Customer, Loan

class LoanCreateSerializer(serializers.ModelSerializer):
    customer_external_id = serializers.CharField(write_only=True)

    class Meta:
        model = Loan
        fields = ['external_id', 'amount', 'outstanding', 'contract_version', 'customer_external_id']

    def create(self, validated_data):
        customer_external_id = validated_data.pop('customer_external_id')
        customer = Customer.objects.get(external_id=customer_external_id)

        # Verificar si el monto excede el límite de crédito del cliente
        total_debt = Loan.objects.filter(customer=customer, status__in=[Loan.STATUS_PENDING, Loan.STATUS_ACTIVE]).aggregate(total_outstanding=Sum('outstanding'))['total_outstanding'] or 0
        if total_debt + validated_data['amount'] > customer.score:
            raise serializers.ValidationError("El monto del préstamo excede el límite de crédito del cliente.")

        validated_data['customer'] = customer
        loan = Loan.objects.create(**validated_data)
        return loan