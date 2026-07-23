param(
  [Parameter(Mandatory=$true)][string]$pptx,
  [Parameter(Mandatory=$true)][string]$pdf,
  [Parameter(Mandatory=$true)][string]$png
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $png | Out-Null
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = -1
try {
  $pres = $ppt.Presentations.Open($pptx, $true, $true, $false)
  $pres.SaveAs($pdf, 32)
  $pres.Export($png, 'PNG', 1600, 900)
  $pres.Close()
  Write-Output ('pdf=' + (Test-Path $pdf))
  Write-Output ('png_count=' + (Get-ChildItem $png -Filter '*.PNG').Count)
} finally {
  $ppt.Quit()
}