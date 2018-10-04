from rest_framework import serializers
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import detail_route
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, HttpResponse
from base64 import b64decode
from django.core.files.base import ContentFile
from django.db.models import Q
# from braces.views import CsrfExemptMixin
import xlwt
import datetime as dt
import operator

import uuid
import logging

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import ModeratedModel, Partner, PhotoCooperative, CallStatistics
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
from .models import GeneralErros
from .models import MobileCooperative

from .serializers import RatingSerializer, PartnerSerializer
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
logger = logging.getLogger(__name__)


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

    @detail_route(methods=['GET', 'POST', 'PUT', 'DELETE'], permission_classes=[])
    def add_error(self, request, pk=None):
        if request.method == 'POST':
            GeneralErros.objects.create(
                detail=str(request.data.get('detail')),
                object=str(request.data.get('object'))
            )
            # serializer = GeneralErrosSerializer(data=request.data)
            # if serializer.is_valid():
            # serializer.save()
        return Response(status=status.HTTP_201_CREATED)


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
    permission_classes = (AllowAny,)
    # queryset = Catador.objects.all()
    queryset = Catador.objects.filter(active=True)
    http_method_names = ['get', 'post', 'update', 'options', 'patch', 'delete']

    def get_queryset(self):
        """
        Adding custom filter by params.
        :return:
        """

        # Filter by 'search' will search in
        # (name, nickname, endereço (rua, bairro, cidade, estado), material)
        search = self.request.query_params.get('search', None)
        filter_by_name = self.request.query_params.get('name', False)
        filter_by_nickname = self.request.query_params.get('nickname', False)
        filter_by_address = self.request.query_params.get('address', False)
        materials = self.request.query_params.getlist('materials')

        if search is not None or filter_by_address or materials:
            q_objects = Q()

            if search is not None:
                if filter_by_name:
                    q_objects |= Q(name__contains=search)
                if filter_by_nickname:
                    q_objects |= Q(nickname__contains=search)

            if filter_by_address:
                # q_objects |= Q(region__contains=search)
                # q_objects |= Q(address_region__contains=search)
                # q_objects |= Q(country__contains=search)
                state = self.request.query_params.get('city')
                city = self.request.query_params.get('city')

                if state:
                    q_objects |= Q(state=state)

                if city:
                    q_objects |= Q(city=city)

            queryset = Catador.objects.filter(q_objects)

            if materials:
                if queryset:
                    queryset = queryset\
                        .filter(materials_collected__in=materials)
                # else:
                #     queryset = Catador.objects\
                #         .filter(materials_collected__in=materials)
        else:
            queryset = Catador.objects.all()

        return queryset

    @detail_route(methods=['POST', 'OPTIONS'], permission_classes=[AllowAny])
    def add(self, request):
        print(request.data)
        if request.method == 'POST' and request.data:
            pass
        pass

    @detail_route(methods=['GET', 'POST'], permission_classes=[])
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


@api_view(['POST'])
def cadastro_catador(request):
    """
        Save catador in an one only method
    """

    if not request.data['user'] or not request.data['catador']:
        return Response('Usuario and Catador is required', status=status.HTTP_400_BAD_REQUEST)

    user = None
    user_serializer = None
    catador = None
    catador_serializer = None

    try:
        # register user
        user_request = request.data['user']

        if user_request['username']:
            exist = User.objects.filter(username=user_request['username'])
            if exist:
                return Response('Usuário já existente', status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=user_request)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # register catador
        catador_request = request.data['catador']
        catador_request['user'] = user.pk
        catador_serializer = CatadorSerializer(data=catador_request)
        catador_serializer.is_valid(raise_exception=True)
        catador = catador_serializer.save()

        # register phones
        if request.data['phones']:
            phones_request = request.data['phones']
            for phone in phones_request:
                if phone.get('phone'):
                    m = Mobile.objects.create(
                        phone=phone.get('phone'),
                        mno=phone.get('mno'),
                        has_whatsapp=phone.get('has_whatsapp', False)
                    )
                    MobileCatador.objects.create(mobile=m, catador=catador)

        # register location
        if request.data['location']:
            location = request.data['location']
            georeference = LatitudeLongitude.objects.create(
                latitude=location.get('latitude'),
                longitude=location.get('longitude'))

            GeorefCatador.objects.create(georef=georeference, catador=catador)

        # register avatar
        try:
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
            elif request.data['avatar']:
                data = request.data['avatar']
                avatar = base64ToFile(data)

            UserProfile.objects.create(user=user, avatar=avatar)
        except Exception:
            pass

        res = {'catador_pk': catador.pk}
        return Response(res, status=status.HTTP_200_OK)

    except Exception as error:
        logger.error(error)

        if user:
            user.delete()

        if catador:
            catador.delete()

        err = {}

        if (user_serializer and user_serializer.errors) or (catador_serializer and catador_serializer.errors):
            err['user'] = user_serializer.errors
            err['catador'] = catador_serializer.errors
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        raise


@api_view(['POST'])
def edit_catador(request):
    """
        Edit catador in an one only method
    """
    if not request.data['user'] or not request.data['catador']:
        return Response('Usuario and Catador is required', status=status.HTTP_400_BAD_REQUEST)

    catador = None
    catador_serializer = None

    try:
        # register user
        user_request = request.data['user']
        if user_request['id']:
            user = User.objects.get(id=user_request['id'])
            if user:
                user.first_name = user_request['first_name']
                user.last_name = user_request['last_name']
                user.save()

        # register catador
        catador_request = request.data['catador']
        catador = Catador.objects.get(pk=catador_request['id'])
        catador_serializer = CatadorSerializer(catador, data=catador_request)

        catador_serializer.is_valid(raise_exception=True)
        catador = catador_serializer.save()

        # register phones

        if request.data['phones']:
            phones_request = request.data['phones']
            for phone in phones_request:
                if phone.get('phone'):
                    phone_id = phone.get('id')
                    p = phone.get('phone')
                    mno = phone.get('mno')

                    if phone_id:
                        m = Mobile.objects.get(pk=phone_id)
                        m.phone = p
                        m.mno = mno
                        m.has_whatsapp = int(phone.get('has_whatsapp'))
                        m.save()
                    else:
                        m = Mobile.objects.create(
                            phone=p,
                            mno=mno,
                            has_whatsapp=bool(phone.get('has_whatsapp', False))
                        )
                        MobileCatador.objects.create(mobile=m, catador=catador)

        # register location
        if request.data['location']:
            location = request.data['location']
            gc = GeorefCatador.objects.get(catador=catador)
            if gc:
                gc.latitude = location.get('latitude'),
                gc.longitude = location.get('longitude')
                gc.save()
            else:
                georeference = LatitudeLongitude.objects.create(
                    latitude=location.get('latitude'),
                    longitude=location.get('longitude'))

                GeorefCatador.objects.create(georef=georeference, catador=catador)

        # register avatar
        try:
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
            elif request.data['avatar']:
                data = request.data['avatar']
                avatar = base64ToFile(data)

            up = UserProfile.objects.get(user=user)
            if up:
                up.avatar = avatar
                up.save()
            else:
                UserProfile.objects.create(user=user, avatar=avatar)

        except Exception:
            pass

    except Exception as error:
        logger.error(error)
        err = {}

        if catador_serializer and catador_serializer.errors:
            err['catador'] = catador_serializer.errors
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        raise

    return Response('ok', status=status.HTTP_200_OK)


@api_view(['POST'])
def cadastro_cooperativa(request):
    """
        Save cooperative in a one only method
    """

    if not request.data['user'] or not request.data['cooperativa']:
        return Response('Usuario and Cooperativa is required', status=status.HTTP_400_BAD_REQUEST)

    user = None
    user_serializer = None
    cooperativa = None
    cooperativa_serializer = None

    try:
        cooperativa_request = request.data['cooperativa']

        # check by phone (only one cooperative by phone is required)
        phones = request.data['phones']
        if phones and phones[0] and phones[0]['phone']:
            phone = phones[0]['phone']
            if Mobile.objects.filter(phone=phone).exists():
                return Response('Já existe uma cooperativa com esse telefone.', status=status.HTTP_400_BAD_REQUEST)

        # register user
        user_request = request.data['user']

        if user_request['username']:
            exist = User.objects.filter(username=user_request['username'])
            if exist:
                return Response('Usuário já existente', status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=user_request)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # register cooperativa
        cooperativa_request['user'] = user.pk
        cooperativa_serializer = CooperativeSerializer(data=cooperativa_request)
        cooperativa_serializer.is_valid(raise_exception=True)
        cooperativa = cooperativa_serializer.save()
        cooperativa.save()

        # register phones
        if request.data['phones']:
            phones_request = request.data['phones']
            for phone in phones_request:
                if phone.get('phone'):
                    m = Mobile.objects.create(
                        phone=phone.get('phone'),
                        mno=phone.get('mno'),
                        has_whatsapp=bool(phone.get('whatsapp', False))
                    )
                    m.save()
                    MobileCooperative.objects.create(mobile=m, cooperative=cooperativa)

        # register materials
        if request.data['materials']:
            materials_request = request.data['materials']
            for material in materials_request:
                cooperativa.materials_collected.add(material)

        # register avatar
        try:
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
            elif request.data['avatar']:
                data = request.data['avatar']
                avatar = base64ToFile(data)

            UserProfile.objects.create(user=user, avatar=avatar)
        except Exception:
            pass

        # Photos
        if cooperativa_request['photos']:
            for photo in cooperativa_request['photos']:
                file = base64ToFile(photo)
                PhotoCooperative.objects.create(
                    cooperative=cooperativa,
                    full_photo=file,
                    author=cooperativa.user)

        # Partners
        if cooperativa_request['partners']:
            # gen = (p for p in cooperativa_request['partners'] if p.image and p.name)
            for p in cooperativa_request['partners']:
                if p['image'] and p['name']:
                    file = base64ToFile(p['image'])
                    partner = Partner.objects.create(name=p['name'], image=file)
                    cooperativa.partners.add(partner)

    except Exception as error:
        logger.error(error)

        if user:
            user.delete()

        if cooperativa and cooperativa.pk:
            cooperativa.delete()

        err = {}

        if (user_serializer and user_serializer.errors) or (cooperativa_serializer and cooperativa_serializer.errors):
            err['user'] = user_serializer.errors
            err['cooperativa'] = cooperativa_serializer.errors
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        raise

    return Response('ok', status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_cooperativa(request):
    """
        Edit cooperative in a one only method
    """

    if not request.data['user'] or not request.data['cooperativa']:
        return Response('Usuario and Cooperativa is required', status=status.HTTP_400_BAD_REQUEST)

    user = None
    cooperativa = None
    cooperativa_serializer = None

    try:
        # register user
        user_request = request.data['user']
        if user_request['id']:
            user = User.objects.get(id=user_request['id'])
            if user:
                user.first_name = user_request['first_name']
                user.last_name = user_request['last_name']
                user.save()

        # register cooperativa
        cooperativa_request = request.data['cooperativa']
        cooperativa = Cooperative.objects.get(pk=cooperativa_request['id'])
        cooperativa_serializer = CooperativeSerializer(cooperativa, data=cooperativa_request)
        cooperativa_serializer.is_valid(raise_exception=True)
        cooperativa = cooperativa_serializer.save()

        # register phones
        if request.data['phones']:
            phones_request = request.data['phones']
            for phone in phones_request:
                if phone.get('phone'):
                    if phone.get('id'):
                        m = Mobile.objects.get(pk=phone.get('id'))
                        m.phone = phone.get('phone')
                        m.mno = phone.get('mno')
                        m.has_whatsapp = int(phone.get('whatsapp'))
                        m.save()
                    else:
                        m = Mobile.objects.create(
                            phone=phone.get('phone'),
                            mno=phone.get('mno'),
                            has_whatsapp=bool(phone.get('whatsapp', False))
                        )
                        MobileCooperative.objects.create(mobile=m, cooperative=cooperativa)

        # register avatar
        try:
            if request.FILES.get('avatar'):
                avatar = request.FILES['avatar']
            elif request.data['avatar']:
                data = request.data['avatar']
                avatar = base64ToFile(data)

            up = UserProfile.objects.get(user=user)
            if up:
                up.avatar = avatar
                up.save()
            else:
                UserProfile.objects.create(user=user, avatar=avatar)

        except Exception:
            pass

        # Photos
        if cooperativa_request['photos']:
            for photo in cooperativa_request['photos']:
                if type(photo) is dict:
                    if 'delete' in photo and photo['delete']:
                        res = PhotoCooperative.objects.filter(pk=photo['id'])
                        if res and res[0]:
                            res[0].delete()
                else:
                    file = base64ToFile(photo)
                    PhotoCooperative.objects.create(
                        cooperative=cooperativa,
                        full_photo=file,
                        author=cooperativa.user)

        # Partners
        if cooperativa_request['partners']:
            for partner in cooperativa_request['partners']:
                if 'delete' in partner and partner['delete']:
                    p = Partner.objects.filter(pk=partner['pk'])
                    if p and p[0]:
                        cooperativa.partners.remove(p[0])
                elif not 'pk' in partner:
                    file = base64ToFile(partner['image'])
                    p = Partner.objects.create(name=partner['name'], image=file)
                    cooperativa.partners.add(p)

    except Exception as error:
        logger.error(error)
        err = {}
        if cooperativa_serializer and cooperativa_serializer.errors:
            err['catador'] = cooperativa_serializer.errors
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        raise

    return Response('ok', status=status.HTTP_200_OK)


@api_view(['GET'])
def get_docs(request, doc):
    from django.core.files.storage import FileSystemStorage
    from django.conf import settings
    import os

    if doc == '1':
        file_name = 'cata-duvidas.pdf'
    elif doc == '2':
        file_name = 'guia-cadastro.pdf'
    else:
        return Response('Doc not found', status=status.HTTP_200_OK)

    fs = FileSystemStorage(os.path.join(settings.BASE_DIR, 'reports'))

    with fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        return response


@api_view(['POST'])
def add_statistic(request):
    # data = request.data['statistic']
    data = request.data

    if not data or not data['catador']:
        return Response('Statistic required', status=status.HTTP_400_BAD_REQUEST)

    try:
        catador = Catador.objects.get(pk=data['catador'])
        statistic = CallStatistics(catador=catador, phone=data['phone'])
        statistic.save()
        return Response('Success', status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(e)
        return Response('Error on save',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class PartnerViewSet(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['^name']
    ordering_fields = ['name']
    http_method_names = ['get', 'post', 'update', 'patch', 'options', 'delete']
    # permission_classes = (AllowAny,)
    # authentication_classes = []


class CooperativeViewSet(viewsets.ModelViewSet):
    # pagination_class = PostLimitOffSetPagination
    serializer_class = CooperativeSerializer
    queryset = Cooperative.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'id']
    ordering_fields = ['name', 'email', 'id']
    http_method_names = ['get', 'post', 'update', 'patch', 'options', 'delete']
    permission_classes = (AllowAny,)
    authentication_classes = []

    # def get_permissions(self):
    #     if self.request.method in ['GET', 'POST']:
    #         self.permission_classes = [AllowAny]
    #
    #     return super(self).get_permissions()

    def get_queryset(self):
        """
        Adding custom filter by params.
        :return:
        """

        # Filter by 'search' will search in (name, email, phrase)
        search = self.request.query_params.get('search', None)
        filter_by_name = self.request.query_params.get('name', False)
        filter_by_address = self.request.query_params.get('address', False)
        materials = self.request.query_params.getlist('materials')

        if search is not None or filter_by_address or materials:
            q_objects = Q()

            if search is not None and filter_by_name:
                q_objects |= Q(name__contains=search)

            if filter_by_address:
                # q_objects |= Q(address_region__contains=search)
                # q_objects |= Q(country__contains=search)
                state = self.request.query_params.get('city')
                city = self.request.query_params.get('city')

                if state:
                    q_objects |= Q(state=state)

                if city:
                    q_objects |= Q(city=city)

            queryset = Cooperative.objects.filter(q_objects)

            if materials:
                if queryset:
                    queryset = queryset\
                        .filter(materials_collected__in=materials)
                # else:
                #     queryset = Cooperative.objects\
                #         .filter(materials_collected__in=materials)
        else:
            queryset = Cooperative.objects.all()

        return queryset

    @csrf_exempt
    @detail_route(methods=['GET', 'POST', 'DELETE', 'OPTIONS'], permission_classes=[])
    def add(self, request, pk=None):
        serializer = CooperativeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    @detail_route(methods=['GET', 'OPTIONS'], permission_classes=[AllowAny])
    def partners(self, request, pk=None):
        cooperative = self.get_object()
        serializer = PartnerSerializer(cooperative.partners, many=True)
        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST', 'PUT', 'DELETE'], permission_classes=[])
    def phones(self, request, pk=None):
        cooperative = self.get_object()
        if request.method == 'POST' and request.data:
            for phone in request.data:
                if phone.get('phone') and phone.get('mno'):
                    m = Mobile.objects.create(
                        phone=phone.get('phone'),
                        mno=phone.get('mno'),
                        has_whatsapp=bool(phone.get('whatsapp', False))
                    )
                    MobileCooperative.objects.create(mobile=m, cooperative=cooperative)
        elif request.method == 'DELETE' and request.data:
            for phone in request.data:
                Mobile.objects.get(id=phone.get('id')).delete()

        serializer = MobileSerializer(cooperative.phones, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def materials(self, request, pk=None):
        cooperative = self.get_object()
        serializer = MaterialSerializer(cooperative.materials)
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
                    row['nickname'] = row['nickname'] \
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
                    minibio=row['apresentacao'],  # historia e/ou apresentacao no csv
                    address_base=row['endereco'],
                    region=row['regiao'],
                    kg_week=int(row['quilos_dia_coleta']) * 6,
                    # how_many_years_work=int(row['anos_coleta']), # Esse campo não existe
                    # cooperative_name=row['cooperativa'], # Esse campo não existe
                    safety_kit=bool(int(row['carroca_seguranca'])),
                    has_motor_vehicle=bool(int(row['carroca_motor'])))
                # has_smartphone_with_internet=bool(int(row['carroca_internet'])) # Esse campo não existe

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


def export_catadores_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="catadores.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Catadores')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['pk', 'Nome', 'Apelido', 'Telefone(s)',
               'Possui foto?', 'Lat/Long', 'Cidade', 'Estado',
               'Endereço onde costuma trabalhar',
               'Número', 'Bairro', 'Frase de apresentação', 'Mini Biografia',
               'Cadastrado por', 'Outro usuário - Nome', 'Outro usuário - Email',
               'Outro usuário - Whatsapp', 'Tem veículo motorizado',
               'Tem smartphone com internet móvel', 'Teve a Carroça Pimpada?',
               'Recebeu o Kit de Segurança?', 'Kit de Segurança: Bota',
               'Kit de Segurança: Luva', 'Kit de Segurança: Freios',
               'Kit de Segurança: Fitas refletivas', 'Kit de Segurança: Fitas refletivas',
               'Kit de Segurança: Retrovisor', 'Trabalha com qual ferro velho',
               'Quantos dias trabalha por semana', 'Há quantos anos coleta',
               'Quantos Kg coleta por dia?', 'Quantos Kg coleta por semana?',
               'Ano de nascimento', 'Trabalha desde', 'Criado em', 'Atualizado em',
               'Ativo', 'Materiais coletados']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    db_columns = ['pk', 'name', 'nickname', 'phones', 'avatar', 'georef',
                  'city', 'state', 'address_base', 'number', 'address_region',
                  'presentation_phrase', 'minibio', 'registered_by_another_user',
                  'another_user_name', 'another_user_email', 'another_user_whatsapp',
                  'has_motor_vehicle', 'has_smartphone_with_internet',
                  'carroca_pimpada', 'safety_kit', 'safety_kit_boot',
                  'safety_kit_gloves', 'safety_kit_brakes',
                  'safety_kit_reflective_tapes', 'safety_kit_reflective_tapes',
                  'safety_kit_rearview', 'iron_work', 'how_many_days_work_week',
                  'how_many_years_work', 'kg_day', 'kg_week', 'year_of_birth',
                  'works_since', 'created_on', 'modified_date', 'active',
                  'materials_collected']

    rows = Catador.objects.all()

    for row in rows:
        row_num += 1
        count = 0
        for col in db_columns:
            # if col in ['pk', 'name', 'nickname', 'city', 'address_base',
            #            'number', 'address_region', 'presentation_phrase']:
            #     ws.write(row_num, count, row.__getattribute__(col), font_style)

            if col in ['phones',
                       'avatar',
                       'georef',
                       'registered_by_another_user',
                       'materials_collected']:
                value = ''

                if col == 'phones':
                    try:
                        value = ', '.join([p.phone for p in row.phones])
                    except:
                        value = 'Não informado'

                if col == 'avatar':
                    try:
                        value = 'Sim' if row.user.userprofile.avatar else 'Não'
                    except:
                        value = 'Não'

                if col == 'georef':
                    try:
                        geo = GeorefCatador.objects.get(catador_id=row.id)
                        if geo:
                            value = str(geo.georef.latitude) + ', ' + str(geo.georef.longitude)
                    except:
                        value = 'Não informado'

                if col == 'registered_by_another_user':
                    value = row.another_user_name if row.registered_by_another_user else 'Próprio catador'

                if col == 'materials_collected':
                    try:
                        for material in row.materials_collected.get_queryset():
                            if value:
                                value += ', ' + material.name
                            else:
                                value = material.name
                    except:
                        value = 'Não informado'

                ws.write(row_num, count, value, font_style)

            else:
                col_value = row.__getattribute__(col)
                if isinstance(col_value, (dt.datetime, dt.date, dt.time)):
                    ws.write(row_num, count, col_value.strftime('%d/%m/%Y'), font_style)
                else:
                    ws.write(row_num, count, col_value, font_style)

            count += 1

    wb.save(response)
    return response
