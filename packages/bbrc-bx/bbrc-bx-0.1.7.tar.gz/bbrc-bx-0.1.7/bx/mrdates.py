from bx.command import Command
import tempfile


class MRDatesCommand(Command):
    """Collect acquisition dates from MR sessions.

    Usage:
     bx mrdates <resource_id>
    """
    nargs = 1

    def __init__(self, *args, **kwargs):
        super(MRDatesCommand, self).__init__(*args, **kwargs)

    def parse(self):
        id = self.args[0]  # should be a project or an experiment_id

        from bx.dicom import collect_mrdates
        res = self.run_id(id, collect_mrdates)
        if len(res) == 1:
            print(res.iloc[0])
        else:
            if self.destdir is None:
                self.destdir = tempfile.gettempdir()
            self.to_excel(id, res)
