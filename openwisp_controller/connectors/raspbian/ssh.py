from ..ssh import Ssh


class Raspbian(Ssh):
    # TODO: implement backend check
    backend = 'netjsonconfig.Raspbian'

    def push(self):
        config = self.device.config.generate()
        self.upload(config, '/tmp/config.tar.gz')
        # TODO: complete this
