from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView


class User_view(APIView):
    def get(self, request, format=None):
        try:
            data = request.GET
            user = request.user
            users = []
            try:
                users = User.objects.all().values('username')
                print(users)
            except:
                print("There are no users")

            return JsonResponse(list(users), safe=False)
        except:
            return JsonResponse({"message":"Oops, something went wrong"})


class Company_view(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET
            logged_user = User.objects.all().get(pk = request.user.id)
            print('logged_user: ' + str(logged_user))
            #company = []
            try:
                    companyRecuperada = Company.objects.all().get(user = logged_user)
                    thiscompany = Company.objects.all().filter(user = logged_user).values()
            except:
                    companyId = data['companyId']
                    companyUserRecuperado = User.objects.all().get(pk = companyId)
                    print('company user recuperada: ' + str(companyUserRecuperado))
                    thiscompany = Company.objects.all().filter(user = companyUserRecuperado).values()
                    print('company recuperada: ' + str(thiscompany))


            return JsonResponse(list(thiscompany), safe=False)




class whoami(APIView):
    def get(self, request, format=None):
            try:
                request.user.datascientist
                return JsonResponse({'user_type': 'ds'})
            except:
                try:
                    request.user.company
                    return JsonResponse({'user_type': 'com'})
                except:
                    return JsonResponse({'user_type': 'None'})
