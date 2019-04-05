from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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