from rest_framework.test import APITestCase
from ..models import Customer, Loan

class LoanStateTests(APITestCase):
    """
    Pruebas para el estado de los préstamos.
    """

    def setUp(self):
        """
        Configura los datos necesarios para las pruebas de estado del préstamo.
        """
        self.customer = Customer.objects.create(external_id="external_01", score=1000.0, status=1)
        self.loan = Loan.objects.create(
            external_id="loan_01",
            customer=self.customer,
            amount=500.0,
            outstanding=500.0
        )

    def test_activate_loan(self):
        """
        Verifica que un préstamo se pueda activar correctamente.
        """
        response = self.client.post(f'/api/loans/{self.loan.external_id}/activate/')
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, Loan.STATUS_ACTIVE)

    def test_reject_loan(self):
        """
        Verifica que un préstamo se pueda rechazar correctamente.
        """
        response = self.client.post(f'/api/loans/{self.loan.external_id}/reject/')
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, Loan.STATUS_REJECTED)