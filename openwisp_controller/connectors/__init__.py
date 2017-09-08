default_app_config = 'openwisp_controller.connectors.apps.ConnectorsConfig'

from .openwrt.ssh import OpenWrt
from .airos.ssh import AirOs
from .raspbian.ssh import Raspbian
