#!python3
from pathlib import Path
import re
import sys
from typing import Any


def extract_changelog_content(changelog: Any, version):

    if Path(changelog).exists():
        changelog_text: str = Path(changelog).read_text()
    elif isinstance(changelog, bytes):
        changelog_text = changelog.decode("utf-8")
    elif isinstance(changelog, str):
        changelog_text = changelog
    else:
        raise TypeError("Invalid type for changelog")

    # Extract the header for the changelog
    header = re.search(r"([#\s]{2}Changelog)([\s\S]*?(?=[#]{2}))", changelog_text, re.MULTILINE)

    # Extract the relevant version marked changes
    version_extract_pattern = r"(^[#]{2}.*\[" + re.escape(version) + r"\][\s\S]*?(?=^[#]{2}\s))"
    version_extract = re.search(version_extract_pattern, changelog_text, re.MULTILINE)
    if header and version_extract:
        return f"{header.group().strip()}\n\n{version_extract.group().strip()}".strip()
    else:
        return None


# Read the changelog file
with open("CHANGELOG.md", "r") as file:
    changelog_text = file.read()

if __name__ == "__main__":
    # Extract content for the specified version
    changelog_text = sys.argv[1]
    input_version = sys.argv[2]
    output_content = extract_changelog_content(changelog_text, input_version)

    if output_content:
        print(output_content)
    else:
        print(f"Changelog for version {input_version} not found.")
        exit(1)
