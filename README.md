# Markdown to HTML Converter

This project provides a Python-based transformer that turns Markdown content into a professionally styled, publication-ready HTML page. It supports fenced code blocks, tables, automatic table of contents anchors, and a built-in blog theme.

## Requirements

- Python 3.9 or newer
- Git (for cloning the repository)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-org>/codex-markdown-converter.git
   cd codex-markdown-converter
   ```
   Replace `<your-org>` with the account or organization that hosts the repository.

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   On Windows PowerShell use `./.venv/Scripts/Activate.ps1`.

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install markdown pygments
   ```

## Usage

Convert any Markdown file to HTML:

```bash
python markdown_converter.py path/to/input.md -o path/to/output.html
```

- If `-o/--output` is omitted, the script writes a `.html` file alongside the source Markdown.
- Provide a custom CSS file with `--css custom.css` to override the default theme.

## Testing the Converter

1. Ensure you are inside the virtual environment (`source .venv/bin/activate`).
2. Create a sample Markdown file or use one in the repository, for example:
   ```bash
   python markdown_converter.py sample.md -o sample.html
   ```
3. Open the generated HTML in a browser to verify formatting and styling.

For additional manual testing, try Markdown features such as:

- Nested headings to verify the automatically generated table of contents.
- Fenced code blocks with language hints to inspect syntax highlighting.
- Tables, blockquotes, and images to confirm layout and responsive behavior.

## Deactivating the Environment

When you are finished, deactivate the virtual environment with:

```bash
deactivate
```

## Troubleshooting

- If you encounter `ModuleNotFoundError: No module named 'markdown'`, ensure the virtual environment is active and dependencies are installed.
- On macOS systems that enforce PEP 668, always install packages inside the virtual environment rather than globally.

## License

Add your chosen license here.
