# PyPI Package Scraper

## Overview

This project is a Python-based tool designed to retrieve the latest version of a package from the Python Package Index (PyPI), download the package, and extract its dependencies for analysis.

---

## How It Works

1. Fetch Package Information  
   The script queries the PyPI JSON API to obtain metadata for the given package, including the latest available version.

2. Select and Download Package  
   The tool selects a downloadable file, prioritizing `.whl` (wheel) format and falling back to `.tar.gz` if necessary. The package is then downloaded using a streaming approach.

3. Extract Package Contents  
   - `.whl` and `.zip` files are extracted using the `zipfile` module  
   - `.tar.gz` files are extracted using the `tarfile` module  

4. Extract Dependencies  
   The script parses dependency information from:
   - `METADATA` or `PKG-INFO` files (primary source)  
   - `requirements.txt` (fallback source)  

5. Output  
   The final output includes the package name, version, and a structured list of dependencies.

---

## Security Perspective

This tool can be used to support security analysis of Python packages by:

- Inspecting package metadata before installation  
- Identifying external dependencies that may introduce risk  
- Supporting supply chain security analysis  
- Assisting in the detection of potentially malicious or suspicious packages  

It provides a foundation for further enhancements such as vulnerability scanning and behavioral analysis.

---

## Error Handling

The script includes handling for common failure scenarios:

- Invalid or non-existent package names  
- Network errors or timeouts during API calls and downloads  
- Missing metadata files within the package  
- Unsupported or unexpected file formats  

Exceptions are managed to ensure the program fails gracefully and provides meaningful error messages.
