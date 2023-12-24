import subprocess
from pathlib import Path
from sys import exit


def get_git_diff() -> list[str]:
    diff = subprocess.run(
        ["git", "diff", "--name-only", "--cached"], capture_output=True
    )
    diff_parsed = diff.stdout.decode("utf-8").split("\n")
    return diff_parsed


def get_versions() -> list[str]:
    versions = [str(p) for p in Path("versions").glob("*.png")]
    return versions


def check_consistency(diff: list[str], versions: list[str]) -> None:
    for version in versions:
        if version in diff:
            other_versions = [v for v in versions if v != version]
            for other_version in other_versions:
                if other_version not in diff:
                    print(
                        f"ERROR: {version} is in the diff, but {other_version} is not."
                    )
                    print("Please make sure that both versions are changed.")
                    print("If you are sure that this is correct, run")
                    print(f"    git add {other_version}")
                    print("and then commit again.")
                    exit(1)


def main() -> None:
    diff = get_git_diff()
    versions = get_versions()
    check_consistency(diff, versions)


if __name__ == "__main__":
    main()
