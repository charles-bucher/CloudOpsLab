#Requires -RunAsAdministrator

# Safe Windows Bloatware Removal Script

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "    Safe Windows Bloatware Removal Tool" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

# Create backup of installed apps list
$backupPath = "$env:USERPROFILE\Desktop\InstalledApps_Backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
Write-Host "Creating backup of installed apps..." -ForegroundColor Yellow
Get-AppxPackage | Select-Object Name, PackageFullName | Out-File -FilePath $backupPath
Write-Host "Backup created at: $backupPath" -ForegroundColor Green
Write-Host ""

# List of safe-to-remove bloatware
$bloatwareList = @(
    "Microsoft.3DBuilder",
    "Microsoft.BingFinance",
    "Microsoft.BingNews",
    "Microsoft.BingSports",
    "Microsoft.BingWeather",
    "Microsoft.GetHelp",
    "Microsoft.Getstarted",
    "Microsoft.Messaging",
    "Microsoft.Microsoft3DViewer",
    "Microsoft.MicrosoftOfficeHub",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.MicrosoftStickyNotes",
    "Microsoft.MixedReality.Portal",
    "Microsoft.Office.OneNote",
    "Microsoft.OneConnect",
    "Microsoft.People",
    "Microsoft.Print3D",
    "Microsoft.SkypeApp",
    "Microsoft.Wallet",
    "Microsoft.WindowsAlarms",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.WindowsMaps",
    "Microsoft.WindowsSoundRecorder",
    "Microsoft.Xbox.TCUI",
    "Microsoft.XboxApp",
    "Microsoft.XboxGameOverlay",
    "Microsoft.XboxGamingOverlay",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.XboxSpeechToTextOverlay",
    "Microsoft.YourPhone",
    "Microsoft.ZuneMusic",
    "Microsoft.ZuneVideo",
    "*.CandyCrush*",
    "*.Facebook*",
    "*.Twitter*",
    "*.Spotify*",
    "*.Disney*",
    "king.com.*",
    "*.Minecraft*",
    "*.Netflix*",
    "*.LinkedInforWindows",
    "*.Duolingo*",
    "*.Pandora*",
    "*.Instagram*"
)

# Apps to NEVER remove
$protectedApps = @(
    "Microsoft.Windows.Cortana",
    "Microsoft.WindowsStore",
    "Microsoft.WindowsCalculator",
    "Microsoft.Windows.Photos",
    "Microsoft.ScreenSketch",
    "Microsoft.Paint",
    "Microsoft.MSPaint",
    "Microsoft.WindowsCamera",
    "Microsoft.StorePurchaseApp",
    "Microsoft.VCLibs*",
    "Microsoft.NET*",
    "Microsoft.DesktopAppInstaller"
)

# Scan for bloatware
Write-Host "Scanning for bloatware..." -ForegroundColor Yellow
$foundBloatware = @()

foreach ($bloat in $bloatwareList) {
    $apps = Get-AppxPackage -Name $bloat -AllUsers -ErrorAction SilentlyContinue
    if ($apps) {
        $foundBloatware += $apps
    }
}

if ($foundBloatware.Count -eq 0) {
    Write-Host ""
    Write-Host "No bloatware found! Your system is already clean." -ForegroundColor Green
    pause
    exit
}

# Display found bloatware
Write-Host ""
Write-Host "Found $($foundBloatware.Count) bloatware apps:" -ForegroundColor Yellow
$foundBloatware | ForEach-Object { Write-Host "  - $($_.Name)" }

# Confirmation
Write-Host ""
Write-Host "Do you want to remove these apps? (Y/N)" -ForegroundColor Yellow
$confirmation = Read-Host
if ($confirmation -ne 'Y' -and $confirmation -ne 'y') {
    Write-Host "Operation cancelled. No changes made." -ForegroundColor Cyan
    pause
    exit
}

# Remove bloatware
Write-Host ""
Write-Host "Removing bloatware..." -ForegroundColor Yellow
$removed = 0
$failed = 0

foreach ($app in $foundBloatware) {
    $isProtected = $false
    foreach ($protected in $protectedApps) {
        if ($app.Name -like $protected) {
            $isProtected = $true
            break
        }
    }
    
    if ($isProtected) {
        Write-Host "  Skipping protected app: $($app.Name)" -ForegroundColor Yellow
        continue
    }
    
    try {
        Write-Host "  Removing: $($app.Name)..."
        Remove-AppxPackage -Package $app.PackageFullName -ErrorAction Stop
        Write-Host "  Removed: $($app.Name)" -ForegroundColor Green
        $removed++
    }
    catch {
        Write-Host "  Failed to remove: $($app.Name)" -ForegroundColor Red
        Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

# Summary
Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "                    SUMMARY" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "Successfully removed: $removed apps" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "Failed to remove: $failed apps" -ForegroundColor Red
}
Write-Host "Backup file: $backupFile" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Note: Some changes may require a restart to take effect." -ForegroundColor Yellow
Write-Host "Would you like to restart now? (Y/N)" -ForegroundColor Yellow
$restart = Read-Host
if ($restart -eq 'Y' -or $restart -eq 'y') {
    Restart-Computer
} else {
    Write-Host ""
    Write-Host "Done! Remember to restart when convenient." -ForegroundColor Green
}

pause