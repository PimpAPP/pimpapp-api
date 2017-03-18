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


class MaterialType(models.Model):
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Tipos de materiais'

    def __str__(self):
        return self.description


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

    created_on = models.DateTimeField(auto_now_add=True)

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
        verbose_name=_('Apelido'))

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

    # Lock feature
    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    is_locked = models.BooleanField(
        verbose_name=_('Permite edição Publica'),
        default=False)

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


class Carroceiro(BaseMapMarker):

    """
    Class used for modeling a instance of Carroceiro in our DB.
    by default, this table will be addressed as carroceiro_carroceiro
    """

    class Meta:
        verbose_name = 'Catadores'

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

    materials_collected = models.ManyToManyField(MaterialType)

    life_history = models.TextField(
        blank=True, null=True)

    how_many_collect_day = models.FloatField(
        blank=True, null=True,
        verbose_name=_('Quanto coleta por dia?'))

    how_many_collect_week = models.FloatField(
        blank=True, null=True,
        verbose_name=_('Quanto coleta por semana?'))

    how_years_many_collect = models.IntegerField(
        blank=True, null=True,
        verbose_name=_('A quantos anos coleta?'))

    internet_outside = models.BooleanField(
        default=False,
        verbose_name=_('Possui internet na rua?'))

    days_week_work = models.CharField(
        max_length=13, null=True, blank=True)

    works_since = models.DateField(blank=True, null=True)

    @property
    def geolocation(self):
        obj = self.latitudelongitude_set.all().latest('created_on')
        return obj

    @property
    def photos(self):
        objs = self.photo_set.all().order_by('created_on')
        return objs

    @property
    def phones(self):
        objs = self.phone_set.all().order_by('created_on')
        return objs

    @property
    def comments(self):
        objs = self.rating_set.all().order_by('created_on')
        return objs

    def __str__(self):
        return self.name

    # Compatibility MeteorJS version
    def load_mongo_obj(self, mongo_obj):

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
            carroceiro=self,
            reverse_geocoding=mongo_obj.get('base_address', ''),
            latitude=mongo_obj.get('latitude', 0.0),
            longitude=mongo_obj.get('longitude', 0.0)
        )

        if mongo_obj.get('telephone1', ''):
            Phone.objects.create(
                carroceiro=self,
                phone=mongo_obj.get('telephone1', ''),
                mno=mongo_obj.get('operator_telephone1', '').upper()[:1],
                has_whatsapp=mongo_obj.get('whatsapp1', ''),
                mobile_internet=mongo_obj.get('internet1', '')
            )

        if mongo_obj.get('telephone2', ''):
            Phone.objects.create(
                carroceiro=self,
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
    author = models.ForeignKey(User, blank=False)
    carroceiro = models.ForeignKey(Carroceiro, blank=False)
    residue = models.ForeignKey('Residue', blank=False)

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
        return str(self.id)

    def clean(self):
        '''Usuario pode ter apenas uma coleta em aberto'''

        if self.moderation_status == 'P':
            if Collect.objects.filter(author=self.author, moderation_status='P').count() > 0:
                raise ValidationError('Usuário pode ter apenas uma coleta em aberto')


class MaterialBase(ModeratedModel):
    """
        Tipical Carroceiro's services:
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
        abstract = True
        verbose_name = 'Serviços e Meteriais'
        verbose_name_plural = 'Serviços e Meteriais'

    # Metadata about recycling
    works_since = models.DateTimeField(blank=True)
    est_kg_day = models.PositiveIntegerField(blank=True)
    days_week = models.PositiveIntegerField(blank=True)

    # fields:
    freight = models.BooleanField(
        verbose_name=_("Serviço de Frete e Carreto"),
        default=False)
    large_objects = models.BooleanField(
        verbose_name=_('Volumosos'),
        help_text=_('Exemplo: sofá, geladeira, fogão, etc...'),
        default=False)
    demolition_waste = models.BooleanField(
        verbose_name=_('Resíduo de Construção Civil'),
        help_text=_('entulho, tintas, madeira, etc...'),
        default=False)
    e_waste = models.BooleanField(
        verbose_name=_('Eletroeletrônicos'),
        help_text=_('Exemplo: computadores, pilhas, baterias, etc...'),
        default=False)
    paper = models.BooleanField(
        verbose_name=_('Papel'),
        help_text=('Exemplo: jornal, revista, papel branco, papelão, etc...'),
        default=False)
    glass = models.BooleanField(
        verbose_name=_('Vidro'),
        help_text=_('Exemplo: garrafas, embalagens, etc...'),
        default=False)
    plastic = models.BooleanField(
        verbose_name=_('Plástico'),
        help_text=_('Exemplo: embalagens, canos, etc..'),
        default=False)
    metal = models.BooleanField(
        verbose_name=_('Metais'),
        help_text=_('Exemplo: ferro, cobre, alumínio, etc..)'),
        default=False)
    wood = models.BooleanField(
        verbose_name=_('Madeira'),
        help_text=_('Exemplo: tábuas, ripas, etc...'),
        default=False)
    cooking_oil = models.BooleanField(
        verbose_name=_('Óleo de cozinha'),
        default=False)


class Material(MaterialBase):
    ''' Usuário é obrigado a marcar quais materia estão na coleta '''

    # control:
    carroceiro = models.OneToOneField(
        Carroceiro,
        related_name='materials',
        blank=False,
        null=True,
        on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.carroceiro)

    def clean(self):
        if self.freight or self.large_objects or self.demolition_waste or \
                self.e_waste or self.paper or self.glass or self.plastic or \
                self.metal or self.wood or self.cooking_oil:
            return
        else:
            raise ValidationError('Pelo menos um tipo de material deve ser informado')


class MaterialColeta(MaterialBase):
    # control:
    coleta = models.OneToOneField(
        Collect,
        related_name='materials',
        blank=False,
        null=True,
        on_delete=models.SET_NULL)


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
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)


class LatitudeLongitudeColeta(LatitudeLongitudeBase):
    # control:
    coleta = models.ForeignKey(Collect, unique=False, blank=False)


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

    # control:
    author = models.ForeignKey(User, unique=False, blank=False)
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)

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


class PhotoBase(ModeratedModel):
    """
        DOCS: TODO
    """

    # control:
    author = models.ForeignKey(User, unique=False, blank=False)

    # fields:
    # file will be uploaded to MEDIA_ROOT/full_photo
    full_photo = VersatileImageField(upload_to='full_photo')
    ppoi = PPOIField(verbose_name=_('Primary Point of Interest (PPOI)'))


class Photo(PhotoBase):
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)


class PhotoCollectUser(PhotoBase):
    coleta = models.ForeignKey(Collect, unique=False, blank=False)

    def __str__(self):
        return self.author.username + ' - ' + str(self.full_photo)


class PhotoCollectCatador(PhotoBase):
    coleta = models.ForeignKey(Collect, unique=False, blank=False)

    def __str__(self):
        return self.author.username + ' - ' + str(self.full_photo)


class Phone(ModeratedModel):
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

    # control:
    carroceiro = models.ForeignKey(Carroceiro,
                                   # related_name='phones',
                                   unique=False, blank=False)

    # fields:
    phone = models.CharField(
        max_length=20,
        #validators=[RegexValidator(regex=r'^\d{8,15}$',
        #                           message='Phone number must have at least 8 digits and/or up to 15 digits.')],
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


class Residue(models.Model):
    description = models.CharField(max_length=200)
    materials = models.ManyToManyField(MaterialType)
    user = models.ForeignKey(User)

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


class ResiduePhoto(PhotoBase):
    residue = models.ForeignKey(Residue, unique=False, blank=False)

    def __str__(self):
        return str(self.residue) + ' - ' + str(self.full_photo)


class ResidueLocation(LatitudeLongitudeBase):
    residue = models.OneToOneField(
        Residue)

    def __str__(self):
        return self.residue.description + ': Lat: ' + str(self.latitude) +\
               ' - Long: ' + str(self.longitude)


class PhoneNumbers(models.Model):
    MNO_CHOICES = (
        ('V', 'Vivo'),
        ('T', 'TIM'),
        ('C', 'Claro'),
        ('O', 'Oi'),
        ('N', 'Nextel'),
        ('P', 'Porto Conecta'),
    )
    number = models.CharField(max_length=15)
    mobile_operator = models.CharField(max_length=1, choices=MNO_CHOICES)

    def __str__(self):
        return self.number + ' - ' + self.mobile_operator


class Partner(ModeratedModel):
    name = models.CharField(max_length=100)
    image = VersatileImageField(upload_to='cooperatives/partners')

    def __str__(self):
        return self.name


class Cooperative(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phrase = models.CharField(max_length=200)
    history = models.TextField(max_length=500, null=True, blank=True)
    phones = models.ManyToManyField(PhoneNumbers)
    user = models.OneToOneField(User)
    address = models.CharField(max_length=200)
    region_where_operates = models.CharField(max_length=200)
    how_many_cooperators = models.IntegerField()
    how_many_collect_day = models.FloatField()
    how_many_collect_week = models.FloatField()
    how_many_years_collecting = models.IntegerField()
    how_many_material_collected = models.FloatField()
    image = VersatileImageField(upload_to='cooperatives')
    materials_collected = models.ManyToManyField(MaterialType)
    partners = models.ManyToManyField(Partner, blank=True)

    @property
    def photos(self):
        objs = self.photocooperative.all().order_by('created_on')
        return objs

    def __str__(self):
        return self.name


class PhotoCooperative(PhotoBase):
    cooperative = models.ForeignKey(Cooperative, unique=False, blank=False)

    def __str__(self):
        return self.cooperative.name + ' - ' + self.full_photo.name
