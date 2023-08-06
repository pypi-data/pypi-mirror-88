import os.path as op
import os
import tempfile
import argparse
import pkgutil
import inspect
import logging as log


def __get_modules__(m):
    modules = []
    prefix = m.__name__ + '.'
    log.info('prefix : %s' % prefix)
    for importer, modname, ispkg in pkgutil.iter_modules(m.__path__, prefix):
        module = __import__(modname, fromlist='dummy')
        if not ispkg:
            modules.append(module)
        else:
            modules.extend(__get_modules__(module))
    return modules


def __find_all_commands__(m):
    """Browses bx and looks for any class named as a Command"""
    modules = []
    classes = []
    modules = __get_modules__(m)
    forbidden_classes = []  # Test, ScanTest, ExperimentTest]
    for m in modules:
        for name, obj in inspect.getmembers(m):
            if inspect.isclass(obj) and 'Command' in name \
                    and obj not in forbidden_classes:
                classes.append(obj)
    return classes


class ReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            msg = "readable_dir:{0} is not a valid path".format(prospective_dir)
            raise argparse.ArgumentTypeError(msg)
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            msg = "readable_dir:{0} is not a readable dir".format(prospective_dir)
            raise argparse.ArgumentTypeError(msg)


def parse(parser, command):
    c = command(parser.command, parser.args, parser.xnat, parser.destdir,
                parser.overwrite)

    if len(c.args) == 0:
        msg = c.__doc__
        cn = parser.command
        print('\nHelp for command `%s`:\n\n%s' % (cn, msg))

    elif len(c.args) == command.nargs:
        if command.nargs == 1 or c.args[0] in command.subcommands:
            c.parse()
        else:
            subcommands = '\n - '.join(command.subcommands)
            msg = '\n%s invalid\n\nAvailable subcommands:\n - %s' % (c.args[0],
                                                                     subcommands)
            print(msg)

    else:
        msg = c.__doc__
        cn = parser.command
        msg = '\n\nMissing argument(s)\n\nHelp for command `%s`:\n\n%s' % (cn,
                                                                           msg)
        print(msg)


def parse_args(command, args, x, destdir=tempfile.gettempdir(), overwrite=False):
    from bx.command import Command
    parser = Command(command, args, x, destdir, overwrite=overwrite)

    import bx
    commands = __find_all_commands__(bx)
    commands = {e.__name__.split('.')[-1].lower()[:-7]: e for e in commands}

    if command in commands.keys():

        log.debug('Command: %s' % command)
        if command == 'nifti' and len(args) == 1:
            args.insert(0, 'usable')
        if command in ['freesurfer6']:
            ans = ''

            if not os.environ.get('CI_TEST', None):
                while ans not in ['1', '2']:
                    msg = 'Please confirm if you want FREESURFER6 or FREESURFER6_HIRES.' \
                          ' (1) FREESURFER6 (2) FREESURFER6_HIRES ?'
                    ans = input(msg)

            if ans == '2':
                command = 'freesurfer6hires'
                parser = Command(command, args, x, destdir, overwrite=overwrite)

        try:
            parse(parser, commands[command])
        except ValueError as ve:
            log.error(ve)

    else:
        msg = '%s not found \n\nValid commands:\n %s' \
              % (command, '\n '.join([e for e, v in commands.items() if e != '']))
        log.error(msg)
        # raise Exception(msg)


def create_parser():
    import argparse
    cfgfile = op.join(op.expanduser('~'), '.xnat.cfg')

    import bx
    commands = __find_all_commands__(bx)
    commands = {e.__name__.split('.')[-1].lower()[:-7]: e.__doc__ \
                for e in commands if e.__name__ != 'Command'}
    from bx import __version__
    epilog = 'bx (v%s)\n\nExisting commands:\n' % __version__

    for e, v in commands.items():
        i = int(len(str(e)) / 6)
        tabs = (3 - i) * '\t'
        v = '%s%s' % (tabs, v) if v is not None else ''
        epilog = epilog + ' %s %s\n' % (e, str(v).split('\n')[0])

    epilog = epilog + '\nbx is distributed in the hope that it will be useful, ' \
                      'but WITHOUT ANY WARRANTY. \nSubmit issues/comments/PR at ' \
                      'http://gitlab.com/xgrg/bx.\n\nAuthors: Greg Operto, ' \
                      'Jordi Huguet - BarcelonaBeta Brain Research Center (2019)'

    from argparse import RawTextHelpFormatter
    parser = argparse.ArgumentParser(description=epilog,
                                     formatter_class=RawTextHelpFormatter)  # , epilog=epilog)
    parser.add_argument('command', help='bx command')
    parser.add_argument('args', help='bx command', nargs="*")
    parser.add_argument('--config', help='XNAT configuration file',
                        required=False, default=cfgfile)
    parser.add_argument('--dest', help='Destination folder',
                        required=False, action=ReadableDir)
    parser.add_argument('--verbose', '-v', action='store_true', default=False,
                        help='Display verbosal information (optional)', required=False)
    parser.add_argument('--overwrite', '-O', action='store_true', default=False,
                        help='Overwrite', required=False)

    from bx import __version__
    parser.add_argument('-V', '--version', action='version', version="%(prog)s ("+__version__+")")

    return parser
