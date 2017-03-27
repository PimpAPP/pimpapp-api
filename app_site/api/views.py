from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, \
    AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import ModeratedModel
from .models import Catador
from .models import LatitudeLongitude
from .models import MobileCatador
from .models import Rating
from .models import Collect
from .models import Residue
from .models import Cooperative
from .models import GeorefCatador
from .models import Mobile
from .models import PhotoResidue

from .serializers import RatingSerializer
from .serializers import MobileSerializer
from .serializers import CatadorSerializer
from .serializers import MaterialSerializer
from .serializers import CollectSerializer
from .serializers import UserSerializer
from .serializers import ResidueSerializer
from .serializers import CooperativeSerializer
from .serializers import LatitudeLongitudeSerializer
from .serializers import PhotoResidueSerializer

from .permissions import IsObjectOwner, IsCatadorOrCollectOwner

from .pagination import PostLimitOffSetPagination

public_status = (ModeratedModel.APPROVED, ModeratedModel.PENDING)


class PermissionBase(APIView):
    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS', 'HEAD', 'POST']:
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsObjectOwner]

        return super(PermissionBase, self).get_permissions()


class RecoBaseView(PermissionBase):
    pagination_class = PostLimitOffSetPagination


class UserViewSet(RecoBaseView, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


def create_new_comment(data):
    comment = Rating(comment=data['comment'], author_id=data['author'],
                     rating=data['rating'],
                     carroceiro_id=data['carroceiro'])
    return comment.save()


class CatadorViewSet(viewsets.ModelViewSet):
    """
        CatadorViewSet Routes:

        /api/catadores/
        /api/catadores/<pk>
        /api/catadores/<pk>/comments (GET, POST, PUT, PATCH, DELETE) pass pk parameter
        /api/catadores/<pk>/georef (GET, POST)
        /api/catadores/<pk>/phones (GET, POST, DELETE)

    """
    serializer_class = CatadorSerializer
    permission_classes = (IsObjectOwner,)
    queryset = Catador.objects.all()
    pagination_class = PostLimitOffSetPagination

    @detail_route(methods=['GET', 'POST'],
                  permission_classes=[IsObjectOwner])
    def georef(self, request, pk=None):
        """
        Get all geolocation from one Catador
        :param request:
        :param pk:
        :return:
        """
        if request.method == 'POST':
            data = request.data

            georeference = LatitudeLongitude.objects.create(
                latitude=data.get('latitude'),
                longitude=data.get('longitude'))

            GeorefCatador.objects.create(
                georef=georeference, catador=self.get_object())

        serializer = LatitudeLongitudeSerializer(
            self.get_object().geolocation, many=True)

        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
                  permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        catador = self.get_object()

        data = request.data

        if request.method in ['POST', 'PUT', 'PATCH']:
            defaults = {'comment': data.get('comment'),
                        'author_id': data.get('author'),
                        'rating': data.get('rating'),
                        'carroceiro_id': data.get('carroceiro')
                        }
            catador.comments.update_or_create(defaults, id=data.get('pk'))

        if request.method == 'DELETE':
            rating = get_object_or_404(
                Rating, pk=data.get('pk'), author_id=data.get('author'),
                carroceiro_id=data.get('carroceiro')
            )
            rating.delete()

        serializer = RatingSerializer(catador.comments, many=True)
        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST', 'PUT', 'DELETE'])
    def phones(self, request, pk=None):
        catador = self.get_object()
        data = request.data

        if request.method == 'POST':
            m = Mobile.objects.create(
                phone=data.get('phone'), mno=data.get('mno'),
                has_whatsapp=data.get('has_whatsapp', False),
                mobile_internet=data.get('mobile_internet', False),
                notes=data.get('notes')
            )
            MobileCatador.objects.create(mobile=m, catador=catador)
        elif request.method == 'DELETE':
            Mobile.objects.get(id=data.get('id')).delete()

        serializer = MobileSerializer(catador.phones, many=True)

        return Response(serializer.data)

    @detail_route(methods=['get'])
    def materials(self, request, pk=None):
        catador = self.get_object()
        serializer = MaterialSerializer(catador.materials)
        return Response(serializer.data)


class RatingViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Rating.objects.filter(
        moderation_status__in=public_status)
    pagination_class = PostLimitOffSetPagination


class RatingByCarroceiroViewSet(RecoBaseView, viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = RatingSerializer

    def get_queryset(self):
        catador = self.kwargs['catador']
        queryset = Rating.objects.filter(
            moderation_status__in=public_status,
            carroceiro__id=Catador(user=self.request.user))


class CollectViewSet(RecoBaseView, viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = CollectSerializer
    permission_classes = (IsCatadorOrCollectOwner, IsAuthenticated)
    queryset = Collect.objects.filter(
        moderation_status__in=public_status)


class ResidueViewSet(RecoBaseView, viewsets.ModelViewSet):
    serializer_class = ResidueSerializer
    queryset = Residue.objects.filter()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'description', 'user']

    @detail_route(methods=['GET', 'POST'],
                  permission_classes=[IsObjectOwner])
    def photos(self, request, pk=None):
        """
        Get all geolocation from one Catador
        :param request:
        :param pk:
        :return:
        """

        residue = self.get_object()

        if request.method == 'POST':
            data = request.data
            photo = request.FILES['full_photo']

            PhotoResidue.objects.create(
                author=request.user, residue=residue, full_photo=photo)

        serializer = PhotoResidueSerializer(residue.residue_photos, many=True)

        return Response(serializer.data)


class CooperativeViewSet(RecoBaseView, viewsets.ModelViewSet):
    serializer_class = CooperativeSerializer
    queryset = Cooperative.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'id']
    ordering_fields = ['name', 'email', 'id']
