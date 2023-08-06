# bx

[![pipeline status](https://gitlab.com/xgrg/bx/badges/master/pipeline.svg)](https://gitlab.com/xgrg/bx/commits/master)
[![coverage report](https://gitlab.com/xgrg/bx/badges/master/coverage.svg)](https://gitlab.com/xgrg/bx/commits/master)
[![downloads](https://img.shields.io/pypi/dm/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)
[![python versions](https://img.shields.io/pypi/pyversions/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)
[![pypi version](https://img.shields.io/pypi/v/bbrc-bx.svg)](https://pypi.org/project/bbrc-bx/)

BarcelonaBeta + XNAT = BX

## Example:

![example](https://gitlab.com/xgrg/tweetit/raw/master/resources/004-Collecting-FreeSurfer-data-from-XNAT.gif)

## Usage

```
bx <command> <subcommand> <resource_id> --config /path/to/.xnat.cfg --dest /tmp [--overwrite]
```

`resource_id` may be a reference to a whole XNAT project, some specific imaging
session (as found in the table returned by `bx id PROJECT_ID`) or a 'list' of
sessions (a list of existing lists may be obtained by `bx lists display`).

### Commands:

```
bx nifti <resource_id>
```

- Download a NIfTI from a given sequence from an experiment/entire project.


## SPM12

```
bx spm12 volumes <resource_id>
```

- Download a table with grey/white matter and CSF volumes estimated from SPM12 segmentations

```
bx spm12 files <resource_id>
```

- Download SPM12 segmentations from an experiment/entire project

```
bx spm12 report <resource_id>
```

- Download a quality report from an SPM12 segmentation for an experiment/entire project

```
bx spm12 tests <resource_id>
```

- Download a table with results from automatic validation tests from an SPM12 segmentation for an experiment/entire project

```
bx spm12 snapshot <resource_id>
```

- Download a snapshot of SPM12 segmentation results for an experiment/entire project


## CAT12

```
bx cat12 volumes <resource_id>
```

- Download a table with grey/white matter and CSF volumes estimated from CAT12 segmentations

```
bx cat12 files <resource_id>
```

- Download CAT12 segmentations from an experiment/entire project

```
bx cat12 report <resource_id>
```

- Download a quality report from an CAT12 segmentation for an experiment/entire project

```
bx cat12 tests <resource_id>
```

- Download a table with results from automatic validation tests from an CAT12 segmentation for an experiment/entire project

```
bx cat12 snapshot <resource_id>
```

- Download a snapshot of CAT12 segmentation results for an experiment/entire project


## FreeSurfer6

```
bx freesurfer6 aseg <resource_id>
```

- Download a table with FreeSurfer `aseg` results for an experiment/entire project

```
bx freesurfer6 aparc <resource_id>
```

- Download a table with FreeSurfer `aparc` results for an experiment/entire project

```
bx freesurfer6 hippoSfVolumes <resource_id>
```

- Download a table with FreeSurfer `hippoSfVolumes` results for an experiment/entire project


```
bx freesurfer6 snapshot <resource_id>
```

- Download a snapshot of SPM12 segmentation results for an experiment/entire project


```
bx freesurfer6 files <resource_id>
```

- Download FreeSurfer6 segmentations from an experiment/entire project

## ASHS


```
bx ashs volumes <resource_id>
```

- Download a table with hippocampal subfield volumes produced by ASHS for an
 experiment/entire project


 ```
 bx ashs files <resource_id>
 ```

 - Download ASHS segmentations from an experiment/entire project


 ```
 bx ashs snapshot <resource_id>
 ```

 - Download a snapshot of SPM12 segmentation results for an experiment/entire project

## DTIFIT


 ```
 bx dtifit files <resource_id>
 ```

 - Download DTIFIT results from an experiment/entire project


 ```
 bx dtifit snapshot <resource_id>
 ```

 - Download a snapshot of DTIFIT results for an experiment/entire project


## Cortical AD signatures

```
bx signature thickness <resource_id>
bx signature grayvol <resource_id>
```

- Download composite measurements labeled as 'signatures' of Alzheimer's Disease
as described in *Jack et al., Alzheimers Dement. 2017* and *Dickerson et al., Neurology, 2011*.


## PET imaging

```
bx ftm maps <resource_id>
bx fdg maps <resource_id>
```
- Download FTM/FDG images provided some user-specified reference region.

```
bx ftm centiloids <resource_id>
```
- Collect centiloid scales from amyloid maps for a given session/over an entire
project and store them in an Excel file.

```
bx fdg landau <resource_id>
```
- Collect AD signatures as described in *Landau et al., Ann Neurol., 2012* for
a given session / over an entire project and store them in an Excel file.


## Miscellaneous

```
bx id <resource_id>
```

- Download a table including subject IDs, experiment IDs and XNAT IDs for an experiment/entire project


```
bx mrdates <resource_id>
```

- Download a table with acquisition dates from an experiment/entire project

## White matter lesions

```
bx bamos volumes <resource_id>
```

- Download volumes of white matter lesions as segmented by BaMOS (*Sudre et al.,
  IEEE TMI, 2015*).


## Dependencies

Requires [`bbrc-pyxnat>=1.4.1`](https://gitlab.com/pyxnat/pyxnat/tree/bbrc) and
the following librairies: `requests`, `six`, `lxml`, `nibabel`, `pydicom`,
  `numpy`, `pandas`, `xlutils`, `tqdm` and `openpyxl`.


## Install

```
pip install bbrc-bx
```

## Development

Please contact us for details on how to contribute.

[![BarcelonaBeta](https://www.barcelonabeta.org/sites/default/files/logo-barcelona-beta_0.png)](https://www.barcelonabeta.org/)
