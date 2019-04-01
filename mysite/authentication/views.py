from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HelloWorld(APIView):
    def get(self, request, format=None):
        saludo = 'Hola, ' + str(request.user) + '!'
        return Response({'saludo':saludo})