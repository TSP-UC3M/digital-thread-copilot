<#
.SYNOPSIS
  Runs the local checks of rule R5 before a push (plan step B5).
.DESCRIPTION
  1. Documentation build in strict mode
  2. Freshness of the translations
  3. Lint, unit tests and functional tests
  4. Message of the last commit against Conventional Commits
  Exits with code 0 when every check passes, 1 otherwise.
  Run it from the repository root, inside the virtual environment:
      .\scripts\check.ps1
      .\scripts\check.ps1 -SkipCommitlint   (when Node.js is not installed)
#>
param([switch]$SkipCommitlint)

$failed = @()

function Invoke-Check([string]$Name, [scriptblock]$Command) {
    Write-Host "== $Name" -ForegroundColor Cyan
    & $Command
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $Name" -ForegroundColor Red
        $script:failed += $Name
    }
}

Invoke-Check "documentation build (strict)" { python -m mkdocs build --strict }
Invoke-Check "translations" { python scripts/check_translations.py --strict }
Invoke-Check "lint and tests" { python scripts/dev.py check }

if ($SkipCommitlint) {
    Write-Host "== commit message: skipped on request" -ForegroundColor Yellow
} elseif (-not (Get-Command commitlint -ErrorAction SilentlyContinue)) {
    Write-Host "FAILED: commitlint is not installed (see CONTRIBUTING.md), or use -SkipCommitlint" -ForegroundColor Red
    $failed += "commit message"
} else {
    Invoke-Check "commit message" { git log -1 --format=%B | commitlint }
}

if ($failed.Count -gt 0) {
    Write-Host ("Checks failed: " + ($failed -join ", ")) -ForegroundColor Red
    exit 1
}
Write-Host "All checks passed." -ForegroundColor Green
exit 0
