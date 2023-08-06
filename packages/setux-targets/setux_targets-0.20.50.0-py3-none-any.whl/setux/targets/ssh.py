from tempfile import NamedTemporaryFile
from os.path import isdir, basename
from importlib import import_module
from pathlib import Path

from setux.core.errors import ExecError
from setux.core.target import Target
from . import logger, info, error
from . import remote_tpl


# pylint: disable=arguments-differ


class SSH(Target):
    def __init__(self, **kw):
        self.host = kw.pop('host', None)
        self.priv = kw.pop('priv', None)
        user = kw.pop('user', None)
        if user:
            self.host = f'{user}@{self.host}'
        kw['name'] = kw.pop('name', self.host)
        super().__init__(**kw)

    def skip(self, line):
        if (
            line.startswith('Connection to')
            and line.endswith('closed.')
        ): return True
        return False

    def run(self, *arg, **kw):
        arg, kw = self.parse(*arg, **kw)
        command = ' '.join(arg)
        check = kw.pop('check', False)
        cmd = ['ssh']
        if self.priv: cmd.extend(['-i', self.priv])
        cmd.append(self.host)
        cmd.append('-t')
        if '"' in command or "'" in command:
            command2 = command.replace("'", r"'\''")
            cmd.append(f"'{command2}'")
        else:
            cmd.extend(arg)
        kw['skip'] = self.skip
        ret, out, err =  super().run(*cmd, **kw)
        self.trace(command, ret, out, err, **kw)
        if check and ret:
            raise ExecError(command, ret, out, err)
        return ret, out, err

    def __call__(self, command, **kw):
        ret, out, err = self.run(command, **kw)
        info('\n\t'.join(out))
        return ret

    def chk_cnx(self, report='quiet'):
        ret, out, err = self.run('uname', report='quiet')
        if ret == 0:
            return True
        else:
            if report!='quiet':
                key = f'-i {self.priv} ' if self.priv else ''
                msg = [
                    f' {self.name} ! connection error !',
                    f'ssh {key}{self.host}\n',
                ]
                error('\n'.join(msg))
            return False

    def scp(self, *arg, **kw):
        arg, kw = self.parse(*arg, **kw)
        cmd = ['scp']
        if self.priv: cmd.extend(['-i', self.priv])
        cmd.extend(arg)
        ret, out, err =  super().run(*cmd, **kw)
        self.trace('scp '+' '.join(arg), ret, out, err, **kw)
        return ret, out, err

    def send(self, local, remote=None, quiet=False):
        local =  Path(local)
        assert local.is_file()
        remote = Path(remote) if remote else local
        if not quiet: info(f'\tsend {local} -> {remote}')
        ret, out, err = self.scp(f'{local} {self.host}:{remote}')
        return ret==0

    def fetch(self, remote, local, quiet=False):
        if not quiet: info(f'\tfetch {local} <- {remote}')
        ret, out, err = self.scp(f'{self.host}:{remote} {local}')
        return ret==0

    def rsync_opt(self):
        if self.priv:
            return f'-e "ssh -i {self.priv}"'
        else:
            return '-e ssh'

    def sync(self, src, dst=None):
        assert isdir(src), f'\n ! sync reqires a dir ! {src} !\n'
        if not src.endswith('/'): src+='/'
        if not dst: dst = src
        info(f'\tsync {src} -> {dst}')
        return self.rsync(f'{src} {self.host}:{dst}')

    def read(self, path, mode='rt', critical=True, report='normal'):
        if report=='normal':
            info(f'\tread {path}')
        with NamedTemporaryFile(mode=mode) as tmp:
            self.fetch(path, tmp.name, quiet=True)
            content = tmp.read()
        return content

    def write(self, path, content, mode='wt', report='normal'):
        if report=='normal':
            info(f'\twrite {path}')
        dest = path[:path.rfind('/')]
        self.run(f'mkdir -p {dest}', report=report)
        with NamedTemporaryFile(mode=mode) as tmp:
            tmp.write(content)
            tmp.flush()
            self.send(tmp.name, path, quiet=True)
        return self.read(path, mode=mode.replace('w','r'), report='quiet') == content

    def export(self, name, root):
        info(f'\texport {name} -> {root}')
        cls = self.modules.items[name]
        mod = cls(self.distro)
        for module in mod.submodules:
            self.export(module, root)
        full = import_module(cls.__module__).__file__
        name = basename(full)
        self.send(
            full,
            f'{root}/setux/modules/{name}',
        )

    def remote(self, module, export_path=None, **kw):
        with logger.quiet():
            self.pip.install('setux')
            path = export_path or '/tmp/setux/import'
            name = 'exported.py'
            self.export(module, path)
            kwargs = ', '+', '.join(f"{k}='{v}'" for k,v in kw.items()) if kw else ''
            self.write('/'.join((path, name)), remote_tpl.deploy.format(**locals()))
            ret, out, err = self.script(remote_tpl.script.format(**locals()))
        info('\t'+'\n\t'.join(out))
        return ret, out, err

    def __str__(self):
        return f'SSH({self.name})'
