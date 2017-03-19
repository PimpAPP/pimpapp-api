from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# This code is triggered whenever a new user has been created and saved to the database

#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
@receiver(post_save, sender=User)
def create_auth_token(sender, instance, **kwargs):
    token, created = Token.objects.get_or_create(user=instance)
    import pdb; pdb.set_trace()
    print instance.username, created

# TODO NAO FUNFA.... foi movido para models
