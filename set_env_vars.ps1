# PowerShell script to set environment variables
Write-Host "Setting environment variables..."

# Set JAVA_HOME (typical installation path for Amazon Corretto)
$javaHome = "C:\Program Files\Amazon Corretto\jdk17.0.12_7"
if (Test-Path $javaHome) {
    [Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome, "User")
    Write-Host "JAVA_HOME set to: $javaHome"
} else {
    # Try to find Java installation
    $javaPaths = @(
        "C:\Program Files\Amazon Corretto\*",
        "C:\Program Files\Java\*",
        "C:\Program Files (x86)\Java\*"
    )
    
    $foundJava = $false
    foreach ($path in $javaPaths) {
        $dirs = Get-ChildItem -Path $path -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match "jdk" }
        if ($dirs) {
            $javaHome = $dirs[0].FullName
            [Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome, "User")
            Write-Host "JAVA_HOME set to: $javaHome"
            $foundJava = $true
            break
        }
    }
    
    if (-not $foundJava) {
        Write-Host "WARNING: Java installation not found. JAVA_HOME not set."
    }
}

# Set ANDROID_HOME (typical installation path for Android SDK)
$androidHome = "C:\Users\czp\AppData\Local\Android\Sdk"
[Environment]::SetEnvironmentVariable("ANDROID_HOME", $androidHome, "User")
Write-Host "ANDROID_HOME set to: $androidHome"

# Update PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$pathsToAdd = @()

if ($javaHome -and (Test-Path $javaHome)) {
    $javaBin = Join-Path $javaHome "bin"
    $pathsToAdd += $javaBin
}

if (Test-Path $androidHome) {
    $androidPlatformTools = Join-Path $androidHome "platform-tools"
    $androidTools = Join-Path $androidHome "tools"
    $androidToolsBin = Join-Path $androidHome "tools\bin"
    $pathsToAdd += $androidPlatformTools, $androidTools, $androidToolsBin
}

# Add new paths to PATH if they're not already there
foreach ($path in $pathsToAdd) {
    if ($path -and (Test-Path $path) -and ($currentPath -notlike "*$path*")) {
        $currentPath = "$path;$currentPath"
    }
}

[Environment]::SetEnvironmentVariable("PATH", $currentPath, "User")
Write-Host "PATH updated with Java and Android paths"

# Display current environment variables
Write-Host "`nCurrent environment variables:"
Write-Host "JAVA_HOME: $([Environment]::GetEnvironmentVariable('JAVA_HOME', 'User'))"
Write-Host "ANDROID_HOME: $([Environment]::GetEnvironmentVariable('ANDROID_HOME', 'User'))"