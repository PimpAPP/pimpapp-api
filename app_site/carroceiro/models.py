from django.db import models
from django.core.validators import RegexValidator

class CarroceiroAlreadyExistsException(Exception):
    pass

class Carroceiro(models.Model):

    """
    Class used for modeling a instance of Carroceiro in our DB.
    by default, this table will be addressed as carroceiro_carroceiro
    """
    name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^\d{8,15}$',
                                                                       message='Phone number must have at least 8 digits and/or up to 15 digits.')], default='00000000')
    address = models.CharField(max_length=120, default='')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    # This method was overwriten to make sure that every time a phone is stored it belongs to the same person.
    # And to avoid that the same person is registred twich on the same adress, latitude and longitude.
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        carroceiro_list = Carroceiro.objects.filter(phone=self.phone)
        for c in carroceiro_list:
            if not ((c.name == self.name) and (c.phone == self.phone)):
                raise CarroceiroAlreadyExistsException("This phone belong to another carroceiro")
        for c in carroceiro_list:
            if (c.longitude == self.longitude) and (c.latitude == self.latitude) and (c.adress == self.address):
                raise CarroceiroAlreadyExistsException("This carroceiro is already in our database, "
                                                       "you can't register the same person on the same adress twice")
        super(Carroceiro, self).save()


    def __str__(self):
        return self.name
