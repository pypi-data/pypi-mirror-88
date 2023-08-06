import argparse
import gus.const as THE


def get_parsed():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=THE.VERSION)
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        dest="source",
        default="",
        help="location of source file",
    )
    parser.add_argument(
        "-t",
        "--telescope",
        action="store_const",
        dest="source",
        const="TELESCOPE",
        help="check recent posts indexed by Telescope",
    )
    parser.add_argument(
        "-r",
        "--rtf",
        action="store_const",
        dest="output",
        const="rtf",
        default=THE.OUTPUT,
        help="output as rich text file",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_const",
        dest="output",
        const="json",
        help="output as json",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_const",
        dest="wanted",
        const=THE.ALL,
        default=THE.ALL,
        help="output includes all results",
    )
    parser.add_argument(
        "-g",
        "--good",
        action="store_const",
        dest="wanted",
        const=[THE.GOOD],
        help="output includes only [GOOD] results",
    )
    parser.add_argument(
        "-b",
        "--bad",
        action="store_const",
        dest="wanted",
        const=[THE.FAIL],
        help="output includes only [FAIL] results",
    )
    parser.add_argument(
        "-i", "--ignore", action="store", dest="ignore", help="location of ignore file"
    )
    return parser.parse_args()
