import os
import re
import textwrap
import shutil

# Root folder containing all repos
REPO_ROOT = r"C:\Users\buche\docs\Desktop\REPOS"

# Max line length
MAX_LINE_LEN = 79

def backup_file(filepath):
    backup_path = filepath + ".bak"
    if not os.path.exists(backup_path):
        shutil.copyfile(filepath, backup_path)
        print(f"Backup created: {backup_path}")

def fix_line_length(line):
    if len(line) <= MAX_LINE_LEN:
        return [line]
    # Try simple wrap for comments, strings, or print statements
    if line.strip().startswith("#") or '"' in line or "'" in line:
        return textwrap.wrap(line, width=MAX_LINE_LEN)
    return [line]

def fix_file(filepath):
    backup_file(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    fixed_lines = []
    skip_next_empty = False

    for i, line in enumerate(lines):
        # Remove unused import: simple heuristic
        if re.match(r'^\s*import pytest', line):
            print(f"Removed unused import in {filepath}: {line.strip()}")
            continue

        # Fix simple indentation error: function/class with no indented block
        if re.match(r'^\s*(def |class )', line):
            if i+1 < len(lines) and lines[i+1].strip() == "":
                # Insert default pass if next line empty
                fixed_lines.append(line)
                fixed_lines.append("    pass\n")
                skip_next_empty = True
                continue

        if skip_next_empty and line.strip() == "":
            skip_next_empty = False
            continue

        # Fix line too long
        wrapped = fix_line_length(line.rstrip("\n"))
        fixed_lines.extend([w + "\n" for w in wrapped])

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)
    print(f"Fixed file: {filepath}")

def scan_and_fix():
    for repo in os.listdir(REPO_ROOT):
        repo_path = os.path.join(REPO_ROOT, repo)
        if not os.path.isdir(repo_path):
            continue
        print(f"\n=== Processing Repo: {repo} ===\n")
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    fix_file(file_path)

if __name__ == "__main__":
    scan_and_fix()
