"""
Portfolio Deep Auditor
Purpose: [AWS automation script]
Author: Charles Bucher
"""

# Import required libraries
import os
import re
from pathlib import Path


# ================= CONFIG =================
ROOT_FOLDERS = [
    r"C:\Users\buche\docs\Desktop\REPOS",
    # add another root here if needed
]

AUTO_FIX = True
README_SECTIONS = [
    "Overview",
    "Architecture",
    "Features",
    "Setup",
    "Usage",
    "Skills Demonstrated",
    "License"
]

CLOUD_KEYWORDS = [
    "aws", "ec2", "s3", "iam", "lambda", "cloudwatch",
    "terraform", "cloudformation", "boto3", "devops"
]
# ==========================================

def safe_read(path):
    """
        Function to safe_read.
    """

    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def score_readme(readme_text):
    """
        Function to score_readme.
    """

    score = 0
    missing = []

    for section in README_SECTIONS:
        if re.search(rf"#+\s*{section}", readme_text, re.IGNORECASE):
            score += 100 / len(README_SECTIONS)
        else:
            missing.append(section)

    return round(score, 1), missing

def score_cloud_relevance(text):
    """
        Function to score_cloud_relevance.
    """

    hits = sum(1 for kw in CLOUD_KEYWORDS if kw in text.lower())
    return min(100, hits * 12)

def documentation_score(repo_path):
    """
        Function to documentation_score.
    """

    py_files = list(repo_path.rglob("*.py"))
    if not py_files:
        return 0

    documented = 0
    for f in py_files:
        content = safe_read(f)
        if '"""' in content or "def " in content and "#" in content:
            documented += 1

    return round((documented / len(py_files)) * 100, 1)

def autofix_readme(readme_path, missing_sections):
    """
        Function to autofix_readme.
    """

    if not AUTO_FIX:
        return

    content = safe_read(readme_path)
    with readme_path.open("a", encoding="utf-8") as f:
        for section in missing_sections:
            f.write(f"\n\n## {section}\n_TODO: Describe this section._\n")

def ensure_license(repo_path):
    """
        Function to ensure_license.
    """

    license_path = repo_path / "LICENSE"
    if license_path.exists():
        return

    if AUTO_FIX:
        license_path.write_text("MIT License\n\nCopyright (c)")

def analyze_repo(repo_path):
    """
        Function to analyze_repo.
    """

    print("=" * 60)
    print(f"Repo: {repo_path.name}")

    readme = repo_path / "README.md"
    readme_text = safe_read(readme)

    readme_score, missing_sections = score_readme(readme_text)
    cloud_score = score_cloud_relevance(readme_text)
    doc_score = documentation_score(repo_path)

    total = round((readme_score + cloud_score + doc_score) / 3, 1)

    print(f"README Score: {readme_score}%")
    print(f"Cloud Relevance: {cloud_score}%")
    print(f"Documentation Score: {doc_score}%")
    print(f"TOTAL SCORE: {total}%")

    if missing_sections:
        print("Suggestions:")
        for sec in missing_sections:
            print(f"  • Add README section: {sec}")
        autofix_readme(readme, missing_sections)

    if cloud_score < 50:
        print("  • Increase AWS/service-specific examples")

    if doc_score < 50:
        print("  • Add docstrings and inline comments")

    ensure_license(repo_path)

def main():
    """
        Function to main.
    """

    for root in ROOT_FOLDERS:
        root_path = Path(root)
        if not root_path.exists():
            continue

        for item in root_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                analyze_repo(item)


if __name__ == "__main__":
    main()