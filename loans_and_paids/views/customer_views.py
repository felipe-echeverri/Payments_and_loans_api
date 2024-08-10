from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from ..models.customer import Customer
from ..serializers.customer_serializer import CustomerSerializer
from ..serializers.customer_serializer import CustomerBalanceSerializer
from ..models import Customer, Loan
from django.db.models import Sum


class CustomerCreateListView(generics.ListCreateAPIView):
    """
    Vista API para enumerar todos los clientes o crear un nuevo cliente.
    El cliente se crea con un estado activo (1) por defecto.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        # Asegúrese de que el cliente se cree con el estado activo (1)
        serializer.save(status=1)

class CustomerDetailView(RetrieveAPIView):
    """
    Vista API para recuperar los detalles de un cliente por su ID externo.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'external_id'

class CustomerBalanceView(views.APIView):
    """
    Vista API para recuperar la información del saldo de un cliente.
    Devuelve el monto disponible del cliente en función de su puntaje y deuda total.
    """
    def get(self, request, external_id):
        try:
            customer = Customer.objects.get(external_id=external_id)
            loans = Loan.objects.filter(customer=customer, status__in=[1, 2])
            total_debt = loans.aggregate(Sum('outstanding'))['outstanding__sum'] or 0
            available_amount = customer.score - total_debt
            
            data = {
                'external_id': customer.external_id,
                'score': customer.score,
                'available_amount': available_amount,
                'total_debt': total_debt,
            }
            serializer = CustomerBalanceSerializer(data)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)