import os
import os.path as op
import logging as log
from tqdm import tqdm


def download_experiment(x, e, resource_name, validator, overwrite, destdir):

    e_id = e['ID']
    e = x.select.experiment(e_id)
    # resource_name is None when downloading reports only
    if resource_name is not None:
        r = e.resource(resource_name)
        if not r.exists():
            log.error('%s has no %s resource' % (e_id, resource_name))
            return
        dd = op.join(destdir, e_id)
        if op.isdir(dd) and not overwrite:
            msg = '%s already exists. Skipping %s.' % (dd, e_id)
            log.error(msg)
        else:
            if op.isdir(dd) and overwrite:
                msg = '%s already exists. Overwriting %s.' % (dd, e_id)
                log.warning(msg)
            elif not op.isdir(dd):
                os.mkdir(dd)
            r.get(dest_dir=dd)

    v = e.resource('BBRC_VALIDATOR')
    f = v.pdf(validator)

    if f is not None:
        fp = op.join(destdir, f.label()) if resource_name is None \
            else op.join(dd, f.label())
        # if resource_name is None:
        log.debug('Saving it in %s.' % fp)
        f.get(dest=fp)
    return destdir


def download(x, experiments, resource_name, validator, destdir, subcommand,
             overwrite=False):

    if subcommand in ['files', 'report']:
        type = 'experiment'
    elif subcommand == 'snapshot':
        type = 'snapshot'
    elif subcommand == 'rc':
        type = 'rc'
    else:
        log.error('Invalid subcommand (%s).' % subcommand)

    if len(experiments) > 1:
        log.info('Now initiating download for %s experiments.'
                 % len(experiments))
        experiments = tqdm(experiments)
    for e in experiments:
        log.debug(e)
        try:
            if type == 'experiment':
                fp = download_experiment(x, e, resource_name, validator,
                                         overwrite, destdir)

            elif type == 'snapshot':
                fp = download_snapshot(x, e, resource_name, validator,
                                       overwrite, destdir)

            elif type == 'rc':
                fp = download_rc(x, e, resource_name, validator, destdir)
        except KeyboardInterrupt:
            return

    if len(experiments) == 1:
        log.info('Saving it in %s' % fp)


def download_snapshot(x, e, resource_name, validator, overwrite, destdir):
    rn = 'BBRC_VALIDATOR'
    e_id = e['ID']
    r = x.select.experiment(e_id).resource(rn)
    if r.exists():
        fp = op.join(destdir, '%s.jpg' % e_id)
        try:
            fp = r.download_snapshot(validator, fp)
        except Exception as exc:
            log.error('%s has no %s (%s)' % (e_id, validator, exc))
        return fp
    else:
        log.error('%s has no %s' % (e_id, validator))


def download_rc(x, e, resource_name, validator, destdir):
    e_id = e['ID']
    log.debug(e_id)
    subject_label = e['subject_label']

    e = x.select.experiment(e_id)
    r = e.resource(resource_name)
    if not r.exists():
        log.error('%s has no %s resource' % (e_id, resource_name))
        return
    try:
        r.download_rc(destdir)
        v = e.resource('BBRC_VALIDATOR')
        if v.exists():
            fp = op.join(destdir, '%s_%s.jpg' % (subject_label, e_id))
            try:
                v.download_snapshot(validator, fp)
            except Exception as exc:
                log.error('%s has no %s (%s)' % (e_id, validator, exc))
        else:
            log.warning('%s has not %s' % (e, validator))

    except Exception as exc:
        log.error('%s failed. Skipping (%s).' % (e_id, exc))
    return destdir


def measurements(x, experiments, subfunc, resource_name='FREESURFER6'):
    from tqdm import tqdm
    import pandas as pd

    table = []
    for e in tqdm(experiments):
        log.debug(e)
        try:
            s = e['subject_label']
            e_id = e['ID']
            r = x.select.experiment(e_id).resource(resource_name)
            if not r.exists():
                log.error('%s has no %s resource' % (e_id, resource_name))
                continue

            if subfunc == 'aparc':
                volumes = r.aparc()
            elif subfunc == 'aseg':
                volumes = r.aseg()
            elif subfunc == 'centiloids':
                c = r.centiloids(optimized=True)
                volumes = pd.DataFrame([c], columns=[subfunc])
            elif subfunc == 'landau':
                v1 = r.landau_signature(optimized=True,
                                        reference_region='vermis')
                v2 = r.landau_signature(optimized=True,
                                        reference_region='pons')
                volumes = pd.concat([v1, v2])
                del volumes['atlas']
            elif subfunc == 'hippoSfVolumes':
                volumes = r.hippoSfVolumes(mode='T1')
            elif subfunc == 'bamos_volumes':
                volumes = pd.DataFrame([r.volume()], columns=['volume'])
            elif subfunc == 'volumes':
                volumes = r.volumes()
                if isinstance(volumes, dict):
                    volumes = pd.DataFrame(volumes, index=[s])

            volumes['subject'] = s
            volumes['ID'] = e['ID']
            table.append(volumes)
        except KeyboardInterrupt:
            return pd.concat(table).set_index('ID').sort_index()
        except Exception as exc:
            log.error('Failed for %s. Skipping it. (%s)' % (e, exc))

    data = pd.concat(table).set_index('ID').sort_index()
    return data
