from django.db import models
import paypalrestsdk
from django.db import models
from django.contrib.auth.models import *
from django import forms
from django.utils import timezone
from django.template.defaultfilters import default
from django.db.models.fields.related import OneToOneField

from datame.models import Offer

# Create your models here.

class PagoPaypalManager(models.Manager):
    def crear_pago(self, payment_id, offer):
        pago=self.create(offer=offer,
            payment_id=payment_id,
            precio=offer.price_offered)
        return pago



class OfferPaypalBill(models.Model):
    offer = models.OneToOneField(Offer,on_delete=models.SET(0))
    # Identificador de paypal para este pago
    payment_id = models.CharField(max_length=64, db_index=True)
    # Id unico asignado por paypal a cada usuario no cambia aunque
    # la dirección de email lo haga.
    payer_id = models.CharField(max_length=128, blank=True, db_index=True)
    # Dirección de email del cliente proporcionada por paypal.
    payer_email = models.EmailField(blank=True)
    pagado = models.BooleanField(default=False)

    precio = models.DecimalField(max_digits=8, decimal_places=2,
                                 default=0.0)
    objects = PagoPaypalManager()