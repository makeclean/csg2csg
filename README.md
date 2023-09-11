[![CI test results](https://github.com/makeclean/csg2csg/actions/workflows/ci.yaml/badge.svg)](https://github.com/makeclean/csg2csg/actions/workflows/ci.yaml)

# csg2csg
A tool to translate common Monte Carlo geometry formats between each other.

## How to use
Right now the code is petty rough.

Install the latest version released on PyPi using pip
```bash
pip3 install csg2csg --user
```

Install the latest version on the repository using pip
```bash
pip install git+https://github.com/makeclean/csg2csg.git  --user
```

Run from the terminal with ``csg2csg -i filename -f format`` where filename is the input filename and format is the file format of the input file. Options for the file format include several neutronics codes [mcnp, serpent, openmc, phits, fluka] each is at a different level of completeness.

The default is to attempt to translate the input file into all neutronics codes but users can specify which codes with the ``-o`` flag.

To see all the run options type ``csg2csg -h`` in the terminal

## Caveats
Several! Right now only MCNP can be read, and then written to MCNP, Serpent and OpenMC. 
When the file can be read only a subset of MCNP surfaces can be read

MCNP Surfaces Supported
 - P,PX,PY,PZ
 - S SO SX  SY SZ
 - CX CY CZ C/X C/Y C/Z
 - SQ
 - GQ
 - KX, KY, KZ
 - TX TY TZ
 - Macrobodies - RPP, SPH and RCC 
 - X, Y, Z - one and two coefficent only


MCNP Surfaces Not Yet Supported
 - X, Y, Z - three coefficient
 - Macrobodies - BOX, RHP, HEX, REC, TRC, ELL, WEB, ARB

Transforms
 - Are read and interpretted, but nothing is done with them, in the future codes that support cell transformations will use it, but right now MCNP is the only code that does surface transformations 
