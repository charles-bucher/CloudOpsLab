"""
Ultimate Repo Validator
Purpose: [AWS automation script]
Author: Charles Bucher
"""

# Import required libraries
import os
import re
import pathlib
from pathlib import Path


# -------------------------------
# Configuration
# -------------------------------
REQUIRED_README_SECTIONS = [
    "TL;DR", "Quick Start", "Incident Scenarios", 
    "Installation", "Skills", "License", "Contact"
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bPLACEHOLDER\b",
    r"\bFIXME\b"
]

CODE_EXTENSIONS = [".py", ".tf", ".ps1", ".sh", ".js"]  # extend as needed
README_FILENAME = "README.md"

# -------------------------------
# Helper functions
# -------------------------------

def safe_read_text(file_path: Path) -> str:
    try:
        return file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"[WARN] Failed to read {file_path}: {e}")
        return ""
def check_placeholders(file_path: Path):
    """
        Function to check_placeholders.
    """

    content = safe_read_text(file_path)
    issues = []
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, content):
            issues.append(f"{file_path} contains placeholder: {pattern}")
    return issues
def check_readme(readme_path: Path):
    """
        Function to check_readme.
    """

    content = safe_read_text(readme_path)
    missing_sections = []
    for section in REQUIRED_README_SECTIONS:
        if section not in content:
            missing_sections.append(section)
    return missing_sections
def check_code_quality(file_path: Path):
    """
        Function to check_code_quality.
    """

    # Very basic checks; can integrate pylint/flake8 later
    content = safe_read_text(file_path)
    issues = []
    if len(content.strip()) == 0:
        issues.append(f"{file_path} is empty")
    if "\t" in content:
        issues.append(f"{file_path} contains tabs instead of spaces")
    return issues
def validate_repo(repo_path: Path):
    """
        Function to validate_repo.
    """

    report = {
        "missing_readme_sections": [],
        "placeholders": [],
        "code_issues": [],
        "missing_files": []
    }

    # Check README
    readme_path = repo_path / README_FILENAME
    if readme_path.exists():
        report["missing_readme_sections"] = check_readme(readme_path)
    else:
        report["missing_files"].append(str(readme_path))
    
    # Walk repo
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = Path(root) / file
            # Skip hidden files
            if file_path.name.startswith("."):
                continue
            # Check placeholders
            report["placeholders"].extend(check_placeholders(file_path))
            # Check code quality
            if file_path.suffix in CODE_EXTENSIONS:
                report["code_issues"].extend(check_code_quality(file_path))
    
    return report

# -------------------------------
# Main
# -------------------------------def main(root_folder: str):
    """
        Function to main.
    """

    root_path = Path(root_folder)
    if not root_path.exists():
        print(f"[ERROR] Folder not found: {root_folder}")
        return
    
    for repo_name in os.listdir(root_path):
        repo_path = root_path / repo_name
        if repo_path.is_dir():
            print(f"\nValidating repo: {repo_name}")
            report = validate_repo(repo_path)
            # Print summary
            for k, v in report.items():
                if v:
                    print(f"[ISSUES] {k}:")
                    for issue in v:
                        print(f"   • {issue}")
            if not any(report.values()):
                print("[OK] No issues found!")

if __name__ == "__main__":
    main("C:/Users/buche/docs/Desktop/REPOS")