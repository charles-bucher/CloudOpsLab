import os
import subprocess
from pathlib import Path

# Required files/folders and README sections
REQUIRED_FILES = ["LICENSE"]
REQUIRED_FOLDERS = ["scripts", "docs", "tests"]
REQUIRED_README_SECTIONS = ["Overview", "Deployment", "Tech Stack", "Architecture"]

# Autopep8 options
AUTOPEP8_FLAGS = ["--in-place", "--aggressive", "--aggressive", "--recursive"]

def run_autopep8(repo_path):
    """Run autopep8 on a repo to auto-fix lint issues."""
    python_files = [str(p) for p in Path(repo_path).rglob("*.py")]
    if python_files:
        subprocess.run(["python", "-m", "autopep8"] + AUTOPEP8_FLAGS + python_files)

def run_flake8(repo_path):
    """Run flake8 and return output."""
    result = subprocess.run(
        ["python", "-m", "flake8", repo_path], capture_output=True, text=True
    )
    return result.stdout.strip()

def check_structure(repo_path):
    issues = []
    for file in REQUIRED_FILES:
        if not (Path(repo_path) / file).exists():
            issues.append(f"Missing required file: {file}")
            (Path(repo_path) / file).touch()
    for folder in REQUIRED_FOLDERS:
        folder_path = Path(repo_path) / folder
        if not folder_path.exists():
            issues.append(f"Missing required folder: {folder}")
            folder_path.mkdir(parents=True, exist_ok=True)
    return issues

def check_readme(repo_path):
    readme_path = Path(repo_path) / "README.md"
    missing_sections = []
    if not readme_path.exists():
        readme_path.touch()
        content = ""
    else:
        with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    for section in REQUIRED_README_SECTIONS:
        if section not in content:
            missing_sections.append(section)
            content += f"\n## {section}\n\nTBD\n"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    return missing_sections

def scan_secrets(repo_path):
    # Placeholder: detect potential secrets by file names
    secrets = []
    for path in Path(repo_path).rglob("*"):
        if path.name.lower() in ["conftest_safe.py", ".gitignore", ".env"]:
            secrets.append(str(path))
    return secrets

def calculate_hireability(lint_issues, structure_issues, readme_issues, secrets):
    """Simple scoring: start at 100%, minus issues."""
    score = 100
    score -= 10 * len(lint_issues.splitlines()) if lint_issues else 0
    score -= 5 * len(structure_issues)
    score -= 5 * len(readme_issues)
    score -= 5 * len(secrets)
    return max(score, 0)

def process_repo(repo_path):
    print(f"\n=== Scanning Repo: {Path(repo_path).name} ===\n")

    # Auto-fix Python files
    run_autopep8(repo_path)

    # Run flake8 lint check
    lint_issues = run_flake8(repo_path)
    if lint_issues:
        print(lint_issues)
    else:
        print("No Python lint issues detected.")

    # Check and fix structure
    structure_issues = check_structure(repo_path)
    if structure_issues:
        print("Auto-fixed missing structure items.")
    else:
        print("Structure OK.")

    # Check and fix README
    readme_issues = check_readme(repo_path)
    if readme_issues:
        print("Auto-fixed missing README sections.")
    else:
        print("README OK.")

    # Scan for secrets
    secrets = scan_secrets(repo_path)
    if secrets:
        print("\nSecurity Issues / Secrets:")
        for s in secrets:
            print(f"- Potential secret in file: {s}")
    else:
        print("\nNo secrets detected.")

    # Calculate hireability
    score = calculate_hireability(lint_issues, structure_issues, readme_issues, secrets)
    print(f"\nRepo Hireability Score: {score}%")
    print("-" * 40)

def main():
    base_path = Path.cwd()
    for repo in base_path.iterdir():
        if repo.is_dir():
            process_repo(str(repo))

if __name__ == "__main__":
    main()
