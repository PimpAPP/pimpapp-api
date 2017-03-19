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
        max_length=128,
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
    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

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

    @property
    def geolocation(self):
        obj = self.latitudelongitude_set.all().latest('created_on')
        return obj

    @property
    def photos(self):
        # PhotoCatador
        objs = self.photocatador_set.all().order_by('created_on')
        return objs

    @property
    def phones(self):
        objs = self.phonecatador_set.all().order_by('created_on')
        return objs

    @property
    def comments(self):
        objs = self.rating_set.all().order_by('created_on')
        return objs

    @property
    def collects(self):
        return self.collect_set.all()

    def __str__(self):
        return self.name

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

        self.name = mongo_obj.get('name', self.mongo_hash)
        self.catador_type = mongo_obj.get('catador_type', 'C')
        self.minibio = mongo_obj.get('miniBio', '')
        self.has_motor_vehicle = mongo_obj.get('motorizedVehicle', False)
        self.carroca_pimpada = mongo_obj.get('carrocaPimpada', False)

        self.address_base = mongo_obj.get('base_address', '')
        self.region = mongo_obj.get('region', '')
        self.city = mongo_obj.get('city', '')
        self.country = mongo_obj.get('country', 'Brasil')

        # Other Objects
        LatitudeLongitude.objects.create(
            catador=self,
            reverse_geocoding=mongo_obj.get('base_address', ''),
            latitude=mongo_obj.get('latitude', 0.0),
            longitude=mongo_obj.get('longitude', 0.0)
        )

        if mongo_obj.get('telephone1', ''):
            Mobile.objects.create(
                catador=self,
                phone=mongo_obj.get('telephone1', ''),
                mno=mongo_obj.get('operator_telephone1', '').upper()[:1],
                has_whatsapp=mongo_obj.get('whatsapp1', ''),
                mobile_internet=mongo_obj.get('internet1', '')
            )

        if mongo_obj.get('telephone2', ''):
            Mobile.objects.create(
                catador=self,
                phone=mongo_obj.get('telephone2', ''),
                mno=mongo_obj.get('operator_telephone2', '').upper()[:1],
                has_whatsapp=mongo_obj.get('whatsapp2', ''),
                mobile_internet=mongo_obj.get('internet2', '')
            )

        self.save()


class Collect(ModeratedModel):
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
        return 'Cat: ' + self.catador.user.username + ' - Autor:' + self.author.username

    def clean(self):
        '''Usuario pode ter apenas uma coleta em aberto'''

        if self.moderation_status == 'P':
            if Collect.objects.filter(author=self.author, moderation_status='P').count() > 0:
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



class LatitudeLongitudeBase(ModeratedModel):
    """
        DOCS: TODO
    """

    class Meta:
        abstract = True

    # fields:
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    # Reference point
    reverse_geocoding = models.CharField(max_length=128, default='', null=True, blank=True)


class LatitudeLongitude(LatitudeLongitudeBase):
    # control:
    catador = models.ForeignKey('Catador', unique=False, blank=False)


class LatitudeLongitudeColeta(LatitudeLongitudeBase):
    # control:
    coleta = models.ForeignKey('Collect', unique=False, blank=False)


class RatingBase(ModeratedModel):
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


class RatingCooperative(ModeratedModel):
    # control:
    cooperative = models.ForeignKey('Cooperative', unique=False, blank=False)


class PhotoBase(ModeratedModel):
    """
        DOCS: TODO
    """

    # control:
    author = models.ForeignKey(User, unique=False, blank=False)

    # fields:
    # file will be uploaded to MEDIA_ROOT/full_photo
    ppoi = PPOIField(verbose_name=_('Primary Point of Interest (PPOI)'))


class PhotoCatador(PhotoBase):
    full_photo = VersatileImageField(upload_to='catador')
    catador = models.ForeignKey(Catador, unique=False, blank=False)


class PhotoCollectUser(PhotoBase):
    full_photo = VersatileImageField(upload_to='coleta')
    coleta = models.ForeignKey(Collect, unique=False, blank=False)

    def __str__(self):
        return self.author.username + ' - ' + str(self.full_photo)


class PhotoCollectCatador(PhotoBase):
    full_photo = VersatileImageField(upload_to='coleta-catador')
    coleta = models.ForeignKey(Collect, unique=False, blank=False)

    def __str__(self):
        return self.author.username + ' - ' + str(self.full_photo)


class PhotoCooperative(PhotoBase):
    full_photo = VersatileImageField(upload_to='cooperative')
    cooperative = models.ForeignKey('Cooperative', unique=False, blank=False)

    def __str__(self):
        return self.cooperative.name + ' - ' + self.full_photo.name


class ResiduePhoto(PhotoBase):
    full_photo = VersatileImageField(upload_to='residue')
    residue = models.ForeignKey('Residue', unique=False, blank=False)

    def __str__(self):
        return str(self.residue) + ' - ' + str(self.full_photo)


class BaseMobile(ModeratedModel):
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


class MobileCatador(ModeratedModel):
    # control:
    catador = models.ForeignKey(Catador,
                                   # related_name='phones',
                                   unique=False, blank=False)

class MobileCooperative(ModeratedModel):
    # control:
    cooperative = models.ForeignKey('Cooperative',
                                   # related_name='phones',
                                   unique=False, blank=False)


class Residue(models.Model):
    description = models.CharField(max_length=200)
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
        photos = self.residuephoto_set.all()
        return photos

    @property
    def residue_location(self):
        location = self.residuelocation_set.all()
        return location


class ResidueLocation(LatitudeLongitudeBase):
    residue = models.OneToOneField(
        Residue)

    def __str__(self):
        return self.residue.description + ': Lat: ' + str(self.latitude) +\
               ' - Long: ' + str(self.longitude)



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
        return self.name


