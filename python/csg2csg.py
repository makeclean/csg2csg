#!/usr/env/python3

from MCNPInput import MCNPInput
from SerpentInput import SerpentInput
from OpenMCInput import OpenMCInput

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
    
    input = MCNPInput(filename)
    input.read()
    input.process()

    serpent = SerpentInput()
    serpent.from_input(input)
    mkdir("serpent")
    serpent.write_serpent("serpent/file.serp")

    mcnp = MCNPInput()
    mcnp.from_input(input)
    mkdir("mcnp")
    mcnp.write_mcnp("mcnp/file.mcnp")

    openmc = OpenMCInput()
    openmc.from_input(input)
    mkdir("openmc")
    openmc.write_openmc("openmc/file.openmc")
    
    logging.info("Finshed")

if __name__ == "__main__":
    main(sys.argv[1:])
    
