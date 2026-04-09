import requests
import os
import tarfile
import zipfile
import tempfile
from pathlib import Path

class PyPIScraper:
    PYPI_URL = "https://pypi.org/pypi/{}/json"

    def __init__(self, package_name):
        self.package_name = package_name
        self.package_info = None
        self.download_url = None
        self.version = None
        self.temp_dir = tempfile.mkdtemp()

    def fetch_package_info(self):
        try:
            response = requests.get(self.PYPI_URL.format(self.package_name), timeout=10)
            response.raise_for_status()
            self.package_info = response.json()
            self.version = self.package_info["info"]["version"]
            print(f"[+] Latest version: {self.version}")
        except Exception as e:
            raise Exception(f"Failed to fetch package info: {e}")

    def get_download_url(self):
        try:
            urls = self.package_info["urls"]
            # Prefer wheel over source
            for file in urls:
                if file["filename"].endswith(".whl"):
                    self.download_url = file["url"]
                    return
            # fallback to tar.gz
            for file in urls:
                if file["filename"].endswith(".tar.gz"):
                    self.download_url = file["url"]
                    return
            raise Exception("No valid package format found")
        except Exception as e:
            raise Exception(f"Error getting download URL: {e}")

    def download_package(self):
        try:
            filename = os.path.join(self.temp_dir, self.download_url.split('/')[-1])
            with requests.get(self.download_url, stream=True, timeout=20) as r:
                r.raise_for_status()
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"[+] Downloaded: {filename}")
            return filename
        except Exception as e:
            raise Exception(f"Download failed: {e}")

    def extract_package(self, file_path):
        extract_path = os.path.join(self.temp_dir, "extracted")
        os.makedirs(extract_path, exist_ok=True)

        try:
            if file_path.endswith(".tar.gz"):
                with tarfile.open(file_path, "r:gz") as tar:
                    tar.extractall(extract_path)
            elif file_path.endswith(".whl") or file_path.endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
            else:
                raise Exception("Unsupported file format")

            print(f"[+] Extracted to: {extract_path}")
            return extract_path
        except Exception as e:
            raise Exception(f"Extraction failed: {e}")

    def parse_dependencies(self, extract_path):
        dependencies = set()

        # Check metadata (preferred)
        try:
            for root, _, files in os.walk(extract_path):
                for file in files:
                    if file.endswith("METADATA") or file.endswith("PKG-INFO"):
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if line.startswith("Requires-Dist:"):
                                    dep = line.split(":", 1)[1].strip()
                                    dependencies.add(dep)
        except Exception:
            pass

        # Fallback: requirements.txt
        try:
            for root, _, files in os.walk(extract_path):
                if "requirements.txt" in files:
                    with open(os.path.join(root, "requirements.txt"), 'r') as f:
                        for line in f:
                            dependencies.add(line.strip())
        except Exception:
            pass

        return list(dependencies)

    def run(self):
        self.fetch_package_info()
        self.get_download_url()
        file_path = self.download_package()
        extract_path = self.extract_package(file_path)
        deps = self.parse_dependencies(extract_path)

        return {
            "package": self.package_name,
            "version": self.version,
            "dependencies": deps
        }


if __name__ == "__main__":
    package = input("Enter package name: ")
    scraper = PyPIScraper(package)

    try:
        result = scraper.run()
        print("\n=== RESULT ===")
        print(f"Package: {result['package']}")
        print(f"Version: {result['version']}")
        print("Dependencies:")
        for dep in result["dependencies"]:
            print(f" - {dep}")
    except Exception as e:
        print(f"[ERROR] {e}")
