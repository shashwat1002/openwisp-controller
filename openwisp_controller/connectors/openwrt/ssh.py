from ..ssh import Ssh


class OpenWrt(Ssh):
    # TODO: implement backend check
    backend = 'netjsonconfig.OpenWrt'

    def push(self):
        self.shell.exec_command('/etc/init.d/openwisp_config restart')
