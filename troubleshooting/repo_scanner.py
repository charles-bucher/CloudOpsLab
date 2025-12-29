import os
import json

BASE_DIR = os.getcwd()
OUTPUT_FILE = "repo_scan_report.json"

# Define which repos expect Terraform
# True = Terraform required, False = optional / not needed
TERRAFORM_EXPECTED = {
    "AWS_Cloud_Support_Sim": True,
    "AWS_Cloudops_Suite": True,
    "AWS_Error_Driven_Troubleshooting_Lab": True,
    "CloudOpsLab": False,       # Script repo → no Terraform needed
    "charles-bucher": False,    # Portfolio repo → no Terraform needed
    "charles-bucher.github.io": True
}

results = []

def score_repo(has_readme, has_gitignore, script_count, terraform_present, terraform_required):
    score = 50

    if has_readme:
        score += 15
    if has_gitignore:
        score += 10
    if script_count > 0:
        score += 10
    if terraform_required and terraform_present:
        score += 15
    elif not terraform_required:
        # If Terraform not expected, auto-award points
        score += 15

    score = min(score, 100)

    if score >= 95:
        grade = "A"
    elif score >= 85:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"

    return score, grade


print("\n=== Repo Scanner Results ===\n")

for repo in sorted(os.listdir(BASE_DIR)):
    repo_path = os.path.join(BASE_DIR, repo)

    # Skip anything that is not a git repo
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        continue

    terraform_required = TERRAFORM_EXPECTED.get(repo, True)

    has_readme = os.path.isfile(os.path.join(repo_path, "README.md"))
    has_gitignore = os.path.isfile(os.path.join(repo_path, ".gitignore"))

    script_count = 0
    terraform_present = False

    for root, _, files in os.walk(repo_path):
        for f in files:
            if f.endswith((".py", ".ps1", ".sh")):
                script_count += 1
            if f.endswith(".tf"):
                terraform_present = True

    issues = []
    if not has_readme:
        issues.append("Missing README.md")
    if not has_gitignore:
        issues.append("Missing .gitignore")
    if terraform_required and not terraform_present:
        issues.append("No Terraform files detected")

    score, grade = score_repo(
        has_readme,
        has_gitignore,
        script_count,
        terraform_present,
        terraform_required
    )

    results.append({
        "repo": repo,
        "has_readme": has_readme,
        "has_gitignore": has_gitignore,
        "script_count": script_count,
        "terraform_present": terraform_present,
        "terraform_required": terraform_required,
        "issues": issues,
        "score": score,
        "grade": grade
    })

    # Terminal output
    print(f"{repo}")
    print(f"  Grade: {grade} | Score: {score}")
    print(f"  Scripts: {script_count} | Terraform: {terraform_present} |
Terraform Required: {terraform_required}")
    if issues:
        for issue in issues:
            print(f"  ⚠ {issue}")
    else:
        print("  ✅ No issues detected")
    print("-" * 40)

# Write JSON output
with open(OUTPUT_FILE, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nScan complete. JSON report written to {OUTPUT_FILE}\n")
