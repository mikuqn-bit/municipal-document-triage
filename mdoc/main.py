from .cli import parse_args
from .pipeline import run_ingest

def main(argv=None) -> int:
    cmd, cfg = parse_args(argv)
    if cmd == "ingest":
        run_ingest(cfg)
        return 0
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
