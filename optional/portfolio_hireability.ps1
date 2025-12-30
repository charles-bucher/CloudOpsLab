# === CONFIG ===
$reposRoot = "C:\Users\buche\docs\Desktop\REPOS"

# Expected README sections per repo
$readmeSections = @{
    "AWS Cost Optimization Tool" = @("Incident Scenarios","Skills","License")
    "CloudOpsLab" = @("TL;DR","Quick Start","Incident Scenarios","Installation","Contact")
}

# Function to clean placeholders in scripts/hooks
function Clean-Placeholders {
    param([string]$filePath)
    if (Test-Path $filePath) {
        (Get-Content $filePath) -replace '\bTODO\b', '' | Set-Content $filePath
        Write-Host "Cleaned placeholder in $filePath"
    }
}

# Function to check for missing README sections
function Check-Readme-Sections {
    param([string]$readmePath, [string[]]$sections)
    $issues = @()
    if (Test-Path $readmePath) {
        $content = Get-Content $readmePath
        foreach ($section in $sections) {
            if ($content -notmatch $section) {
                $issues += "Missing README section: $section"
            }
        }
    } else {
        $issues += "README.md missing"
    }
    return $issues
}

# Function to scan a repo for issues and compute hireability score
function Scan-Repo {
    param([string]$repoPath)
    $repoName = Split-Path $repoPath -Leaf
    $issues = @()

    # Check for empty files
    $emptyFiles = Get-ChildItem -Path $repoPath -Recurse -File | Where-Object { $_.Length -eq 0 }
    foreach ($f in $emptyFiles) { $issues += "Empty file: $($f.FullName)" }

    # Check for placeholders in scripts/hooks
    $placeholderFiles = Get-ChildItem -Path $repoPath -Recurse -File | Where-Object { $_.Extension -in ".sh",".ps1",".sample" }
    foreach ($f in $placeholderFiles) {
        if ((Get-Content $f.FullName) -match '\bTODO\b') {
            $issues += "Placeholder found in: $($f.FullName)"
        }
    }

    # Check README sections
    if ($readmeSections.ContainsKey($repoName)) {
        $issues += Check-Readme-Sections (Join-Path $repoPath "README.md") $readmeSections[$repoName]
    }

    # Compute hireability score (simple heuristic)
    $score = 100
    if ($issues.Count -gt 0) {
        $score -= [math]::Round(($issues.Count * 3),2) # 3 points per issue
        if ($score -lt 0) { $score = 0 }
    }

    return [PSCustomObject]@{
        Repo = $repoName
        Score = $score
        Issues = $issues
    }
}

# === MAIN SCAN ===
$results = @()
Get-ChildItem -Path $reposRoot -Directory | ForEach-Object {
    $repoPath = $_.FullName
    $results += Scan-Repo $repoPath
}

# === DISPLAY RESULTS ===
foreach ($r in $results) {
    Write-Host "Repo: $($r.Repo)"
    Write-Host "Hireability Score: $($r.Score)%"
    if ($r.Issues.Count -gt 0) {
        Write-Host "Issues:"
        $r.Issues | ForEach-Object { Write-Host "  • $_" }
    }
    Write-Host "---------------------------"
}

# Overall portfolio score
$overallScore = [math]::Round(($results | Measure-Object Score -Average).Average,2)
Write-Host "Overall Portfolio Hireability Score: $overallScore%"
