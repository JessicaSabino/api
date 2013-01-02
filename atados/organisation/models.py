from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Organisation(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(max_length=50)

    @models.permalink
    def get_absolute_url(self):
        return ('slug', (self.slug,))

    def __unicode__(self):
        return self.name