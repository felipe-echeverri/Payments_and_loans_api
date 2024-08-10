from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from ..models.loan import Loan
from ..serializers.loan_serializer import LoanCreateSerializer


class LoanCreateView(APIView):
    """
    Vista API para crear un nuevo préstamo para un cliente.
    """
    def post(self, request):
        serializer = LoanCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanListView(APIView):
    """
    Vista API para enumerar todos los préstamos asociados con un cliente específico.
    """
    def get(self, request, customer_external_id):
        loans = Loan.objects.filter(customer__external_id=customer_external_id)
        serializer = LoanCreateSerializer(loans, many=True)
        return Response(serializer.data)

class LoanActivateView(APIView):
    """
    Vista API para activar un préstamo por su ID externo.
    """
    def post(self, request, external_id):
        loan = get_object_or_404(Loan, external_id=external_id)
        loan.activate_loan()
        return Response({"status": "Préstamo activado."}, status=status.HTTP_200_OK)

class LoanRejectView(APIView):
    """
    Vista API para rechazar un préstamo por su ID externo.
    """
    def post(self, request, external_id):
        loan = get_object_or_404(Loan, external_id=external_id)
        loan.reject_loan()
        return Response({"status": "Préstamo rechazado"}, status=status.HTTP_200_OK)