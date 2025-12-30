#!/usr/bin/env python3
"""
Repository Auto-Linter
Automatically fixes Python code style issues across all repositories
"""

import os
import subprocess
import sys
from pathlib import Path

# =============================
# CONFIG
# =============================
REPOS_ROOT = os.path.dirname(os.path.abspath(__file__))

IGNORE_NAMES = {
    "AWS Cloud Scripts",
    "CloudSnippets",
    "cloud_portfolio_report.json",
    "cloud_portfolio_report",
    "__pycache__",
    ".git",
    "venv",
    "node_modules",
    ".venv",
    "env"
}

PYTHON_EXTENSIONS = (".py",)

# Autopep8 configuration
AUTOPEP8_OPTIONS = [
    "--in-place",           # Modify files in place
    "--aggressive",         # More aggressive fixes
    "--aggressive",         # Even more aggressive
    "--max-line-length=100" # PEP 8 recommends 79, but 100 is more practical
]

# =============================
# HELPERS
# =============================

def check_autopep8_installed():
    """Check if autopep8 is installed."""
    try:
        result = subprocess.run(
            ["autopep8", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def is_repo_dir(name):
    """Check if a directory should be scanned as a repository."""
    full_path = os.path.join(REPOS_ROOT, name)
    return (
        os.path.isdir(full_path) and
        name not in IGNORE_NAMES and
        not name.startswith(".")
    )

def find_python_files(repo_path):
    """Recursively find all Python files in a repository."""
    py_files = []
    
    try:
        for root, dirs, files in os.walk(repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_NAMES and not d.startswith('.')]
            
            for f in files:
                if f.endswith(PYTHON_EXTENSIONS):
                    py_files.append(os.path.join(root, f))
    except Exception as e:
        print(f"[ERROR] Failed to scan {repo_path}: {e}")
    
    return py_files

def fix_lint(file_path):
    """Fix linting issues in a Python file using autopep8."""
    try:
        # Run autopep8
        result = subprocess.run(
            ["autopep8"] + AUTOPEP8_OPTIONS + [file_path],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return True, None
        else:
            return False, result.stderr
            
    except FileNotFoundError:
        return False, "autopep8 not found"
    except Exception as e:
        return False, str(e)

def get_file_size(file_path):
    """Get file size in KB."""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / 1024
    except:
        return 0

# =============================
# MAIN SCRIPT
# =============================

def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("🔧 CLOUDOPSLAB AUTO-LINTER")
    print("=" * 70)
    print(f"\nScanning repositories in: {REPOS_ROOT}\n")
    
    # Check if autopep8 is installed
    if not check_autopep8_installed():
        print("❌ ERROR: autopep8 is not installed")
        print("\n📦 Install with:")
        print("   pip install autopep8")
        sys.exit(1)
    
    print("✅ autopep8 is installed\n")
    
    # Find all repositories
    repos = [r for r in os.listdir(REPOS_ROOT) if is_repo_dir(r)]
    
    if not repos:
        print("⚠️  No repositories found to scan")
        return
    
    print(f"📂 Found {len(repos)} repositories to scan\n")
    
    # Results tracking
    results = {}
    total_files_fixed = 0
    total_files_scanned = 0
    total_errors = 0
    
    # Process each repository
    for repo in sorted(repos):
        repo_path = os.path.join(REPOS_ROOT, repo)
        
        print("=" * 70)
        print(f"📦 REPO: {repo}")
        print("=" * 70)
        
        # Find Python files
        py_files = find_python_files(repo_path)
        total_files_scanned += len(py_files)
        
        if not py_files:
            print("   ℹ️  No Python files found")
            results[repo] = {
                "files_scanned": 0,
                "files_fixed": 0,
                "errors": 0,
                "details": []
            }
            continue
        
        print(f"   🔍 Found {len(py_files)} Python file(s)")
        
        # Fix each file
        fixed_files = []
        error_files = []
        
        for f in py_files:
            relative_path = os.path.relpath(f, repo_path)
            file_size = get_file_size(f)
            
            success, error = fix_lint(f)
            
            if success:
                fixed_files.append({
                    "path": relative_path,
                    "size": file_size
                })
                print(f"   ✅ {relative_path} ({file_size:.1f} KB)")
            else:
                error_files.append({
                    "path": relative_path,
                    "error": error
                })
                print(f"   ❌ {relative_path} - Error: {error}")
        
        # Store results
        total_files_fixed += len(fixed_files)
        total_errors += len(error_files)
        
        results[repo] = {
            "files_scanned": len(py_files),
            "files_fixed": len(fixed_files),
            "errors": len(error_files),
            "details": fixed_files + error_files
        }
        
        # Summary for this repo
        print(f"\n   📊 Summary:")
        print(f"      • Files scanned: {len(py_files)}")
        print(f"      • Files fixed: {len(fixed_files)}")
        if error_files:
            print(f"      • Errors: {len(error_files)}")
        print()
    
    # Final summary
    print("=" * 70)
    print("✅ LINTING COMPLETE")
    print("=" * 70)
    print(f"\n📊 Overall Statistics:")
    print(f"   • Repositories scanned: {len(repos)}")
    print(f"   • Total Python files: {total_files_scanned}")
    print(f"   • Files successfully fixed: {total_files_fixed}")
    
    if total_errors > 0:
        print(f"   • Errors encountered: {total_errors}")
    
    # Success rate
    if total_files_scanned > 0:
        success_rate = (total_files_fixed / total_files_scanned) * 100
        print(f"   • Success rate: {success_rate:.1f}%")
    
    print("\n" + "=" * 70 + "\n")
    
    # Return exit code based on results
    if total_errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()