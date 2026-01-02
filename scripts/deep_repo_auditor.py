"""
Deep Repo Auditor
Purpose: [AWS automation script]
Author: Charles Bucher
"""

# Import required libraries
import os
import re
from pathlib import Path


ROOT = Path.cwd()

REQUIRED_README_SECTIONS = [
    "TL;DR",
    "Overview",
    "Setup Instructions",
    "Usage Examples",
    "Incident Scenarios",
    "Screenshots",
    "Contact"
]

CLOUD_KEYWORDS = [
    "aws", "ec2", "s3", "lambda", "iam", "cloudwatch",
    "terraform", "vpc", "rds", "cloud"
]

CODE_EXTENSIONS = (".py", ".sh", ".ps1")

def read_file_safe(path):
    """
        Function to read_file_safe.
    """

    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def scan_readme(repo):
    """
        Function to scan_readme.
    """

    readme = repo / "README.md"
    if not readme.exists():
        return 0, ["Missing README.md"], []

    content = read_file_safe(readme)
    missing = []
    fixes = []

    for section in REQUIRED_README_SECTIONS:
        if section.lower() not in content.lower():
            missing.append(section)
            fixes.append(f"## {section}\n\n_TODO_\n")

    if fixes:
        readme.write_text(content + "\n\n" + "\n".join(fixes),
encoding="utf-8")

    score = max(0, 100 - (len(missing) * 10))
    return score, missing, ["Added missing README sections"] if fixes else []

def scan_cloud_relevance(repo):
    """
        Function to scan_cloud_relevance.
    """

    text = ""
    for file in repo.rglob("*"):
        if file.is_file():
            text += read_file_safe(file).lower()

    hits = sum(1 for k in CLOUD_KEYWORDS if k in text)
    score = min(100, int((hits / len(CLOUD_KEYWORDS)) * 100))
    suggestions = []
    if score < 70:
        suggestions.append("Add more AWS/cloud terminology and examples.")
    return score, suggestions

def scan_docs(repo):
    """
        Function to scan_docs.
    """

    files = [f for f in repo.rglob("*") if f.suffix in CODE_EXTENSIONS]
    if not files:
        return 0, ["No code files found"]

    commented = 0
    fixes = []

    for file in files:
        content = read_file_safe(file)
        if '"""' in content or "#" in content:
            commented += 1
        else:
            header = f'"""\n{file.name} - Entry-level cloud script\n"""\n\n'
            file.write_text(header + content, encoding="utf-8")
            fixes.append(f"Added docstring to {file.name}")

    score = int((commented / len(files)) * 100)
    suggestions = []
    if score < 70:
        suggestions.append("Increase docstrings and inline comments.")
    return score, suggestions + fixes

def scan_structure(repo):
    """
        Function to scan_structure.
    """

    expected = ["README.md", "src", "tests"]
    score = 100
    missing = []

    for e in expected:
        if not (repo / e).exists():
            missing.append(e)
            score -= 10

    suggestions = []
    if missing:
        suggestions.append(f"Consider adding: {', '.join(missing)}")

    return max(score, 0), suggestions

def audit_repo(repo):
    """
        Function to audit_repo.
    """

    print(f"\n🔍 Repo: {repo.name}")

    readme_score, readme_missing, readme_fixes = scan_readme(repo)
    cloud_score, cloud_suggestions = scan_cloud_relevance(repo)
    docs_score, docs_suggestions = scan_docs(repo)
    structure_score, structure_suggestions = scan_structure(repo)

    total = (
        cloud_score * 0.30 +
        readme_score * 0.25 +
        docs_score * 0.25 +
        structure_score * 0.10 +
        (100 if readme_score > 70 else 50) * 0.10
    )

    print(f"  Cloud Relevance: {cloud_score}%")
    print(f"  README Quality: {readme_score}%")
    print(f"  Documentation: {docs_score}%")
    print(f"  Structure: {structure_score}%")
    print(f"  TOTAL SCORE: {round(total,1)}%")

    suggestions = (
        readme_missing +
        cloud_suggestions +
        docs_suggestions +
        structure_suggestions
    )

    if suggestions:
        print("  Suggestions:")
        for s in suggestions:
            print(f"   • {s}")
    else:
        print("  ✅ Repo is entry-level ready")

def main():
    """
        Function to main.
    """

    print("=" * 60)
    print("ENTRY-LEVEL CLOUD PORTFOLIO DEEP AUDITOR")
    print("=" * 60)

    for repo in ROOT.iterdir():
        if repo.is_dir() and not repo.name.startswith("."):
            audit_repo(repo)

    print("\n✅ Deep scan completed. Small fixes applied safely.")


if __name__ == "__main__":
    main()