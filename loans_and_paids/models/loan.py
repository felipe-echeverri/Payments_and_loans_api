from django.utils import timezone
from django.db import models
from loans_and_paids.models import Customer

class Loan(models.Model):
    """
    Representa un préstamo asociado a una cliente.
    """
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    outstanding = models.DecimalField(max_digits=20, decimal_places=10)

    # Loan estados
    STATUS_PENDING = 1  # "pending"
    STATUS_ACTIVE = 2   # "active"
    STATUS_REJECTED = 3 # "rejected"
    STATUS_PAID = 4     # "paid"

    STATUS_CHOICES = [
        (STATUS_PENDING, 'pending'),
        (STATUS_ACTIVE, 'active'),
        (STATUS_REJECTED, 'rejected'),
        (STATUS_PAID, 'paid'),
    ]

    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    contract_version = models.CharField(max_length=30, null=True, blank=True)
    maximum_payment_date = models.DateTimeField(null=True, blank=True)
    taken_at = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, related_name='loans', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def activate_loan(self):
        """
        Activa el préstamo si está en estado pendiente.
        """
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_ACTIVE
            self.taken_at = timezone.now()
            self.save()

    def reject_loan(self):
        """
        Rechaza el préstamo si está en estado pendiente.
        """
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_REJECTED
            self.save()

    def mark_as_paid(self):
        """
        Marca el préstamo como pagado si el monto pendiente es cero.
        """
        if self.outstanding == 0:
            self.status = self.STATUS_PAID
            self.save()

    def __str__(self):
        return self.external_id