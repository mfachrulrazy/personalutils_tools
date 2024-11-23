# Internal Utilities Personal Tools

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

**Internal Tools** is a lightweight and simple Python-based utility package designed to streamline common file processing tasks. It includes three scripts:
- **CSV to JSON Converter**: Converts CSV files into JSON format.
- **File Joiner**: Merges multiple Excel or CSV files into a single file.
- **PDF Merger**: Combines multiple PDF files into a single PDF document.

These tools are highly configurable and designed for simplicity, making them perfect for internal or personal use.

---

## Features

- **CSV to JSON Conversion**:
  - Converts CSV files into neatly formatted JSON files.
  - Automatically processes all `.csv` files in the source directory.
- **File Joiner**:
  - Merges Excel and CSV files with consistent column structures.
  - Outputs the combined data as a single Excel file.
- **PDF Merger**:
  - Combines multiple PDF files into a single file, maintaining page order. Sort the file by name to order the joined pdf files.
- **Configurable**:
  - Source and output directories can be specified using a configuration file.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Pip (Python package installer)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/internal-tools.git
   cd internal-tools

2. Install dependencies:
    ```bash
    pip install -r requirements.txt


## Configuration
The tool uses a config.json file for specifying directories:

- d_csvjsonin: Directory containing input files for CSV to JSON.
- d_csvjsonout: Directory where output files of CSV of JSON will be saved.
- d_joinin: Directory containing input files for Joining CSV or Excel script.
- d_joinout: Directory where output files of Joining CSV or Excel script will be saved.
- d_pdfin: Directory containing input files for Merge PDF Files.
- d_pdfout: Directory where output files of Merge PDF Files will be saved.
- csv_delimiter: default is ";"
- output_filename: only for Join file script

Update the paths as needed before running the scripts.

## Usage
Use the tool from command line:
     ```bash
    python [script].py

## License
This project is licensed under the MIT License. See the LICENSE file for details.