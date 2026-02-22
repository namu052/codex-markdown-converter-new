#!/usr/bin/env python3
"""Markdown to HTML converter with enhanced blog-ready styling."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import markdown  # type: ignore
    from markdown.extensions.toc import slugify_unicode
except ModuleNotFoundError as exc:
    sys.stderr.write(
        "The 'markdown' package is required. Install it via 'pip install markdown pygments'.\n"
    )
    raise


BASE_CSS = """
:root {
  color-scheme: light dark;
  --bg: #ffffff;
  --fg: #1f2933;
  --accent: #2563eb;
  --accent-muted: #dbeafe;
  --border: #e5e7eb;
  --code-bg: #0f172a;
  --code-fg: #e2e8f0;
  --inline-code-bg: rgba(37, 99, 235, 0.08);
  --inline-code-fg: #1f2933;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--fg);
}

main {
  max-width: 768px;
  margin: 4rem auto;
  padding: 0 1.5rem 4rem;
  line-height: 1.7;
}

article {
  font-size: 1.0625rem;
}

article h1,
article h2,
article h3,
article h4,
article h5,
article h6 {
  color: var(--fg);
  font-weight: 700;
  line-height: 1.2;
  scroll-margin-top: 5rem;
}

article h1 { font-size: 2.75rem; margin-bottom: 1.5rem; }
article h2 { font-size: 2rem; margin-top: 2.5rem; margin-bottom: 1rem; }
article h3 { font-size: 1.6rem; margin-top: 2rem; margin-bottom: 0.75rem; }
article h4 { font-size: 1.3rem; margin-top: 1.8rem; margin-bottom: 0.5rem; }
article h5 { font-size: 1.1rem; margin-top: 1.6rem; margin-bottom: 0.5rem; }
article h6 { font-size: 1rem; margin-top: 1.4rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.08em; }

article p {
  margin: 1rem 0;
}

article a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease;
}

article a:hover {
  border-color: var(--accent);
}

article img {
  display: block;
  max-width: 100%;
  margin: 2rem auto;
  border-radius: 0.75rem;
  box-shadow: 0 15px 35px rgba(15, 23, 42, 0.15);
}

article blockquote {
  margin: 2rem 0;
  padding: 1.5rem;
  border-left: 4px solid var(--accent);
  background: var(--accent-muted);
  color: #1e293b;
  border-radius: 0.5rem;
}

article ul,
article ol {
  margin: 1.25rem 0 1.25rem 1.75rem;
  padding: 0;
}

article li + li {
  margin-top: 0.5rem;
}

article pre {
  position: relative;
  margin: 2rem 0;
  padding: 1.5rem;
  background: var(--code-bg);
  color: var(--code-fg);
  border-radius: 0.75rem;
  overflow: auto;
  font-family: 'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
  font-size: 0.95rem;
}

article code {
  font-family: 'JetBrains Mono', 'Fira Code', 'SFMono-Regular', Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
  font-size: 0.95rem;
}

article :not(pre) > code {
  padding: 0.15rem 0.35rem;
  background: var(--inline-code-bg);
  color: var(--inline-code-fg);
  border-radius: 0.35rem;
}

article table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  font-size: 0.95rem;
}

article th,
article td {
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  text-align: left;
}

article thead {
  background: rgba(37, 99, 235, 0.08);
  font-weight: 600;
}

article tbody tr:nth-child(even) {
  background: rgba(148, 163, 184, 0.15);
}

article hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 3rem 0;
}

article figure {
  margin: 2.5rem 0;
  text-align: center;
}

article figcaption {
  margin-top: 0.75rem;
  font-size: 0.9rem;
  color: #64748b;
}

header.article-header {
  margin-bottom: 3rem;
}

header.article-header .meta {
  color: #64748b;
  font-size: 0.95rem;
}

nav.toc {
  margin: 2rem 0;
  padding: 1.5rem;
  border-radius: 0.75rem;
  background: rgba(148, 163, 184, 0.15);
}

nav.toc h2 {
  margin-top: 0;
  font-size: 1.1rem;
}

nav.toc ul {
  list-style: none;
  margin: 0;
  padding-left: 0;
}

nav.toc li {
  margin: 0.35rem 0;
}

nav.toc a {
  border: none;
}

@media (max-width: 720px) {
  main {
    margin: 2.5rem auto;
    padding: 0 1rem 2.5rem;
  }

  article h1 {
    font-size: 2.2rem;
  }

  article h2 {
    font-size: 1.8rem;
  }
}
""".strip()


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{title}</title>
    <style>
{css}
    </style>
  </head>
  <body>
    <main>
      <article aria-label=\"Blog post content\">
{body}
      </article>
    </main>
  </body>
</html>
"""


def extract_title(md_text: str) -> str:
    """Return the first level-1 heading as title, else fallback."""
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return "Untitled Article"


def render_markdown(md_text: str) -> str:
    """Render markdown to HTML with commonly used extensions."""
    extensions = [
        "fenced_code",
        "codehilite",
        "tables",
        "toc",
        "sane_lists",
        "smarty",
    ]
    extension_configs = {
        "codehilite": {
            "linenums": False,
            "guess_lang": False,
        },
        "toc": {
            "permalink": True,
            "slugify": slugify_unicode,
        },
    }
    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
    return md.convert(md_text)


def build_document(markdown_text: str, css: str = BASE_CSS) -> str:
    """Create full HTML document from markdown text."""
    rendered = render_markdown(markdown_text)
    title = extract_title(markdown_text)
    formatted_css = "\n".join(f"      {line}" for line in css.splitlines())
    body = "\n".join(f"        {line}" if line else "" for line in rendered.splitlines())
    return HTML_TEMPLATE.format(title=title, css=formatted_css, body=body)


def convert(markdown_path: Path, html_path: Path | None = None) -> Path:
    """Convert markdown file to HTML and write result to disk."""
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    markdown_text = markdown_path.read_text(encoding="utf-8")
    html = build_document(markdown_text)

    if html_path is None:
        html_path = markdown_path.with_suffix(".html")

    html_path.write_text(html, encoding="utf-8")
    return html_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Markdown files into styled HTML blog posts.",
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Path to the Markdown file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Optional path for the generated HTML file. Defaults to <source>.html",
    )
    parser.add_argument(
        "--css",
        type=Path,
        help="Optional path to a CSS file that overrides the default theme.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    css_text = BASE_CSS
    if args.css:
        if not args.css.exists():
            sys.stderr.write(f"CSS override not found: {args.css}\n")
            return 1
        css_text = args.css.read_text(encoding="utf-8")

    markdown_text = args.source.read_text(encoding="utf-8")
    html = build_document(markdown_text, css=css_text)

    output_path = args.output or args.source.with_suffix(".html")
    output_path.write_text(html, encoding="utf-8")

    print(f"Generated HTML -> {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
