import pytz, datetime
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db.models import Q
from django.http import HttpResponseNotFound



class Offer_view(APIView):
    def get(self, request, format=None):
        try:
            data = request.GET
            if data.get('search') != None:
                date = datetime.datetime.utcnow()
                ofertas = Offer.objects.filter(Q(title__contains = data['search']) | Q(description__contains = data['search']), limit_time__gte = date, finished=False).values()
                return JsonResponse(list(ofertas), safe=False)
            elif data.get('offerId') != None:
                ofertas = Offer.objects.filter(id = data['offerId']).values()
                return JsonResponse(list(ofertas), safe=False)
            else:
                ofertas = []
                try:
                    thisCompany = Company.objects.all().get(user = request.user)
                    # All offers instead only those who don't have an applicant
                    ofertas = Offer.objects.all().filter(company = thisCompany).values()
                except:
                    date = datetime.datetime.utcnow()
                    thisDS = DataScientist.objects.all().get(user = request.user)
                    applies = Apply.objects.all().filter(dataScientist = thisDS)
                    user_applied_offers = [a.offer.id for a in applies]
                    # All offers whos time has not come yet
                    ofertas = Offer.objects.all().filter(limit_time__gte = date, finished=False).exclude(id__in=user_applied_offers).values()
                return JsonResponse(list(ofertas), safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"message":"Sorry! Something went wrong..."})
    def post(self, request, format=None):
        try:
            data = request.POST
            title = data['title']
            description = data['description']
            price_offered = data['price_offered']
            limit_time = data['limit_time']
            contract = data['contract']
            files = data['files']
            thisCompany = Company.objects.all().get(user = request.user)
            # Time management
            date = limit_time.split(" ")[0].split("-")
            hour = limit_time.split(" ")[1].split(":")

            limit_time =  datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(hour[0]), int(hour[1]), 0, 0, pytz.UTC)


            new_offer = Offer.objects.create(title=title, description=description, price_offered=float(price_offered), limit_time=limit_time, contract=contract, files=files, company = thisCompany)


            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new offer')
            return JsonResponse({"message":"Successfully created new offer"})
        except Exception as e:
            return JsonResponse({"message":"Sorry! Something went wrong..."})

    def delete (self, request, pk = None, format=None):
        try:
            if pk is None:
                pk = self.kwargs['pk']
            offer = Offer.objects.all().get(pk=pk)

            thisCompany = Company.objects.all().get(user = request.user)
            ofertasCompany = Offer.objects.all().filter(company = thisCompany).values()
            if(ofertasCompany.filter(Q(title__contains =offer))):
                offer.delete()
                return JsonResponse({"message":"Successfully deleted offer"})
            else:
                return JsonResponse({"message":"You do not own this offer"})
        except Exception as e:
            print(e)
            return JsonResponse({"message":"Sorry! Something went wrong..."})

class Offer_admin_view(APIView):
    def get(self, request, format=None):
        try:
            logged_user = request.user

            if logged_user.is_superuser or logged_user.is_staff:

                response = []

                offers = Offer.objects.all().values()

                for offer in offers:
                    company = Company.objects.get(id = offer.get('company_id'))
                    response.append({
                        'offer_id' : str(offer.get('id')),
                        'title' : str(offer.get('title')),
                        'description' : str(offer.get('description')),
                        'price_offered' : str(offer.get('price_offered')),
                        'creation_date' : str(offer.get('creation_date')),
                        'limit_date' : str(offer.get('limit_date')),
                        'finished' : str(offer.get('finished')),
                        'files' : str(offer.get('files')),
                        'contract' : str(offer.get('contract')),
                        'company_id' : str(offer.get('company_id')),
                        'company_name' : company.name
                    })

                return JsonResponse(list(response), safe = False)

            else:
                return JsonResponse({"message":"Sorry! You don't have access to this resource..."})

        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})
    
    def delete(self, request, offer_id, format=None):
        try:
            logged_user = request.user

            if logged_user.is_superuser or logged_user.is_staff:
                lookup_url_kwarg = "offer_id"

                offer = Offer.objects.get(id = self.kwargs.get(lookup_url_kwarg))

                message = Message.objects.create(receiver = offer.company.user, sender = logged_user, title = 'Your offer: ' + str(offer) + ', was deleted', body = 'Our administrators detected that your offer was in some way inappropriate')

                offer.delete()

            return JsonResponse({"message":"Successfuly deleted offer"})

        except Exception as e:
            return JsonResponse({"message" : str(e)})
