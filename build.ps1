param([string]$TectonicPath = '')
$ErrorActionPreference = 'Stop'
$previousFontConfig = $env:FONTCONFIG_FILE
Push-Location -LiteralPath $PSScriptRoot
try {
    $tectonicCompiler = if ($TectonicPath) { $TectonicPath } else {
        (Get-Command tectonic -ErrorAction SilentlyContinue).Source
    }
    if ($tectonicCompiler) {
        # Portable Tectonic on Windows needs a fontconfig search path.
        if (-not $env:FONTCONFIG_FILE -and $env:WINDIR) {
            $taskBuildDir = Join-Path $PSScriptRoot '.build'
            $taskFontCache = Join-Path $taskBuildDir 'font-cache'
            New-Item -ItemType Directory -Path $taskFontCache -Force | Out-Null
            $taskFontDir = [System.Security.SecurityElement]::Escape((Join-Path $env:WINDIR 'Fonts').Replace('\', '/'))
            $taskCacheDir = [System.Security.SecurityElement]::Escape($taskFontCache.Replace('\', '/'))
            $taskFontConfig = Join-Path $taskBuildDir 'fontconfig.conf'
            $taskFontXml = "<?xml version=`"1.0`"?><!DOCTYPE fontconfig SYSTEM `"fonts.dtd`"><fontconfig><dir>$taskFontDir</dir><cachedir>$taskCacheDir</cachedir></fontconfig>"
            [System.IO.File]::WriteAllText($taskFontConfig, $taskFontXml, [System.Text.UTF8Encoding]::new($false))
            $env:FONTCONFIG_FILE = $taskFontConfig
        }
        & $tectonicCompiler --keep-logs --keep-intermediates main.tex
        if ($LASTEXITCODE -ne 0) { throw 'Tectonic compilation failed.' }
    } else {
        $xetexCompiler = Get-Command xelatex -ErrorAction SilentlyContinue
        $bibCompiler = Get-Command bibtex -ErrorAction SilentlyContinue
        if (-not $xetexCompiler -or -not $bibCompiler) {
            throw 'Install Tectonic, or XeLaTeX and BibTeX. See COMPILE.md.'
        }
        & $xetexCompiler.Source -interaction=nonstopmode -halt-on-error main.tex
        if ($LASTEXITCODE -ne 0) { throw 'First XeLaTeX pass failed.' }
        & $bibCompiler.Source main
        if ($LASTEXITCODE -ne 0) { throw 'BibTeX failed.' }
        foreach ($pass in 1..2) {
            & $xetexCompiler.Source -interaction=nonstopmode -halt-on-error main.tex
            if ($LASTEXITCODE -ne 0) { throw "XeLaTeX pass $pass failed." }
        }
    }
    Copy-Item -LiteralPath 'main.pdf' -Destination 'Nguyen_Phuong_Nam_Thesis_RCFree_Revised.pdf' -Force
    Write-Output 'PDF created: Nguyen_Phuong_Nam_Thesis_RCFree_Revised.pdf'
} finally {
    $env:FONTCONFIG_FILE = $previousFontConfig
    Pop-Location
}
