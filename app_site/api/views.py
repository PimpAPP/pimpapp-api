from rest_framework import generics
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
from .models import LatitudeLongitude
from .models import Catador

from .models import RatingCatador
from .models import RatingCooperative

from .models import PhotoCatador
from .models import PhotoCollectUser
from .models import PhotoCollectCatador

from .models import MobileCatador
from .models import MobileCooperative

from .models import Mobile
from .models import Rating
from .models import Collect
from .models import Residue
from .models import Cooperative

from .serializers import RatingSerializer
#from .serializers import PhotoSerializer
from .serializers import MobileSerializer
from .serializers import CatadorSerializer
from .serializers import MaterialSerializer
from .serializers import LatitudeLongitudeSerializer
from .serializers import CollectSerializer
from .serializers import UserSerializer
from .serializers import ResidueSerializer
from .serializers import CooperativeSerializer

from .permissions import IsObjectOwner, IsCatadorOrCollectOwner

public_status = (ModeratedModel.APPROVED, ModeratedModel.PENDING)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PermissionBase(APIView):
    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS', 'HEAD', 'POST']:
            self.permission_classes = [IsAuthenticated]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsObjectOwner]

        return super(PermissionBase, self).get_permissions()


def create_new_comment(data):
    comment = Rating(comment=data['comment'], author_id=data['author'],
                     rating=data['rating'],
                     carroceiro_id=data['carroceiro'])
    return comment.save()


class CarroceiroViewSet(viewsets.ModelViewSet):
    """
        CatadorViewSet Routes:

        /api/carroceiro/
        /api/carroceiro/<pk>
        /api/carroceiro/<pk>/comments (GET, POST, PUT, PATCH, DELETE) pass pk parameter
        /api/carroceiro/<pk>/photos
        /api/carroceiro/<pk>/phones
        /api/carroceiro/<pk>/materials

    """
    serializer_class = CatadorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Catador.objects.all()

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

    #@detail_route(methods=['get'])
    #def photos(self, request, pk=None):
    #    catador = self.get_object()
    #    serializer = PhotoSerializer(catador.photos, many=True)
    #    return Response(serializer.data)

    @detail_route(methods=['get'])
    def phones(self, request, pk=None):
        catador = self.get_object()
        serializer = MobileSerializer(catador.phones, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def materials(self, request, pk=None):
        catador = self.get_object()
        serializer = MaterialSerializer(catador.materials)
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


#class PhotoViewSet(viewsets.ModelViewSet):
#    """
#        DOCS: TODO
#    """
#    serializer_class = PhotoSerializer
#    permission_classes = (IsAuthenticatedOrReadOnly,)
#    queryset = Photo.objects.filter(
#        moderation_status__in=public_status)


class MobileViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = MobileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Mobile.objects.filter(
        moderation_status__in=public_status)


class RatingByCarroceiroViewSet(PermissionBase, viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = RatingSerializer

    def get_queryset(self):
        catador = self.kwargs['catador']
        queryset = Rating.objects.filter(
            moderation_status__in=public_status,
            carroceiro__id=carroceiro)


#class PhotoByCatadorViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
#    """
#        DOCS: TODO
#    """
#    serializer_class = PhotoSerializer
#    permission_classes = (IsAuthenticatedOrReadOnly,)
#
#    def get_queryset(self):
#        catador = self.kwargs['catador']
#        queryset = Photo.objects.filter(
#            moderation_status__in=public_status,
#            carroceiro__id=carroceiro)


class CollectViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = CollectSerializer
    permission_classes = (IsCatadorOrCollectOwner, IsAuthenticated)
    queryset = Collect.objects.filter(
        moderation_status__in=public_status)


class ResidueViewSet(PermissionBase, viewsets.ModelViewSet):
    serializer_class = ResidueSerializer
    queryset = Residue.objects.filter()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'description', 'user']


class CooperativeViewSet(PermissionBase, viewsets.ModelViewSet):
    serializer_class = CooperativeSerializer
    queryset = Cooperative.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'id']
    ordering_fields = ['name', 'email', 'id']
