from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

def get_group(user):
    try:
        return user.groups.all()[0].name
    except IndexError:
        return ''

class Account(User):
    GENDER = (('male', _('Male')), ('female', _('Female')))

    gender = models.CharField(max_length=10, choices=GENDER, verbose_name=_(u'Gender'),
                              help_text=_("Choices: ['male', 'female']"), blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', verbose_name=_(u"Avatar"), blank=True, null=True)
    class Meta:
        abstract = True

    def __str__(self):
        return self.get_full_name()