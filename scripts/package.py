"""Rename every subdirectory in `versions` to `VanillaPvP <version>` and place them in ZIP files."""

import subprocess
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

    vanillapvp_version = get_vanillapvp_version()

    for version_dir in VERSIONS_DIR.iterdir():
        if not version_dir.is_dir():
            continue

        mc_version = version_dir.name

        zip_name = f"VanillaPvP_{vanillapvp_version}_for_{mc_version}.zip"
        zip_path = PACKAGE_DIR / zip_name
        with ZipFile(zip_path, "w") as zip_file:
            copy_to_zip(version_dir, zip_file)

        print(f"{mc_version} -> {zip_path}")

    print("Done!")


def copy_to_zip(source: Path, destination_zip: ZipFile):
    with destination_zip as zipf:
        for file_path in source.glob("**/*"):
            if file_path.is_file():
                archive_path = file_path.relative_to(source)
                zipf.write(file_path, arcname=archive_path)


def get_vanillapvp_version() -> str:
    output = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"], capture_output=True
    )
    version = output.stdout.decode("utf-8").strip()
    return version


if __name__ == "__main__":
    main()
