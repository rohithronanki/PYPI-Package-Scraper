# 🐍 PyPI Package Scraper

A Python-based tool that retrieves the latest version of a package from PyPI, downloads it, and extracts its dependencies for analysis.

---

## 🚀 Features

- 🔍 Fetches latest package version from PyPI
- 📦 Downloads package (`.whl` or `.tar.gz`)
- 📂 Extracts package contents safely
- 🧩 Parses dependencies from:
  - `METADATA` / `PKG-INFO`
  - `requirements.txt` (fallback)
- ⚠️ Handles errors (network issues, missing files, unsupported formats)

---

## 📌 Use Case

This tool is useful for:
- Dependency analysis
- Supply chain security research
- Malware inspection in Python packages
- Automation in DevSecOps pipelines

---

## 🛠️ Installation

```bash
pip install requests
```

---

## ▶️ Usage

```bash
python pypiscrapper.py
```

### Input

```bash
Enter package name: requests
```

### Output

```bash
Package: requests
Version: 2.x.x
Dependencies:
 - certifi
 - urllib3
 - charset-normalizer
```

---

## ⚙️ How It Works

1. **Fetch Package Info**
   - Uses PyPI JSON API:
   ```
   https://pypi.org/pypi/<package>/json
   ```

2. **Select Download File**
   - Prefers `.whl` (wheel)
   - Falls back to `.tar.gz`

3. **Download Package**
   - Streams file to avoid memory issues

4. **Extract Files**
   - Uses:
     - `zipfile` for `.whl`
     - `tarfile` for `.tar.gz`

5. **Parse Dependencies**
   - Primary: `METADATA` / `PKG-INFO`
   - Fallback: `requirements.txt`

---

## 📂 Project Structure

```
pypiscrapper.py
README.md
```

---

## ⚠️ Error Handling

The script handles:
- ❌ Invalid package names
- 🌐 Network timeouts
- 📦 Unsupported file formats
- 📄 Missing metadata files

---

## 🔐 Security Perspective

This tool can be extended for:
- Malicious package detection
- Dependency risk scoring
- Static analysis of packages
- Supply chain attack prevention

---

## 🔧 Future Improvements

- 🔁 Recursive dependency resolution
- 📊 Dependency tree visualization
- 🚨 CVE/Vulnerability integration
- ⚡ Parallel processing for bulk scanning
- 🌐 REST API interface

---

## 🤝 Contributing

Feel free to fork and improve the project:
- Add new parsing methods
- Improve detection capabilities
- Optimize performance

---

## 📜 License

This project is for educational and research purposes.

---

## 👨‍💻 Author

Developed as part of a security-focused assignment to demonstrate:
- Python development
- Package ecosystem understanding
- Security analysis mindset
