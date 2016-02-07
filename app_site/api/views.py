from django.shortcuts import render

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Authorship
from .models import ProfileInfo
from .models import Carroceiro
from .models import Rating
from .models import Photo

from .serializers import ProfileInfoSerializer
from .serializers import RatingSerializer
from .serializers import PhotoSerializer
from .serializers import CarroceiroSerializer
from .serializers import MaterialSerializer

public_status = (Authorship.APPROVED, Authorship.PENDING)

class CarroceiroViewSet(viewsets.ModelViewSet):
    """
        CarroceiroViewSet Routes:

        /api/carroceiro/
        /api/carroceiro/<pk>
        /api/carroceiro/<pk>/profile_info
        /api/carroceiro/<pk>/comments
        /api/carroceiro/<pk>/photos
        /api/carroceiro/<pk>/materials

    """
    serializer_class = CarroceiroSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Carroceiro.objects.all()

    @detail_route(methods=['get'])
    def profile_info(self, request, pk=None):
        carroceiro = self.get_object()
        serializer =  ProfileInfoSerializer(carroceiro.profile_info)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def comments(self, request, pk=None):
        carroceiro = self.get_object()
        serializer =  RatingSerializer(carroceiro.comments, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def photos(self, request, pk=None):
        carroceiro = self.get_object()
        serializer = PhotoSerializer(carroceiro.photos, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def materials(self, request, pk=None):
        carroceiro = self.get_object()
        serializer = MaterialSerializer(carroceiro.materials)
        return Response(serializer.data)


class ProfileInfoViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = ProfileInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ProfileInfo.objects.filter(
            moderation_status__in=public_status)

class RatingViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Rating.objects.filter(
            moderation_status__in=public_status)


class PhotoViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Photo.objects.filter(
            moderation_status__in=public_status)


class RatingByCarroceiroViewSet(generics.ListAPIView):
    """
        DOCS: TODO
    """
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        carroceiro = self.kwargs['carroceiro']
        queryset = Rating.objects.filter(
                moderation_status__in=public_status,
                carroceiro__id=carroceiro)


class PhotoByCarroceiroViewSet(generics.ListAPIView):
    """
        DOCS: TODO
    """
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        carroceiro = self.kwargs['carroceiro']
        queryset = Photo.objects.filter(
                moderation_status__in=public_status,
                carroceiro__id=carroceiro)
