import argparse
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class IngestConfig:
    inbox: Path
    out: Path
    registry: Path

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mdoc", description="Municipal Document Triage Assistant")
    sp = p.add_subparsers(dest="command", required=True)

    ingest = sp.add_parser("ingest", help="Process documents from inbox folder")
    ingest.add_argument("--inbox", type=Path, required=True, help="Folder with incoming documents")
    ingest.add_argument("--out", type=Path, required=True, help="Output folder")
    ingest.add_argument("--registry", type=Path, required=True, help="Excel registry (.xlsx)")
    return p

def parse_args(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    if args.command == "ingest":
        return args.command, IngestConfig(inbox=args.inbox, out=args.out, registry=args.registry)
    raise ValueError("Unknown command")
