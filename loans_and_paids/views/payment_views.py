from rest_framework import generics
from ..models.payment import Payment
from ..serializers.payment_serializer import PaymentSerializer


class PaymentCreateListView(generics.ListCreateAPIView):
    """
    Vista API para enumerar todos los pagos o crear un nuevo pago.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentsByCustomerView(generics.ListAPIView):
    """
    Vista API para enumerar todos los pagos asociados con un cliente específico.
    """
    serializer_class = PaymentSerializer

    def get_queryset(self):
        customer_id = self.kwargs['external_id']
        return Payment.objects.filter(loan__customer__external_id=customer_id)