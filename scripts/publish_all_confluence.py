"""Publish all approved AI-Expense-Advisor SDLC artifacts to Confluence."""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.confluence_publisher import ConfluenceConfig, ConfluencePublishError, ConfluenceClient


ARTIFACTS = (
    ("Requirements", "docs/requirements.md"),
    ("Architecture", "docs/architecture.md"),
    ("Design Review", "docs/design-review.md"),
    ("Sprint Plans", "docs/impl-plan.md"),
    ("Test Reports", "docs/test-report.md"),
    ("Release Notes", "docs/release-notes.md"),
    ("Audit Reports", "docs/workflow-report-WF-2026-001.html"),
)


def markdown_to_storage_html(markdown: str) -> str:
    """Convert approved Markdown into escaped, readable Confluence HTML."""
    lines = markdown.splitlines()
    output: list[str] = []
    in_code_block = False
    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                output.append("</pre>")
            else:
                output.append("<pre>")
            in_code_block = not in_code_block
        elif in_code_block:
            output.append(html.escape(line))
        elif line.startswith("### "):
            output.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("## "):
            output.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            output.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("- "):
            output.append(f"<li>{html.escape(line[2:])}</li>")
        elif line.strip():
            output.append(f"<p>{html.escape(line)}</p>")
    if in_code_block:
        output.append("</pre>")
    return "\n".join(output)


def publish_artifacts(dry_run: bool = False) -> list[str]:
    """Publish each configured artifact and return the resulting page IDs."""
    root = Path(__file__).parents[1]
    client = None if dry_run else ConfluenceClient(ConfluenceConfig.from_environment())
    page_ids: list[str] = []
    if dry_run:
        print("DRY RUN: AI Expense Advisor")
    else:
        root_response = client.publish_page(
            "AI Expense Advisor",
            "<h1>AI Expense Advisor</h1><p>Agentic SDLC documentation.</p>",
        )
        root_page_id = root_response.get("id")
        if root_page_id is None:
            raise ConfluencePublishError("Confluence root page response did not include an id")
        page_ids.append(str(root_page_id))
        print(f"Published AI Expense Advisor: page {root_page_id}")

    for title, relative_path in ARTIFACTS:
        path = root / relative_path
        content = path.read_text(encoding="utf-8")
        storage_html = content if path.suffix == ".html" else markdown_to_storage_html(content)
        if dry_run:
            print(f"DRY RUN: {title} <- {relative_path}")
            continue
        response = client.publish_page(
            title,
            storage_html,
            parent_page_id=root_page_id,
        )
        page_id = str(response.get("id", "unknown"))
        page_ids.append(page_id)
        print(f"Published {title}: page {page_id}")
    return page_ids


def main() -> int:
    """Publish all approved artifacts or display the batch in dry-run mode."""
    parser = argparse.ArgumentParser(description="Publish AI-Expense-Advisor artifacts to Confluence")
    parser.add_argument("--dry-run", action="store_true", help="List pages without contacting Confluence")
    args = parser.parse_args()
    publish_artifacts(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
