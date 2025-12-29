import os
import json
import re

# =============================
# CONFIG
# =============================
REPOS_ROOT = os.getcwd()

IGNORE_NAMES = {
    "AWS Cloud Scripts",
    "CloudSnippets",
    "cloud_portfolio_report.json",
    "cloud_portfolio_report"
}

AWS_KEYWORDS = {
    "aws", "ec2", "s3", "lambda", "iam", "cloudwatch",
    "terraform", "cdk", "boto3", "vpc", "rds",
    "autoscaling", "cloudformation"
}

REQUIRED_README_SECTIONS = [
    "Overview",
    "Architecture",
    "Features",
    "Setup",
    "Usage",
    "Skills Demonstrated",
    "License"
]

REPORT_PATH = os.path.join(REPOS_ROOT, "cloud_portfolio_report.json")

# =============================
# HELPERS
# =============================
def safe_read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

def detect_repo_type(repo_name):
    if repo_name.endswith(".github.io"):
        return "portfolio-site"
    if repo_name.lower() in {"charles-bucher"}:
        return "profile-repo"
    return "cloud-project"

def score_readme(readme_text):
    if not readme_text:
        return 0.0, REQUIRED_README_SECTIONS.copy()

    found = []
    for section in REQUIRED_README_SECTIONS:
        if re.search(rf"#+\s*{re.escape(section)}", readme_text, re.I):
            found.append(section)

    score = round((len(found) / len(REQUIRED_README_SECTIONS)) * 100, 1)
    missing = [s for s in REQUIRED_README_SECTIONS if s not in found]
    return score, missing

def score_cloud_relevance(text):
    if not text:
        return 0.0
    hits = sum(1 for kw in AWS_KEYWORDS if kw in text.lower())
    return round((hits / len(AWS_KEYWORDS)) * 100, 1)

def score_documentation(repo_path):
    total_files = 0
    documented = 0

    for root, _, files in os.walk(repo_path):
        for f in files:
            if f.endswith((".py", ".sh", ".ps1")):
                total_files += 1
                content = safe_read(os.path.join(root, f))
                if '"""' in content or "#" in content:
                    documented += 1

    if total_files == 0:
        return 0.0

    return round((documented / total_files) * 100, 1)

def auto_fix_empty_files(repo_path):
    fixes = []
    for root, _, files in os.walk(repo_path):
        for f in files:
            full = os.path.join(root, f)
            if f.endswith((".py", ".sh", ".ps1")) and os.path.getsize(full) ==
0:
                with open(full, "w") as w:
                    w.write("# Auto-filled placeholder\n")
                fixes.append(f)
    return fixes

# =============================
# START SCAN
# =============================
print("="*60)
print("🚀 Starting Cloud Portfolio Scan")
print(f"Scanning repos in: {REPOS_ROOT}")
print("="*60)

results = {}
scanned_count = 0
skipped_count = 0

for repo in os.listdir(REPOS_ROOT):
    if repo in IGNORE_NAMES or repo.startswith("."):
        print(f"[SKIP] Ignoring {repo}")
        skipped_count += 1
        continue

    repo_path = os.path.join(REPOS_ROOT, repo)
    if not os.path.isdir(repo_path):
        continue

    scanned_count += 1
    readme_path = os.path.join(repo_path, "README.md")
    readme_text = safe_read(readme_path)
    repo_type = detect_repo_type(repo)

    readme_score, missing_sections = score_readme(readme_text)
    cloud_score = score_cloud_relevance(readme_text)
    doc_score = score_documentation(repo_path)
    fixes = auto_fix_empty_files(repo_path)

    total_score = round(
        (readme_score * 0.4) +
        (cloud_score * 0.3) +
        (doc_score * 0.3),
        1
    )

    suggestions = []
    for sec in missing_sections:
        suggestions.append(f"Add README section: {sec}")
    if cloud_score < 50:
        suggestions.append("Increase AWS/cloud keywords and examples")
    if doc_score < 50:
        suggestions.append("Add docstrings and inline comments")
    for f in fixes:
        suggestions.append(f"Auto-filled empty file: {f}")

    results[repo] = {
        "Type": repo_type,
        "README Score": readme_score,
        "Cloud Relevance": cloud_score,
        "Documentation Score": doc_score,
        "TOTAL SCORE": total_score,
        "Suggestions": suggestions
    }

    # =============================
    # TERMINAL OUTPUT
    # =============================
    print("\n" + "=" * 60)
    print(f"📂 Repo: {repo}")
    print(f"Type: {repo_type}")
    print(f"README Score: {readme_score}%")
    print(f"Cloud Relevance: {cloud_score}%")
    print(f"Documentation Score: {doc_score}%")
    print(f"TOTAL SCORE: {total_score}%")
    if suggestions:
        print("💡 Suggestions:")
        for s in suggestions:
            print(f"  • {s}")
    else:
        print("✅ No suggestions, this repo is solid!")

# =============================
# FINAL SUMMARY
# =============================
print("\n" + "="*60)
print("✅ Scan Complete")
print(f"Total Repos Scanned: {scanned_count}")
print(f"Total Repos Skipped: {skipped_count}")
if results:
    top_repo = max(results.items(), key=lambda x: x[1]["TOTAL SCORE"])
    print(f"Highest Scoring Repo: {top_repo[0]} ({top_repo[1]['TOTAL
SCORE']}%)")
print("="*60)

# =============================
# SAVE REPORT
# =============================
with open(REPORT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print("\n📄 Full report saved to:", REPORT_PATH)
