PORTFOLIO_OPS_RUNBOOK.md
# Portfolio Ops Runbook

## Purpose
Portfolio Ops scripts are **meta-operations** used to audit, validate, harden, and continuously improve cloud and GitHub repositories.  
These scripts simulate how CloudOps and DevOps teams enforce **quality, security, and operational standards at scale**.

This runbook documents **when, why, and how** to run each Portfolio Ops script.

---

## Scope
These scripts operate on:
- Git repositories
- CloudOps portfolios
- Automation pipelines
- Documentation and structure standards

They are **read-only or low-risk corrective tools**, designed for:
- Entry-level CloudOps
- Junior DevOps
- Platform support engineers
- Consulting readiness

---

## When to Run Portfolio Ops

| Scenario | Action |
|--------|-------|
New repo created | Run full portfolio scan |
Before job application | Run audit + summary |
After major refactor | Run validation checks |
CI failure | Run compliance + lint scripts |
Security review | Run security + exposure scans |

---

## Script Inventory

### 01️⃣ Commit Auto Fixer
**Script:** `portfolio_ops_01_commit_auto_fixer.py`

**Purpose**
- Normalizes commit messages
- Removes unsafe emojis / formatting
- Enforces professional commit standards

**Run**
```bash
python portfolio_ops_01_commit_auto_fixer.py

02️⃣ Repo Issue Remediator

Script: portfolio_ops_02_repo_issue_remediator.py

Purpose

Fixes common repo hygiene issues

Missing READMEs

Bad file placement

Naming inconsistencies

Run

python portfolio_ops_02_repo_issue_remediator.py

03️⃣ Safe Repo Fix Helper

Script: portfolio_ops_03_safe_repo_fix_helper.py

Purpose

Applies non-destructive fixes only

Prevents accidental data loss

Used in regulated or shared repos

Run

python portfolio_ops_03_safe_repo_fix_helper.py

04️⃣ Repo Compliance Check

Script: portfolio_ops_04_repo_compliance_check.py

Purpose
Validates:

README presence

License file

Folder structure

Security.md existence

Output

Pass / Fail report

Actionable remediation notes

Run

python portfolio_ops_04_repo_compliance_check.py

05️⃣ Repo Security Scan

Script: portfolio_ops_05_repo_security_scan.py

Purpose
Detects:

Hardcoded secrets

Unsafe patterns

Credential exposure risks

⚠️ Read-only
Does NOT modify files.

Run

python portfolio_ops_05_repo_security_scan.py

06️⃣ Repo String Cleanup

Script: portfolio_ops_06_repo_string_cleanup.py

Purpose

Removes profanity / placeholder text

Fixes casing and formatting

Normalizes documentation language

Run

python portfolio_ops_06_repo_string_cleanup.py

07️⃣ Code Lint Cleanup

Script: portfolio_ops_07_code_lint_cleanup.py

Purpose

Removes unused imports

Fixes formatting drift

Improves readability

Run

python portfolio_ops_07_code_lint_cleanup.py

08️⃣ Repo Validation Check

Script: portfolio_ops_08_repo_validation_check.py

Purpose
Final gate before:

Publishing

Tagging

Releasing

Checks:

All scripts runnable

Required folders exist

No empty files

Run

python portfolio_ops_08_repo_validation_check.py

Expected Output

Clear PASS / WARN / FAIL indicators

No silent failures

Human-readable summaries

Failure Handling

If a script fails:

Read the error message

Fix manually OR

Re-run remediation scripts

Re-validate

Never ignore failures — they simulate production blockers.

Best Practices

Run Portfolio Ops locally before pushing

Tag repos only after passing validation

Keep scripts idempotent

Treat your portfolio like production

Why This Matters

Most portfolios show what someone built.

This shows:

How you operate

How you prevent issues

How you think at scale

That’s CloudOps maturity.

Ownership

Maintained by: Charles Bucher
Role simulated: CloudOps / Platform Engineer


---

## 📂 Where this file goes (important)



CloudOpsLab/
└── portfolio_ops/
├── PORTFOLIO_OPS_RUNBOOK.md ✅
├── portfolio_ops_01_commit_auto_fixer.py
├── portfolio_ops_02_repo_issue_remediator.py
└── ...

