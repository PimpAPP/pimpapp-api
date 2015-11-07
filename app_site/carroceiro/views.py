from .models import Carroceiro
from .models import CarroceiroAlreadyExistsException
from .serializers import CarroceiroSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status


class CarroceirosList(APIView):
    """
    List all Carroceiros and/or Create a new Carroceiro.
    """
    def get(self, request, format=None):
        carroceiros = Carroceiro.objects.all()
        serializer = CarroceiroSerializer(carroceiros, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CarroceiroSerializer(data=request.data)
        # regex validation first
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except CarroceiroAlreadyExistsException:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarroceiroFindByPhone(APIView):
    """
    List all Carroceiros given their cellphone.
    It's assumed that a Carroceiro can have multiple addresses, hence one cellphone would have multiple entries .
    """
    def get(self, request, phone, format=None):
        try:
            carroceiro_list = Carroceiro.objects.filter(phone=phone)
            carroceiro_list_serializer = CarroceiroSerializer(carroceiro_list, many=True)
            return Response(carroceiro_list_serializer.data)
        except Carroceiro.DoesNotExist:
            raise Http404

class CarroceiroDetail(APIView):
    """
    Update ,Retrieve and Delete a instance of Carroceiro given their id.
    """
    def get(self, request, id, format=None):
        try:
            carroceiro = Carroceiro.objects.get(id=id)
            carroceiro = CarroceiroSerializer(carroceiro)
            return Response(carroceiro.data)
        except Carroceiro.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        try:
            carroceiro = Carroceiro.objects.get(id=id)
            carroceiro.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Carroceiro.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        carroceiro = Carroceiro.objects.get(id=id)
        serializer = CarroceiroSerializer(carroceiro, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except CarroceiroAlreadyExistsException:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


