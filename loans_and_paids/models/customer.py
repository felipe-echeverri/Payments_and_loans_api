from django.db import models

class Customer(models.Model):
    """
    Representa a una cliente con préstamos asociados.
    """
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField(default=1)  # 1 para Activo, 2 para Inactivo
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.external_id