"""
Download large export files from Travis CAD with progress tracking.

This script streams the download in chunks to handle large files without
loading everything into memory at once.

Usage:
    python download_export.py

Requirements:
    pip install requests tqdm
"""

import requests
import zipfile
from pathlib import Path

# Optional: tqdm provides a nice progress bar
# If not installed, the script falls back to basic progress printing
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Note: Install 'tqdm' for a nicer progress bar: pip install tqdm")


def download_large_file(url: str, dest_path: Path, chunk_size: int = 8192) -> bool:
    """
    Download a large file with progress tracking using chunked streaming.

    Args:
        url: The URL to download from
        dest_path: Where to save the file
        chunk_size: Size of chunks to download at a time (default 8KB)

    Returns:
        True if successful, False otherwise

    Note:
        This streams the file in chunks rather than loading it all into memory,
        similar to how you might use chunked reading in R with readr::read_csv_chunked().
    """
    print(f"Downloading: {url}")
    print(f"Saving to: {dest_path}")

    try:
        # stream=True means we don't download the whole file at once
        # This is critical for large files - similar to lazy evaluation in R
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Get total file size from headers (if server provides it)
        total_size = int(response.headers.get('content-length', 0))

        if total_size:
            size_mb = total_size / (1024 * 1024)
            print(f"File size: {size_mb:.1f} MB")
        else:
            print("File size: Unknown (server didn't provide content-length)")

        # Download in chunks and write to file
        downloaded = 0

        with open(dest_path, 'wb') as f:
            # Use tqdm progress bar if available, otherwise basic progress
            if HAS_TQDM and total_size:
                # tqdm wraps the iterator and shows a progress bar
                chunks = tqdm(
                    response.iter_content(chunk_size=chunk_size),
                    total=total_size // chunk_size,
                    unit='KB',
                    unit_scale=True,
                    desc="Downloading"
                )
            else:
                chunks = response.iter_content(chunk_size=chunk_size)

            for chunk in chunks:
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Basic progress printing if no tqdm
                    if not HAS_TQDM and total_size:
                        pct = (downloaded / total_size) * 100
                        print(f"\rProgress: {pct:.1f}% ({downloaded / 1024 / 1024:.1f} MB)", end='')

        print(f"\nDownload complete: {dest_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"\nDownload failed: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path) -> list:
    """
    Extract a ZIP file and return list of extracted files.
    Renames files to use underscores instead of hyphens for consistency.

    Args:
        zip_path: Path to the ZIP file
        extract_to: Directory to extract into

    Returns:
        List of extracted file paths (with standardized names)
    """
    print(f"\nExtracting: {zip_path}")

    extracted_files = []

    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Show contents before extracting
        print(f"ZIP contains {len(zf.namelist())} file(s):")
        for name in zf.namelist():
            info = zf.getinfo(name)
            size_mb = info.file_size / (1024 * 1024)
            print(f"  - {name} ({size_mb:.1f} MB)")

        # Extract all files
        zf.extractall(extract_to)

        # Rename files: replace hyphens with underscores for consistency
        for name in zf.namelist():
            original_path = extract_to / name
            standardized_name = name.replace("-", "_")
            standardized_path = extract_to / standardized_name

            if original_path != standardized_path and original_path.exists():
                original_path.rename(standardized_path)
                print(f"  Renamed: {name} -> {standardized_name}")
                extracted_files.append(standardized_path)
            else:
                extracted_files.append(original_path)

    print(f"Extracted to: {extract_to}")
    return extracted_files


if __name__ == "__main__":
    # Project paths (consistent with other scripts)
    PROJECT_ROOT = Path(__file__).parent
    DATA_RAW = PROJECT_ROOT / "data" / "raw"

    # Create directory if it doesn't exist
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    # Available export URLs from Travis CAD
    EXPORTS = {
        "special_2025": {
            "url": "https://traviscad.org/wp-content/largefiles/2025%20Special%20export%20Supp%201%2007202025.zip",
            "description": "2025 Special Export (July 2025)"
        },
        "special_2025_supp": {
            "url": "https://traviscad.org/wp-content/largefiles/2025%20Special%20export%20Supp%208%2001072026.zip",
            "description": "2025 Supplemental Special Export (January 2026)"
        }
    }

    # Select which export to download
    print("="*60)
    print("Travis CAD Export Downloader")
    print("="*60)
    print("\nAvailable exports:")
    for key, info in EXPORTS.items():
        print(f"  {key}: {info['description']}")

    # Default to the main special export
    selected = "special_2025"

    print(f"\nDownloading: {EXPORTS[selected]['description']}")
    print("-"*60)

    # Download the ZIP file
    url = EXPORTS[selected]["url"]
    zip_filename = url.split("/")[-1].replace("%20", "_")
    zip_path = DATA_RAW / zip_filename

    if zip_path.exists():
        print(f"ZIP file already exists: {zip_path}")
        response = input("Re-download? (y/n): ").strip().lower()
        if response != 'y':
            print("Skipping download.")
        else:
            download_large_file(url, zip_path)
    else:
        success = download_large_file(url, zip_path)
        if not success:
            print("Download failed. Please check the URL and your internet connection.")
            exit(1)

    # Extract the ZIP file
    if zip_path.exists():
        extracted = extract_zip(zip_path, DATA_RAW)

        print("\n" + "="*60)
        print("DONE")
        print("="*60)
        print(f"Files ready in: {DATA_RAW}")
        print("\nNext step: Update json_filename in JSON_schema_extract.py to match")
        print("the extracted JSON file, then run:")
        print("  python JSON_schema_extract.py")
