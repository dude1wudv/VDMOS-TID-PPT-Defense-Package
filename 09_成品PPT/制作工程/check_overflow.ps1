param([Parameter(Mandatory=$true)][string]$pptx)
$ErrorActionPreference='Stop'
$ppt=New-Object -ComObject PowerPoint.Application
$ppt.Visible=-1
try {
  $pres=$ppt.Presentations.Open($pptx,$true,$true,$false)
  $issues=@()
  foreach($slide in $pres.Slides){
    foreach($shape in $slide.Shapes){
      try {
        if($shape.HasTextFrame -and $shape.TextFrame.HasText){
          $bh=$shape.TextFrame2.TextRange.BoundHeight
          $bw=$shape.TextFrame2.TextRange.BoundWidth
          $availableH=$shape.Height-$shape.TextFrame2.MarginTop-$shape.TextFrame2.MarginBottom
          $availableW=$shape.Width-$shape.TextFrame2.MarginLeft-$shape.TextFrame2.MarginRight
          if($bh -gt ($availableH+2) -and $shape.TextFrame2.AutoSize -eq 0){
            $issues += [pscustomobject]@{slide=$slide.SlideIndex;shape=$shape.Name;boundH=[math]::Round($bh,1);availableH=[math]::Round($availableH,1);text=$shape.TextFrame.TextRange.Text.Substring(0,[math]::Min(50,$shape.TextFrame.TextRange.Text.Length))}
          }
        }
      } catch {}
    }
  }
  $out=[pscustomobject]@{ok=($issues.Count -eq 0);overflow_count=$issues.Count;issues=$issues}
  $out | ConvertTo-Json -Depth 5
  $pres.Close()
} finally {$ppt.Quit()}