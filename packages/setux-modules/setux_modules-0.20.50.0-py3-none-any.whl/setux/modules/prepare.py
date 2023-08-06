from setux.core.module import Module


class Distro(Module):
    '''Minimum System Requieremnts
    '''
    def do_deploy(self, target, **kw):
        get_pip = '/tmp/setux/get_pip.py'
        target.dir('/tmp/setux').deploy()
        target.deploy('download',
            url = 'https://bootstrap.pypa.io/get-pip.py',
            dst = get_pip,
        )
        target.run(f'python3 {get_pip} --force-reinstall')
        return self.install(target,
            pkg = 'vim',
        )


class FreeBSD(Distro):
    def do_deploy(self, target, **kw):
        return self.install(target,
            pkg = 'sudo bash python',
        )

