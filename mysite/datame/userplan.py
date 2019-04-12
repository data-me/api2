from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime
from dateutil.relativedelta import *
import traceback
import pytz

class userPlanHistory(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            response = {}
            userPlanHistory = []
            logged_user = User.objects.all().get(pk = request.user.id)
            try:
                #List my userplan payments
                loggedDataScientist = DataScientist.objects.all().get(user=logged_user)
                userPlanHistory = list(UserPlan.objects.filter(dataScientist= loggedDataScientist).values())
                response.update({
                    'userId':str(logged_user.id),
                    'dataScientistId': str(loggedDataScientist.id),
                    'userPlanHistory': userPlanHistory
                })
            except:
                try:
                    # List userplan as administrator
                    assert logged_user.is_staff
                    dataScientist = DataScientist.objects.all().get(pk=request.GET.get('dataScientistId'))
                    userPlanHistory = list(UserPlan.objects.filter(dataScientist=dataScientist)
                                           .filter(isPayed=True).values())
                    response.update({
                        'userId': str(logged_user.id),
                        'dataScientistId': str(dataScientist.id),
                        'userPlanHistory': userPlanHistory
                    })
                except:
                    try:
                        #Trying to list payment plan as a company will not return the said list
                        companyRecuperada = Company.objects.all().get(user=logged_user)
                        return JsonResponse({"message": "Sorry! As a company you cannot access to this DataScientist User Plan."})
                    except:
                        return JsonResponse(
                            {"message": "Oops, something went wrong"})
            return JsonResponse(response, safe=False)

class currentUserPlan(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            response={}
            try:
                if request.user.id is not None and request.GET.get('dataScientistId') is None:
                    dataScientist_user = User.objects.all().get(pk = request.user.id)
                    dataScientist = DataScientist.objects.all().get(user=dataScientist_user)
                else:
                    dataScientist = DataScientist.objects.all().get(pk=request.GET.get('dataScientistId'))
            except:
                return JsonResponse({"message": "Sorry, there was a problem retrieving the Data Scientist"})
            try:
                userPlanHistory = UserPlan.objects.filter(dataScientist=dataScientist)\
                    .filter(isPayed=True).order_by('-expirationDate')
                response['dataScientistId'] = dataScientist.id
                currentUserPlan = None
                if 0 < userPlanHistory.count():
                    currentUserPlan = userPlanHistory.first()

                if currentUserPlan is None or currentUserPlan.expirationDate < datetime.now(pytz.utc):
                    response['currentUserPlan'] = 'FREE'
                    response['expirationDate'] = ''
                    response['startDate'] = ''
                elif currentUserPlan is not None and datetime.now(pytz.utc) < currentUserPlan.expirationDate:
                    response['currentUserPlan'] = 'PRO'
                    response['expirationDate'] = str(currentUserPlan.expirationDate)
                    response['startDate'] = str(currentUserPlan.startDate)
                else:
                    response['message'] = 'Sorry, we could not retrieve data scientist userPlan data.'
            except:
                traceback.print_exc()
                return JsonResponse({"message": "Oops, something went wrong"})

            return JsonResponse(response, safe=False)
class payUserPlan(APIView):
    def post(self, request, format=None):
        logged_user = User.objects.all().get(pk=request.user.id)
        try:
            dataScientist = DataScientist.objects.all().get(user=logged_user)
        except:
            return JsonResponse({"message": "Only data scientists can update their user plan."})
        userPlanHistory = UserPlan.objects.filter(dataScientist=dataScientist).filter(isPayed=True).order_by('-expirationDate')
        currentUserPlan = None
        if 0 < userPlanHistory.count():
            currentUserPlan = userPlanHistory.first()
        startDate = None
        expirationDate = None
        try:
            nMonths = int(request.POST.get('nMonths'), 10)
        except:
            return JsonResponse({"message": "Sorry, but nMonths could not be correctly parsed."})
        if 24 < nMonths or currentUserPlan is not None and datetime.now(pytz.utc)+relativedelta(months=+24) < currentUserPlan.expirationDate+relativedelta(months=+nMonths):
            return JsonResponse({"message": "Sorry, but you cannot pay a user plan further than 24 month from now."})
        if currentUserPlan is None or currentUserPlan.expirationDate < datetime.now(pytz.utc):
            startDate = datetime.now(pytz.utc)
            expirationDate = startDate+relativedelta(months=+nMonths)
        elif currentUserPlan is not None and datetime.now(pytz.utc) < currentUserPlan.expirationDate:
            startDate = currentUserPlan.expirationDate
            expirationDate = startDate+relativedelta(months=+nMonths)
        else:
            return JsonResponse({"message": "There was an unexpected case when determining the period for the user plan."})

        try:
            new_userPlanPayment =  UserPlan.objects.create(dataScientist=dataScientist, type='PRO', startDate=startDate, expirationDate=expirationDate);
            response = {}
            response['message'] = "Successfully created or extended your user plan"
            response['userplan_pk'] = new_userPlanPayment.id
            return JsonResponse(response, safe=False)
        except:
            traceback.print_exc()
            return JsonResponse({"message": "Oops, something went wrong"})