from setux.core import __version__
from setux.logger import info
from setux.core.module import Module


class Distro(Module):
    '''Show infos
    '''
    def deploy(self, target, **kw):
        user = target.login.name
        os = target.os
        python = target.run('python3 -V')[1][0]
        host = target.distro.host

        inst = '-' #len(list(target.Package.installed()))
        avail = '-' #len(list(target.Package.available()))
        #packages : {inst} / {avail}

        infos =  f'''
        target : {target}
        distro : {target.distro.name}
        python : {python}
        os     : {os.kernel} {os.version} / {os.arch}
        user   : {user}
        host   : {host.name} : {host.addr}
        setux  : {__version__}
        '''

        info(infos)

        return True
