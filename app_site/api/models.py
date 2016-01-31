# TODO

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class CarroceiroAlreadyExistsException(Exception):
    pass


class Carroceiro(models.Model):
    """
    Class used for modeling a instance of Carroceiro in our DB.
    by default, this table will be addressed as carroceiro_carroceiro
    """

    CATADOR = 'C'
    COOPERATIVA = 'O'
    ECOPONTO = 'P'

    TYPE_CHOICES = (
        (CATADOR, _('Catador')),
        (COOPERATIVA, _('Cooperativa')),
        (ECOPONTO, _('Ecoponto')),
    )

    name = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=15,
        validators=[RegexValidator(regex=r'^\d{8,15}$',
        message='Phone number must have at least 8 digits and/or up to 15 digits.')],
        default='', null=True, blank=True)

    catador_type = models.CharField(max_length=1, default=CATADOR,
           choices=TYPE_CHOICES)

    @property
    def geolocation(self):
        obj = self.latitudelongitude_set.all().latest('created_on')
        return obj

    @property
    def materials(self):
        obj = self.material_set.all().latest('created_on')
        return obj

    @property
    def photos(self):
        obj = self.photo_set.all().latest('created_on')
        return obj

    @property
    def profile_info(self):
        # TODO: filter
        obj = self.profileinfo_set.objects.all().latest('created_on')
        return obj

    def __str__(self):
        return self.name


class Authorship(models.Model):
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

    user = models.ForeignKey(User, unique=False, blank=False)
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    moderation_status = models.CharField(
            verbose_name=_('Status de Moderação'),
            help_text=_('O status "Rejected" não permite que o registro seja mostrado.'),
            max_length=1,
            choices=MODERATION_CHOICES,
            default=PENDING)


class Material(Authorship):
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
        verbose_name = 'Serviços e Meteriais'
        verbose_name_plural = 'Serviços e Meteriais'

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


class LatitudeLongitude(Authorship):
    """
        DOCS: TODO
    """
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    # Reference point
    address = models.CharField(max_length=120, default='', null=True, blank=True)


class Rating(Authorship):
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


class Photo(Authorship):
    # file will be uploaded to MEDIA_ROOT/full_photo
    full_photo = models.ImageField(upload_to='full_photo')
    thumbnail = models.ImageField(blank=True, upload_to='thumbnail')


class BaseProfileInfo(Authorship):
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
    # Porto Seguro

    # Mobile Network Operator (MNO)
    MNO_CHOICES = (
        (VIVO, 'Vivo'),
        (TIM, 'TIM'),
        (CLARO, 'Claro'),
        (OI, 'Oi'),
        (NEXTEL, 'Nextel'),
    )

    class Meta:
        abstract = True

    name = models.CharField(
            max_length=64,
            verbose_name=_('Nome'))

    phone = models.CharField(
            max_length=16,
            verbose_name=_('Telefone Móvel'))

    mno = models.CharField(
            max_length=1,
            choices=MNO_CHOICES,
            verbose_name=_('Operadora Móvel'))

    has_whatsapp = models.BooleanField(
            verbose_name=_('Usa o WhatsAPP?'),
            default=False)

    address = models.CharField(
            max_length=128,
            verbose_name=_("Endereço onde costuma trabalhar."))

    region = models.CharField(
            max_length=64,
            verbose_name=_("Região onde costuma trabalhar.")) # Any sense?

    city = models.CharField(
            max_length=64,
            verbose_name=_("Cidade em que trabalha"))

    has_motor_vehicle = models.BooleanField(default=False)
    carroca_pimpada = models.BooleanField(default=False)


class ProfileInfo(BaseProfileInfo):
    """
        DOCS: TODO
    """
    def save(self, *args, **kwargs):
        super(ProfileInfo, self).save(*args, **kwargs)
        self.archive()

    def archive(self):
        obj = ProfileInfoHistoric.from_profile(self)
        obj.save()


class ProfileInfoHistoric(BaseProfileInfo):
    """
        DOCS: TODO
    """
    original_pk = models.IntegerField()

    @classmethod
    def from_profile(cls, profile_info, save=False):

        self = cls()

        fields = ['user', 'carroceiro', 'moderation_status', 'name', 'phone', 'mno',
            'has_whatsapp', 'address', 'region',
            'city', 'has_motor_vehicle', 'carroca_pimpada']

        self.original_pk = profile_info.pk

        for field in fields:
            value = getattr(profile_info, field)
            setattr(self, field, value)

        if save:
            self.save()

        return self
