param([Parameter(Mandatory=$true)][string]$Project,[string]$Version="v1.6.0",[switch]$EnableLearning)
$ErrorActionPreference="Stop"
if(!(Test-Path $Project -PathType Container)){throw "Project directory missing"}
$root=(Resolve-Path $Project).Path
if(Test-Path "$root\.agents"){throw "Existing .agents directory: use the upgrade guide; refusing overwrite"}
if(Test-Path "$root\.opencode\plugins\experience-recorder.js"){throw "Existing recorder plugin: refusing overwrite"}
if(Test-Path "$root\opencode.jsonc"){throw "Existing opencode.jsonc: merge instructions manually"}
if(!(Get-Command python -ErrorAction SilentlyContinue)){throw "Python 3.12+ is required"}
$tmp=Join-Path $env:TEMP ("webdev-"+[guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force $tmp | Out-Null
try {
 $url="https://github.com/ytvee-dev/webdev-agent-kit/releases/download/$Version"
 $file="webdev-agent-kit-codex-$Version.tar.gz"
 Invoke-WebRequest "$url/$file" -OutFile "$tmp\kit.tar.gz"
 Invoke-WebRequest "$url/SHA256SUMS" -OutFile "$tmp\SHA256SUMS"
 $expected=Get-Content "$tmp\SHA256SUMS" | Where-Object {$_ -match ("^[0-9a-fA-F]{64}\s+\*?"+[regex]::Escape($file)+"$")}
 if(@($expected).Count -ne 1){throw "Archive checksum not found"}
 $sha=($expected -split "\s+")[0]
 if((Get-FileHash "$tmp\kit.tar.gz" -Algorithm SHA256).Hash -ne $sha){throw "SHA256 verification failed"}
 New-Item -ItemType Directory -Force "$tmp\stage" | Out-Null
 tar -xzf "$tmp\kit.tar.gz" -C "$tmp\stage"
 if($LASTEXITCODE -ne 0){throw "Archive extraction failed"}
 $src="$tmp\stage\.agents"
 if(!(Test-Path "$src\skills\agent-self-improvement\assets\integrations\opencode\experience-recorder.js")){throw "Recorder absent"}
 $conf="$root\opencode.json"
 if(Test-Path $conf){
  try {$config=Get-Content $conf -Raw | ConvertFrom-Json} catch {throw "Invalid opencode.json; no changes made"}
 } else {$config=[pscustomobject]@{'$schema'='https://opencode.ai/config.json'}}
 $p=$config.PSObject.Properties['instructions']
 if($p -and $p.Value -isnot [array]){throw "instructions must be array"}
 $rules=@()
 if($p){$rules=@($p.Value)}
 if($rules -notcontains ".agents/AGENTS.md"){$rules+= ".agents/AGENTS.md"}
 if($p){$p.Value=@($rules)}else{$config | Add-Member -MemberType NoteProperty -Name instructions -Value @($rules)}
 Copy-Item $src "$root\.agents" -Recurse
 if(Test-Path $conf){Copy-Item $conf "$conf.webdev-backup"}
 ($config | ConvertTo-Json -Depth 100) | Set-Content $conf -Encoding UTF8
 New-Item -ItemType Directory -Force "$root\.opencode\plugins" | Out-Null
 Copy-Item "$root\.agents\skills\agent-self-improvement\assets\integrations\opencode\experience-recorder.js" "$root\.opencode\plugins\experience-recorder.js"
 $learn="$root\.agents\skills\agent-self-improvement\scripts\learning.py"
 if($EnableLearning){python $learn on --project $root;if($LASTEXITCODE -ne 0){throw "Could not enable learning"}}
 Write-Host "WebDev $Version installed for OpenCode. Restart OpenCode. Recording is opt-in."
 Write-Host "Verify: python '$learn' status --project '$root'"
} finally {Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue}
