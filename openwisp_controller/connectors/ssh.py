import ipaddress
import logging
import paramiko
import six
from scp import SCPClient

from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property

from .utils import get_interfaces

logger = logging.getLogger(__name__)


class Ssh(object):
    # TODO: implement schema
    schema = {}

    def __init__(self, device_connector):
        self.connector = device_connector
        self.device = device_connector.device
        self.shell = paramiko.SSHClient()
        self.shell.load_system_host_keys()
        self.shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()

    @cached_property
    def _addresses(self):
        deviceip_set = list(self.device.deviceip_set.all()
                                       .only('address')
                                       .order_by('priority'))
        address_list = []
        for deviceip in deviceip_set:
            address = deviceip.address
            ip = ipaddress.ip_address(address)
            if not ip.is_link_local:
                address_list.append(address)
            else:
                for interface in get_interfaces():
                    address_list.append('{0}%{1}'.format(address, interface))
        try:
            address_list.append(self.device.config.last_ip)
        except ObjectDoesNotExist:
            pass
        return address_list

    @cached_property
    def _params(self):
        return self.connector.get_params()

    def connect(self):
        success = False
        for address in self._addresses:
            try:
                self.shell.connect(address, **self._params)
            except Exception as e:
                print(e)
                # TODO: we probably need to log this kind of information
                # into to the DB and show it to the user
                logger.exception(e)
            else:
                success = True
                break
        if not success:
            # TODO: improve exception
            raise Exception('Could not connect to device')

    def push(self):
        raise NotImplementedError()

    def upload(self, fl, remote_path):
        scp = SCPClient(self.shell.get_transport())
        scp.putfo(fl, remote_path)
        scp.close()
