"""Command-line entry point for running resume analysis outside the UI."""

import argparse
import json
from pathlib import Path

from pipeline.analyzer import analyze_resume


def parse_args():
    """Parse command-line arguments for the CLI analyzer."""
    parser = argparse.ArgumentParser(
        description="Analyze a PDF resume against a job description."
    )
    parser.add_argument("resume", type=Path, help="Path to the resume PDF")
    parser.add_argument("job_description", type=Path, help="Path to the job description")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON output path; prints to stdout when omitted",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    result = analyze_resume(
        str(args.resume),
        args.job_description.read_text(encoding="utf-8"),
    )
    rendered = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Analysis written to {args.output}")
    else:
        print(rendered)
