# Nuclei Templates Management Script

## Overview

This script helps manage Nuclei templates by organizing them into blocks and removing duplicates.

## Features

- Count the total number of YAML templates in a specified directory.
- Remove duplicate templates using `fdupes`.
- Organize templates into blocks of a specified size within a `partitioned` directory.

## Prerequisites

- Python 3.x installed.
- `fdupes` package installed (for duplicate removal).

## Usage

1. Clone the repository or download the `manage-cent-templates.py` script.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script with Python 3:

   ```bash
   python3 manage-cent-templates.py
