from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime, timedelta
import traceback
import pytz

class userPlanHistory(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET
            userPlanHistory = []
            logged_user = User.objects.all().get(pk = request.user.id)
            try:
                #List my userplan payments
                loggedDataScientist = DataScientist.objects.all().get(user=logged_user)
                userPlanHistory = UserPlan.objects.filter(dataScientist= loggedDataScientist).values()
                userPlanHistory.append({
                    'userId':str(logged_user.id),
                    'dataScientistId': str(loggedDataScientist.id),
                    'userPlanHistory':userPlanHistory.extend()
                })
            except:
                try:
                    # List userplan as administrator
                    assert loggedDataScientist.is_staff
                    dataScientist = DataScientist.objects.all().get(id=data['dataScientistId'])
                    userPlanHistory = UserPlan.objects.filter(dataScientist=loggedDataScientist).values()
                    userPlanHistory.append({
                        'userId': str(logged_user.id),
                        'dataScientistId': str(dataScientist.id),
                        'userPlanHistory': userPlanHistory.extend()
                    })
                except:
                    #Trying to list payment plan as a company will not return the said list
                    companyRecuperada = Company.objects.all().get(user=logged_user)
                    return JsonResponse({"message": "Sorry! As a company you cannot access to this DataScientist User Plan."})
            return JsonResponse(list(userPlanHistory), safe=False)

class currentUserPlan(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            response={}
            try:
                if request.user.id is not None:
                    dataScientist_user = User.objects.all().get(pk = request.user.id)
                    dataScientist = DataScientist.objects.all().get(user=dataScientist_user)
                else:
                    dataScientist = DataScientist.objects.all().get(user=request.GET['dataScientistId'])
            except:
                return JsonResponse({"message": "Sorry, there was a problem retrieving the Data Scientist"})
            try:
                print('Second Try')
                userPlanHistory = UserPlan.objects.filter(dataScientist=dataScientist).order_by('-expirationDate')
                print('Querying... ' + str( userPlanHistory ))
                response['dataScientistId'] = dataScientist.id
                print('Is there a saved user plan?' + str(userPlanHistory.count()))
                if 0 < userPlanHistory.count():
                    print('There is at least one userPlan payment.')
                    currentUserPlan = userPlanHistory.first()
                    print('The currentUserPlan was assigned.')

                print('Any problem reaching the ifs?')
                print('Structure of a UserPlan' + str(currentUserPlan))
                print('Is current userPlan None' + str(currentUserPlan is None))
                try:
                    print('currentUserPlan is expired? ' + str(currentUserPlan.expirationDate < datetime.now(pytz.utc)))
                except:
                    traceback.print_exc()
                print('Is current userPlan None or currentUserPlan is expired? ' + str(currentUserPlan is None or currentUserPlan.expirationDate < datetime.datetime.now()))
                if currentUserPlan is None or currentUserPlan.expirationDate < datetime.now(pytz.utc):
                    print('The case when is a FREE user')
                    response['currentUserPlan'] = 'FREE'
                    response['expirationDate'] = ''
                    response['startDate'] = ''
                elif (currentUserPlan is not None and datetime.now() < currentUserPlan.expirationDate):
                    print('The case when is a PRO user' + str(currentUserPlan))
                    response['currentUserPlan'] = 'PRO'
                    response['expirationDate'] = str(currentUserPlan.expirationDate)
                    response['startDate'] = str(currentUserPlan.startDate)
                else:
                    response['message'] = 'Oops, something went wrong'
            except:
                return JsonResponse({"message": "Oops, something went wrong"})

            return JsonResponse(response, safe=False)
