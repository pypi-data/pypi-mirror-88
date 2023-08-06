from bx.command import Command
from bx import download as dl


class BAMOSCommand(Command):
    """BAMOS (Bayesian MOdel Selection for white matter lesion segmentation)
    Reference: Sudre et al., IEEE TMI, 2015

    Available subcommands:
     files:\t\tdownload all `BAMOS` outputs
     volumes:\t\tcreates an Excel table with WM lesion volumes

    Usage:
     bx bamos <subcommand> <resource_id>
    """
    nargs = 2
    resource_name = 'BAMOS'
    subcommands = ['volumes', 'files']
    validator = 'BAMOSValidator'

    def __init__(self, *args, **kwargs):
        super(BAMOSCommand, self).__init__(*args, **kwargs)

    def parse(self, test=False):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['files']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        overwrite=self.overwrite, subcommand=subcommand)

        elif subcommand == 'volumes':
            sf = 'bamos_volumes'
            df = self.run_id(id, dl.measurements, subfunc=sf,
                             resource_name=self.resource_name, max_rows=10)
            self.to_excel(id, df)
