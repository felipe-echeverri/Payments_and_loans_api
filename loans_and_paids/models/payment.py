from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .loan import Loan

class Payment(models.Model):
    """
    Representa un pago realizado para préstamos.
    """
    STATUS_COMPLETED = 1
    STATUS_REJECTED = 2

    STATUS_CHOICES = [
        (STATUS_COMPLETED, 'completed'),
        (STATUS_REJECTED, 'rejected'),
    ]

    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_COMPLETED)
    paid_at = models.DateTimeField(null=True, blank=True)
    loan = models.ForeignKey('Loan', related_name='payments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Anula el método de guardar para calcular la deuda total y determinar el estado de pago.
        """
        is_new = self.pk is None  # Compruebe si se trata de un nuevo registro.

        if is_new:
            # Calcular la deuda total del cliente asociada al préstamo.
            total_debt = sum(Decimal(loan.outstanding) for loan in self.loan.customer.loans.filter(status=Loan.STATUS_ACTIVE))

            if self.total_amount > total_debt:
                self.status = self.STATUS_REJECTED
                self.paid_at = None
            else:
                self.status = self.STATUS_COMPLETED
                self.paid_at = timezone.now()

        super().save(*args, **kwargs)

        if is_new and self.status == self.STATUS_COMPLETED:
            self._apply_payment_to_loans()

    def _apply_payment_to_loans(self):
        """
        Aplica el pago a préstamos activos y crea detalles de pago.
        """
        if self.status != self.STATUS_COMPLETED:
            return

        if self.payment_details.exists():
            # Si los detalles de pago ya existen, no continúe
            return

        remaining_amount = Decimal(self.total_amount).quantize(Decimal('0.01'))
        for loan in self.loan.customer.loans.filter(status=Loan.STATUS_ACTIVE).order_by('created_at'):
            if remaining_amount <= Decimal('0.00'):
                break

            payment_amount = min(remaining_amount, Decimal(loan.outstanding).quantize(Decimal('0.01')))

            PaymentDetail.objects.create(
                amount=payment_amount,
                loan=loan,
                payment=self
            )

            loan.outstanding = (Decimal(loan.outstanding) - payment_amount).quantize(Decimal('0.01'))

            if loan.outstanding <= Decimal('0.01'):
                loan.mark_as_paid()
            loan.save()

            remaining_amount -= payment_amount

    def __str__(self):
        return self.external_id

@receiver(post_save, sender=Payment)
def handle_payment_post_save(sender, instance, created, **kwargs):
    """
    Receptor de señal para gestionar acciones de pago posteriores al guardado.
    """
    if created and instance.status == Payment.STATUS_COMPLETED:
        instance._apply_payment_to_loans()

class PaymentDetail(models.Model):
    """
    Representa los detalles de un pago aplicado a un préstamo.
    """
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan = models.ForeignKey('Loan', related_name='payment_details', on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, related_name='payment_details', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.payment.external_id} - {self.loan.external_id}"