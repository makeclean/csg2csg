#!/usr/env/python3

from MCNPInput import MCNPInput
from SerpentInput import SerpentInput
from OpenMCInput import OpenMCInput
from FLUKAInput import FLUKAInput
from PhitsInput import PhitsInput

# for debug info
import logging, sys 
import argparse
import os

# make a directory in which wthe output of csg2csg will
# be stored
def mkdir(directory):
    try:
        os.mkdir(directory)
    except: 
        pass

# the main worker
def main(argv):

    parser = argparse.ArgumentParser(description='csg conversion tool.')
    parser.add_argument('-d','--debug', help = 'turn on debug logging',
                        action="store_true")
    parser.add_argument('-f','--file', help = 'filename to read')
    parser.add_argument('-p','--preserve', 
                        help = 'preserve existing cross section id numbers on write',
                        action="store_true")
    
    parser.add_argument('-o','--output', help = 'output code selections')

    # parse the arguments
    args = parser.parse_args(argv)
      
    # if debugging requested
    if args.debug:
        logging.basicConfig(filename="csg2csg.log", level=logging.DEBUG)

    logging.info("Started")

    if args.file is None:
        print('file not specified')
        sys.exit(1)
    else:
        filename = args.file
    
    if args.output is None:
        print('no output options selected')
        sys.exit(1)
    else:
        if "all" in args.output:
            codes = ["mcnp","serpent","openmc","phits","fluka"]
        else:
            codes = args.output.split(',')

    # read the mcnp input
    input = MCNPInput(filename)
    input.read()
    input.process()

    for code in codes:
        if "serpent" in code:
            print("Producing Serpent output...")
            serpent = SerpentInput()
            serpent.from_input(input)
            mkdir("serpent")
            serpent.write_serpent("serpent/file.serp")
        if "mcnp" in code:
            print("Producing MCNP output...")
            mcnp = MCNPInput()
            mcnp.from_input(input)
            mkdir("mcnp")
            mcnp.write_mcnp("mcnp/file.mcnp")
        if "openmc" in code:
            print("Producing OpenMC output...")
            openmc = OpenMCInput()
            openmc.from_input(input)
            mkdir("openmc")
            openmc.write_openmc("openmc")
        if "phits" in code:
            print("Producing Phits output...")
            phits = PhitsInput()
            phits.from_input(input)
            mkdir("phits")
            phits.write_phits("phits/phits.in")
        if "fluka" in code:
            print("Producing FLUKA output...")
            fluka = FLUKAInput()
            fluka.from_input(input)
            mkdir("fluka")
            fluka.write_fluka("fluka/fluka.inp")
    
    logging.info("Finshed")

if __name__ == "__main__":
    main(sys.argv[1:])
    
