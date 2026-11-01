$ErrorActionPreference='Stop'
$repoRoot=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$cadRoot=Join-Path $repoRoot 'cad/nx'
$launcher='C:/Siemens/nx2406/NXBIN/run_journal.exe'
$records=@();$runs=@{}
$revision=git -C $repoRoot rev-parse HEAD
$oldPose=$env:SX35Z_ATC13_POSE;$oldVerify=$env:SX35Z_VERIFY_RUN
try {
 foreach($pose in @('park','wechsel')) {
  $env:SX35Z_ATC13_POSE=$pose
  foreach($phase in @('build','open_step')) {
   $before=@(Get-ChildItem -LiteralPath $cadRoot -Directory | ForEach-Object FullName)
   $journal=if($phase -eq 'build'){'NX_ATC_Konzept13.py'}else{'NX_ATC_Konzept13_Pruefen.py'}
   if($phase -eq 'open_step') {$env:SX35Z_VERIFY_RUN=$runs[$pose]}
   $scriptPath=Join-Path $repoRoot ('projekt/'+$journal)
   $label=$pose+'_'+$phase;$log=Join-Path $PSScriptRoot ($label+'.log')
   $start=Get-Date
   & $launcher $scriptPath *> $log
   $code=$LASTEXITCODE
   $added=@(Get-ChildItem -LiteralPath $cadRoot -Directory | Where-Object {$_.FullName -notin $before} | ForEach-Object FullName)
   $records += [ordered]@{label=$label;date=$start.ToString('o');command=@($launcher,$scriptPath);cwd=$repoRoot;source_revision=$revision;environment='NX2406/Python3.10.15 Windows';exitcode=$code;seconds=[math]::Round(((Get-Date)-$start).TotalSeconds,2);raw_log=$log;output_directories=$added;verify_target=$env:SX35Z_VERIFY_RUN}
   $records | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $PSScriptRoot 'native_matrix.json')
   Write-Output ($label+' exit='+$code)
   if($code -ne 0){Get-Content $log -Tail 20;throw ('Native failure '+$label)}
   if($phase -eq 'build') {
    if($added.Count -ne 1){throw 'Ambiguous native output'}
    $runs[$pose]=$added[0]
    $runs | ConvertTo-Json | Set-Content (Join-Path $PSScriptRoot 'lieferlaeufe.json')
   }
  }
 }
} finally {$env:SX35Z_ATC13_POSE=$oldPose;$env:SX35Z_VERIFY_RUN=$oldVerify}
