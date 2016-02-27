# TODO

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from simple_history.models import HistoricalRecords
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.fields import PPOIField

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


class Carroceiro(ModeratedModel):
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

    name = models.CharField(
            max_length=64,
            verbose_name=_('Nome'))

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
            default=True)

    # Location
    address_base = models.CharField(
            max_length=128,
            verbose_name=_("Endereço onde costuma trabalhar."))

    region = models.CharField(
            max_length=64,
            verbose_name=_("Região onde costuma trabalhar.")) # Any sense?

    city = models.CharField(
            max_length=64,
            verbose_name=_("Cidade em que trabalha"))

    country = models.CharField(
            max_length=64,
            verbose_name=_("Cidade em que trabalha"))

    # Pimp my Caroca
    has_motor_vehicle = models.BooleanField(
            default=False,
            verbose_name=_("Tem veículo motorizado."))

    carroca_pimpada = models.BooleanField(
            default=False,
            verbose_name=_("Teve a Carroça Pimpada?"))

    @property
    def geolocation(self):
        obj = self.latitudelongitude_set.all().latest('created_on')
        return obj

    @property
    def photos(self):
        objs = self.photo_set.all().order_by('created_on')
        return objs

    @property
    def comments(self):
        objs = self.rating_set.all().order_by('created_on')
        return objs

    def __str__(self):
        return self.name


class Material(ModeratedModel):
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

    # control:
    carroceiro = models.OneToOneField(
            Carroceiro,
            related_name='materials',
            blank=False,
            null=True,
            on_delete=models.SET_NULL)

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


class LatitudeLongitude(ModeratedModel):
    """
        DOCS: TODO
    """

    # control:
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)

    # fields:
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    # Reference point
    reverse_geocoding = models.CharField(max_length=128, default='', null=True, blank=True)


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


class Photo(ModeratedModel):
    """
        DOCS: TODO
    """

    # control:
    author = models.ForeignKey(User, unique=False, blank=False)
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)

    # fields:
    # file will be uploaded to MEDIA_ROOT/full_photo
    full_photo = VersatileImageField(upload_to='full_photo')
    ppoi = PPOIField(verbose_name=_('Primary Point of Interest (PPOI)'))


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
    # Porto Seguro

    # Mobile Network Operator (MNO)
    MNO_CHOICES = (
        (VIVO, 'Vivo'),
        (TIM, 'TIM'),
        (CLARO, 'Claro'),
        (OI, 'Oi'),
        (NEXTEL, 'Nextel'),
    )

    # control:
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)

    # fields:
    phone = models.CharField(
            max_length=16,
            validators=[RegexValidator(regex=r'^\d{8,15}$',
            message='Phone number must have at least 8 digits and/or up to 15 digits.')],
            verbose_name=_('Telefone Móvel'))

    mno = models.CharField(
            max_length=1,
            choices=MNO_CHOICES,
            verbose_name=_('Operadora Móvel'),
            blank=True)

    has_whatsapp = models.BooleanField(
            verbose_name=_('Usa o WhatsAPP?'),
            default=False)

    notes = models.CharField(
            verbose_name=_('Comentário'),
            max_length=140, blank=True)

