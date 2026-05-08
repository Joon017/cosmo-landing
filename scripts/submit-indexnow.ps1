param(
  [string]$SiteRoot = "https://getcosmoapp.com",
  [string]$Key = "947b59ae-0baf-4b2b-a6fe-3b3621828c4d",
  [string]$Endpoint = "https://api.indexnow.org/indexnow",
  [int]$BatchSize = 100,
  [switch]$IncludeVerificationFiles,
  [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$siteRoot = $SiteRoot.TrimEnd("/")
$hostName = ([Uri]$siteRoot).Host
$keyFilePath = Join-Path $repoRoot "$Key.txt"

if (-not (Test-Path -LiteralPath $keyFilePath)) {
  throw "Missing IndexNow key file at $keyFilePath"
}

function Get-RelativeRepoPath {
  param(
    [Parameter(Mandatory = $true)]
    [string]$FullPath
  )

  return $FullPath.Substring($repoRoot.Length).TrimStart("\", "/")
}

function Convert-ToPublicUrl {
  param(
    [Parameter(Mandatory = $true)]
    [string]$RelativePath
  )

  $normalized = $RelativePath.Replace("\", "/")

  if ($normalized -eq "index.html") {
    return "$siteRoot/"
  }

  if ($normalized -match "/index\.html$") {
    return "$siteRoot/" + $normalized.Substring(0, $normalized.Length - "index.html".Length)
  }

  return "$siteRoot/$normalized"
}

$htmlFiles = Get-ChildItem -Path $repoRoot -Recurse -File -Filter *.html |
  Where-Object {
    $relative = (Get-RelativeRepoPath -FullPath $_.FullName).Replace("\", "/")
    $fileName = [IO.Path]::GetFileName($relative)
    $relative -notlike ".git/*" -and
    $relative -ne "index_deprecated.html" -and
    $fileName -notmatch '^google[a-z0-9]+\.html$'
  } |
  ForEach-Object {
    Get-RelativeRepoPath -FullPath $_.FullName
  }

$urlSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)

foreach ($relativePath in $htmlFiles) {
  [void]$urlSet.Add((Convert-ToPublicUrl -RelativePath $relativePath))
}

if ($IncludeVerificationFiles) {
  $verificationFiles = Get-ChildItem -Path $repoRoot -File |
    Where-Object { $_.Name -match '^[A-Za-z0-9-]+\.txt$|^google[a-z0-9]+\.html$' } |
    ForEach-Object {
      Get-RelativeRepoPath -FullPath $_.FullName
    }

  foreach ($relativePath in $verificationFiles) {
    [void]$urlSet.Add((Convert-ToPublicUrl -RelativePath $relativePath))
  }
}

$urls = @($urlSet) | Sort-Object

if ($urls.Count -eq 0) {
  throw "No URLs found to submit."
}

Write-Host "Prepared $($urls.Count) URLs for IndexNow submission."
Write-Host "Host: $hostName"
Write-Host "Endpoint: $Endpoint"

if ($DryRun) {
  $urls | ForEach-Object { Write-Host $_ }
  exit 0
}

for ($i = 0; $i -lt $urls.Count; $i += $BatchSize) {
  $lastIndex = [Math]::Min($i + $BatchSize - 1, $urls.Count - 1)
  $batch = $urls[$i..$lastIndex]
  $payload = @{
    host = $hostName
    key = $Key
    urlList = $batch
  } | ConvertTo-Json -Depth 4

  try {
    $response = Invoke-WebRequest -Method Post -Uri $Endpoint -ContentType "application/json; charset=utf-8" -Body $payload
    Write-Host "Submitted $($batch.Count) URLs. HTTP $($response.StatusCode)"
  }
  catch {
    if ($_.Exception.Response) {
      $statusCode = [int]$_.Exception.Response.StatusCode
      throw "IndexNow submission failed with HTTP $statusCode"
    }

    throw
  }
}
