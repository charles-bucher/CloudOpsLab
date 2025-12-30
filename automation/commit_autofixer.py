import os
import subprocess

# ===== Config =====
REQUIRED_FILES = ["LICENSE"]
REQUIRED_FOLDERS = ["scripts", "docs", "tests"]
REQUIRED_README_SECTIONS = ["Overview", "Deployment", "Tech Stack",
"Architecture"]

# ===== Helper Functions =====
def check_structure(repo_path):
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(repo_path, f)):
            missing.append(f)
    for d in REQUIRED_FOLDERS:
        if not os.path.isdir(os.path.join(repo_path, d)):
            missing.append(d)
    return missing

def check_readme(repo_path):
    readme_path = os.path.join(repo_path, "README.md")
    missing_sections = []
    if not os.path.isfile(readme_path):
        return False, REQUIRED_README_SECTIONS
    with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        for section in REQUIRED_README_SECTIONS:
            if section not in content:
                missing_sections.append(section)
    return True, missing_sections

def scan_secrets(repo_path):
    potential_secrets = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".yml", ".yaml", ".sh", ".env",
".gitignore")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "SECRET" in content or "KEY" in content or "TOKEN" in
content:
                        potential_secrets.append(path)
    return potential_secrets

def run_flake8(repo_path):
    result = subprocess.run(
        ["python", "-m", "flake8", repo_path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def auto_fix(repo_path):
    subprocess.run([
        "python", "-m", "autopep8", repo_path, 
        "--in-place", "--recursive", "--max-line-length", "79"
    ])

def update_readme(repo_path, missing_sections):
    readme_path = os.path.join(repo_path, "README.md")
    if not os.path.isfile(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("# Project README\n\n")
    with open(readme_path, "a", encoding="utf-8") as f:
        for section in missing_sections:
            f.write(f"\n## {section}\n\nPlaceholder content.\n")

# ===== Main Processing =====
def process_repo(repo_path):
    print(f"\n=== Scanning Repo: {os.path.basename(repo_path)} ===\n")

    # Auto-fix Python lint first
    auto_fix(repo_path)

    # Run flake8
    lint_output = run_flake8(repo_path)
    if lint_output:
        print(lint_output)
    else:
        print("No Python lint issues detected.")

    # Check structure
    missing_structure = check_structure(repo_path)
    if missing_structure:
        print("\nStructure Issues:")
        for item in missing_structure:
            print(f"- Missing required item: {item}")
    else:
        print("\nStructure OK.")

    # Check README
    readme_present, missing_readme = check_readme(repo_path)
    if missing_readme:
        print("\nREADME Issues:")
        for section in missing_readme:
            print(f"- README missing section: {section}")
        update_readme(repo_path, missing_readme)
        print("Auto-fixed missing README sections.")
    else:
        print("\nREADME OK.")

    # Check secrets
    secrets = scan_secrets(repo_path)
    if secrets:
        print("\nSecurity Issues / Secrets:")
        for s in secrets:
            print(f"- Potential secret in file: {s}")
    else:
        print("\nNo secrets detected.")

    # Compute Hireability Score
    score = 100
    if missing_structure:
        score -= 20
    if missing_readme:
        score -= 10
    if lint_output:
        score -= 10
    if secrets:
        score -= 25
    print(f"\nRepo Hireability Score: {score}%")
    print("-" * 40)

# ===== Run on all repos =====
base_path = os.getcwd()
for repo in os.listdir(base_path):
    repo_path = os.path.join(base_path, repo)
    if os.path.isdir(repo_path):
        process_repo(repo_path)
