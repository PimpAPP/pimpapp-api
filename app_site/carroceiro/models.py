from django.db import models
from django.core.validators import RegexValidator


class CarroceiroAlreadyExistsException(Exception):
    pass


class Materials(self.Models):
    # TODO: Write the rest
    created_on =  models.DateTimeField(auto_now_add=True)
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)
    paper = models.BooleanField(default=False)
    freight = models.BooleanField(default=False)
    large_objects = models.BooleanField(default=False)

class Carroceiro(models.Model):
    """
    Class used for modeling a instance of Carroceiro in our DB.
    by default, this table will be addressed as carroceiro_carroceiro
    """

    CATADOR = 'C'
    COOPERATIVA = 'O'
    ECOPONTO = 'P'

    TYPE_CHOICES = (
        (CATADOR, 'Catador')
        (COOPERATIVA, 'Cooperativa')
        (ECOPONTO, 'Ecoponto')
    )

    name = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=15,
        validators=[RegexValidator(regex=r'^\d{8,15}$',
        message='Phone number must have at least 8 digits and/or up to 15 digits.')],
        default='', null=True, blank=True)
    address = models.CharField(max_length=120, default='', null=True, blank=True)
    #latitude = models.FloatField(default=0.0)
    #longitude = models.FloatField(default=0.0)

    type = models.CharField(max_length=1, default=CATADOR,
           choices=TYPE_CHOICES)

    @property
    def geolocation(self):
        obj = self.latitudelongitude_set.objects.all().latest('created_on')

        geo_dict = {
            'latitude': obj.latitude,
            'longitude': obj.longitude,
        }

        return geo_dict

    @property
    def meterials(self):
        obj = self.materials_set.objects.all().latest('created_on')
        return obj

    ## This method was overwrittne to avoid that the same person is registred twice on the same adress, latitude and longitude.
    #def save(self, force_insert=False, force_update=False, using=None,
    #         update_fields=None):
    #    carroceiro_list = Carroceiro.objects.filter(phone=self.phone)
    #    for c in carroceiro_list:
    #        if (c.longitude == self.longitude) and (c.latitude == self.latitude) and (c.adress == self.address):
    #            raise CarroceiroAlreadyExistsException("This carroceiro is already in our database, "
    #                                                   "you can't register the same person on the same adress twice")
    #    super(Carroceiro, self).save()

    def __str__(self):
        return self.name


class LatitudeLongitude(models.Model):
    """
        DOCS: TODO
    """
    created_on =  models.DateTimeField(auto_now_add=True)
    carroceiro = models.ForeignKey(Carroceiro, unique=False, blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
