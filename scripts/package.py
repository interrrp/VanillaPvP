"""Rename every subdirectory in `versions` to "VanillaPvP <version>" and put them in zip files"""

from pathlib import Path
from shutil import rmtree
from zipfile import ZipFile

ROOT = Path(__file__).parent.parent
VERSIONS_DIR = ROOT / "versions"
PACKAGE_DIR = ROOT / "packages"


def main() -> None:
    if PACKAGE_DIR.exists():
        rmtree(PACKAGE_DIR)
        print("Removed old packages")
    PACKAGE_DIR.mkdir()

    for version_dir in VERSIONS_DIR.glob("*"):
        if not version_dir.is_dir():
            continue

        version = version_dir.name

        zip_name = f"VanillaPvP {version}.zip"
        zip_path = PACKAGE_DIR / zip_name
        with ZipFile(zip_path, "w") as zip_file:
            copytree_to_zip(version_dir, zip_file)

        print(f"{version} -> {zip_path}")

    print("Done!")


def copytree_to_zip(source: Path, destination_zip: ZipFile):
    with destination_zip as zipf:
        for file_path in source.glob("**/*"):
            if file_path.is_file():
                archive_path = file_path.relative_to(source)
                zipf.write(file_path, arcname=archive_path)


if __name__ == "__main__":
    main()
