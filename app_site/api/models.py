# TODO

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from carroceiro.models import Carroceiro

class Authorship(models.Model):

    APPROVED = 'A'
    REJECTED = 'R'
    PENDING = 'P'

    MODERATION_CHOICES = (
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    )

    class Meta:
        abstract = True

    user = models.ForeignKey(User, unique=False, blank=False)
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    moderation_status = models.CharField(max_length=1,
                                      choices=MODERATION_CHOICES,
                                      default=PENDING)


class Rating(Authorship):

    rating = models.IntegerField(blank=True)
    comment = models.CharField(max_length=140, blank=True)

    def clean(self):
        if not self.rating and not self.comment:
            raise ValidationError(_('Rating or comment required.'))


class Photo(Authorship):
    # TODO
    full_photo = models.ImageField()
    thumbnail = models.ImageField(blank=True)


class BaseProfileInfo(Authorship):

    class Meta:
        abstract = True

    name = models.CharField(max_length=64)

    phone = models.CharField(max_length=16)
    operadora = models.CharField(max_length=16)
    has_whatsapp = models.BooleanField(default=False)

    address = models.CharField(max_length=128,
        verbose_name=u"Endereço onde costuma trabalhar.")
    region = models.CharField(max_length=64,
        verbose_name=u"Região onde costuma trabalhar.") # Makes sense?
    # City ???

    has_motor_vehicle = models.BooleanField(default=False)
    carroca_pimpada = models.BooleanField(default=False)


class ProfileInfo(BaseProfileInfo):

    def save(self, *args, **kwargs):
        archive()
        # do something

    def archive(self):
        obj = ProfileInfoHistoric.from_profile(self)
        obj.save()


class ProfileInfoHistoric(BaseProfileInfo):

    @classmethod
    def from_profile(cls, profile_info):
        # copy
        pass
