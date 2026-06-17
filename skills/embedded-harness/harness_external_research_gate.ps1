param(
  [string]$TaskText = "",
  [string]$ClaimText = "",
  [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"
$policy = Get-Content -LiteralPath (Join-Path $PSScriptRoot "embedded_harness_policy.json") -Raw | ConvertFrom-Json
$combined = "$TaskText`n$ClaimText"
$matchedTriggers = @()

foreach ($trigger in $policy.external_research_triggers) {
  if ($combined -match [regex]::Escape($trigger)) {
    $matchedTriggers += $trigger
  }
}

if ($combined -match '\b20\d{2}[-/]\d{1,2}([-/]\d{1,2})?\b') {
  $matchedTriggers += "date_pattern"
}
$versionPattern = '\b(v\d+\.\d+(\.\d+)?|(?:version|release|sdk|node|python|npm|package|plugin|model)\s*:?\s*v?\d+\.\d+(\.\d+)?)\b'
if ($combined -match $versionPattern) {
  $matchedTriggers += "version_pattern"
}
if ($combined -match 'https?://|github\.com') {
  $matchedTriggers += "url_or_github_pattern"
}

$needs = $matchedTriggers.Count -gt 0
$result = [ordered]@{
  ts = (Get-Date).ToString("o")
  phase = "external_research_gate"
  status = "pass"
  needs_external_research = $needs
  matched_triggers = @($matchedTriggers | Select-Object -Unique)
  rule = "deterministic string/date/version/url trigger; no extra LLM judgment"
}

$json = $result | ConvertTo-Json -Depth 20
if ($OutputPath) {
  $dir = Split-Path -Parent $OutputPath
  if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  Set-Content -LiteralPath $OutputPath -Value $json -Encoding UTF8
}
$json
