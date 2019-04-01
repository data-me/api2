from django.shortcuts import render
import datetime, json, pytz, datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from http.client import HTTPResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from statsmodels.sandbox.distributions.sppatch import expect
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.models import Group,Permission

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Offer):
            return str(obj)
        return super().default(obj)


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

class Message_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            title = data['title']
            body = data['body']
            moment = datetime.datetime.utcnow()
            #receiverId = User.objects.all().get(user = data['receiverId'])
            username = data['username']
            receiver = User.objects.all().get(username = username)
            senderId = request.user
            print(senderId)

            new_message = Message.objects.create(title=title, body=body, moment=moment, receiver=receiver, sender=senderId)

            print('Sucessfully created new message')
            return JsonResponse({"message":"Successfully created new message"})
        except Exception as e:
            print(e)
            return JsonResponse({"message":"Oops, something went wrong"})
    def get(self, request, format=None):
        try:
            data = request.GET
            user = request.user
            messages = []
            try:
                messages = Message.objects.all().filter(receiver = user).values()
                print(messages)
            except:
                print("You have 0 messages")

            return JsonResponse(list(messages), safe=False)
        except:
            return JsonResponse({"message":"Oops, something went wrong"})


# Create your views here.

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

                    applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado).values()
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


class CV_view(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET
            secs = []
            logged_user = User.objects.all().get(pk = request.user.id)
            try:
                    #Ver mi CV
                    dataScientistRecuperado = DataScientist.objects.all().get(user = logged_user)
                    curriculum = CV.objects.all().filter(owner = dataScientistRecuperado).first()
                    sections = Section.objects.all().filter(cv = curriculum)
                    for sec in sections:
                        items = []
                        sec_items = Item.objects.all().filter(section = sec).values()
                        items.extend(sec_items)
                        secs.append({
                            'Section':str(sec),
                            'Section_Id':str(sec.id),
                            'Items':items
                        });

            except:
                    #Ver CV de otro
                    dataScientistId = data['dataScientistId']
                    dataScientistUserRecuperado = User.objects.all().get(pk = dataScientistId)
                    scientist = DataScientist.objects.all().get(user = dataScientistUserRecuperado)
                    curriculum = CV.objects.all().filter(owner = scientist).first()
                    sections = Section.objects.all().filter(cv = curriculum)
                    for sec in sections:
                        items = []
                        sec_items = Item.objects.all().filter(section = sec).values()
                        items.extend(sec_items)
                        secs.append({
                            'Section':str(sec),
                            'Section_Id':str(sec.id),
                            'Items':items
                        });

            return JsonResponse(list(secs), safe=False)

    def post(self, request, format=None):
        try:
            data = request.POST
            logged_user = DataScientist.objects.all().get(pk = request.user.datascientist.id)

            new_curriculum = CV.objects.create(owner=logged_user)

            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new curriculum')
            return JsonResponse({"message":"Successfully created new curriculum"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})

class Create_section_name(APIView):
    def post(self, request, format=None):
        try:
            if request.user.is_superuser or request.user.is_staff:
                data = request.POST

                new_section_name = Section_name.objects.create(name = data['name'])

                return JsonResponse({"message":"Successfully created new section name"})

            else:
                return JsonResponse({"message":"You do not have permission to perform this action"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})


class Section_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            sec = Section_name.objects.all().get(name = data['name'])

            logged_user = DataScientist.objects.all().get(pk = request.user.datascientist.id)

            cv = CV.objects.all().get(owner = logged_user)

            new_section = Section.objects.create(name = sec, cv = cv)

            return JsonResponse({"message":"Successfully created new section"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})

class Section_name_view(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET
            secnames = Section_name.objects.all().values()
            return JsonResponse(list(secnames), safe=False)


class Item_view(APIView):
    def post(self, request, format=None):
            try:
                data = request.POST

                secid = data['secid']

                section = Section.objects.all().get(pk = secid)

                logged_userid = request.user.datascientist.id

                if logged_userid == section.cv.owner.id:

                    date_start = data['datestart']
                    date_finish = request.POST.get('datefinish')

                    if date_finish != None:
                        if date_start < date_finish:

                            try:
                                item_tosave = Item.objects.all().get(pk = data['itemid'])

                                item_tosave.name = data['name']
                                item_tosave.description = data['description']
                                item_tosave.entity = data['entity']
                                item_tosave.date_start = date_start
                                item_tosave.date_finish = date_finish

                                item_tosave.save()

                                return JsonResponse({"message":"Successfully edited item"})
                            except:
                                itemname = data['name']
                                description = data['description']
                                entity = data['entity']

                                new_item = Item.objects.create(name = itemname, section = section, description = description, entity = entity, date_start = date_start, date_finish = date_finish)

                                return JsonResponse({"message":"Successfully created new item"})
                        else:
                            return JsonResponse({"message":"Sorry, the starting date must be before the ending date!"})
                    else:
                        try:
                            print('olawenas')
                            item_tosave = Item.objects.all().get(pk = data['itemid'])

                            item_tosave.name = data['name']
                            item_tosave.description = data['description']
                            item_tosave.entity = data['entity']
                            item_tosave.date_start = date_start

                            item_tosave.save()

                            return JsonResponse({"message":"Successfully edited item"})
                        except:
                            print('olawenas')
                            itemname = data['name']
                            description = data['description']
                            entity = data['entity']

                            new_item = Item.objects.create(name = itemname, section = section, description = description, entity = entity, date_start = date_start)

                            return JsonResponse({"message":"Successfully created new item"})
            except:
                return JsonResponse({"message":"Sorry! Something went wrong..."})

def populate(request):
    try:
        company = Group.objects.create(name='Company')
        dataScientist = Group.objects.create(name='DataScientist')

        admin = User.objects.create_user('admin', email='lennon@thebeatles.com', password='admin', is_staff=True)
        permissions = Permission.objects.all()
        for p in permissions:
            admin.user_permissions.add(p)
        data1 = User.objects.create_user(username='data1',email='data1@beatles.com',password='123456data1')
        data1.groups.add(dataScientist)

        data2 = User.objects.create_user(username='data2',email='data2@beatles.com',password='123456data2')
        data2.groups.add(dataScientist)

        company1 = User.objects.create_user(username='company1',email='company1@beatles.com',password='123456com1')
        company1.groups.add(company)

        company2 = User.objects.create_user(username='company2',email='company2@beatles.com',password='123456com2')
        company2.groups.add(company)

        dataScientist1 = DataScientist.objects.create(user = data1,name = "DataScientist 1",surname = "DS1")
        dataScientist2 = DataScientist.objects.create(user = data2,name = "DataScientist 2",surname = "DS2")

        company01 = Company.objects.create(user = company1, name = 'Company 1', description = 'Description 1',nif = 'nif1', logo = 'www.company1.com')
        company02 = Company.objects.create(user = company2, name = 'Company 2', description = 'Description 2',nif = 'nif2', logo = 'www.company2.com')

        return JsonResponse({'message': 'DB populated'})
    except:
        return JsonResponse({'Error': 'DB already populated'})

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
