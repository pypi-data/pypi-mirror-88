from shutil import copy
from pathlib import Path

from setux.core.errors import ExecError
from setux.core.target import Target
from . import error, info, debug


# pylint: disable=arguments-differ


class Local(Target):
    def __init__(self, **kw):
        kw['name'] = kw.get('name', 'local')
        super().__init__(**kw)

    def run(self, *arg, **kw):
        arg, kw = self.parse(*arg, **kw)
        check = kw.pop('check', False)
        ret, out, err =  super().run(*arg, **kw)
        self.trace(' '.join(arg), ret, out, err, **kw)
        if check and ret:
            raise ExecError(' '.join(arg), ret, out, err)
        return ret, out, err

    def __call__(self, command, **kw):
        ret, out, err = self.run(command, **kw)
        print('\n'.join(out))
        print('\n'.join(err))
        return ret

    def read(self, path, mode='rt', critical=True, report='normal'):
        if report=='normal':
            info(f'\tread {path}')
        return open(path, mode).read()

    def write(self, path, content, mode='wt', report='normal'):
        if report=='normal':
            info(f'\twrite {path}')
        dest = path[:path.rfind('/')]
        self.run(f'mkdir -p {dest}', report=report)
        with open(path, mode) as out:
            out.write(content)
        return open(path, mode=mode.replace('w','r')).read() == content

    def send(self, local, remote, quiet=False):
        local =  Path(local)
        assert local.is_file()
        remote = Path(remote) if remote else local
        info(f'\tsend {local} -> {remote}')
        try:
            copy(local, remote)
            return True
        except:
            return False

    def fetch(self, remote, local):
        info(f'\tfetch {local} <- {remote}')
        try:
            copy(remote, local)
            return True
        except:
            return False

    def sync(self, src, dst=None):
        assert Path(src).is_dir()
        if not src.endswith('/'): src+='/'
        if dst:
            self.dir(dst).set()
            info(f'\tsync {src} -> {dst}')
            return self.rsync(f'{src} {dst}')
        else:
            debug(f'\tskipped {src} -> {dst}')

    def export(self, path):
        error("can't export on local")

    def remote(self, module, export_path=None, **kw):
        error("can't remote on local")

    def __str__(self):
        return f'Local({self.name})'
