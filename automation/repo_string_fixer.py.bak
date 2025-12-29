import os
import re
from pathlib import Path
import shutil

# List of repos and their files with unterminated string issues
repos_to_fix = {
    "AWS_Cloudops_Suite": [
        "conftest_safe.py",
        "index.py",
        "lambdas/index.py",
        "lambdas/my_function/main.py",
        "lambdas/my_function/test_main.py",
        "my_function/index.py",
        "scripts/alerts.py",
        "scripts/guardduty-enable.py",
        "scripts/health_check.py",
        "scripts/remediation.py",
        "tests/test_main.py"
    ],
    "AWS_Cloud_Support_Sim": [
        "conftest_safe.py",
        "main.py",
        "scripts/ultimate_validator.py",
        "scripts/utils.py",
        "src/__init__.py",
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/test_main.py"
    ],
    "AWS_Error_Driven_Troubleshooting_Lab": [
        "conftest_safe.py",
        "lambdas/index.py",
        "src/__init__.py",
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/test_main.py",
        # wildcard for all incident scripts
        "incidents"
    ]
}

root_path = Path("C:/Users/buche/docs/Desktop/REPOS")  # adjust if needed

def fix_strings_in_file(file_path: Path):
    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    shutil.copy(file_path, backup_path)
    print(f"Backup created: {backup_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed_lines = []
    changes_made = False

    for line in lines:
        original_line = line

        # Replace smart quotes
        line = line.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")

        # Fix unterminated strings (naive but works for simple cases)
        if re.search(r'["\']([^"\']*)$', line.strip()):
            line = line.rstrip("\n") + '"' + "\n"
            changes_made = True

        fixed_lines.append(line)

    if changes_made:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(fixed_lines)
        print(f"Fixed unterminated strings in {file_path}")
    else:
        print(f"No changes needed in {file_path}")

def process_repo(repo_name):
    repo_path = root_path / repo_name
    if not repo_path.exists():
        print(f"Repo not found: {repo_name}")
        return

    for file_rel in repos_to_fix[repo_name]:
        file_path = repo_path / file_rel
        if file_rel == "incidents":
            # process all Python files recursively in incidents folder
            incidents_path = repo_path / "incidents"
            for py_file in incidents_path.rglob("*.py"):
                fix_strings_in_file(py_file)
        elif file_path.exists():
            fix_strings_in_file(file_path)
        else:
            print(f"File not found: {file_path}")

def main():
    for repo in repos_to_fix:
        print(f"=== Processing Repo: {repo} ===")
        process_repo(repo)
        print(f"Finished processing {repo}\n")

if __name__ == "__main__":
    main()
