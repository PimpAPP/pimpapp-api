from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ProfileInfo
from .models import Rating
from .models import Photo

#from .models.Authorship import APPROVED
#from .models.Authorship import PENDING
from .models import Authorship

from .serializers import ProfileInfoSerializer
from .serializers import RatingSerializer
from .serializers import PhotoSerializer

public_status = (Authorship.APPROVED, Authorship.PENDING)

class ProfileInfoViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = ProfileInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'carroceiro'
    queryset = ProfileInfo.objects.filter(
            moderation_status__in=public_status)


class RatingViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'carroceiro'
    queryset = Rating.objects.filter(
            moderation_status__in=public_status)


class PhotoViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'carroceiro'
    queryset = Photo.objects.filter(
            moderation_status__in=public_status)
