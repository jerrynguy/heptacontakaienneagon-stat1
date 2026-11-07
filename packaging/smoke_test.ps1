# Smoke test for the Windows exe: launch it several times, make sure it stays alive.
# Usage: pwsh packaging/smoke_test.ps1 -Exe dist\HeptacontakaienneagonStat.exe [-Runs 5] [-Screenshot shot.png]
param(
    [Parameter(Mandatory = $true)][string]$Exe,
    [int]$Runs = 5,
    [int]$WaitSeconds = 15,
    [string]$Screenshot = ""
)
$ErrorActionPreference = "Stop"
$name = [System.IO.Path]::GetFileNameWithoutExtension($Exe)
$failed = 0
for ($i = 1; $i -le $Runs; $i++) {
    $p = Start-Process -FilePath $Exe -PassThru
    Start-Sleep -Seconds $WaitSeconds
    if ($i -eq 1 -and $Screenshot) {
        Add-Type -AssemblyName System.Windows.Forms, System.Drawing
        $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
        [System.Drawing.Graphics]::FromImage($bmp).CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
        $bmp.Save($Screenshot)
    }
    if ($p.HasExited) {
        Write-Host "Run ${i}/${Runs}: FAILED - app exited early (exit code $($p.ExitCode))"
        $failed++
    } else {
        Write-Host "Run ${i}/${Runs}: OK - still running after $WaitSeconds s"
    }
    Get-Process -Name $name -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
}
if ($failed -gt 0) { Write-Error "$failed of $Runs runs failed"; exit 1 }
Write-Host "All $Runs runs OK: $Exe"
