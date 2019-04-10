from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

#para el dashboard
class Submitions_view(APIView):
    def get(self, request, format=None):
        user_logged = User.objects.all().get(pk = request.user.id)
        if (user_logged.is_superuser or user_logged.is_staff):
            try:    
                submitions = Submition.objects.all().values()
                return JsonResponse(list(submitions), safe=False)
            except:
                print("there are no submitions")
        return JsonResponse({"message":"Oops, something went wrong"})

class Submition_view(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            data = request.POST
            offerId = data['offerId']
            file = data['file']
            comments = data['comments']
            user_logged = User.objects.all().get(pk = request.user.id)
            if (not user_logged.groups.filter(name='DataScientist').exists()):
                res = JsonResponse({"message":"Only DataScientist can make a submition"})
            else:
                dataScientist = DataScientist.objects.all().get(user = request.user)
                offer = Offer.objects.all().get(pk = offerId)
                Submition.objects.create(offer = offer, dataScientist = dataScientist, file = file, comments = comments, status = 'SU')
                res = JsonResponse({"message":"Submition created successfully"})
            return res
        except Exception as e:
            return JsonResponse({"message":"Oops, something went wrong" + str(e)})
    def get(self, request, format=None):
        try:
            user_logged = User.objects.all().get(pk = request.user.id)
            if (user_logged.groups.filter(name='Company').exists()):
                    thisCompany = Company.objects.all().get(user = request.user)
                    submitions = Submition.objects.filter(offer__company = thisCompany).values('dataScientist_id','offer_id','comments','file','status','offer__title', 'id')
                    return JsonResponse(list(submitions), safe=False)
            elif(user_logged.groups.filter(name='DataScientist').exists()):
                    dataScientistRecuperado = DataScientist.objects.all().get(user = request.user)
                    submitions = Submition.objects.filter(dataScientist = dataScientistRecuperado).values('dataScientist_id','offer_id','comments','file','status','offer__title', 'id')
                    return JsonResponse(list(submitions), safe=False)
        except Exception as e:
            return JsonResponse({"message":"Oops, something went wrong" + str(e)})
        
class Check_submition(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            data = request.POST
            applyId = data['applyId']
            res = JsonResponse({"message": "false"}, safe = False)
            user_logged = User.objects.all().get(pk = request.user.id)
            if (not user_logged.groups.filter(name='DataScientist').exists()):
                res = JsonResponse({"message": "false"}, safe = False)
            else:
                dataScientist = DataScientist.objects.all().get(user = request.user)
                apply = Apply.objects.all().get(pk = applyId)
                if (apply.status == 'AC' and apply.dataScientist == dataScientist and (not Submition.objects.all().filter(offer = apply.offer).exists())):
                    res = JsonResponse({"message": "true"}, safe = False)
            return res
        except Exception as e:
            return JsonResponse({"message":"Oops, something went wrong" + str(e)})
        
class Change_status(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            data = request.POST
            submitId = data['submitId']
            status = data['status']
            submit = Submition.objects.all().get(pk = submitId)
            user_logged = User.objects.all().get(pk = request.user.id)
            if ((not user_logged.groups.filter(name='Company').exists())):
                return JsonResponse({"message": "Only the a company can do that"}, safe = False)
            company = Company.objects.all().get(user = user_logged)
            if(not submit.offer.company == company):
                return JsonResponse({"message": "Only the owner company can do that"}, safe = False)
            else:
                Submition.objects.all().filter(pk = submitId).update(status = status)
            return JsonResponse({"message": "Status changed"}, safe = False)
        except Exception as e:
            return JsonResponse({"message":"Oops, something went wrong" + str(e)})