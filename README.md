# Compile Markdown

A Python tool for combining Markdown files from a folder hierarchy into a single compiled document. This tool is perfect for creating documentation, books, or reports from multiple Markdown files while preserving structure and formatting.

## Features

- **Hierarchical compilation**: Combines Markdown files from nested folders
- **Configurable ordering**: Use YAML files to specify the order of files and folders
- **Title management**: Automatically handles titles and heading levels
- **Frontmatter support**: Preserves YAML frontmatter as metadata sections
- **Flexible output**: Control what gets included and how it's formatted
- **Recursive processing**: Optionally compile subdirectories recursively
- **Title substitutions**: Replace titles using configuration files

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd compile-markdown
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python compile_markdown.py
```

This will compile all Markdown files in the current directory into a `compiled` folder.

### Command Line Options

```bash
python compile_markdown.py [OPTIONS]
```

#### Options

- `-a, --all`: Include all markdown files, even those not specified in YAML configuration
- `-c, --config PATH`: Path to the YAML config file (default: `compile.yaml` in source directory)
- `-k, --keep-numbers`: Keep leading numbers in titles (e.g., "01 Introduction" stays as is)
- `-o, --output PATH`: Output directory or file path (default: `./compiled` in source directory)
- `-p, --propagate`: Propagate compilation up to parent directories
- `-r, --recursive`: Compile files recursively through subdirectories
- `-s, --source PATH`: Path to the source directory (default: current working directory)
- `-t, --target PATH`: Path to the target directory relative to source directory
- `-y, --yaml PATH`: Path to the YAML order file (default: `order.yaml` in directory to compile)
- `-m, --mod PATH`: Path to the YAML modification file for title substitutions

### Configuration Files

#### Order Configuration (`order.yaml`)

Define the order and structure of your compilation:

```yaml
root:
  - introduction.md
  - getting-started:
      - title: "Getting Started Guide"
      - order:
          - installation.md
          - configuration.md
  - advanced-topics
  - conclusion.md
```

#### Global Configuration (`compile.yaml`)

Set default options for compilation:

```yaml
include_all: true
keep_numbers: false
output: "./docs"
recursive: true
source: "./content"
yaml_path: "./config/order.yaml"
propagate: false
target: ""
modification_path: "./config/modifications.yaml"
```

#### Title Modifications (`modifications.yaml`)

Replace or modify titles during compilation:

```yaml
substitutions:
  "01 Getting Started": "Quick Start Guide"
  "API Reference": "Complete API Documentation"
```

## How It Works

1. **File Discovery**: The tool scans the source directory for Markdown files
2. **Order Resolution**: If an `order.yaml` file exists, it uses that to determine file order; otherwise, it processes files alphabetically
3. **Content Processing**:
   - Extracts and preserves YAML frontmatter
   - Adjusts heading levels based on folder depth
   - Removes or modifies leading numbers from titles
   - Applies title substitutions
4. **Compilation**: Combines all content into a single Markdown file with proper hierarchy

## Examples

### Example 1: Simple Compilation
```bash
# Compile current directory
python compile_markdown.py

# Compile specific source to specific output
python compile_markdown.py -s ./docs -o ./output/combined.md
```

### Example 2: Recursive with Custom Order
```bash
# Recursively compile with custom order file
python compile_markdown.py -r -y ./config/book-order.yaml -o ./published/
```

### Example 3: Full Configuration
```bash
# Use all options
python compile_markdown.py \
  --source ./content \
  --output ./dist/documentation.md \
  --yaml ./config/order.yaml \
  --mod ./config/titles.yaml \
  --recursive \
  --all \
  --keep-numbers
```

## File Structure Example

```
project/
├── compile_markdown.py
├── content/
│   ├── order.yaml
│   ├── 01-introduction.md
│   ├── 02-getting-started/
│   │   ├── installation.md
│   │   └── configuration.md
│   ├── 03-advanced/
│   │   ├── .no-headings
│   │   ├── api.md
│   │   └── plugins.md
│   └── conclusion.md
└── compiled/
    └── content.md
```

## Special Files

- **`.no-headings`**: Place this file in a directory to replace section headings with horizontal rules (`* * *`)
- **`.end_compile`**: Place this file in a directory to prevent recursive compilation beyond this point
- **`order.yaml`**: Defines the compilation order for the directory
- **Frontmatter**: YAML frontmatter in Markdown files is preserved as "Metadata" sections

## Requirements

- Python 3.6+
- PyYAML 6.0.2

## License

[Add your license information here]

## Contributing

[Add contributing guidelines here]
