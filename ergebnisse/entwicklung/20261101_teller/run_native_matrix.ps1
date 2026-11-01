$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../..')).Path
$launcher = 'C:/Siemens/nx2406/NXBIN/run_journal.exe'
$cadRoot = Join-Path $repoRoot 'cad/nx'
$matrix = @()
$fullRun = $null
$originalVerify = $env:SX35Z_VERIFY_RUN
$sourceFiles = @(Get-ChildItem (Join-Path $repoRoot 'projekt') -File | Where-Object { $_.Extension -in '.py','.json' })
$sourceFiles += Get-Item (Join-Path $repoRoot 'projekt/Einkauf/Kaufteile_09.json')
$sourceFiles | ForEach-Object {
    [ordered]@{path=$_.FullName.Substring($repoRoot.Length+1);sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
} | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $PSScriptRoot 'native_source_hashes.json')
try {
    foreach ($journal in @('NX_Metadaten_Pruefen','NX_Blech_Pruefen','NX_KSS_Pruefen',
        'NX_Umbau_Kern_Pruefen','NX_Normteile_ATC_Pruefen','NX_CNC_Gesamtansicht','NX_Git_Lieferstand_Pruefen')) {
        if ($journal -eq 'NX_Git_Lieferstand_Pruefen') {
            if (-not $fullRun) { throw 'No successful full run available' }
            $env:SX35Z_VERIFY_RUN = $fullRun
        }
        $before = @(Get-ChildItem -LiteralPath $cadRoot -Directory | ForEach-Object FullName)
        $start = Get-Date
        $scriptPath = Join-Path $repoRoot ('projekt/'+$journal+'.py')
        $logPath = Join-Path $PSScriptRoot ('final_'+$journal+'.stdout.txt')
        & $launcher $scriptPath *> $logPath
        $runExit = $LASTEXITCODE
        $added = @(Get-ChildItem -LiteralPath $cadRoot -Directory | Where-Object { $_.FullName -notin $before } | ForEach-Object FullName)
        $matrix += [ordered]@{journal=$journal;date=$start.ToString('o');
            command=@($launcher,$scriptPath);cwd=$repoRoot;source_base='e87f522';
            source_snapshot='native_source_hashes.json';environment='NX2406 Python3.10.15 Windows';
            seconds=[math]::Round(((Get-Date)-$start).TotalSeconds,2);exitcode=$runExit;
            raw_log=$logPath;output_directories=$added;verify_target=$env:SX35Z_VERIFY_RUN}
        $matrix | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $PSScriptRoot 'native_matrix.json')
        Write-Output ($journal+' exit='+$runExit)
        if ($runExit -ne 0) { Get-Content -LiteralPath $logPath -Tail 25; throw ('Journal failed: '+$journal) }
        if ($journal -eq 'NX_CNC_Gesamtansicht') {
            if ($added.Count -ne 1) { throw 'Full output directory ambiguous' }
            $fullRun = $added[0]
            $fullRun | Set-Content (Join-Path $PSScriptRoot 'lieferlauf.txt')
        }
    }
} finally { $env:SX35Z_VERIFY_RUN = $originalVerify }
