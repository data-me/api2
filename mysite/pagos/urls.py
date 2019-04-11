from django.urls import path
from .views import PaypalView, AcceptPaypalView, PaypalUserPlanPaymentView, AcceptPaypalUserPlanPayment
    #CancelPaypalUserPlanPayment



urlpatterns = [
    path(r'create_papyal_payment/<int:offer_pk>/',
        view  = PaypalView.as_view(),
        name  = "pago-paypal"),
    path(r'accept_paypal_payment/<str:paymentId>/<str:token_paypal>/<str:payerID>/',
        view  = AcceptPaypalView.as_view(),
        name  = "accept-pago-paypal"),
    path('paypal_userPlan_payment', PaypalUserPlanPaymentView.as_view()),
    path('accept_paypal_userPlan_payment', AcceptPaypalUserPlanPayment.as_view()),
    #path('cancel_paypal_userPlan_payment', CancelPaypalUserPlanPayment.as_view()),
    # url(
    #     regex = r'^aceptar-pago/$',
    #     view  = PaypalExecuteView.as_view(),
    #     name  = "aceptar-pago-paypal"),
]
