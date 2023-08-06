from setux.main import banner


doc = f'''{banner}

setux [Module | Command] [*args | **kwargs] [Target]

Deploy Module or Execute Command on Target


Module or Command:
    - Deploy Module ( see the "modules" command )
    - Execute Command ( see the "help" command )
    - if not specified : enter REPL on Target

Target:
    - May be passed on command line
    - Set in environement as "setux_target"
    - defaults to "Local"
'''


def usage(*args):
    print(doc)
