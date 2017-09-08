from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConnectorsConfig(AppConfig):
    name = 'openwisp_controller.connectors'
    label = 'connectors'
    verbose_name = _('Network Access Credentials')
