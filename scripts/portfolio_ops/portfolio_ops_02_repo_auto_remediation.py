#!/usr/bin/env python3
"""
Repository Scanner and Auto-Fixer
Scans repositories for common issues and auto-fixes them
"""

# Import required libraries
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
        try:
            subprocess.run(
                ["python", "-m", "autopep8"] + AUTOPEP8_FLAGS + python_files,
                check=False
            )
            print(f"✅ Auto-fixed Python formatting in {len(python_files)} files")
        except Exception as e:
            print(f"⚠️  Could not run autopep8: {e}")
            print("   Install with: pip install autopep8")

def run_flake8(repo_path):
    """Run flake8 and return output."""
    try:
        result = subprocess.run(
            ["python", "-m", "flake8", repo_path],
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"⚠️  Could not run flake8: {e}")
        print("   Install with: pip install flake8")
        return ""

def check_structure(repo_path):
    """Check for required files and folders."""
    issues = []
    
    # Check required files
    for file in REQUIRED_FILES:
        file_path = Path(repo_path) / file
        if not file_path.exists():
            issues.append(f"Missing required file: {file}")
            # Create placeholder
            file_path.touch()
            print(f"   ✅ Created: {file}")
    
    # Check required folders
    for folder in REQUIRED_FOLDERS:
        folder_path = Path(repo_path) / folder
        if not folder_path.exists():
            issues.append(f"Missing required folder: {folder}")
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created: {folder}/")
    
    return issues

def check_readme(repo_path):
    """Check and fix README sections."""
    readme_path = Path(repo_path) / "README.md"
    missing_sections = []
    
    # Read existing content
    if not readme_path.exists():
        readme_path.touch()
        content = f"# {Path(repo_path).name}\n\n"
        print(f"   ✅ Created: README.md")
    else:
        with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    
    # Check for required sections
    for section in REQUIRED_README_SECTIONS:
        if section not in content:
            missing_sections.append(section)
            content += f"\n## {section}\n\nContent to be added.\n"
            print(f"   ✅ Added section: {section}")
    
    # Write updated content
    if missing_sections:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    return missing_sections

def scan_secrets(repo_path):
    """Scan for potential secrets or sensitive files."""
    secrets = []
    sensitive_patterns = [
        ".env",
        "conftest_safe.py",
        "credentials",
        "secrets",
        "api_key",
        "private_key",
        ".pem",
        ".key"
    ]
    
    for path in Path(repo_path).rglob("*"):
        if path.is_file():
            filename_lower = path.name.lower()
            for pattern in sensitive_patterns:
                if pattern in filename_lower:
                    secrets.append(str(path))
                    break
    
    return secrets

def calculate_hireability(lint_issues, structure_issues, readme_issues, secrets):
    """Calculate repository quality score."""
    score = 100
    
    # Deduct points for issues
    if lint_issues:
        lint_count = len(lint_issues.splitlines())
        score -= min(lint_count * 2, 30)  # Cap at -30 for lint issues
    
    score -= len(structure_issues) * 5
    score -= len(readme_issues) * 5
    score -= len(secrets) * 5
    
    return max(score, 0)

def process_repo(repo_path):
    """Process a single repository."""
    repo_name = Path(repo_path).name
    
    print("\n" + "=" * 70)
    print(f"📂 SCANNING REPO: {repo_name}")
    print("=" * 70 + "\n")
    
    # Skip hidden directories and common non-repo folders
    skip_dirs = {'.git', 'node_modules', 'venv', '__pycache__', '.vscode', '.idea'}
    if repo_name.startswith('.') or repo_name in skip_dirs:
        print(f"⏭️  Skipping: {repo_name}\n")
        return
    
    # 1. Auto-fix Python files with autopep8
    print("🔧 Auto-fixing Python formatting...")
    run_autopep8(repo_path)
    
    # 2. Run flake8 lint check
    print("\n🔍 Running lint checks...")
    lint_issues = run_flake8(repo_path)
    if lint_issues:
        print("⚠️  Lint issues found:")
        # Only show first 10 lines to avoid clutter
        lines = lint_issues.splitlines()
        for line in lines[:10]:
            print(f"   {line}")
        if len(lines) > 10:
            print(f"   ... and {len(lines) - 10} more issues")
    else:
        print("✅ No Python lint issues detected")
    
    # 3. Check and fix structure
    print("\n📁 Checking repository structure...")
    structure_issues = check_structure(repo_path)
    if not structure_issues:
        print("✅ Structure OK")
    
    # 4. Check and fix README
    print("\n📝 Checking README.md...")
    readme_issues = check_readme(repo_path)
    if not readme_issues:
        print("✅ README OK")
    
    # 5. Scan for secrets
    print("\n🔒 Scanning for sensitive files...")
    secrets = scan_secrets(repo_path)
    if secrets:
        print("⚠️  Potential sensitive files detected:")
        for s in secrets:
            relative_path = Path(s).relative_to(repo_path)
            print(f"   • {relative_path}")
    else:
        print("✅ No sensitive files detected")
    
    # 6. Calculate hireability score
    score = calculate_hireability(lint_issues, structure_issues, readme_issues, secrets)
    
    print("\n" + "-" * 70)
    print(f"📊 REPO QUALITY SCORE: {score}%")
    
    # Score interpretation
    if score >= 90:
        print("   🟢 EXCELLENT - Portfolio ready!")
    elif score >= 70:
        print("   🟡 GOOD - Minor improvements needed")
    elif score >= 50:
        print("   🟠 FAIR - Several issues to address")
    else:
        print("   🔴 NEEDS WORK - Major improvements required")
    
    print("-" * 70)

def main():
    """Main execution - scan all repos in current directory."""
    base_path = Path.cwd()
    
    print("\n" + "=" * 70)
    print("🚀 CLOUDOPSLAB REPOSITORY SCANNER")
    print("=" * 70)
    print(f"\nScanning repositories in: {base_path}\n")
    
    repos_found = 0
    repos_scanned = 0
    
    for item in base_path.iterdir():
        if item.is_dir():
            repos_found += 1
            # Check if it looks like a git repository
            if (item / '.git').exists() or repos_found <= 10:  # Limit scans
                process_repo(str(item))
                repos_scanned += 1
    
    print("\n" + "=" * 70)
    print(f"✅ SCAN COMPLETE")
    print(f"   Total directories: {repos_found}")
    print(f"   Repositories scanned: {repos_scanned}")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()