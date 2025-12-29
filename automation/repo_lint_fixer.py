import os
import re

# --- Fix functions ---
def fix_indentation(file_path):
    """Fix indentation errors in Python files."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Simple heuristic: indent function body if not already indented
        if re.match(r"def .*\(.*\):\s*$", line):
            new_lines.append(line)
            next_index = lines.index(line) + 1
            if next_index < len(lines) and not lines[next_index].startswith("    "):
                lines[next_index] = "    " + lines[next_index]
        else:
            new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def fix_unterminated_strings(file_path):
    """Fix unterminated string literals (add missing quotes)."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix common unterminated strings: add closing quote if missing
    content = re.sub(r'(["\'])([^"\']*)$', r'\1\2\1', content, flags=re.MULTILINE)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def wrap_long_lines(file_path, max_len=79):
    """Wrap lines that exceed max_len characters."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if len(line) > max_len:
            # Wrap by splitting at spaces
            while len(line) > max_len:
                split_index = line.rfind(" ", 0, max_len)
                if split_index == -1:
                    split_index = max_len
                new_lines.append(line[:split_index] + "\n")
                line = "    " + line[split_index:].lstrip()
            new_lines.append(line)
        else:
            new_lines.append(line)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def add_pytest_import(file_path):
    """Add 'import pytest' if undefined names detected."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    need_import = False
    for line in lines:
        if re.search(r'\bpytest\b', line):
            need_import = True
            break

    if need_import and not any("import pytest" in l for l in lines):
        lines.insert(0, "import pytest\n")
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

# --- Main processing ---
def process_repo(repo_path):
    print(f"=== Processing Repo: {os.path.basename(repo_path)} ===")
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                # Backup
                backup_path = file_path + ".bak"
                if not os.path.exists(backup_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    with open(backup_path, "w", encoding="utf-8") as f:
                        f.write(content)
                # Fixes
                fix_indentation(file_path)
                fix_unterminated_strings(file_path)
                wrap_long_lines(file_path)
                add_pytest_import(file_path)
    print(f"Finished processing {os.path.basename(repo_path)}\n")

def main():
    # List all repos in your REPOS folder
    base_dir = os.getcwd()
    for repo_name in os.listdir(base_dir):
        repo_path = os.path.join(base_dir, repo_name)
        if os.path.isdir(repo_path):
            process_repo(repo_path)

if __name__ == "__main__":
    main()
