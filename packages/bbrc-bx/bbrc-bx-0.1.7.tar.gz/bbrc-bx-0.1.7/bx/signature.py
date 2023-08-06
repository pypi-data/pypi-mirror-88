from bx.command import Command
from bx import download as dl
import logging as log


class SignatureCommand(Command):
    """Download composite measurements labeled as 'signatures' of Alzheimer's Disease

    Available subcommands:
     thickness:\t\tbased on FreeSurfer's cortical thickness
     grayvol:\t\tbased on FreeSurfer's local cortical gray matter volumes

    Usage:
     bx signature <subcommand> <resource_id>

    Signatures are calculated in two versions, weighted and not.
    Weighted means that the formula has been applied by normalizing each
    ROI value by local surface area (as explained in the papers).
    Not-weighted versions correspond to mean values across regions.

    References:
    - Jack et al., Alzheimers Dement. 2017
    - Dickerson et al., Neurology, 2011
    """
    nargs = 2
    subcommands = ['thickness', 'grayvol']

    def __init__(self, *args, **kwargs):
        super(SignatureCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]  # should be a project or an experiment_id

        if subcommand in ['thickness', 'grayvol']:
            from bx import xnat
            experiments = xnat.collect_experiments(self.xnat, id, max_rows=10)
            d = {'thickness': 'ThickAvg', 'grayvol': 'GrayVol'}
            df = signatures(self.xnat, experiments, d[subcommand],
                            resource_name='FREESURFER6_HIRES')
            self.to_excel(id, df)


def __signature__(x, experiment_id, regions, weighted=True,
                  measurement='ThickAvg', resource_name='FREESURFER6_HIRES'):

    e = x.select.experiment(experiment_id)
    r = e.resource(resource_name)
    aparc = r.aparc()

    weighted_sum = 0
    total_surf_area = 0

    query = 'region == "{region}" & side == "{side}" & \
             measurement == "{measurement}"'

    for r in regions:
        for s in ['left', 'right']:
            q = query.format(region=r, side=s, measurement=measurement)
            thickness = float(aparc.query(q)['value'])

            q = query.format(region=r, side=s, measurement='SurfArea')
            surf_area = int(aparc.query(q)['value'])

            weighted_sum += thickness * surf_area if weighted else thickness
            total_surf_area += surf_area

    if weighted:
        final = weighted_sum / total_surf_area
    else:
        final = weighted_sum / (2 * len(regions))

    return final


def signature(x, experiment_id, measurement=None, resource_name='FREESURFER6_HIRES'):
    import pandas as pd

    columns = ['signature', 'weighted', 'measurement', 'value']
    table = []
    for sig in ['jack', 'dickerson']:

        if sig == 'jack':
            regions = ['entorhinal', 'inferiortemporal', 'middletemporal',
                       'fusiform']
        elif sig == 'dickerson':
            regions = ['middletemporal', 'inferiortemporal', 'temporalpole',
                       'inferiorparietal', 'superiorfrontal', 'superiorparietal',
                       'supramarginal', 'precuneus', 'parstriangularis',
                       'parsopercularis', 'parsorbitalis']

        for weighted in [False, True]:
            meas = ['ThickAvg', 'GrayVol']
            if measurement:
                meas = [measurement]
            for m in meas:
                res = __signature__(x, experiment_id, regions, weighted, m,
                                    resource_name=resource_name)
                row = [sig, weighted, m, res]
                table.append(row)
    return pd.DataFrame(table, columns=columns)


def signatures(x, experiments, measurement=None, resource_name='FREESURFER6_HIRES'):
    from tqdm import tqdm
    import pandas as pd

    table = []
    for e in tqdm(experiments):
        log.debug(e)
        try:
            s = e['subject_label']
            e_id = e['ID']
            volumes = signature(x, e_id, measurement=measurement,
                                resource_name=resource_name)

            volumes['subject'] = s
            volumes['ID'] = e['ID']
            table.append(volumes)
        except KeyboardInterrupt:
            return pd.concat(table).set_index('ID').sort_index()
        except Exception as exc:
            log.error('Failed for %s. Skipping it. (%s)'%(e, exc))

    data = pd.concat(table).set_index('ID').sort_index()
    return data
