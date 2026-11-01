$ErrorActionPreference='Stop'
$repoRoot=(Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$cadRoot=Join-Path $repoRoot 'cad/nx'
$launcher='C:/Siemens/nx2406/NXBIN/run_journal.exe'
$sources=@(Get-ChildItem (Join-Path $repoRoot 'projekt') -File | Where-Object {$_.Extension -in '.py','.json'})
$sources+=Get-Item (Join-Path $repoRoot 'projekt/Einkauf/Kaufteile_09.json')
$sources | ForEach-Object {[ordered]@{path=$_.FullName.Substring($repoRoot.Length+1);sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}} | ConvertTo-Json | Set-Content (Join-Path $PSScriptRoot 'native_source_hashes.json')
$tasks=@(
 @('teller','NX_Normteile_ATC_Pruefen'),@('park','NX_CNC_Gesamtansicht'),
 @('park_open','NX_Git_Lieferstand_Pruefen'),@('wechsel','NX_CNC_Wechselstellung'),
 @('wechsel_open','NX_Git_Lieferstand_Pruefen'))
$records=@();$runs=@{};$originalVerify=$env:SX35Z_VERIFY_RUN
try {
 foreach($task in $tasks) {
  $label=$task[0];$journal=$task[1]
  if($label.EndsWith('_open')) {$env:SX35Z_VERIFY_RUN=$runs[$label.Replace('_open','')]}
  $before=@(Get-ChildItem -LiteralPath $cadRoot -Directory | ForEach-Object FullName)
  $start=Get-Date;$scriptPath=Join-Path $repoRoot ('projekt/'+$journal+'.py')
  $log=Join-Path $PSScriptRoot ('native_'+$label+'.stdout.txt')
  & $launcher $scriptPath *> $log
  $runExit=$LASTEXITCODE
  $added=@(Get-ChildItem -LiteralPath $cadRoot -Directory | Where-Object {$_.FullName -notin $before} | ForEach-Object FullName)
  $records += [ordered]@{label=$label;journal=$journal;date=$start.ToString('o');command=@($launcher,$scriptPath);cwd=$repoRoot;source_base='b6e4643d5558780936f7b622af0102ad64041215';source_snapshot='native_source_hashes.json';environment='NX2406 Python3.10.15 Windows';exitcode=$runExit;seconds=[math]::Round(((Get-Date)-$start).TotalSeconds,2);raw_log=$log;output_directories=$added;verify_target=$env:SX35Z_VERIFY_RUN}
  $records | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $PSScriptRoot 'native_matrix.json')
  Write-Output ($label+' exit='+$runExit)
  if($runExit -ne 0) {Get-Content $log -Tail 20;throw ('Native failure '+$label)}
  if($label -in @('park','wechsel')) {
   if($added.Count -ne 1) {throw 'Ambiguous full assembly output'}
   $runs[$label]=$added[0]
   $runs | ConvertTo-Json | Set-Content (Join-Path $PSScriptRoot 'lieferlaeufe.json')
  }
 }
} finally {$env:SX35Z_VERIFY_RUN=$originalVerify}
