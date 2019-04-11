import datetime
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from django.forms.models import model_to_dict

#para el admin
class Applications_view(APIView):
    def get(self, request, format=None):
        try:

            user_logged = User.objects.all().get(pk = request.user.id)
            applications = []
            if (user_logged.is_superuser or user_logged.is_staff):
                try:
                    applications = Apply.objects.all().values()
                except:
                    print("There are no applications")
                return JsonResponse(list(applications), safe=False)
        except:
            return JsonResponse({"message":"Oops, something went wrong"})
#para el admin
class ApplicationsAccepted_view(APIView):
    def get(self, request, format=None):
        try:

            user_logged = User.objects.all().get(pk = request.user.id)
            applicationsAccepted = []
            if (user_logged.is_superuser or user_logged.is_staff):
                try:
                    applicationsAccepted = Apply.objects.all().filter(status = 'AC').values()
                except:
                    print("There are no applications accepted")
                return JsonResponse(list(applicationsAccepted), safe=False)
        except:
            return JsonResponse({"message":"Oops, something went wrong"})

class ApplicationsOfOffer(APIView):
    def get(self, request, offer_id, format=None):
        try:
            lookup_url_kwarg = "offer_id"
            offer = Offer.objects.get(id = self.kwargs.get(lookup_url_kwarg))

            applicationsOfOffer = Apply.objects.all().filter(offer = offer).values()

            return JsonResponse(list(applicationsOfOffer), safe=False)

        except:
            return JsonResponse({"There are no applications for the offer"})



class Apply_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            title = data['title']
            description = data['description']
            date = datetime.datetime.utcnow()
            user_logged = User.objects.all().get(pk = request.user.id)
            if (not user_logged.groups.filter(name='DataScientist').exists()):
                return JsonResponse({"message":"Only DataScientist can apply"})
            dataScientist = DataScientist.objects.all().get(user = request.user)
            offerId = data['offerId']
            offer = Offer.objects.all().get(pk = offerId)
            applysInOffer = Apply.objects.all().filter(offer = offer)
            for apply in applysInOffer:
                if(apply.dataScientist.id == dataScientist.id):
                    return JsonResponse({"message":"DataScientist already applied"})
            new_apply = Apply.objects.create(title=title, description=description, status='PE', date=date, dataScientist = dataScientist, offer = offer)
            return JsonResponse({"message":"Successfully created new apply"})
        except:
            return JsonResponse({"message":"Oops, something went wrong"})
    def get(self, request, format=None):
        try:
            user_logged = User.objects.all().get(pk = request.user.id)
            if (user_logged.groups.filter(name='Company').exists()):
                    thisCompany = Company.objects.all().get(user = request.user)
                    offers = Offer.objects.all().filter(company = thisCompany).distinct()
                    applys = []
                    data = request.GET
                    #filtro = data['filtro']
                    #TODO Cuando se realice el login lo ideal es que no se le tenga que pasar la ID del principal, sino recuperarla mediante autentificacion

                    for offer in offers:
                        applysInOffer = Apply.objects.all().filter(offer = offer, status = 'PE').values()
                        applysInOffer_2 = []
                        for i in applysInOffer:
                            i["DS_User_id"] = DataScientist.objects.filter(id=i["dataScientist_id"]).values_list()[0][1]
                            applysInOffer_2.append(i)
                        applys.extend(applysInOffer_2)

                    return JsonResponse(list(applys), safe=False)
            elif(user_logged.groups.filter(name='DataScientist').exists()):
                    dataScientistRecuperado = DataScientist.objects.all().get(user = request.user)
                    applys = []
                    data = request.GET
                    #TODO Cuando se realice el login lo ideal es que no se le tenga que pasar la ID del principal, sino recuperarla mediante autentificacion

                    applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado).values('title','description','date','status','dataScientist_id','offer_id','offer__files','id')
                    return JsonResponse(list(applys), safe=False)
        except:
            return JsonResponse({"message":"Oops, something went wrong"})

# Accept/Reject contract

class AcceptApply_view(APIView):
    def post(self, request, format=None):
        try:
            user_logged = User.objects.all().get(pk = request.user.id)
            if (user_logged.groups.filter(name='Company').exists()):
                company = Company.objects.all().get(user = user_logged)
                data = request.POST
                idApply = data['idApply']
                apply = Apply.objects.all().get(pk = idApply)
                if(apply.offer.company == company):
                    if (apply.offer.finished == True):
                        res = JsonResponse({"message":"Offer has been already accepted"})
                    else:
                        applysToUpdate = Apply.objects.all().filter(offer = apply.offer).update(status = 'RE')
                        apply.status = 'AC'
                        apply.save()
                        apply.offer.finished = True
                        apply.offer.save()
                        res = JsonResponse(model_to_dict(apply), safe=False)
                else:
                    res = JsonResponse({"message":"The company doesnt own the offer"})
            else:
                res = JsonResponse({"message":"Only companies can update an apply"})
            return res
        except:
                return JsonResponse({"message":"Oops, something went wrong"})


class Apply_v2_view(APIView):
    def delete(self, request, application_id, format=None):
        try:
            application = Apply.objects.get(pk=application_id)
            owner = DataScientist.objects.get(user=request.user)
            if(application.dataScientist == owner and application.status == 'PE'):
                application.delete()
                res = JsonResponse({"code": "200", "message": "Application successfully deleted"})
            else:
                res = JsonResponse({"code": "401", "message": "The applications is not yours or is not pending"})
            return res
        except:
            return JsonResponse({"message": "Oops, something went wrong"})
