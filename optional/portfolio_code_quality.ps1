# PortfolioCodeQualityScanner.ps1
# Deep scans all repos in a folder and evaluates completeness and code quality

# Root folder containing all your repos
$reposRoot = "C:\Users\buche\docs\Desktop\REPOS"

# Define expected README sections per repo
$readmeSections = @{
    "AWS Cost Optimization Tool" = @("Incident Scenarios","Skills","License")
    "CloudOpsLab" = @("TL;DR","Quick Start","Incident Scenarios","Installation","Contact")
}

# Function to clean placeholders
function Clean-Placeholders {
    param([string]$filePath)
    if (Test-Path $filePath) {
        (Get-Content $filePath) -replace '\bTODO\b','' | Set-Content $filePath
    }
}

# Function to check code quality
function Check-CodeQuality {
    param([string]$filePath)
    $issues = @()
    if ((Test-Path $filePath) -and ((Get-Item $filePath).Length -eq 0)) {
        $issues += "Empty file"
    }
    # Basic Python checks
    if ($filePath -like "*.py") {
        $content = Get-Content $filePath -Raw
        if ($content -notmatch "def\s") { $issues += "No functions/classes" }
        if ($content -notmatch "#") { $issues += "No comments" }
    }
    # Basic PowerShell checks
    if ($filePath -like "*.ps1") {
        $content = Get-Content $filePath -Raw
        if ($content -notmatch "#") { $issues += "No comments" }
    }
    return $issues
}

# Scan each repo
$results = @()
Get-ChildItem -Path $reposRoot -Directory | ForEach-Object {
    $repoName = $_.Name
    $repoPath = $_.FullName
    $issues = @()

    # Fix placeholders in scripts, hooks
    Get-ChildItem -Path $repoPath -Recurse -File | Where-Object { $_.Extension -in ".sh",".ps1",".sample" } | ForEach-Object {
        Clean-Placeholders $_.FullName
    }

    # Check README sections
    $readmePath = Join-Path $repoPath "README.md"
    if ((Test-Path $readmePath) -and $readmeSections.ContainsKey($repoName)) {
        $expectedSections = $readmeSections[$repoName]
        $readmeContent = Get-Content $readmePath -Raw
        foreach ($section in $expectedSections) {
            if ($readmeContent -notmatch [regex]::Escape($section)) {
                $issues += "Missing README section: $section"
            }
        }
    }

    # Scan all files for code quality
    Get-ChildItem -Path $repoPath -Recurse -File | ForEach-Object {
        $fileIssues = Check-CodeQuality $_.FullName
        foreach ($i in $fileIssues) {
            $issues += "$i in: $($_.FullName)"
        }
    }

    # Calculate hireability score
    $score = if ($issues.Count -eq 0) { 100 } else { [math]::Round(100 - ($issues.Count * 3),2) }
    if ($score -lt 0) { $score = 0 }

    $results += [PSCustomObject]@{
        Repo  = $repoName
        Score = $score
        Issues = $issues
    }
}

# Display per repo
foreach ($r in $results) {
    Write-Host "---------------------------"
    Write-Host "Repo: $($r.Repo)"
    Write-Host "Hireability Score: $($r.Score)%"
    if ($r.Issues.Count -gt 0) {
        Write-Host "Issues:"
        foreach ($i in $r.Issues) { Write-Host "  • $i" }
    }
}

# Display overall portfolio score
$overallScore = [math]::Round(($results | Measure-Object Score -Average).Average,2)
Write-Host "---------------------------"
Write-Host "Overall Portfolio Hireability Score: $overallScore%"
Write-Host "---------------------------"
