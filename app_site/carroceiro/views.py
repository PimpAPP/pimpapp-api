from .models import Carroceiro
from .models import CarroceiroAlreadyExistsException
from .serializers import CarroceiroSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from geopy.distance import vincenty


class CarroceirosList(generics.ListAPIView):
    """
    List all Carroceiros and/or Create a new Carroceiro.
    This view allows filtering by the attributes "type" and "phone"
    """
    queryset = Carroceiro.objects.all()
    serializer_class = CarroceiroSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('type', 'phone')

    def post(self, request, format=None):
        serializer = CarroceiroSerializer(data=request.data)
        # regex validation first
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except CarroceiroAlreadyExistsException:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarroceiroRadiusFilter(APIView):
    """
    List all Carroceiros who are within a certain radius in kilometers given the user's latitude and longitude which
    is the reference point to calculte this radius filter.
    """
    def get(self, request, lat_1, long_1, radius, format=None):
        try:
            carroceiro_full_list = Carroceiro.objects.all()
            carroceiro_list_serializer = CarroceiroSerializer(self.filterWithinRadius(carroceiro_full_list, lat_1, long_1, radius), many=True)
            return Response(carroceiro_list_serializer.data)
        except Carroceiro.DoesNotExist:
            raise Http404

    def filterWithinRadius(self, carroceiro_list, lat1, long1, radius):
        filter_carroceiro_list = []
        for c in carroceiro_list:
            (lat_aux, long_aux) = (c.latitude, c.longitude)
            if vincenty((lat_aux, long_aux), (lat1, long1)).km <= float(radius):
                filter_carroceiro_list.append(c)
        return filter_carroceiro_list


class CarroceiroDetail(APIView):
    """
    Update, Retrieve and Delete a instance of Carroceiro given their id.
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


