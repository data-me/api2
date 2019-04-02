import pytz, datetime
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db.models import Q



class Offer_view(APIView):
    def get(self, request, format=None):
        try:
            data = request.GET
            if data.get('search') != None:
                date = datetime.datetime.utcnow()
                ofertas = Offer.objects.filter(Q(title__contains = data['search']) | Q(description__contains = data['search']), limit_time__gte = date, finished=False).values()
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
            currency = data['currency']
            limit_time = data['limit_time']
            contract = data['contract']
            files = data['files']
            thisCompany = Company.objects.all().get(user = request.user)
            # Time management
            date = limit_time.split(" ")[0].split("-")
            hour = limit_time.split(" ")[1].split(":")

            limit_time =  datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(hour[0]), int(hour[1]), 0, 0, pytz.UTC)


            new_offer = Offer.objects.create(title=title, description=description, price_offered=float(price_offered), currency=currency, limit_time=limit_time, contract=contract, files=files, company = thisCompany)
            
            
            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new offer')
            return JsonResponse({"message":"Successfully created new offer"})
        except Exception as e:
            return JsonResponse({"message":"Sorry! Something went wrong..."})
