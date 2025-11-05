"""
@Goal:
@Author:
@Date:
"""

import argparse
import logging as log

import sys
import ringsdb_to_print


def main_pdf(url, output):
    from .printpdf import generate_pdf_from_ringsdb

    generate_pdf_from_ringsdb(url, output)


def set_log_level(verbosity):
    verbosity = verbosity.lower()
    configs = {
        "debug": log.DEBUG,
        "info": log.INFO,
        "warning": log.WARNING,
        "error": log.ERROR,
        "critical": log.CRITICAL,
    }
    if verbosity not in configs.keys():
        raise ValueError(
            f"Unknown verbosity level: {verbosity}\nPlease use any in: {configs.keys()}"
        )
    log.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=configs[verbosity],
    )


def main():
    parser = argparse.ArgumentParser(prog="ringsdb_to_print")
    parser.add_argument(
        "--version",
        action="version",
        version=f"{parser.prog} {ringsdb_to_print.__version__}",
    )

    subparsers = parser.add_subparsers(help="sub-command help")

    pdf = subparsers.add_parser(
        "pdf",
        help="Generate printable PDF from RingsDB deck",
        formatter_class=argparse.MetavarTypeHelpFormatter,
    )
    pdf.add_argument("-u", "--url", type=str, required=True, help="RingsDB deck URL")
    pdf.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.pdf",
        help="Output PDF filename [output.pdf]",
    )
    pdf.set_defaults(subparser="pdf")

    for subparser in (pdf,):
        subparser.add_argument(
            "-v",
            "--verbosity",
            type=str,
            default="info",
            help="Verbosity level  [info]",
        )

    args = parser.parse_args()
    if not hasattr(args, "subparser"):
        parser.print_help()
        return
    set_log_level(args.verbosity)
    log.debug(f"Args: {str(args)}")
    if args.subparser == "pdf":
        main_pdf(args.url, args.output)


if __name__ == "__main__":
    main()
