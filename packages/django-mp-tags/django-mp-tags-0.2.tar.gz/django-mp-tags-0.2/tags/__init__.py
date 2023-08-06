
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TagsAppConfig(AppConfig):

    name = 'tags'
    verbose_name = _('Tags')


default_app_config = 'tags.TagsAppConfig'
