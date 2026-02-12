# PowerShell script to download Amazon Corretto 17 JDK
$url = "https://corretto.aws/downloads/latest/amazon-corretto-17-x64-windows-jdk.msi"
$output = "C:\Users\czp\Downloads\amazon-corretto-17.msi"

Write-Host "Downloading Amazon Corretto 17 JDK..."
Write-Host "URL: $url"
Write-Host "Output: $output"

try {
    # Create downloads directory if it doesn't exist
    if (!(Test-Path "C:\Users\czp\Downloads")) {
        New-Item -ItemType Directory -Path "C:\Users\czp\Downloads" -Force
    }
    
    # Download the file
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
    Write-Host "Download completed successfully!"
    
    # Verify file exists
    if (Test-Path $output) {
        $fileSize = (Get-Item $output).Length
        Write-Host "File size: $([math]::Round($fileSize/1MB, 2)) MB"
        return $true
    } else {
        Write-Host "File not found after download"
        return $false
    }
} catch {
    Write-Host "Error downloading: $_"
    return $false
}