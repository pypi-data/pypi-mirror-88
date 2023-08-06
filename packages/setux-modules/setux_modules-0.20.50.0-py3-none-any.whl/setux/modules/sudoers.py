from setux.core.module import Module


# pylint: disable=arguments-differ


class Distro(Module):
    '''Add User to sudoers

    arg:
        user : user name
    '''

    def deploy(self, target, *, user):

        grp = target.groups(user)
        grp.add('wheel')

        line = f'{user} ALL=(ALL) NOPASSWD: ALL'
        sudoers = '/etc/sudoers'
        target.deploy('upd_cfg',
            cfg = sudoers,
            src = f'^{user}',
            dst = line,
            report = 'quiet',
        )

        ok = (
            'wheel' in grp.get()
            and line in target.read(sudoers, report='quiet')
        )

        return ok
