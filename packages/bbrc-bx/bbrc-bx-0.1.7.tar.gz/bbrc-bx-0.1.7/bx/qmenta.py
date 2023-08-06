from bx.command import Command
from bx import download as dl


class QMENTACommand(Command):
    nargs = 2
    resource_name = 'QMENTA_RESULTS'
    subcommands = ['files']
    validator = 'QMENTA'

    def __init__(self, *args, **kwargs):
        super(QMENTACommand, self).__init__(*args, **kwargs)

    def parse(self):
        args = self.args
        subcommand = self.args[0]
        id = self.args[1]  # should be a project or an experiment_id

        if subcommand == 'files':

            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        overwrite=self.overwrite, subcommand=subcommand)

