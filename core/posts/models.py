from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User



class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    author = models.ForeignKey(User, related_name='posts', verbose_name=_("Author"), blank=True, null=True)
    text = models.TextField(verbose_name=_("Text"))
    image =models.ImageField(upload_to='posts', verbose_name=_(u"Post Image"), blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name=_("Tag"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title



class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments', verbose_name=_("Author"))
    text = models.TextField(verbose_name=_("Text"))
    post = models.ForeignKey(Post, related_name='comments', verbose_name=_("Post"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
