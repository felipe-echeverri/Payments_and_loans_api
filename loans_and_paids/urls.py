from django.urls import path
from .views.customer_views import (
    CustomerCreateListView, 
    CustomerDetailView, 
    CustomerBalanceView
)
from .views.loan_views import (
    LoanCreateView, 
    LoanListView, 
    LoanActivateView, 
    LoanRejectView
)
from .views.payment_views import (
    PaymentCreateListView, 
    PaymentsByCustomerView
)


urlpatterns = [

    # Rutas relacionadas con clientes
    # Crear una lista de clientes o crear un nuevo cliente
    path('customers/', CustomerCreateListView.as_view(), name='customer-create-list'),
    # Obtener el saldo de un cliente específico usando su ID externo
    path('customers/<str:external_id>/balance/', CustomerBalanceView.as_view(), name='customer-balance'),
    # Obtener detalles de un cliente específico usando su ID externo
    path('customers/<str:external_id>/', CustomerDetailView.as_view(), name='customer-detail'),

    # Rutas relacionadas con préstamos
    # Crear un nuevo préstamo
    path('loans/', LoanCreateView.as_view(), name='loan-create'),
    # Listar todos los préstamos de un cliente específico usando su ID externo
    path('loans/<str:customer_external_id>/', LoanListView.as_view(), name='loan-list-by-customer'),
    # Activar un préstamo específico usando su ID externo
    path('loans/<str:external_id>/activate/', LoanActivateView.as_view(), name='loan-activate'),
    # Rechazar un préstamo específico usando su ID externo
    path('loans/<str:external_id>/reject/', LoanRejectView.as_view(), name='loan-reject'),

    # Rutas relacionadas con pagos
    # Crear una lista de pagos o crear un nuevo pago
    path('payments/', PaymentCreateListView.as_view(), name='payment-create-list'),
    # Listar todos los pagos asociados con un cliente específico usando su ID externo
    path('payments/customer/<str:external_id>/', PaymentsByCustomerView.as_view(), name='payments-by-customer'),
]
