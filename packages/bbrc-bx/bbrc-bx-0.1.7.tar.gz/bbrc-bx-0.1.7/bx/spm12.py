from bx.command import Command
from bx import download as dl


class SPM12Command(Command):
    """SPM12

    Available subcommands:
     files:\t\tdownload all `SPM12` outputs (segmentation maps, warp fields, everything...)
     volumes:\t\tcreates an Excel table with GM/WM/CSF volumes
     snapshot:\t\tdownload a snapshot from the segmentation results
     report:\t\tdownload the validation report issued by `SPM12Validator`
     tests:\t\tcreates an Excel table with all automatic tests outcomes from `SPM12`
     rc:\t\tdownloads rc* files (DARTEL imports)

    Usage:
     bx spm12 <subcommand> <resource_id>
    """
    nargs = 2
    resource_name = 'SPM12_SEGMENT'
    subcommands = ['volumes', 'files', 'report', 'snapshot', 'tests', 'rc']
    validator = 'SPM12SegmentValidator'

    def __init__(self, *args, **kwargs):
        super(SPM12Command, self).__init__(*args, **kwargs)

    def parse(self, test=False):
        subcommand = self.args[0]
        id = self.args[1]

        if subcommand in ['files', 'report', 'snapshot']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        overwrite=self.overwrite, subcommand=subcommand)

        elif subcommand in ['rc']:
            self.run_id(id, dl.download, resource_name=self.resource_name,
                        validator=self.validator, destdir=self.destdir,
                        subcommand='rc')

        elif subcommand == 'volumes':
            df = self.run_id(id, dl.measurements, subfunc=subcommand,
                             resource_name=self.resource_name, max_rows=10)
            self.to_excel(id, df)

        elif subcommand == 'tests':
            version = ['*', '0390c55f']
            from bx import validation as val
            df = self.run_id(id, val.validation_scores,
                             validator=self.validator,
                             version=version, max_rows=25)
            self.to_excel(id, df)
