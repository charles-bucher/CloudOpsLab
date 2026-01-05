<#
.SYNOPSIS
    Audits AWS IAM users for credential exposure risks.

.DESCRIPTION
    - Lists IAM users
    - Audits access key age and usage
    - Flags unused or old keys
    - Identifies admin-level permissions
    Read-only and safe to run.

.REQUIREMENTS
    AWS CLI configured
    iam:ListUsers
    iam:ListAccessKeys
    iam:GetAccessKeyLastUsed
    iam:ListAttachedUserPolicies
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$MaxKeyAgeDays = 90

function Get-DaysOld {
    param ([datetime]$Date)
    return (New-TimeSpan -Start $Date -End (Get-Date)).Days
}

function Get-IAMUsers {
    aws iam list-users --output json | ConvertFrom-Json | Select-Object -ExpandProperty Users
}

function Get-AccessKeys {
    param ($UserName)
    aws iam list-access-keys --user-name $UserName --output json |
        ConvertFrom-Json | Select-Object -ExpandProperty AccessKeyMetadata
}

function Get-KeyLastUsed {
    param ($AccessKeyId)

    try {
        $data = aws iam get-access-key-last-used --access-key-id $AccessKeyId --output json |
            ConvertFrom-Json
        return $data.AccessKeyLastUsed.LastUsedDate
    } catch {
        return $null
    }
}

function Test-AdminAccess {
    param ($UserName)

    try {
        $policies = aws iam list-attached-user-policies --user-name $UserName --output json |
            ConvertFrom-Json | Select-Object -ExpandProperty AttachedPolicies

        foreach ($p in $policies) {
            if ($p.PolicyName -match "(?i)admin") {
                return $true
            }
        }
    } catch {}

    return $false
}

Write-Output "`n===== IAM CREDENTIAL EXPOSURE AUDIT =====`n"

$users = Get-IAMUsers

if (-not $users) {
    Write-Output "✅ No IAM users found."
    exit
}

foreach ($user in $users) {

    Write-Output "🔍 IAM User: $($user.UserName)"

    if (Test-AdminAccess -UserName $user.UserName) {
        Write-Warning "Admin-level policy attached"
    }

    $keys = Get-AccessKeys -UserName $user.UserName

    if (-not $keys) {
        Write-Output "  ✅ No access keys"
        continue
    }

    foreach ($key in $keys) {
        $age = Get-DaysOld $key.CreateDate
        $lastUsed = Get-KeyLastUsed $key.AccessKeyId

        Write-Output "  🔑 Access Key: $($key.AccessKeyId)"
        Write-Output "     Status: $($key.Status)"
        Write-Output "     Age: $age days"

        if ($age -gt $MaxKeyAgeDays) {
            Write-Warning "     Key older than $MaxKeyAgeDays days"
        }

        if ($lastUsed) {
            $lastUsedDays = Get-DaysOld ([datetime]$lastUsed)
            Write-Output "     Last Used: $lastUsedDays days ago"

            if ($lastUsedDays -gt $MaxKeyAgeDays) {
                Write-Warning "     Key unused for $MaxKeyAgeDays+ days"
            }
        } else {
            Write-Warning "     Key has never been used"
        }
    }

    Write-Output ""
}

Write-Output "===== AUDIT COMPLETE =====`n"
