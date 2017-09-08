import collections
import json

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from django_netjsonconfig.base.base import BaseModel

from openwisp_users.mixins import ShareableOrgMixin
from jsonfield import JSONField


CONNECTOR_CHOICES = (
    ('openwisp_controller.connectors.OpenWrt', 'OpenWRT/LEDE: SSH'),
    ('openwisp_controller.connectors.AirOs', 'Ubiquiti AirOS: SSH'),
    ('openwisp_controller.connectors.Raspbian', 'Raspbian: SSH'),
)


class Connector(ShareableOrgMixin, BaseModel):
    """
    Connector model prototype1
    """
    connector = models.CharField(_('connector'),
                                 choices=CONNECTOR_CHOICES,
                                 max_length=128,
                                 db_index=True)
    params = JSONField(_('parameters'),
                       default=dict,
                       help_text=_('global connection parameters'),
                       load_kwargs={'object_pairs_hook': collections.OrderedDict},
                       dump_kwargs={'indent': 4})


@python_2_unicode_compatible
class DeviceConnector(models.Model):
    device = models.ForeignKey('config.Device')
    connector = models.ForeignKey(Connector)
    enabled = models.BooleanField(default=True, db_index=True)
    params = JSONField(_('parameters'),
                       default=dict,
                       blank=True,
                       help_text=_('local connection parameters (will override '
                                   'the global parameters if specified)'),
                       load_kwargs={'object_pairs_hook': collections.OrderedDict},
                       dump_kwargs={'indent': 4})

    # def __str__(self):
    #     return '{0} {1}'.format(self.connector.name, self.device.name)

    def get_params(self):
        params = self.connector.params.copy()
        params.update(self.params)
        return params

    @cached_property
    def connector_class(self):
        return import_string(self.connector.connector)

    @cached_property
    def connector_instance(self):
        return self.connector_class(self)


@python_2_unicode_compatible
class DeviceIp(models.Model):
    device = models.ForeignKey('config.Device')
    address = models.GenericIPAddressField(_('IP address'))
    priority = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{0} {1}'.format(self.address, self.device.name)
