# csg2csg
A tool to translate common Monte Carlo geometry formats between each other.

## How to use
Right now the code is petty rough; as is the install procedure.

Clone the repository
```sh
$ git clone https://github.com/makeclean/csg2csg
```


add the   csg2csg/python path to your $PATH environment

Run python3 csg2csg.py --file <mcnp input file>

## Caveats
Several! Right now only MCNP can be read, and then written to MCNP Serpent and OpenMC. 
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

Tranforms
 - Are read and interpretted, but nothing is done with them, in the future codes that support cell transformations will use it, but right now MCNP is the only code that does surface transformations 
