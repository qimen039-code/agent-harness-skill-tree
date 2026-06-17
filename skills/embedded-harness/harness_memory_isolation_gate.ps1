param(
  [string]$ProjectLane = "PROJECTLESS",
  [string]$RequestedPath = "",
  [switch]$CrossReferenceAllow,
  [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"
$policy = Get-Content -LiteralPath (Join-Path $PSScriptRoot "embedded_harness_policy.json") -Raw | ConvertFrom-Json

$allowedRoots = @()
if ($policy.memory_roots.PSObject.Properties.Name -contains $ProjectLane) {
  $allowedRoots = @($policy.memory_roots.$ProjectLane)
}

$status = "pass"
$reason = "no requested path"
$resolvedRequested = $null

if ($RequestedPath) {
  try {
    $resolvedRequested = (Resolve-Path -LiteralPath $RequestedPath -ErrorAction Stop).Path
  } catch {
    $resolvedRequested = [System.IO.Path]::GetFullPath($RequestedPath)
  }

  $inside = $false
  foreach ($root in $allowedRoots) {
    $rootFull = [System.IO.Path]::GetFullPath($root)
    if ($resolvedRequested.ToLowerInvariant().StartsWith($rootFull.ToLowerInvariant())) {
      $inside = $true
      break
    }
  }

  if ($inside) {
    $reason = "requested path is inside active project memory roots"
  } elseif ($CrossReferenceAllow) {
    $status = "cross_reference_allowed"
    $reason = "requested path is outside active lane but explicit cross-reference allow was provided"
  } else {
    $status = "blocked"
    $reason = "requested path is outside active project memory roots"
  }
}

$result = [ordered]@{
  ts = (Get-Date).ToString("o")
  phase = "memory_isolation_gate"
  status = $status
  project_lane = $ProjectLane
  allowed_roots = $allowedRoots
  requested_path = $RequestedPath
  resolved_requested_path = $resolvedRequested
  reason = $reason
}

$json = $result | ConvertTo-Json -Depth 20
if ($OutputPath) {
  $dir = Split-Path -Parent $OutputPath
  if ($dir) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  Set-Content -LiteralPath $OutputPath -Value $json -Encoding UTF8
}
$json
if ($status -eq "blocked") { exit 2 }


