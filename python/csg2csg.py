#!/usr/env/python3

from MCNPInput import MCNPInput
from SerpentInput import SerpentInput

# for debug info
import logging, sys 
import argparse

# the main worker
def main(argv):

    parser = argparse.ArgumentParser(description='csg conversion tool.')
    parser.add_argument('-d','--debug', help = 'turn on debug logging',
                        action="store_true")
    parser.add_argument('-f','--file', help = 'filename to read')
    
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
    serpent.write_serpent("file.serp")
    mcnp = MCNPInput()
    mcnp.from_input(input)
    mcnp.write_mcnp("file.mcnp")

    logging.info("Finshed")

if __name__ == "__main__":
    main(sys.argv[1:])
    
