
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
import traceback

from django.http import JsonResponse

from .models import OfferPaypalBill
from datame.models import Offer

import paypalrestsdk


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
            raise Exception(pago.error)

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
        print('Hello logs')
        print('PaymentID =>', payment_id)
        print('PayerID =>', payer_id)
        pago_paypal = paypalrestsdk.Payment.find(payment_id)
        print('hi')
        print('Pago paypal=>', pago_paypal)
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
            print('I received params, paymentId:', paymentId, " and token:", token_paypal, "and payerID:", payerID)
            registro_pago = self._aceptar_pago_paypal(paymentId, payerID)

            res = {"message": "Offer created! "}
            return JsonResponse(res)
        except Exception as e:
            print('This is error =>',e)
            traceback.print_exc()
            res = {"message":"Oops, something went wrong"}
            return JsonResponse(res)

