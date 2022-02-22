#!/usr/bin/env python3

from csg2csg.MCNPInput import MCNPInput
from csg2csg.SerpentInput import SerpentInput
from csg2csg.OpenMCInput import OpenMCInput
from csg2csg.FLUKAInput import FLUKAInput
from csg2csg.PhitsInput import PhitsInput

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
def main():

    argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="csg conversion tool.")

    parser.add_argument(
        "-d", "--debug", help="Turn on debug logging", action="store_true"
    )

    parser.add_argument("-i", "--input", help="Filename to read in", required=True)

    parser.add_argument(
        "-f",
        "--format",
        choices=["mcnp", "serpent", "openmc", "phits", "fluka"],
        help="format of the input file",
        default="mcnp",
    )

    parser.add_argument(
        "-p",
        "--preserve",
        help="Preserve existing cross section id numbers on write",
        action="store_true",
    )

    parser.add_argument(
        "-o", "--output", nargs="+", help="Output code selections", default="all"
    )

    parser.add_argument(
        "-q",
        "--quick",
        help="Perform quick translation, skip surface comparison - model may not transport",
        action="store_true",
    )

    # parse the arguments
    args = parser.parse_args(argv)

    # if debugging requested
    if args.debug:
        logging.basicConfig(filename="csg2csg.log", level=logging.DEBUG)

    logging.info("Started")

    filename = args.input

    if "all" in args.output:
        codes = ["mcnp", "serpent", "openmc", "phits", "fluka"]
    else:
        codes = args.output

    if args.format == "mcnp":
        # read the mcnp input
        input = MCNPInput(filename, args.quick)
        input.read()
        input.process()
    elif args.format == "serpent":
        # read the serpent input
        input = SerpentInput(filename)
        input.read()
        input.process()
    elif args.format == "openmc":
        raise NotImplementedError("OpenMC input files are not supported yet")
    elif args.format == "phits":
        raise NotImplementedError("Phits input files are not supported yet")
    elif args.format == "fluka":
        raise NotImplementedError("Fluka input files are not supported yet")

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

    logging.info("Finished")


if __name__ == "__main__":
    main()
