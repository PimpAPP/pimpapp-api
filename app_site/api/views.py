from django.shortcuts import render

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Authorship
from .models import ProfileInfo
from .models import Carroceiro
from .models import Rating
from .models import Photo

from .serializers import ProfileInfoSerializer
from .serializers import RatingSerializer
from .serializers import PhotoSerializer
from .serializers import CarroceiroSerializer

public_status = (Authorship.APPROVED, Authorship.PENDING)

class CarroceiroViewSet(viewsets.ModelViewSet):
    """
        DOCS: CarroceiroViewSet -> TODO
    """
    serializer_class = CarroceiroSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Carroceiro.objects.all()


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
