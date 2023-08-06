from os import environ
from os.path import expanduser
from sys import argv

from setux.targets import Local, SSH
from setux.logger import debug
from setux.repl import commands
from setux.repl.repl import repl, help
from .usage import usage


def get_target(name=None, dest=None):
    name = name or environ.get('setux_target')
    dest = dest or environ.get('setux_outdir', expanduser('~/setux'))
    if name:
        target = SSH(name=name, host=name, outdir=dest)
        if not target.cnx:
            target = None
    else:
        target = Local(outdir=dest)
    return target


def main():

    if len(argv)==1:
        target = get_target()
        debug(f'repl {target}')
        repl(target)


    else:
        del argv[0]
        try: target = get_target(argv[-1])
        except: target = None
        if target:
            del argv[-1]
        else:
            target = get_target()

        if argv:
            name, *args = argv
        else:
            repl(target)
            return

        if name in target.modules.items:
            try:
                k = dict(i.split('=') for i in args)
                try:
                    target.deploy(name, **k)
                except KeyError as x:
                    key = x.args[0]
                    print(f'\n ! missing argument : {key}  !\n')
                    commands['module'](target, name)
            except ValueError:
                m = "module's arguments must be keyword arguments\n"
                print(f'\n ! invalid argument : {" ".join(args)} !\n ! {m}')
                commands['module'](target, name)
            return

        if name=='help':
            cmd = help
            help(args[0] if args else None)
        else:
            cmd = commands.get(name)
            if cmd:
                cmd(target, args[0] if args else None)
            else:
                print(f'\n ! {name} !\n')
                return usage()


