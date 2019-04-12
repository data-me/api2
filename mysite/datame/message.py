import pytz, datetime
from .models import *
from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.views import APIView

#para dashboard
class Messages_view(APIView):
    def get(self, request, format=None):
        user_logged = User.objects.all().get(pk = request.user.id)
        if (user_logged.is_superuser or user_logged.is_staff):
            try:    
                messages = Message.objects.all().values()
                return JsonResponse(list(messages), safe=False)
            except:
                print("there are no messages")
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
            isAlert = False
            receiver = User.objects.all().get(username = username)
            senderId = request.user
            print('Messager senderId =>', senderId)

            new_message = Message.objects.create(title=title, body=body, moment=moment, receiver=receiver, sender=senderId, isAlert= isAlert)

            return JsonResponse({"message":"Successfully created new message"})
        except Exception as e:
            print(e)
            return JsonResponse({"message":"El usuario no existe / User doesn't exists"})
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
        