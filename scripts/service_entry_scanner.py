"""
Service Entry Scanner
Purpose: [AWS automation script]
Author: Charles Bucher
"""

# Import required libraries
import os
import re


# Define cloud keywords relevant to entry-level cloud
CLOUD_KEYWORDS = [
    "aws", "ec2", "s3", "lambda", "terraform", "cloudwatch",
    "vpc", "iam", "rds", "cloudformation", "sns", "sqs"
]

# Define scoring weights
WEIGHTS = {
    "cloud_relevance": 0.4,
    "readme_quality": 0.3,
    "documentation_quality": 0.3
}
def scan_repo(repo_path):
    """
        Function to scan_repo.
    """

    repo_name = os.path.basename(repo_path)
    cloud_hits = 0
    readme_sections = 0
    documentation_quality = 0

    # Count cloud keywords
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".sh", ".md", ".yaml", ".json")):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8")
as f:
                        content = f.read().lower()
                        cloud_hits += sum(1 for kw in CLOUD_KEYWORDS if kw in content)
                        # Simple documentation check: count TODOs or comments
                        documentation_quality += content.count("#") +
content.count("'''") + content.count('"""')
                except Exception as e:
                    print(f"[WARN] Could not read {file}: {e}")

    # Check README for sections
    readme_path = os.path.join(repo_path, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            for section in ["tl;dr", "setup instructions", "usage examples",
"contact"]:
                if section in content:
                    readme_sections += 1

    # Compute percentages
    cloud_score = min(100, cloud_hits * 5)  # arbitrary scale
    readme_score = (readme_sections / 4) * 100
    doc_score = min(100, documentation_quality / 10)  # arbitrary scale

    total_score = (
        cloud_score * WEIGHTS["cloud_relevance"]
        + readme_score * WEIGHTS["readme_quality"]
        + doc_score * WEIGHTS["documentation_quality"]
    )

    # Generate suggestions
    suggestions = []
    if cloud_score < 70:
        suggestions.append("Add more AWS/cloud keywords and examples.")
    if readme_score < 75:
        suggestions.append("Enhance README sections: TL;DR, Setup, Usage,
Contact.")
    if doc_score < 50:
        suggestions.append("Add more comments and docstrings to scripts.")

    return {
        "repo": repo_name,
        "cloud_score": round(cloud_score, 1),
        "readme_score": round(readme_score, 1),
        "doc_score": round(doc_score, 1),
        "total_score": round(total_score, 1),
        "suggestions": suggestions
    }
def scan_all_repos(base_path):
    """
        Function to scan_all_repos.
    """

    results = []
    for repo_name in os.listdir(base_path):
        repo_path = os.path.join(base_path, repo_name)
        if os.path.isdir(repo_path):
            results.append(scan_repo(repo_path))
    return results

if __name__ == "__main__":
    base_path = r"C:\Users\buche\docs\Desktop\REPOS"  # change if needed
    results = scan_all_repos(base_path)

    print("="*60)
    print("ENTRY-LEVEL CLOUD PORTFOLIO DEEP SCAN")
    print("="*60)
    for r in results:
        print(f"Repo: {r['repo']}")
        print(f"  Cloud Score: {r['cloud_score']}%")
        print(f"  README Score: {r['readme_score']}%")
        print(f"  Documentation Score: {r['doc_score']}%")
        print(f"  Total Score: {r['total_score']}%")
        if r['suggestions']:
            print(f"  Suggestions: {', '.join(r['suggestions'])}")
        print("-"*60)