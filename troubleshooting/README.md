# Troubleshooting & Portfolio Analysis Scripts

This folder contains scripts for analyzing and troubleshooting GitHub portfolios. These tools help identify issues that could impact your professional presentation and hireability.

---

## 🔍 Repository Analysis & Auditing

### `repo_scanner.py`
Scans GitHub repositories for common issues and best practices.

**Checks:**
- README quality and completeness
- License presence
- Documentation structure
- File organization

**Purpose:** Identify portfolio weaknesses before employers see them  
**Use Case:** Pre-application portfolio audit

**How to Run:**
```bash
python repo_scanner.py
```

---

### `deep_repo_auditor.py`
Comprehensive repository analysis with detailed scoring.

**Analyzes:**
- Code structure and organization
- Documentation quality
- Project completeness
- Professional presentation

**Purpose:** Deep dive into repository quality  
**Use Case:** Get detailed feedback on specific projects

**How to Run:**
```bash
python deep_repo_auditor.py
```

---

### `ultimate_repo_validator.py`
All-in-one repository validation and scoring tool.

**Purpose:** Complete portfolio health check  
**Use Case:** Comprehensive pre-interview portfolio review

**How to Run:**
```bash
python ultimate_repo_validator.py
```

---

## 📝 Code Quality & Best Practices

### `commit_message_analyzer.py`
Analyzes Git commit message quality and patterns.

**Evaluates:**
- Commit message clarity
- Commit frequency and patterns
- Professional commit practices

**Purpose:** Ensure commit history reflects professional development practices  
**Use Case:** Clean up commit history before sharing repositories

**How to Run:**
```bash
python commit_message_analyzer.py
```

---

## 🔐 Security & Credential Scanning

### `credential_scanner.py`
Scans repositories for exposed credentials, API keys, and secrets.

**Detects:**
- Hard-coded passwords
- API keys and tokens
- AWS credentials
- Other sensitive data

**Purpose:** Prevent security vulnerabilities in public repos  
**Use Case:** Critical pre-commit security check

**How to Run:**
```bash
python credential_scanner.py
```

---

## 🚀 Portfolio Optimization

### `scan_portfolio.py`
Quick scan of entire GitHub portfolio for common issues.

**Purpose:** Fast overview of portfolio health  
**Use Case:** Regular portfolio maintenance check

**How to Run:**
```bash
python scan_portfolio.py
```

---

### `portfolio_booster.py`
Provides actionable recommendations to improve portfolio impact.

**Generates:**
- Improvement suggestions
- Priority areas to address
- Optimization strategies

**Purpose:** Maximize portfolio impact on recruiters  
**Use Case:** Optimize before job search campaigns

**How to Run:**
```bash
python portfolio_booster.py
```

---

### `portfolio_entry_scanner.py`
Analyzes portfolio from entry-level job seeker perspective.

**Focus:**
- Entry-level relevant projects
- Demonstrable skills
- Professional presentation

**Purpose:** Ensure portfolio targets entry-level roles effectively  
**Use Case:** Optimize for cloud support and junior DevOps positions

**How to Run:**
```bash
python portfolio_entry_scanner.py
```

---

## 🖼️ Asset Management

### `list_pngs.sh`
Lists all PNG image files in repository structure.

**Purpose:** Inventory visual assets and documentation images  
**Use Case:** Verify image assets are properly committed

**How to Run:**
```bash
bash list_pngs.sh
```

---

## 📋 Prerequisites

- Python 3.8+
- Git installed and configured
- GitHub CLI (optional, for enhanced features)
- Required Python packages:
  ```bash
  pip install requests PyGithub gitpython --break-system-packages
  ```

---

## 🔧 Setup Instructions

1. **Configure GitHub Access:**
   - Some scripts may require GitHub Personal Access Token
   - Create token at: https://github.com/settings/tokens

2. **Install Dependencies:**
   ```bash
   pip install requests PyGithub gitpython --break-system-packages
   ```

3. **Run Portfolio Scan:**
   ```bash
   python scan_portfolio.py
   ```

4. **Review Results:** Address high-priority issues first

---

## ⚠️ Important Notes

- **Public Repositories Only:** These scripts analyze public GitHub repos
- **Credential Scanner:** Run this BEFORE making any repository public
- **Regular Scans:** Run weekly during active job search
- **Take Action:** Use findings to improve your portfolio, don't just collect reports

---

## 🎯 Coming Soon (AWS Troubleshooting)

- **EC2 Connectivity Checker:** Diagnose SSH/RDP connection issues
- **S3 Permission Auditor:** Identify bucket permission problems  
- **RDS Connection Debugger:** Troubleshoot database connectivity
- **Security Group Analyzer:** Find misconfigured security groups
- **VPC Network Tracer:** Debug network routing issues

---

## 💡 Usage Tips

1. **Start with credential_scanner.py:** Always run this first before making repos public
2. **Use scan_portfolio.py regularly:** Quick health checks during job search
3. **Deep dive before applications:** Run deep_repo_auditor.py before applying to jobs
4. **Fix high-priority issues first:** Focus on credential exposure and missing READMEs
5. **Track improvements:** Re-scan after making changes to measure progress

---

## 🎯 Portfolio Optimization Workflow

```bash
# 1. Security check (CRITICAL - do this first)
python credential_scanner.py

# 2. Quick portfolio overview
python scan_portfolio.py

# 3. Deep analysis of key repos
python deep_repo_auditor.py

# 4. Get improvement recommendations
python portfolio_booster.py

# 5. Entry-level optimization
python portfolio_entry_scanner.py
```