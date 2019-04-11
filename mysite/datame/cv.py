from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView



class CV_view(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET
            secs = []
            logged_user = User.objects.all().get(pk = request.user.id)
            try:
                    #Ver CV de otro
                    dataScientistId = data['dataScientistId']
                    #thiscompany = Company.objects.all().filter(pk = companyId).values()
                    #dataScientistUserRecuperado = User.objects.all().get(pk = dataScientistId)
                    scientist = DataScientist.objects.all().get(pk = dataScientistId)
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


            except:
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

class Item_delete_view(APIView):
    def delete(self, request, item_id, format=None):
        try:
            logged_user = request.user
            datascientist = DataScientist.objects.all().get(user = logged_user)

            lookup_url_kwarg = "item_id"
            item = Item.objects.get(id = self.kwargs.get(lookup_url_kwarg))
            if (datascientist == item.section.cv.owner):
                item.delete()
                return JsonResponse({"message":"Successfully deleted item"})
            else:
                return JsonResponse({"message":"You do not own this offer"})
        except Exception as e:
            return JsonResponse({"message":"Sorry! Something went wrong..."})

class Section_delete_view(APIView):
    def delete(self, request, section_id, format=None):
        try:
            logged_user = request.user
            datascientist = DataScientist.objects.all().get(user = logged_user)

            lookup_url_kwarg = "section_id"
            section = Section.objects.get(id = self.kwargs.get(lookup_url_kwarg))
            if (datascientist == section.cv.owner):
                section.delete()
                return JsonResponse({"message":"Successfully deleted section"})
            else:
                return JsonResponse({"message":"You do not own this offer"})
        except Exception as e:
            return JsonResponse({"message":"Sorry! Something went wrong..."})

class Item_view(APIView):
    def post(self, request, format=None):
            try:
                data = request.POST

                secid = data['secid']

                section = Section.objects.all().get(pk = secid)

                logged_user = request.user.datascientist

                if logged_user == section.cv.owner:

                    date_start = data['datestart']
                    date_finish = request.POST.get('datefinish')

                    if date_finish != None:
                        if date_start < date_finish:

                            try:
                                item_tosave = Item.objects.all().get(id = data['itemid'])

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
