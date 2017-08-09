from rest_framework import serializers
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, HttpResponse
from base64 import b64decode
from django.core.files.base import ContentFile
import uuid

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
from .models import Material
from .models import GeorefResidue
from .models import PhotoCollectCatador
from .models import PhotoCollectUser
from .models import RatingCatador
from .models import RatingCooperative
from .models import UserProfile

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
from .serializers import PhotoCollectCatadorSerializer
from .serializers import PhotoCollectUserSerializer
from .serializers import CatadorsPositionsSerializer
from .serializers import PasswordSerializer

from .permissions import IsObjectOwner

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


class UserViewSet(viewsets.ModelViewSet):
    '''
        Endpoint used to create, update and retrieve users
        Allow: GET, POST, UPDATE, OPTIONS
    '''
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'update', 'options']

    @detail_route(methods=['POST'])
    def photos(self, request, pk=None):
        """
        Get all PHOTOS from one Residue, and enables to upload photos
        to the residue in question
        """
        user = self.get_object()

        if request.method == 'POST':
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
            elif request.data['avatar']:
                data = request.data['avatar']
                avatar = base64ToFile(data)

            UserProfile.objects.create(user=user, avatar=avatar)

        return HttpResponse()

    @detail_route(methods=['POST'])
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer_context = {
            'request': request,
        }
        serializer = UserSerializer(user, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)


@detail_route(methods=['post'])
def set_password(self, request, pk=None):
    """
    Set a users password via thew api
    :param request:
    :param pk:
    :return:
    """

    user = self.get_object()
    serializer = PasswordSerializer(data=request.data)
    if serializer.is_valid():
        if user.check_password(serializer.data['old_password']):
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'content_type': 'Password set'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'content_type': 'Current password incorrect'},
                            status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


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
        /api/catadores/<pk>/comments (GET, POST, PUT, PATCH, DELETE) pass
        pk parameter
        /api/catadores/<pk>/georef (GET, POST)
        /api/catadores/<pk>/phones (GET, POST, DELETE)

    """

    serializer_class = CatadorSerializer
    permission_classes = (IsObjectOwner,)
    queryset = Catador.objects.all()
    http_method_names = ['get', 'post', 'update', 'options', 'patch', 'delete']

    @detail_route(methods=['GET', 'POST'],permission_classes=[])
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

    @detail_route(methods=['GET', 'POST', 'DELETE', 'OPTIONS'],
                  permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        catador = self.get_object()

        data = request.data

        if request.method in ['POST']:
            rating = Rating.objects.create(
                comment=data.get('comment'), author=request.user,
                rating=data.get('rating'))

            RatingCatador.objects.create(catador=catador, rating=rating)

        if request.method == 'DELETE':
            rating = get_object_or_404(
                Rating, pk=data.get('pk'), author_id=request.user)
            rating.delete()

        serializer = RatingSerializer(catador.comments, many=True)
        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST', 'PUT', 'DELETE'], permission_classes=[])
    def phones(self, request, pk=None):
        catador = self.get_object()
        if request.method == 'POST' and request.data:
            for phone in request.data:
                if phone.get('phone') and phone.get('mno'):
                    m = Mobile.objects.create(
                        phone=phone.get('phone'),
                        mno=phone.get('mno'),
                        has_whatsapp=bool(phone.get('whatsapp', False))
                    )
                    MobileCatador.objects.create(mobile=m, catador=catador)
        elif request.method == 'DELETE' and request.data:
            for phone in request.data:
                Mobile.objects.get(id=phone.get('id')).delete()

        serializer = MobileSerializer(catador.phones, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def materials(self, request, pk=None):
        catador = self.get_object()
        serializer = MaterialSerializer(catador.materials)
        return Response(serializer.data)


# Analise and see if we have to keep this view
class RatingViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
    """
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Rating.objects.filter(
        moderation_status__in=public_status)
    pagination_class = PostLimitOffSetPagination


# Analise and see if we have to keep this view
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


class CollectViewSet(viewsets.ModelViewSet):
    """
        DOCS: TODO
        api/accept_collet/ (POST, GET)
        api/photo_catador/ (POST, GET)
        api/photo_user/ (POST, GET)
    """
    serializer_class = CollectSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Collect.objects.filter()
    http_method_names = ['get', 'options', 'post']

    @detail_route(methods=['POST'])
    def accept_collect(self, request, pk):
        collect = self.get_object()
        catador = Catador.objects.get(user=request.user)
        collect.catador = catador
        collect.save()
        return HttpResponse()

    @detail_route(methods=['POST'])
    def catador_confirms(self, request, pk):
        collect = self.get_object()

        'TODO: MOVER REGRA DE NEGOCIO PARA O MODEL'
        if collect.catador.user != request.user:
            raise serializers.ValidationError(
                'Apenas o catador da coleta pode confirmar.')

        collect.catador_confirms = True
        collect.save()
        return HttpResponse()

    @detail_route(methods=['POST'])
    def user_confirms(self, request, pk):
        collect = self.get_object()

        'TODO: MOVER REGRA DE NEGOCIO PARA O MODEL'
        if collect.residue.user != request.user:
            raise serializers.ValidationError(
                'Apenas o usuário que abriu a coleta pode confirmar.')

        collect.user_confirms = True
        collect.save()
        return HttpResponse()

    @detail_route(methods=['GET', 'POST'])
    def photos_catador(self, request, pk=None):
        """
        Get all PHOTOS from one Collect, and enables the catador
        to upload photos to the collect in question
        """

        collect = self.get_object()

        if request.method == 'POST':
            data = request.data
            photo = request.FILES['full_photo']

            PhotoCollectCatador.objects.create(
                author=request.user, coleta=collect, full_photo=photo)

        serializer = PhotoCollectCatadorSerializer(
            collect.photo_collect_catador, many=True)

        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST'])
    def photos_user(self, request, pk=None):
        """
        Get all PHOTOS from one Collect, and enables the user to upload photos
        to the collect in question
        """

        collect = self.get_object()

        if request.method == 'POST':
            data = request.data
            photo = request.FILES['full_photo']

            PhotoCollectUser.objects.create(
                author=request.user, coleta=collect, full_photo=photo)

        serializer = PhotoCollectUserSerializer(collect.photo_collect_catador,
                                                many=True)

        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def change_status(self, request, pk=None):
        """
        Update status
        """

        collect = self.get_object()

        if request.method == 'POST':
            data = request.data
            status = data.get('status')
            collect.status = status
            collect.save()

        return HttpResponse()


class ResidueViewSet(RecoBaseView, viewsets.ModelViewSet):
    """
        Endpoint used to create, update and retrieve residues
        Allow: GET, POST, UPDATE, OPTIONS

        /api/residues/
        /api/residues/<pk>/
        /api/residues/<pk>/photos/
        /api/residues/<pk>/georef/
    """
    serializer_class = ResidueSerializer
    queryset = Residue.objects.filter()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'description', 'user']
    http_method_names = ['get', 'post', 'update', 'options', 'patch']

    @detail_route(methods=['GET', 'POST'],
                  permission_classes=[IsObjectOwner])
    def photos(self, request, pk=None):
        """
        Get all PHOTOS from one Residue, and enables to upload photos
        to the residue in question
        """
        residue = self.get_object()

        if request.method == 'POST':
            if request.FILES.get('full_photo'):
                photo = request.FILES['full_photo']
            else:
                photo = base64ToFile(request.data['full_photo'])

            PhotoResidue.objects.create(
                author=request.user, residue=residue, full_photo=photo)

        serializer = PhotoResidueSerializer(residue.residue_photos, many=True)

        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST', 'UPDATE'],
                  permission_classes=[IsObjectOwner])
    def georef(self, request, pk):
        if request.method == 'POST':
            data = request.data

            georeference = LatitudeLongitude.objects.create(
                latitude=data.get('latitude'),
                longitude=data.get('longitude'))

            GeorefResidue.objects.create(
                georef=georeference, residue=self.get_object())

        serializer = LatitudeLongitudeSerializer(
            self.get_object().residue_location)

        return Response(serializer.data)


class CooperativeViewSet(RecoBaseView, viewsets.ModelViewSet):
    serializer_class = CooperativeSerializer
    queryset = Cooperative.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'id']
    ordering_fields = ['name', 'email', 'id']
    http_method_names = ['get', 'post', 'update', 'patch', 'options', 'delete']

    @detail_route(methods=['GET', 'POST', 'DELETE', 'OPTIONS'],
                  permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        cooperative = self.get_object()

        data = request.data

        if request.method in ['POST']:
            rating = Rating.objects.create(
                comment=data.get('comment'), author=request.user,
                rating=data.get('rating'))

            RatingCooperative.objects.create(catador=cooperative, rating=rating)

        if request.method == 'DELETE':
            rating = get_object_or_404(
                Rating, pk=data.get('pk'), author_id=request.user)
            rating.delete()

        serializer = RatingSerializer(cooperative.comments, many=True)
        return Response(serializer.data)


class MaterialsViewSet(RecoBaseView, viewsets.ModelViewSet):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'id']
    ordering_fields = ['name', 'id']
    http_method_names = ['get', 'options']


class NearestCatadoresViewSet(viewsets.ModelViewSet):
    serializer_class = CatadorsPositionsSerializer
    queryset = Catador.objects.all()


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        return Response({'token': token.key, 'id': token.user_id})


def base64ToFile(data):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    name = str(uuid.uuid4()) + '.' + ext
    avatar = ContentFile(b64decode(imgstr), name=name)

    return avatar


def importCsv():
    import csv
    import os.path
    file_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'api/catadores.csv')

    with open(file_directory, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print('Importando a linha com o ID: ' + str(row['catador_id']))

            try:
                if row['nickname']:
                    row['nickname'] = row['nickname']\
                        .translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})
                else:
                    row['nickname'] = row['name'] \
                        .translate({ord(c): "_" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+ "})

                user = User.objects.create_user(username=row['nickname'],
                                                email=row['email'],
                                                password=row['senha'],
                                                first_name=row['name'])

                # Alguns campos existem no mobile mas não existem na API
                catador = Catador.objects.create(
                    user=user,
                    name=row['name'],
                    nickname=row['nickname'],
                    minibio=row['apresentacao'],#historia e/ou apresentacao no csv
                    address_base=row['endereco'],
                    region=row['regiao'],
                    kg_week=int(row['quilos_dia_coleta']) * 6,
                    #how_many_years_work=int(row['anos_coleta']), # Esse campo não existe
                    #cooperative_name=row['cooperativa'], # Esse campo não existe
                    safety_kit=bool(int(row['carroca_seguranca'])),
                    has_motor_vehicle=bool(int(row['carroca_motor'])))
                    #has_smartphone_with_internet=bool(int(row['carroca_internet'])) # Esse campo não existe

                catador.save()

                if row['materiais_coleta']:
                    materials = row['materiais_coleta'][1:][:-1].replace('"', '').split(',')
                    for material in materials:
                        material_id = get_material_id(material)
                        catador.materials_collected.add(material_id)
                    catador.save()

                if row['foto']:
                    UserProfile.objects.create(user=user, avatar=row['foto'])

                if row['telefone1']:
                    mobile = Mobile.objects.create(
                        phone=row['telefone1'],
                        mno=get_operadora(row['operadora1']),
                        has_whatsapp=bool(int(row['whatsapp'])))

                    mobile_catador = MobileCatador.objects.create(catador=catador, mobile=mobile)
                    mobile_catador.save()

                if row['telefone2']:
                    mobile2 = Mobile.objects.create(
                        phone=row['telefone2'],
                        mno=get_operadora(row['operadora2']),
                        has_whatsapp=bool(int(row['whatsapp2'])))

                    mobile_catador2 = MobileCatador.objects.create(catador=catador, mobile=mobile2)
                    mobile_catador2.save()

            except:
                print('Erro ao importar a linha com o ID: ' + str(row['catador_id']))


def get_operadora(operadora):
    return {
        'tim': 'T',
        'vivo': 'V',
        'claro': 'C',
        'oi': 'O',
        'nextel': 'N',
        'porto': 'P'
    }[operadora.lower()]


def get_material_id(material):
    # Definindo "outros" como default
    return {
        'outros': 12,
        'entulho': 11,
        'mu00f3veis': 10,
        'bateria': 9,
        'eletru00f4nicos': 8,
        'u00f3leos': 7,
        'metais': 6,
        'plu00e1stico': 5,
        'papel': 4,
        'misturado': 3,
        'latas': 2,
        'vidro': 1
    }.get(material.lower(), 12)