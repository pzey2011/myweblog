import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from myweblog import settings

def get_group(user):
    try:
        return user.groups.all()[0].name
    except IndexError:
        return ''


class Account(User):

    GENDER = (('male', _('Male')), ('female', _('Female')))

    gender = models.CharField(max_length=10, choices=GENDER, verbose_name=_(u'Gender'),
                              help_text=_("Choices: ['male', 'female']"), blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', verbose_name=_(u"Avatar"),default='/media/user-default.jpg', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_full_name()
    def avatar_url(self):
        if self.avatar:
            filename = settings.API_URL + self.avatar.url[1:]
            if os.path.isfile(self.avatar.path):
                return filename

        return None

class Profile(Account):
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")