from ..ssh import Ssh


class AirOs(Ssh):
    # TODO: implement backend check
    backend = 'netjsonconfig.AirOs'

    def push(self):
        config = self.device.config.generate()
        self.upload(config, '/tmp/system.cfg')
        self.shell.exec_command('cfgmtd -w /tmp/system.cfg')
        self.shell.exec_command('/usr/local/rc.d/rc.do.softrestart save')
