from django.urls import path
from .views import PaypalView


urlpatterns = [
    path(r'create_papyal_payment/<int:offer_pk>/',
        view  = PaypalView.as_view(),
        name  = "pago-paypal"),
    # url(
    #     regex = r'^aceptar-pago/$',
    #     view  = PaypalExecuteView.as_view(),
    #     name  = "aceptar-pago-paypal"),
]
