# TODO
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.fields import PPOIField

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.db.models.signals import post_save
from django.dispatch import receiver


# This code is triggered whenever a new user has been created and saved to the database
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
@receiver(post_save, sender=User)
def create_auth_token(sender, instance, **kwargs):
    token, created = Token.objects.get_or_create(user=instance)


def get_upload_path(self, filename):
    path = self._upload_to + '/' + filename
    return path


class ModeratedModel(models.Model):
    """
        DOCS: TODO
    """
    APPROVED = 'A'
    REJECTED = 'R'
    PENDING = 'P'

    MODERATION_CHOICES = (
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (PENDING, _('Pending')),
    )

    class Meta:
        abstract = True

    history = HistoricalRecords(inherit=True)

    created_on = models.DateTimeField(auto_now=True)

    moderation_status = models.CharField(
        verbose_name=_('Status de Moderação'),
        help_text=_('O status "Rejected" não permite que o registro seja mostrado.'),
        max_length=1,
        choices=MODERATION_CHOICES,
        default=PENDING)

    # Compatibility MeteorJS version
    mongo_hash = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )


class BaseMapMarker(ModeratedModel):

    class Meta:
        verbose_name = 'Catadores e Cooperativas'
        abstract = True

    CATADOR = 'C'
    COOPERATIVA = 'O'
    ECOPONTO = 'P'

    TYPE_CHOICES = (
        (CATADOR, _('Catador')),
        (COOPERATIVA, _('Cooperativa')),
        (ECOPONTO, _('Ecoponto')),
    )

    name = models.CharField(
        max_length=128,
        verbose_name=_('Nome'))

    slug = models.CharField(
        max_length=141,
        blank=True,
        null=True)

    minibio = models.TextField(
        max_length=512,
        blank=True,
        null=True)

    catador_type = models.CharField(max_length=1, default=CATADOR,
                                    choices=TYPE_CHOICES)

    # Location
    address_base = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Endereço onde costuma trabalhar."))

    region = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("Região onde costuma trabalhar."))  # Any sense?

    city = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name=_("Cidade em que trabalha"))

    country = models.CharField(
        max_length=64,
        blank=True,
        null=True)

    kg_week = models.FloatField(
        blank=True, null=True,
        verbose_name=_('Quantos Kg coleta por semana?'))

    works_since = models.DateField(blank=True, null=True)


class Catador(BaseMapMarker):

    """
    Class used for modeling a instance of Catador in our DB.
    by default, this table will be addressed as catador_catador
    """

    class Meta:
        verbose_name = 'Catador'

    nickname = models.CharField(
        max_length=128,
        verbose_name=_('Apelido'))

    # Lock feature
    user = models.OneToOneField(User)

    is_locked = models.BooleanField(
        verbose_name=_('Permite edição Publica'),
        default=False)

    # Meterials
    materials_collected = models.ManyToManyField('Material')

    # Pimp my Caroca
    has_motor_vehicle = models.BooleanField(
        default=False,
        verbose_name=_("Tem veículo motorizado."))

    carroca_pimpada = models.BooleanField(
        default=False,
        verbose_name=_("Teve a Carroça Pimpada?"))

    safety_kit = models.BooleanField(
        default=False,
        verbose_name=_("Recebeu o Kit de Segurança?"))

    has_family = models.CharField(
        max_length=200,
        null=True, blank=True)

    # M2M
    rating_m2m = models.ManyToManyField(
        'Rating', blank=True, related_name='catadores',
        through='RatingCatador')

    mobile_m2m = models.ManyToManyField(
        'Mobile', blank=True, related_name='catadores',
        through='MobileCatador')

    georef_m2m = models.ManyToManyField(
        'LatitudeLongitude', blank=True, related_name='catadores',
        through='GeorefCatador')

    @property
    def geolocation(self):
        obj = self.georef_m2m.all()
        return obj

    @property
    def photos(self):
        # PhotoCatador
        objs = self.photocatador_set.all().order_by('created_on')
        return objs

    @property
    def phones(self):
        objs = self.mobile_m2m.get_queryset()
        return objs

    @property
    def comments(self):
        objs = self.rating_m2m.get_queryset()
        return objs

    @property
    def collects(self):
        return self.collect_set.filter(active=True)

    @property
    def profile_photo(self):
        return self.user.userprofile.avatar

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    # Compatibility MeteorJS version
    def load_mongo_obj(self, mongo_obj):
        # TODO MOVER

        """
            Exemplo:

            {'_id': 'wzkKgRXfg3zCghqg3',
             'allow_public_edition': True,
             'moderation_status': 'P',
             'catador_type': 'C',
             'created_on': datetime.datetime(2017, 1, 26, 13, 37, 13, 967000),

             'name': 'Kleber Jesuíno',
             'miniBio': 'Tudo posso naquele que me fortalece ! Dá reciclagem sai minhã casa e todo o meu sustento',

             'motorizedVehicle': False,
             'carrocaPimpada': False,
             'email': None,


             'base_address': 'Rua dos Trilhos, 1622 - Mooca, São Paulo - SP, Brasil',
             'latitude': -23.55447239999999,
             'longitude': -46.59407269999997,

             'city': 'São Paulo',
             'country': 'BR',
             'region': 'Mooca',
             'state': 'SP',
             'zip': '03169'

             'observations': None,

             'socialNetwork': None,
             'operator_telephone1': 'TIM',
             'operator_telephone2': None,
             'telephone1': '(11) 93001-2241',
             'telephone2': None,
             'whatsapp1': True,
             'whatsapp2': False,
             'internet1': False,
             'internet2': False,
             }

        """

        self.name = mongo_obj.get('name', self.name)
        self.catador_type = mongo_obj.get('catador_type', 'C')
        self.minibio = mongo_obj.get('miniBio', '')
        self.has_motor_vehicle = mongo_obj.get('motorizedVehicle', False)
        self.carroca_pimpada = mongo_obj.get('carrocaPimpada', False)

        self.address_base = mongo_obj.get('base_address', '')
        self.region = mongo_obj.get('region', '')
        self.city = mongo_obj.get('city', '')
        self.country = mongo_obj.get('country', 'Brasil')
        self.mongo_hash = mongo_obj.get('catador_id')

        catador = self.save()

        if mongo_obj.get('telephone1', ''):
            tel1 = Mobile.objects.create(
                phone=mongo_obj.get('telephone1', ''),
                mno=mongo_obj.get('operator_telephone1', '').upper()[:1],
                has_whatsapp=mongo_obj.get('whatsapp1', ''),
                mobile_internet=mongo_obj.get('internet1', '')
            )
            tel1.save()
            m1 = MobileCatador.objects.create(mobile=tel1, catador_id=self.id)
            m1.save()

        if mongo_obj.get('telephone2', ''):
            tel2 = Mobile.objects.create(
                phone=mongo_obj.get('telephone2', ''),
                mno=mongo_obj.get('operator_telephone2', '').upper()[:1],
                has_whatsapp=mongo_obj.get('whatsapp2', ''),
                mobile_internet=mongo_obj.get('internet2', '')
            )
            tel2.save()
            m2 = MobileCatador.objects.create(mobile=tel2, catador_id=self.id)
            m2.save()

        # Other Objects
        lat = LatitudeLongitude.objects.create(
            reverse_geocoding=mongo_obj.get('base_address', ''),
            latitude=mongo_obj.get('latitude', 0.0),
            longitude=mongo_obj.get('longitude', 0.0)
        )

        georef = GeorefCatador.objects.create(georef=lat, catador_id=self.id)
        georef.save()


class Collect(ModeratedModel):
    _upload_to = 'collectfolder'
    # TODO: Colocar os campos

    """
        Regras:
        - Usuario pode ter apenas uma coleta em aberto
        - Catador pode ter um lista de coletas em aberto
        - Usuario é obrigado a colocar um photo do material
        - Usuário é obrigado a marcar quais materia estão na coleta
    """

    catador_confirms = models.BooleanField()
    user_confirms = models.BooleanField()
    active = models.BooleanField(default=True)

    residue = models.ForeignKey(
        'Residue',
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    catador = models.ForeignKey(
        Catador,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    @property
    def geolocation(self):
        obj = self.latitudelongitudecoleta_set.all().latest('created_on')
        return obj

    @property
    def photo_collect_catador(self):
        objs = self.photocollectcatador_set.all().order_by('created_on')
        return objs

    @property
    def photo_collect_user(self):
        objs = self.photocollectuser_set.all().order_by('created_on')
        return objs

    def __str__(self):
        return 'Cat: ' + str(self.catador)

    def clean(self):
        '''Usuario pode ter apenas uma coleta em aberto'''

        if self.moderation_status == 'P' and self.catador:
            if Collect.objects.filter(catador=self.catador, moderation_status='P').count() > 0:
                raise ValidationError('Usuário pode ter apenas uma coleta em aberto')




class Material(ModeratedModel):
    """
        Tipical Catador's services:
            * Serviço de Frete e Carreto
            * Reciclável (papel, vidro, latas, embalagens, vidro,
                      embalagem longa vida, etc.)
            * Resíduo de Construção Civil (entulho, tintas, madeira, etc.)
            * Resíduos Volumosos (sofá, geladeira, fogão, etc.)
            * Ferro e metais (cobre, alumínio, etc.)
            * Resíduos eletroeletrônicos (computadores, pilhas, baterias,
                                          etc.)

        Materiais que recebe:
            * Papel (jornal, revista, papel branco, papelão, etc.)
            * Vidro (garrafas, embalagens, etc.)
            * Metal (latas de alumínio, embalagem de marmita, etc.)
            * Plástico (embalagens, canos, etc.)
            * Volumosos  (sofá, geladeira, fogão, etc.)
            * Eletroeletrônicos (computadores, pilhas, baterias, etc.)
            * Madeira
            * Sucata (ferro, alumínio, metais, etc.)
            * Óleo de cozinha
            * Outros (embalagem longa vida, etc.)
    """

    class Meta:
        verbose_name = 'Serviços e Meteriais'
        verbose_name_plural = 'Serviços e Meteriais'

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return '%s - %s' % (self.name, self.description)


class LatitudeLongitude(ModeratedModel):
    """
        DOCS: TODO
    """

    class Meta:
        verbose_name = 'GeoReferencia'

    # fields:
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    # Reference point
    reverse_geocoding = models.CharField(max_length=500, default='', null=True, blank=True)

    def __str__(self):
        return '(' + str(self.latitude) + ', ' + str(self.longitude) + ')'


class GeorefCatador(models.Model):
    '''
        Esta classe esta sendo mantida pois futuramente existe a possibilidade
        do catador mandar sua localização e criarmos um caminho por onde ele passou
        quando esse dia chegar basta mudar a chave de onetoone para foreignkey
    '''
    catador = models.OneToOneField(Catador, blank=False)
    georef = models.OneToOneField(LatitudeLongitude, blank=False)

    def __str__(self):
        return self.catador.name + '(' + str(self.georef.latitude) +\
               ', ' + str(self.georef.longitude) + ')'


class Rating(ModeratedModel):
    """
        DOCS: TODO
    """

    POSITIVE = '+'
    NEUTRAL = '0'
    NEGATIVE = '-'

    RATING_CHOICES = (
        (POSITIVE, _('Positiva')),
        (NEUTRAL, _('Neutra')),
        (NEGATIVE, _('Negativa')),
    )

    class Meta:
        verbose_name = _('Comentário e Avaliação')
        verbose_name_plural = _('Comentários e Avaliações')

    def __str__(self):
        return self.author.username + ' - ' + self.comment

    # control:
    author = models.ForeignKey(User, unique=False, blank=False)

    # fields:
    rating = models.CharField(
        max_length=1,
        verbose_name=_('Avaliação'),
        choices=RATING_CHOICES)

    comment = models.CharField(
        verbose_name=_('Comentário'),
        max_length=140, blank=True)

    def clean(self):
        if not self.rating and not self.comment:
            raise ValidationError(_('Rating or comment required.'))


class RatingCatador(ModeratedModel):
    # control:
    catador = models.ForeignKey('Catador', unique=False, blank=False)
    rating = models.OneToOneField(Rating, blank=False)

    def __str__(self):
        return str(self.catador) + ' - ' + str(self.rating)


class RatingCooperative(ModeratedModel):
    # control:
    cooperative = models.ForeignKey('Cooperative', unique=False, blank=False)
    rating = models.OneToOneField('Rating', blank=False)

    def __str__(self):
        return str(self.cooperative) + ' - ' + str(self.rating)


class PhotoBase(ModeratedModel):
    """
        DOCS: TODO
    """
    _upload_to = 'users'

    # control:
    author = models.ForeignKey(User, unique=False, blank=False)

    # fields:
    # file will be uploaded to MEDIA_ROOT/full_photo
    ppoi = PPOIField(verbose_name=_('Primary Point of Interest (PPOI)'))
    full_photo = VersatileImageField(upload_to=get_upload_path)

    def __str__(self):
        return self.author.username + ' - ' + str(self.full_photo)

    class Meta:
        verbose_name = 'Fotos de usuários'
        verbose_name_plural = 'Fotos de usuários'


class PhotoCatador(PhotoBase):
    _upload_to = 'catador'
    catador = models.ForeignKey(Catador, unique=False, blank=False)


class PhotoCollectUser(PhotoBase):
    _upload_to = 'collects'
    coleta = models.ForeignKey(Collect, unique=False, blank=False)

    def __str__(self):
        return self.author.username + ' - ' + str(self.full_photo)


class PhotoCollectCatador(PhotoBase):
    _upload_to = 'collect_catador'
    coleta = models.ForeignKey(Collect, unique=False, blank=False)

    def __str__(self):
        return self.author.username + ' - ' + str(self.full_photo)


class PhotoCooperative(PhotoBase):
    _upload_to = 'cooperatives'
    cooperative = models.ForeignKey('Cooperative', unique=False, blank=False)

    def __str__(self):
        return self.cooperative.name + ' - ' + self.full_photo.name


class PhotoResidue(PhotoBase):
    _upload_to = 'residue'
    residue = models.ForeignKey('Residue', unique=False, blank=False)

    def __str__(self):
        return str(self.residue) + ' - ' + str(self.full_photo)


class Mobile(ModeratedModel):
    """
        DOCS: TODO
    """

    VIVO = 'V'
    TIM = 'T'
    CLARO = 'C'
    OI = 'O'
    NEXTEL = 'N'
    # Algar
    # Sercomtel
    PORTO = 'P'

    # Mobile Network Operator (MNO)
    MNO_CHOICES = (
        (VIVO, 'Vivo'),
        (TIM, 'TIM'),
        (CLARO, 'Claro'),
        (OI, 'Oi'),
        (NEXTEL, 'Nextel'),
        (PORTO, 'Porto Conecta'),
    )

    # fields:
    phone = models.CharField(
        max_length=20,
        #validators=[RegexValidator(regex=r'^\d{8,15}$',
        #                           message='Mobile number must have at least 8 digits and/or up to 15 digits.')],
        verbose_name=_('Telefone Móvel'))

    mno = models.CharField(
        max_length=1,
        choices=MNO_CHOICES,
        verbose_name=_('Operadora Móvel'),
        null=True,
        blank=True)

    has_whatsapp = models.BooleanField(
        verbose_name=_('Usa o WhatsAPP?'),
        default=False)

    mobile_internet = models.BooleanField(
        verbose_name=_('Tem acesso a internet móvel?'),
        default=False)

    notes = models.CharField(
        verbose_name=_('Comentário'),
        max_length=140, blank=True, null=True)

    def __str__(self):
        return self.phone


class MobileCatador(models.Model):
    # control:
    catador = models.ForeignKey(
        Catador, unique=False, blank=False)
    mobile = models.OneToOneField(Mobile, blank=False)

    def __str__(self):
        return str(self.catador) + ' - ' + self.mobile.phone


class MobileCooperative(models.Model):
    # control:
    cooperative = models.OneToOneField(
        'Cooperative', blank=False)
    mobile = models.OneToOneField(Mobile, blank=False)


    def __str__(self):
        return str(self.cooperative.name) + ' - ' + self.mobile.phone


class Residue(models.Model):
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    how_many_kilos = models.FloatField(
        verbose_name=_('Quantos kilos aproximadamente?'),
        default=0
    )
    materials = models.ManyToManyField(Material)

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)

    @property
    def residue_photos(self):
        photos = self.photoresidue_set.all()
        return photos

    @property
    def residue_location(self):
        location = self.residuelocation_set.all()
        return location


class GeorefResidue(models.Model):
    residue = models.OneToOneField(Residue, blank=False)
    georef = models.ForeignKey(LatitudeLongitude, blank=False)


class Cooperative(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phrase = models.CharField(max_length=200)
    user = models.OneToOneField(User)
    address = models.CharField(max_length=200)
    region_where_operates = models.CharField(max_length=200)
    how_many_cooperators = models.IntegerField()
    image = VersatileImageField(upload_to='cooperatives')
    partners = models.ManyToManyField('Partner', blank=True)

    # Meterials
    materials_collected = models.ManyToManyField('Material')

    # M2M
    rating_m2m = models.ManyToManyField(
        'Rating', blank=True, related_name='cooperatives',
        through='RatingCooperative')

    mobile_m2m = models.ManyToManyField(
        'Mobile', blank=True, related_name='cooperatives',
        through='MobileCooperative')

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    @property
    def photos(self):
        objs = self.photocooperative.all().order_by('created_on')
        return objs

    def __str__(self):
        return self.name


class Partner(ModeratedModel):
    name = models.CharField(max_length=100)
    image = VersatileImageField(upload_to='cooperatives/partners')

    def __str__(self):
        return self.name + ' - ' + self.image.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField()

    def __str__(self):
        return self.user.username
