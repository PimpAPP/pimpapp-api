from rest_framework import generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    AllowAny, IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import ModeratedModel
from .models import LatitudeLongitude
from .models import Carroceiro
from .models import Rating
from .models import Photo
from .models import Phone
from .models import Collect
from .models import Residue

from .serializers import RatingSerializer
from .serializers import PhotoSerializer
from .serializers import PhoneSerializer
from .serializers import CarroceiroSerializer
from .serializers import MaterialSerializer
from .serializers import LatitudeLongitudeSerializer
from .serializers import CollectSerializer
from .serializers import UserSerializer
from .serializers import ResidueSerializer
from .serializers import ResidueLocationSerializer
from .serializers import ResiduePhotoSerializer

public_status = (ModeratedModel.APPROVED, ModeratedModel.PENDING)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class CarroceiroViewSet(viewsets.ModelViewSet):
    """
        CarroceiroViewSet Routes:

        /api/carroceiro/
        /api/carroceiro/<pk>
        /api/carroceiro/<pk>/comments
        /api/carroceiro/<pk>/photos
        /api/carroceiro/<pk>/phones
        /api/carroceiro/<pk>/materials

    """
    serializer_class = CarroceiroSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Carroceiro.objects.all()

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
    def phones(self, request, pk=None):
        carroceiro = self.get_object()
        serializer = PhoneSerializer(carroceiro.phones, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def materials(self, request, pk=None):
        carroceiro = self.get_object()
        serializer = MaterialSerializer(carroceiro.materials)
        return Response(serializer.data)


class LatitudeLongitudeViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = LatitudeLongitudeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = LatitudeLongitude.objects.filter(
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


class MobileViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = PhoneSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Phone.objects.filter(
            moderation_status__in=public_status)


class RatingByCarroceiroViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
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


class PhotoByCarroceiroViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
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


class CollectViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = CollectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Collect.objects.filter(
            moderation_status__in=public_status)


class ResidueListAPIView(viewsets.ViewSetMixin, generics.ListAPIView):
    serializer_class = ResidueSerializer
    queryset = Residue.objects.filter()
    filter_backends = [SearchFilter, ]
    search_fields = ['id']


class ResidueCreateAPIView(viewsets.ViewSetMixin, generics.CreateAPIView):
    """
        curl -H "Content-Type: application/json" -X POST -d '{"description": "Via cURL",
        "materials": [1,2]}' http://localhost:8000/api/residues-create/
        -H 'Authorization: Token 6c77f484434be7c4512ab5ccf1458a1a4dc0a96f'

    """
    serializer_class = ResidueSerializer


class ResidueLocationCreateAPIView(viewsets.ViewSetMixin, generics.CreateAPIView):
    """
        curl -H "Content-Type: application/json" -X POST -d
        '{"moderation_status": "A", "mongo_hash": "Hash mongo by cURL",
        "latitude": 123, "longitude": 999, "reverse_geocoding": "reverse cURL",
        "residue": 4}' http://localhost:8000/api/residues-location-create/
        -H 'Authorization: Token 6c77f484434be7c4512ab5ccf1458a1a4dc0a96f'
    """
    serializer_class = ResidueLocationSerializer
    permission_classes = [AllowAny, ]


class ResiduePhotoCreateAPIView(viewsets.ViewSetMixin, generics.CreateAPIView):
    """
        curl -i -X POST -H "Content-Type: multipart/form-data" -F "full_photo=@/home/xtreme/gp.png" -F
        "moderation_status=A" -F "mongo_hash=hash" -F "author=1" -F "residue=1"
        http://localhost:8000/api/residues-photo-create/
        -H 'Authorization: Token 6c77f484434be7c4512ab5ccf1458a1a4dc0a96f'
    """
    serializer_class = ResiduePhotoSerializer
