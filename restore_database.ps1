$ErrorActionPreference = "Stop"

Write-Host "This script will restore the original database from the backup."
Write-Host "WARNING: This will overwrite the current database. All changes will be lost."
$confirmation = Read-Host "Are you sure you want to proceed? (y/n)"

if ($confirmation -eq "y") {
    try {
        # Check if backup exists
        if (-Not (Test-Path "db.sqlite3.backup")) {
            Write-Host "Error: Backup file db.sqlite3.backup not found." -ForegroundColor Red
            exit 1
        }

        # Check if server is running and stop it
        $process = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*runserver*" }
        if ($process) {
            Write-Host "Stopping development server..." -ForegroundColor Yellow
            Stop-Process -Id $process.Id -Force
            Start-Sleep -Seconds 2
        }

        # Remove current database if it exists
        if (Test-Path "db.sqlite3") {
            Remove-Item "db.sqlite3" -Force
        }

        # Copy backup to restore
        Copy-Item "db.sqlite3.backup" "db.sqlite3"
        Write-Host "Database successfully restored from backup." -ForegroundColor Green
    }
    catch {
        Write-Host "Error: $_" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "Operation cancelled." -ForegroundColor Yellow
}
