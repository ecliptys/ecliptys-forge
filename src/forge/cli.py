import argparse

from forge.commands import analyze


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="forge",
        description="Local-first repository intelligence for AI coding agents.",
    )

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a repository.",
    )

    analyze_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the repository. Defaults to the current directory.",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        analyze.main(args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()