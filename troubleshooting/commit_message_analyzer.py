import re
from typing import List, Optional

class CommitMessageAnalyzer:
    """
    Analyzes commit messages for quality, structure, and best‑practice compliance.
    """

    def __init__(self, github_username: str = "buche", auto_fix: bool = False):
        self.github_username = github_username
        self.auto_fix = auto_fix

        # Conventional commit types
        self.allowed_types = [
            "feat", "fix", "docs", "style", "refactor",
            "perf", "test", "build", "ci", "chore", "revert"
        ]

    # ---------------------------------------------------------
    # Core Analysis
    # ---------------------------------------------------------

    def analyze(self, message: str) -> dict:
        """
        Analyze a commit message and return a structured report.
        """

        report = {
            "original": message,
            "is_valid": True,
            "issues": [],
            "suggested_fix": None
        }

        # Check length
        if len(message) > 72:
            report["issues"].append("Subject line exceeds 72 characters.")
            report["is_valid"] = False

        # Check for blank line after subject
        if "\n" in message:
            subject, body = message.split("\n", 1)
            if not body.startswith("\n"):
                report["issues"].append("Missing blank line between subject and body.")
                report["is_valid"] = False
        else:
            subject = message

        # Check conventional commit format
        if not self._is_conventional(subject):
            report["issues"].append("Subject does not follow conventional commit format.")
            report["is_valid"] = False

        # Auto‑fix if enabled
        if self.auto_fix and not report["is_valid"]:
            report["suggested_fix"] = self.suggest_fix(message)

        return report

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _is_conventional(self, subject: str) -> bool:
        """
        Validate conventional commit format: type(scope?): description
        """
        pattern = r"^(" + "|".join(self.allowed_types) + r")(?:\([\w\-]+\))?: .+"
        return bool(re.match(pattern, subject))

    def suggest_fix(self, message: str) -> str:
        """
        Suggest a corrected commit message.
        """

        # Try to extract a type
        suggested_type = "chore"

        # Extract first sentence as description
        description = message.strip().split("\n")[0]
        description = description.capitalize()

        return f"{suggested_type}: {description}"

# ---------------------------------------------------------
# Script Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    analyzer = CommitMessageAnalyzer(github_username="buche", auto_fix=True)

    test_message = input("Enter a commit message to analyze:\n\n")

    result = analyzer.analyze(test_message)

    print("\n--- Analysis Report ---")
    print(f"Valid: {result['is_valid']}")
    print(f"Issues: {result['issues']}")

    if result["suggested_fix"]:
        print("\nSuggested Fix:")
        print(result["suggested_fix"])
