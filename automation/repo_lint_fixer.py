import os
import subprocess

# =============================
# CONFIG
# =============================
REPOS_ROOT = os.path.dirname(os.path.abspath(__file__))

IGNORE_NAMES = {
    "AWS Cloud Scripts",
    "CloudSnippets",
    "cloud_portfolio_report.json",
    "cloud_portfolio_report"
}

PYTHON_EXTENSIONS = (".py",)

# =============================
# HELPERS
# =============================
def is_repo_dir(name):
    return os.path.isdir(os.path.join(REPOS_ROOT, name)) and name not in IGNORE_NAMES and not name.startswith(".")

def find_python_files(repo_path):
    py_files = []
    for root, _, files in os.walk(repo_path):
        for f in files:
            if f.endswith(PYTHON_EXTENSIONS):
                py_files.append(os.path.join(root, f))
    return py_files

def fix_lint(file_path):
    try:
        # autopep8 fixes style in-place
        subprocess.run(["autopep8", "--in-place", "--aggressive", "--aggressive", file_path], check=True)
        return True
    except Exception as e:
        print(f"[ERROR] Linting failed for {file_path}: {e}")
        return False

# =============================
# MAIN SCRIPT
# =============================
results = {}

for repo in os.listdir(REPOS_ROOT):
    if not is_repo_dir(repo):
        print(f"[SKIP] Ignoring {repo}")
        continue

    repo_path = os.path.join(REPOS_ROOT, repo)
    py_files = find_python_files(repo_path)
    fixed_files = []

    for f in py_files:
        if fix_lint(f):
            fixed_files.append(f)

    results[repo] = {
        "Python Files Fixed": len(fixed_files),
        "Files": fixed_files
    }

    # Terminal output
    print("=" * 60)
    print(f"Repo: {repo}")
    print(f"Python files fixed: {len(fixed_files)}")
    if fixed_files:
        for ff in fixed_files:
            print(f"  • {ff}")
    else:
        print("No Python files needed linting.")

print("\n✅ Linting scan complete.")
