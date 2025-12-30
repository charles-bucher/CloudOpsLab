# Automation Scripts

This folder contains scripts that automate repository maintenance, code quality improvements, and portfolio management. These tools eliminate manual work and enforce best practices across your GitHub projects.

## Repository Auto-Fixing Tools

### repo_autofixer.py
Automatically detects and fixes common repository issues.

**Fixes:**
- Missing or incomplete READMEs
- License file issues
- File structure problems
- Documentation gaps

**How to Run:**
```bash
python repo_autofixer.py
```

### repo_safe_autofixer.py
Conservative auto-fixer that only makes safe, non-destructive changes.

**Safe Fixes:**
- Formatting corrections
- Documentation updates
- Metadata improvements

**How to Run:**
```bash
python repo_safe_autofixer.py
```

### repo_lint_fixer.py
Automatically fixes linting and code style issues.

**Addresses:**
- Code formatting (PEP8, style guides)
- Import organization
- Whitespace and indentation
- Common code quality issues

**How to Run:**
```bash
python repo_lint_fixer.py
```

### repo_string_fixer.py
Fixes string-related issues in repository files.

**Corrects:**
- String formatting inconsistencies
- Quote style standardization
- String concatenation improvements

**How to Run:**
```bash
python repo_string_fixer.py
```

## Commit & Version Control Automation

### commit_autofixer.py
Analyzes and improves Git commit messages automatically.

**Improvements:**
- Commit message formatting
- Conventional commit standards
- Message clarity and detail

**How to Run:**
```bash
python commit_autofixer.py
```

## Portfolio Management

### portfolio_master_auto.py
Master automation script for comprehensive portfolio management.

**Automates:**
- Portfolio-wide analysis
- Bulk repository updates
- Status reporting
- Improvement tracking

**How to Run:**
```bash
python portfolio_master_auto.py
```

## Asset Management

### List_pngs.sh
Lists all PNG files across repository structure.

**How to Run:**
```bash
bash List_pngs.sh
```

## Prerequisites

- Python 3.8+
- Git installed and configured
- GitHub CLI (optional, for enhanced features)
- Required Python packages:

```bash
pip install GitPython requests black autopep8 --break-system-packages
```

## Setup Instructions

1. Install Dependencies:
```bash
pip install GitPython requests black autopep8 --break-system-packages
```

2. Configure Git:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

3. Test on Single Repo:
```bash
python repo_safe_autofixer.py
```

4. Review Changes: Always review automated changes before committing

## Important Notes

- Always Review Changes: Automated fixes should be reviewed before pushing
- Use Safe Mode First: Start with repo_safe_autofixer.py before running more aggressive tools
- Backup Important Work: Git commit before running bulk automation scripts
- Test on Non-Critical Repos: Try scripts on test repositories first
- One Repo at a Time: Start with single repository automation before bulk operations

## Coming Soon (AWS Automation)

- Security Group Auditor: Automatically identify and fix security group issues
- Cost Optimization Scanner: Find and remove unused AWS resources
- Snapshot Lifecycle Manager: Automate EBS snapshot creation and cleanup
- IAM Policy Validator: Check IAM policies for security best practices
- Resource Tagger: Bulk tag AWS resources for organization

## Usage Tips

1. Start Conservative: Use repo_safe_autofixer.py first
2. Review Diffs: Always check git diff after running automation
3. Commit Often: Make separate commits for automated changes
4. Test Locally: Run scripts on local repos before pushing changes
5. Document Changes: Note what automated tools were used in commit messages

## Automation Workflow

```bash
# 1. Safe fixes first (low risk)
python repo_safe_autofixer.py

# 2. Check what changed
git status
git diff

# 3. Commit safe changes
git add .
git commit -m "Apply safe automated fixes"

# 4. Fix linting issues
python repo_lint_fixer.py

# 5. Review and commit
git diff
git add .
git commit -m "Fix linting and code style"

# 6. Improve commit history (if needed)
python commit_autofixer.py
```

## Portfolio Automation Best Practices

1. Incremental Changes: Make small, focused automated changes
2. Version Control: Commit before and after automation
3. Manual Review: Always review automated changes manually
4. Test First: Run on test/practice repos before production projects
5. Document Automation: Note which tools were used in project documentation
6. Backup Strategy: Keep backups of original files before bulk automation

## TL;DR

_TODO_

## Overview

_TODO_

## Usage Examples

_TODO_

## Incident Scenarios

_TODO_

## Screenshots

_TODO_

## Contact

_TODO_
