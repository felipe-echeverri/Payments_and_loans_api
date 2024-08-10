from django.test import TestCase
from ..models import Customer, Loan, Payment
from decimal import Decimal

class PaymentTests(TestCase):
    """
    Pruebas para los pagos.
    """

    def setUp(self):
        """
        Configura los datos necesarios para las pruebas de pagos.
        """
        print("Configurando datos de prueba...")
        # Crear un cliente
        self.customer = Customer.objects.create(
            external_id='external_01',
            score=Decimal('4000.0'),
            status=1
        )

        # Crear un préstamo para el cliente
        self.loan = Loan.objects.create(
            external_id='loan_01',
            amount=Decimal('1000.0'),
            outstanding=Decimal('1000.0'),
            status=Loan.STATUS_ACTIVE,
            customer=self.customer
        )

    def test_create_payment_success(self):
        """
        Verifica que un pago se cree correctamente y actualice el outstanding del préstamo.
        """
        payment = Payment.objects.create(
            external_id='payment_01',
            total_amount=Decimal('500.00'),
            loan=self.loan
        )

        # Forzar la actualización del préstamo después del pago
        self.loan.refresh_from_db()

        # Verificar el valor de outstanding después del pago
        self.assertAlmostEqual(self.loan.outstanding, Decimal('500.00'), delta=Decimal('0.01'))

    def test_create_payment_exceeding_debt(self):
        """
        Verifica que un pago que excede el outstanding del préstamo sea rechazado.
        """
        payment = Payment.objects.create(
            external_id='payment_02',
            total_amount=Decimal('1500.0'),  # Excede el outstanding
            status=Payment.STATUS_REJECTED,  # Rejected
            loan=self.loan
        )

        # Asegurarse de que el préstamo sigue con el mismo outstanding
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.outstanding, Decimal('1000.0'))

    def test_mark_loan_as_paid(self):
        """
        Verifica que un préstamo se marque como pagado cuando el outstanding sea 0.
        """
        payment = Payment.objects.create(
            external_id='payment_03',
            total_amount=Decimal('1000.0'),
            status=Payment.STATUS_COMPLETED,  # Completed
            loan=self.loan
        )

        # Asegurarse de que el préstamo esté marcado como pagado
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.outstanding, Decimal('0.0'))
        self.assertEqual(self.loan.status, Loan.STATUS_PAID)

    def test_reject_payment(self):
        """
        Verifica que un pago que excede el outstanding del préstamo sea rechazado.
        """
        payment = Payment.objects.create(
            external_id='payment_02',
            total_amount=Decimal('1500.0'),  # Excede el outstanding
            status=Payment.STATUS_REJECTED,  # Rejected
            loan=self.loan
        )

        # Asegurarse de que el préstamo sigue con el mismo outstanding
        self.loan.refresh_from_db()
        self.assertEqual(self.loan.outstanding, Decimal('1000.0'))
        self.assertEqual(payment.status, Payment.STATUS_REJECTED)