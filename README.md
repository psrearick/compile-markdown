# Compile Markdown

A Python tool for combining Markdown files from a folder hierarchy into a single compiled document. This tool is perfect for creating documentation, books, or reports from multiple Markdown files while preserving structure and formatting.

## Features

- **Hierarchical compilation**: Combines Markdown files from nested folders
- **Configurable ordering**: Use YAML files to specify the order of files and folders
- **Title management**: Automatically handles titles and heading levels
- **Frontmatter support**: Preserves YAML frontmatter as metadata sections
- **Flexible output**: Control what gets included and how it's formatted
- **Recursive processing**: Optionally compile subdirectories recursively into separate files
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
  - If PATH is a directory: Creates a `.md` file named after the source folder inside the directory
  - If PATH is a file: Uses the specified filename directly
- `-p, --propagate`: Propagate compilation up to parent directories
- `-r, --recursive`: Compile files recursively - creates separate compiled files for each subdirectory
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

## Output Behavior

The tool's output behavior depends on whether you specify a directory or a file path:

### Output to Directory
When the output path is a directory (or doesn't exist and will be created as a directory):
```bash
python compile_markdown.py -s ./my-docs -o ./output/
```
- Creates the directory `./output/` if it doesn't exist
- Generates a file named `my-docs.md` inside the output directory
- The filename is derived from the source folder name (with leading numbers removed)

### Output to Specific File
When the output path includes a filename:
```bash
python compile_markdown.py -s ./my-docs -o ./output/documentation.md
```
- Creates the directory `./output/` if it doesn't exist
- Generates a file named `documentation.md` with the compiled content
- Uses the exact filename you specify

### Recursive Output
When using the `--recursive` flag, the tool creates separate compiled files for each subdirectory:
```bash
python compile_markdown.py -r -s ./my-docs -o ./output/
```
- Creates a compiled file for the root directory: `./output/my-docs.md`
- Creates a compiled file for each subdirectory: `./output/subdir1/subdir1.md`, `./output/subdir2/subdir2.md`, etc.
- Maintains the directory structure in the output, with each folder getting its own compiled Markdown file
- Each subdirectory's compiled file contains only the Markdown files from that specific directory

### Default Behavior
Without specifying an output:
```bash
python compile_markdown.py
```
- Creates a `compiled` directory in the source folder
- Generates a file named after the source directory (e.g., `my-project.md`)

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

### Example 1: Basic Output Options
```bash
# Compile current directory to default location (./compiled/)
python compile_markdown.py

# Output to a specific directory (creates "docs.md" inside ./output/)
python compile_markdown.py -s ./docs -o ./output/

# Output to a specific file
python compile_markdown.py -s ./docs -o ./output/combined.md

# Output to current directory with custom filename
python compile_markdown.py -o ./my-documentation.md
```

### Example 2: Recursive Compilation
```bash
# Recursively compile each subdirectory into separate files
python compile_markdown.py -r -s ./docs -o ./output/

# Recursive with custom order file and all options
python compile_markdown.py -r -y ./config/book-order.yaml -o ./published/ --all
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

## File Structure Examples

### Example 1: Default Output (Directory)
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
    └── content.md      # Auto-generated filename from source folder
```

### Example 3: Recursive Output Structure
```
project/
├── compile_markdown.py
├── docs/
│   ├── introduction.md
│   ├── getting-started/
│   │   ├── installation.md
│   │   └── configuration.md
│   └── advanced/
│       ├── api.md
│       └── plugins.md
└── output/
    ├── docs.md                    # Root compilation
    ├── getting-started/
    │   └── getting-started.md     # Subdirectory compilation
    └── advanced/
        └── advanced.md            # Subdirectory compilation
```

## Special Files

- **`.no-headings`**: Place this file in a directory to replace section headings with horizontal rules (`* * *`)
- **`.end_compile`**: Place this file in a directory to prevent recursive compilation beyond this point
- **`order.yaml`**: Defines the compilation order for the directory
- **Frontmatter**: YAML frontmatter in Markdown files is preserved as "Metadata" sections

## Requirements

- Python 3.6+
- PyYAML 6.0.2

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes with tests
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
