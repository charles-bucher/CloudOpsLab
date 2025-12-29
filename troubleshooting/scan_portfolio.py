import os
import re
import json

# Optional: for colored output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = ''
        YELLOW = ''
        GREEN = ''
        BLUE = ''
    class Style:
        RESET_ALL = ''

REPOS_DIR = r"C:\Users\buche\docs\Desktop\REPOS"
PLACEHOLDER_PATTERNS = [
    r"<.*?>",  # generic placeholders like <bucket-name>
    r"YOUR_.*?",  # e.g., YOUR_IAM_ROLE_ARN
    r"test.*key",  # testing keys
    r"aws_access_key_id\s*=\s*['\"].*?['\"]",  # AWS keys hardcoded
    r"aws_secret_access_key\s*=\s*['\"].*?['\"]",
]

def scan_repo(repo_path):
    repo_info = {"repo": os.path.basename(repo_path), "placeholders": [],
"metrics": {}}

    # Metrics
    file_count = 0
    line_count = 0
    readme_present = False
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_count += 1
            if file.lower().startswith("readme"):
                readme_present = True
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as
f:
                    lines = f.readlines()
                    line_count += len(lines)
                    for i, line in enumerate(lines, 1):
                        for pattern in PLACEHOLDER_PATTERNS:
                            if re.search(pattern, line, re.IGNORECASE):
                                repo_info["placeholders"].append({
                                    "file": os.path.relpath(file_path,
REPOS_DIR),
                                    "line": i,
                                    "match": line.strip()
                                })
            except Exception:
                continue

    # Beefiness score (simple heuristic)
    beef_score = min(100, int(file_count / 5 + line_count / 100))
    repo_info["metrics"] = {
        "files": file_count,
        "lines": line_count,
        "readme_present": readme_present,
        "beefiness_score": beef_score
    }

    return repo_info

def print_report(repo_info):
    print(f"{Fore.BLUE}📁 Repository: {repo_info['repo']}{Style.RESET_ALL}")
    print(f"   Files: {repo_info['metrics']['files']}, Lines:
{repo_info['metrics']['lines']}, "
          f"README: {'✅' if repo_info['metrics']['readme_present'] else '❌'}, "
          f"Beefiness Score: {repo_info['metrics']['beefiness_score']}/100")
    if repo_info["placeholders"]:
        print(f"   {Fore.RED}⚠️ Placeholders Found:
{len(repo_info['placeholders'])}{Style.RESET_ALL}")
        for p in repo_info["placeholders"]:
            print(f"      -
{Fore.YELLOW}{p['file']}:{p['line']}{Style.RESET_ALL} → {p['match']}")
    else:
        print(f"   {Fore.GREEN}✅ No placeholders found{Style.RESET_ALL}")
    print("-" * 80)

def main():
    report = []
    for repo in os.listdir(REPOS_DIR):
        repo_path = os.path.join(REPOS_DIR, repo)
        if os.path.isdir(repo_path):
            info = scan_repo(repo_path)
            report.append(info)
            print_report(info)

    # Save JSON report
    report_file = os.path.join(REPOS_DIR, "portfolio_beefiness_scan.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n✅ Full scan complete! JSON report saved to {report_file}")

if __name__ == "__main__":
    main()
