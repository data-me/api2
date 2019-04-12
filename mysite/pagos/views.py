
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView

from django.http import JsonResponse

from .models import OfferPaypalBill
from .models import UserPlanPaypalBill
from datame.models import *

import paypalrestsdk
from paypalrestsdk import Payment
import traceback


# Create your views here.


class PaypalView(APIView):
    def _generar_lista_items(self, offer):
        """ """
        items = []
        items.append({
            "name": str(offer),
            "sku": str(offer.id),
            "price": ('%.2f' % offer.price_offered),
            "currency": "EUR",
            "quantity": 1,
        })
        return items

    def _generar_peticion_pago_paypal(self, offer):
        """Crea el diccionario para genrar el pago paypal de offer"""
        peticion_pago = {
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                # "return_url": settings.SITE_URL + reverse('aceptar-pago-paypal'),
                "return_url": settings.SITE_URL + "offer_paypal_accepted.html",
                "cancel_url": settings.SITE_URL},

            # Transaction -
            "transactions": [{
                # ItemList
                "item_list": {
                    "items": self._generar_lista_items(offer)},

                # Amount
                "amount": {
                    "total": ('%.2f' % offer.price_offered),
                    "currency": 'EUR'},

                # Description
                "description": str(offer),
            }]}

        return peticion_pago

    def _generar_pago_paypal(self, offer):
        """Genera un pago de paypal para offer"""
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET, })

        pago_paypal = paypalrestsdk.Payment(self._generar_peticion_pago_paypal(offer))

        if pago_paypal.create():
            for link in pago_paypal.links:
                if link.method == "REDIRECT":
                    url_pago = link.href
        else:
            raise Exception(pago_paypal.error)

        return url_pago, pago_paypal

    def get_redirect_url(self, *args, **kwargs):
        """Extrae el offer que el usuario quiere comprar, genera un pago de
        paypal por el precio del offer, y devuelve la direccion de pago que
        paypal generó"""
        offer = get_object_or_404(Offer, pk=int(kwargs['offer_pk']))
        url_pago, pago_paypal = self._generar_pago_paypal(offer)

        # Se añade el identificador del pago a la sesion para que PaypalExecuteView
        # pueda identificar al ususuario posteriorment
        self.request.session['payment_id'] = pago_paypal.id

        # Por ultimo salvar la informacion del pago para poder determinar que
        # offer le corresponde, al terminar la transaccion.
        OfferPaypalBill.objects.crear_pago(pago_paypal.id, offer)

        res = {}
        res['url_pago'] = url_pago
        return res

    def get(self, request,offer_pk, format=None):

        data =request.GET

        # offer = get_object_or_404(Offer, pk=int(kwargs['offer_pk']))
        offer = get_object_or_404(Offer, pk=int(offer_pk))
        url_pago, pago_paypal = self._generar_pago_paypal(offer)

        # Se añade el identificador del pago a la sesion para que PaypalExecuteView
        # pueda identificar al ususuario posteriorment
        self.request.session['payment_id'] = pago_paypal.id

        # Por ultimo salvar la informacion del pago para poder determinar que
        # offer le corresponde, al terminar la transaccion.
        OfferPaypalBill.objects.crear_pago(pago_paypal.id, offer)

        res = {}
        res['url_pago'] = url_pago
        # return res

        # url_dict = get_redirect_url(kwargs = data)

        return JsonResponse(res)

#
class AcceptPaypalView(APIView):

    def _aceptar_pago_paypal(self, payment_id, payer_id):
        """Aceptar el pago del cliente, actualiza el registro con los datos
        del cliente proporcionados por paypal"""
        paypalrestsdk.configure({"mode": settings.PAYPAL_MODE,"client_id": settings.PAYPAL_CLIENT_ID,"client_secret": settings.PAYPAL_CLIENT_SECRET, })
        registro_pago = get_object_or_404(OfferPaypalBill, payment_id=payment_id)
        pago_paypal = paypalrestsdk.Payment.find(payment_id)
        if pago_paypal.execute({'payer_id': payer_id}):
            registro_pago.pagado = True
            registro_pago.payer_id = payer_id
            registro_pago.payer_email = pago_paypal.payer['payer_info']['email']
            registro_pago.save()
        else:
            raise HttpResponseBadRequest

        return registro_pago

    def get(self, request,paymentId,token_paypal,payerID,format=None):

        try:
            registro_pago = self._aceptar_pago_paypal(paymentId, payerID)

            res = {"message": "Offer created! "}
            return JsonResponse(res)
        except:
            res = {"message":"Oops, something went wrong"}
            return JsonResponse(res)


class PaypalUserPlanPaymentView(APIView):
    def get(self, request, format=None):
        print("is the paypal_userPlan_payment_getting_to_back?==========")
        if request.method == "GET":
            try:
                response = {}
                try:
                    dataScientist_user = User.objects.all().get(pk = request.user.id)
                    dataScientist = DataScientist.objects.all().get(user=dataScientist_user)
                except:
                    traceback.print_exc()
                    response['DeveloperErrorMessage'] = 'Pagos.views.PaypalUserPlanPaymentView: Logged data scientist could not be retrieved.'
                    response['UserCodeErrorMessage'] = 'None.'
                    return JsonResponse(response, safe=False)

                try:
                    userPlan_pk = request.GET['userplan_pk']
                except:
                    traceback.print_exc()
                    response['DeveloperErrorMessage'] = 'Pagos.views.PaypalUserPlanPaymentView: No userPlan_pk was received.'
                    response['UserCodeErrorMessage'] = 'None.'
                    return JsonResponse(response, safe=False)

                try:
                    userplan = UserPlan.objects.get(pk=userPlan_pk)
                    assert userplan.dataScientist == dataScientist
                    userPlanHistory = UserPlan.objects.filter(dataScientist=dataScientist).order_by('-expirationDate').order_by('-pk')
                    assert 0 < userPlanHistory.count()
                    userplanPaymentPending = userPlanHistory.first()

                    assert userplan == userplanPaymentPending
                except:
                    traceback.print_exc()
                    response['DeveloperErrorMessage'] = 'Pagos.views.PaypalUserPlanPaymentView: An error ocurred retrieving the user plan to pay.'
                    response['UserCodeErrorMessage'] = 'None.'
                    return JsonResponse(response, safe=False)

                numberOfMonths = (userplan.expirationDate.year - userplan.startDate.year) \
                                 + (userplan.expirationDate.month - userplan.startDate.month)

                amountToChargeNMonths = ((userplan.expirationDate.year - userplan.startDate.year) * 12
                                     + (userplan.expirationDate.month - userplan.startDate.month)) * 5.0

                print('Pagos.views.PaypalUserPlanPaymentView: Months that are being payed:' + str(amountToChargeNMonths))

                #Configuring PayPal payment
                paypalrestsdk.configure({
                    "mode": settings.PAYPAL_MODE,
                    "client_id": settings.PAYPAL_CLIENT_ID,
                    "client_secret": settings.PAYPAL_CLIENT_SECRET, })


                # Payment object from paypalrestsdk
                payment = paypalrestsdk.Payment({
                    "intent": "sale",

                    #Paymeny method
                    "payer":{
                        "payment_method": "paypal"
                    },

                    #Set redirect URLs
                    "redirect_urls": {
                        "return_url": settings.SITE_URL + "accept_userplan_payment.html",
                        "cancel_url": settings.SITE_URL + "cancel_userplan_payment.html",
                    },

                    # Set transaction object
                    "transactions": [{
                        "description": "Purchasing PRO plan.",
                        "amount": {
                            "total": amountToChargeNMonths,
                            "currency": "EUR",
                        },
                    # ItemList
                        "item_list": {
                            "items": [
                                {
                                    "name": str(numberOfMonths) + " months of PRO user plan.",
                                    "sku": str(userplan.id),
                                    "price": 5.0,
                                    "currency": "EUR",
                                    "quantity": numberOfMonths,
                                }
                            ]},
                    }]
                })

                # Create payment
                if payment.create():
                    # Extract redirect url
                    for link in payment.links:
                        if link.method == "REDIRECT":
                            # Capture redirect url
                            redirect_url = link.href

                            # Redirect the customer to redirect_url
                else:
                    print("Error while creating payment:")
                    print(payment.error)

                self.request.session['payment_id'] = payment.id

                UserPlanPaypalBill.objects.create_userplan_payment(payment.id, userplan)

                response['redirect_url'] = redirect_url
                response['UserCodeMessage'] = 'Please, proceed with the payment.'
                return JsonResponse(response, safe=False)

            except:
                traceback.print_exc()
                response['DeveloperErrorMessage'] = 'Pagos.views.PaypalUserPlanPaymentView: Oops, something went wrong.'
                response['UserCodeErrorMessage'] = 'None.'
                return JsonResponse(response, safe=False)

class AcceptPaypalUserPlanPayment(APIView):
    def get(self, request, format=None):
        response = {}

        # Payment ID obtained when creating the payment (following redirect)
        try:
            payment_id = request.GET.get('paymentId')
            payer_id = request.GET.get('PayerID')
        except:
            traceback.print_exc()
            raise HttpResponseBadRequest

        # Execute payment with the payer ID from the create payment call (following redirect)
        payment = Payment.find(str(payment_id))

        if payment.execute({"payer_id": str(payer_id)}):
            print("Payment[%s] execute successfully" % (payment.id))
            try:
                userPlan_pk = payment.transactions[0]['item_list']['items'][0]['sku']
                print("The id of the user_plan is " +  str(userPlan_pk))
                userPlan = UserPlan.objects.get(pk=userPlan_pk)
                userPlan.isPayed = True
                print("The said userplan" + str(userPlan.id))
                userPlan.save()
                print("The said userplan" + str(userPlan.isPayed))
            except:
                traceback.print_exc()
                response[
                    'DeveloperErrorMessage'] = 'Pagos.views.PaypalUserPlanPaymentView: No userPlan_pk was received.'
                response['UserCodeErrorMessage'] = 'None.'
                return JsonResponse(response, safe=False)
            response['DeveloperErrorMessage'] = 'Pagos.views.PaypalUserPlanPaymentView: Everything went perfect with payment!.'
            response['MessageCode'] = 'You have paid successfuly'
        else:
            print(payment.error)
            response['DeveloperErrorMessage'] = 'ERRROOOOR!'
            response['MessageCode'] = 'ERRROOOOR!'


        return JsonResponse(response, safe=False)