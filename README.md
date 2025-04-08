# Nexus

Nexus is a command-line tool for converting markdown documents to professionally styled PDFs. It's designed for creating consistent, high-quality documentation from simple markdown files.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Features

- Convert single markdown files or batch process directories
- Customize output with templates and configuration
- Professional document styling with headers, footers, and metadata
- Support for tables, code blocks, and other markdown features
- Configurable page size, margins, and styling options

## Installation

### Prerequisites

- Python 3.8 or higher
- [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) (required by pdfkit)

### Install from source

```bash
git clone https://github.com/y0anfa/nexus.git
cd nexus
pip install .
```

## Quick Start

### Initialize a configuration file

```bash
nexus init
```

This creates a `config.yaml` file with default settings that you can customize.

### Convert a markdown file to PDF

```bash
nexus convert --input document.md --output document.pdf
```

### Batch convert all markdown files in a directory

```bash
nexus batch-convert --input-dir docs/ --output-dir output/
```

## Configuration

Nexus can be configured using a YAML file. Create a default config file with:

```bash
nexus init --output my-config.yaml
```

Example configuration:

```yaml
company: "Your Company"
logo: "path/to/logo.png"
version: "1.0.0"
date: "2023-05-01"
author: "John Doe"
approved_by: "Jane Smith"
comments: "Draft document"
title: "Document Title"
pdf_options:
  page-size: "A4"
  margin-top: "0.75in"
  margin-right: "0.75in"
  margin-bottom: "0.75in"
  margin-left: "0.75in"
```

## Templates

Nexus uses Jinja2 templates for styling PDFs. You can create custom templates or use the built-in templates.

To use a custom template:

```bash
nexus convert --input document.md --output document.pdf --template my-template.html
```

### Creating Custom Templates

Templates are HTML files with Jinja2 templating. Available variables:

- `content`: The HTML content converted from markdown
- `company`: Company name from config
- `logo`: Path to logo from config
- `version`: Document version from config
- `date`: Document date from config
- `author`: Author name from config
- `approved_by`: Approver name from config
- `comments`: Additional comments from config
- `title`: Document title from config

## Command Line Interface

### Global Options

- `--help`: Show help message
- `--version`: Show version information

### Commands

#### `convert`

Convert a single markdown file to PDF.

```bash
nexus convert --input FILE --output FILE [OPTIONS]
```

Options:

- `--input`, `-i`: Path to the input markdown file (required)
- `--output`, `-o`: Path to the output PDF file (required)
- `--template`, `-t`: Path to a custom template file
- `--config`, `-c`: Path to a config file
- `--save-html`: Save intermediate HTML file for debugging

#### `batch-convert`

Convert all markdown files in a directory to PDFs.

```bash
nexus batch-convert --input-dir DIR --output-dir DIR [OPTIONS]
```

Options:

- `--input-dir`, `-i`: Directory containing markdown files (required)
- `--output-dir`, `-o`: Directory for output PDF files (required)
- `--template`, `-t`: Path to a custom template file
- `--config`, `-c`: Path to a config file
- `--save-html`: Save intermediate HTML files for debugging
- `--pattern`, `-p`: Glob pattern to match markdown files (default: *.md)

#### `init`

Initialize a new configuration file with default settings.

```bash
nexus init [OPTIONS]
```

Options:

- `--output`, `-o`: Path to save the config file (default: config.yaml)

## Development

### Setup development environment

```bash
git clone https://github.com/yourusername/nexus.git
cd nexus
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
