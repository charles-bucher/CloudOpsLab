#!/usr/bin/env python3
"""
Repository String Fixer
Fixes unterminated strings and smart quotes across repositories
"""

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
    ],
    "CloudOpsLab": [
        "monitoring/health_check.py",
        "automation/EC2_Start_Stop_Scheduler.py",
        "troubleshooting/repo_scanner.py"
    ]
}

root_path = Path("C:/Users/buche/docs/Desktop/REPOS")  # Adjust if needed

def fix_strings_in_file(file_path: Path):
    """Fix unterminated strings and smart quotes in a Python file."""
    
    # Create backup
    backup_path = file_path.with_suffix(file_path.suffix + ".bak")
    try:
        shutil.copy(file_path, backup_path)
        print(f"   📋 Backup created: {backup_path.name}")
    except Exception as e:
        print(f"   ❌ Could not create backup: {e}")
        return False
    
    # Read file
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"   ❌ Could not read file: {e}")
        return False
    
    original_content = content
    changes_made = False
    
    # Fix smart quotes (curly quotes to straight quotes)
    replacements = [
        ('"', '"'),  # Left double quote
        ('"', '"'),  # Right double quote
        (''', "'"),  # Left single quote
        (''', "'"),  # Right single quote
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            changes_made = True
            print(f"   ✅ Replaced smart quotes: {old} → {new}")
    
    # Fix common unterminated string patterns
    lines = content.split('\n')
    fixed_lines = []
    line_changes = 0
    
    for i, line in enumerate(lines, 1):
        original_line = line
        
        # Check for lines ending with an odd number of quotes
        # (This is a simplified check - full parsing would be better)
        stripped = line.rstrip()
        
        # Count unescaped quotes
        single_quotes = len(re.findall(r"(?<!\\)'", stripped))
        double_quotes = len(re.findall(r'(?<!\\)"', stripped))
        
        # If odd number of quotes and line ends without closing quote
        if (single_quotes % 2 == 1 or double_quotes % 2 == 1):
            # Check if it's likely a string issue (not a comment or other syntax)
            if not stripped.startswith('#') and '=' in stripped:
                # Try to fix by adding closing quote
                if single_quotes % 2 == 1:
                    line = stripped + "'"
                elif double_quotes % 2 == 1:
                    line = stripped + '"'
                
                if line != original_line:
                    print(f"   ✅ Fixed line {i}: Unterminated string")
                    line_changes += 1
                    changes_made = True
        
        fixed_lines.append(line)
    
    # Write back if changes were made
    if changes_made:
        try:
            content = '\n'.join(fixed_lines)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"   ✅ Fixed {line_changes} line(s) in {file_path.name}")
            return True
        except Exception as e:
            print(f"   ❌ Could not write file: {e}")
            # Restore from backup
            shutil.copy(backup_path, file_path)
            return False
    else:
        print(f"   ℹ️  No changes needed in {file_path.name}")
        # Remove backup if no changes
        backup_path.unlink()
        return False

def process_repo(repo_name):
    """Process all files in a repository."""
    repo_path = root_path / repo_name
    
    if not repo_path.exists():
        print(f"   ❌ Repo not found: {repo_name}")
        return
    
    files_processed = 0
    files_fixed = 0
    
    for file_rel in repos_to_fix[repo_name]:
        if file_rel == "incidents":
            # Process all Python files recursively in incidents folder
            incidents_path = repo_path / "incidents"
            if incidents_path.exists():
                print(f"\n   📂 Processing incidents directory...")
                for py_file in incidents_path.rglob("*.py"):
                    if fix_strings_in_file(py_file):
                        files_fixed += 1
                    files_processed += 1
            else:
                print(f"   ⚠️  Incidents folder not found")
        else:
            file_path = repo_path / file_rel
            if file_path.exists():
                if fix_strings_in_file(file_path):
                    files_fixed += 1
                files_processed += 1
            else:
                print(f"   ⚠️  File not found: {file_rel}")
    
    print(f"\n   📊 Summary: {files_fixed}/{files_processed} files fixed")

def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("🔧 REPOSITORY STRING FIXER")
    print("=" * 70)
    print(f"\nRoot path: {root_path}\n")
    
    total_repos = len(repos_to_fix)
    repos_processed = 0
    
    for repo in repos_to_fix:
        print("=" * 70)
        print(f"📦 PROCESSING REPO: {repo}")
        print("=" * 70)
        
        process_repo(repo)
        repos_processed += 1
        
        print(f"\n✅ Finished processing {repo} ({repos_processed}/{total_repos})\n")
    
    print("=" * 70)
    print("✅ ALL REPOSITORIES PROCESSED")
    print("=" * 70)
    print("\n💡 Tips:")
    print("   • Backup files (.bak) were created")
    print("   • Test your scripts after fixing")
    print("   • Delete .bak files once verified")
    print("\n" + "=" * 70 + "\n")

if __name__ == "__main__":
    main()