from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import Customer

class CustomerTests(APITestCase):
    """
    Pruebas para la vista de clientes.
    """

    def test_create_customer(self):
        """
        Verifica que se puede crear un cliente correctamente y que el estado sea activo (1).
        """
        url = reverse('customer-create-list')
        data = {
            "external_id": "external_01",
            "score": 4000.0,
            "preapproved_at": "2023-02-12T22:29:27.177914Z"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 1)  # Verificar que el estado sea activo

    def test_get_customer_balance(self):
        """
        Verifica que se puede obtener el saldo del cliente correctamente.
        """
        # Crear un cliente y un préstamo de prueba
        customer = Customer.objects.create(external_id="external_01", score=4000.0, status=1)
        url = reverse('customer-balance', args=["external_01"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(response.data['available_amount']), 4000.0)
