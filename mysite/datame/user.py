from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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


class Register_view(APIView):
    #permission_classes = (~IsAuthenticated,)
    def post(self, request, format=None):
        try:
            data = request.POST
            type = data['type']
            username = data['username']
            password = data['password']
            name = data['name']
            if (User.objects.filter(username = username).exists()):
                    res = JsonResponse({"message":"Sorry, username already exists"})
            else:
                if (type == 'DS'):
                    group = Group.objects.get(name = 'DataScientist')
                    surname = data['surname']
                    photo = data['photo']
                    address = data['address']
                    phone = data['phone']
                    email = data['email']
                    newUser = User.objects.create(username = username, password = password)
                    newUser.set_password(password)
                    newUser.groups.add(group)
                    newUser.save()
                    newDs = DataScientist.objects.create(user = newUser, name = name, surname = surname, photo = photo, address = address,email = email, phone = phone)
                    CV.objects.create(owner = newDs)
                    res = JsonResponse({"message":"Successfully created new Data Scientist. Welcome!"})

                    print('Creating a NEW DS alert message for adming user')
            
                    # Alert message
                    title = '[ALERT MESSAGE] New data scientist was registered'
                    body = 'Data scientist with DsID: '+str(newDs.id)+' was registered'
                    moment = datetime.datetime.utcnow()
                    username = 'admin'
                    isAlert = True
                    receiver = User.objects.all().get(username = username)
                    senderId = request.user

                    new_message = Message.objects.create(title=title, body=body, moment=moment, receiver=receiver, sender=senderId, isAlert= isAlert)

                    print('Sucessfully created new alert message')
                    
                if (type == 'C'):
                    group = Group.objects.get(name = 'Company')
                    description = data['description']
                    nif = data['nif']
                    logo = data['logo']
                    newUser = User.objects.create(username = username, password = password)
                    newUser.set_password(password)
                    newUser.groups.add(group)
                    newUser.save()
                    newC = Company.objects.create(user = newUser, name = name, description = description, nif = nif, logo = logo)
                    res = JsonResponse({"message":"Successfully created Company. Welcome!"})

                    print('Creating a NEW COMPANY alert message for adming user')
            
                    # Alert message
                    title = '[ALERT MESSAGE] New company was registered'
                    body = 'Company with CompanyID: '+str(newC.id)+' was registered'
                    moment = datetime.datetime.utcnow()
                    username = 'admin'
                    isAlert = True
                    receiver = User.objects.all().get(username = username)
                    senderId = request.user

                    new_message = Message.objects.create(title=title, body=body, moment=moment, receiver=receiver, sender=senderId, isAlert= isAlert)

                    print('Sucessfully created new alert message')
            return res
        except Exception as e:
            return JsonResponse({"message":"Oops, something went wrong" + str(e)})

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
