"""Publish an HTML SDLC artifact to Confluence Cloud."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.confluence_publisher import publish_file


def main() -> int:
    """Parse CLI arguments, publish one HTML file, and print its page URL."""
    parser = argparse.ArgumentParser(description="Publish an HTML document to Confluence")
    parser.add_argument("path", help="Path to the HTML document")
    parser.add_argument("--title", required=True, help="Confluence page title")
    args = parser.parse_args()

    page = publish_file(args.path, args.title)
    print(f"Published Confluence page {page.get('id', 'unknown')}: {args.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
