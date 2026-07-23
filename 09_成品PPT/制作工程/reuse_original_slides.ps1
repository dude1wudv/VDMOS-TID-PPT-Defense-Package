param(
  [Parameter(Mandatory=$true)][string]$draft,
  [Parameter(Mandatory=$true)][string]$source,
  [Parameter(Mandatory=$true)][string]$final
)
$ErrorActionPreference = 'Stop'
$map = @{
  1=1; 11=10; 12=11; 13=12; 14=13; 15=14; 16=15; 17=16;
  27=18; 28=19; 29=20; 30=21; 31=22; 32=23; 33=24; 35=25; 36=26; 37=27;
  41=28; 42=29; 44=30; 45=31; 46=32; 47=33; 48=34; 50=35; 51=36; 67=39
}
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = -1
$target = $ppt.Presentations.Open($draft, $false, $false, $false)
$src = $ppt.Presentations.Open($source, $true, $true, $false)
foreach ($targetNo in ($map.Keys | Sort-Object)) {
    $sourceNo = $map[$targetNo]
    $notes = ''
    try { $notes = $target.Slides.Item($targetNo).NotesPage.Shapes.Placeholders.Item(2).TextFrame.TextRange.Text } catch {}
    $target.Slides.Item($targetNo).Delete()
    [void]$target.Slides.InsertFromFile($source, $targetNo - 1, $sourceNo, $sourceNo)
    $slide = $target.Slides.Item($targetNo)
    foreach ($shape in $slide.Shapes) {
        try {
            if ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
                $text = $shape.TextFrame.TextRange.Text
                if ($text -match '^\d{2} / 44$') {
                    $shape.TextFrame.TextRange.Text = ('{0:D2} / 74' -f $targetNo)
                }
            }
        } catch {}
    }
    try { $slide.NotesPage.Shapes.Placeholders.Item(2).TextFrame.TextRange.Text = $notes } catch {}
}
$target.SaveAs($final, 24)
$src.Close()
$target.Close()
$ppt.Quit()
Write-Output ('final=' + $final)
Write-Output ('reused=' + $map.Count)