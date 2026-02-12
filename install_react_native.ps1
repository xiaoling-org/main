# PowerShell script to install React Native CLI
Write-Host "Installing React Native CLI..."

# Check if Node.js is installed
$nodeVersion = node --version 2>$null
if ($nodeVersion) {
    Write-Host "Node.js version: $nodeVersion"
} else {
    Write-Host "Node.js is not installed. Please install Node.js first."
    Write-Host "You can download it from: https://nodejs.org/"
    exit 1
}

# Check if npm is available
$npmVersion = npm --version 2>$null
if ($npmVersion) {
    Write-Host "npm version: $npmVersion"
} else {
    Write-Host "npm is not available. Please check Node.js installation."
    exit 1
}

# Install React Native CLI globally
Write-Host "Installing React Native CLI globally..."
npm install -g react-native-cli

if ($LASTEXITCODE -eq 0) {
    Write-Host "React Native CLI installed successfully!"
    
    # Verify installation
    $rnVersion = react-native --version 2>$null
    if ($rnVersion) {
        Write-Host "React Native CLI version: $rnVersion"
    } else {
        Write-Host "React Native CLI installed but version check failed."
    }
} else {
    Write-Host "Failed to install React Native CLI. Exit code: $LASTEXITCODE"
}

# Also install Expo CLI (optional but recommended)
Write-Host "`nInstalling Expo CLI (optional)..."
npm install -g expo-cli

if ($LASTEXITCODE -eq 0) {
    Write-Host "Expo CLI installed successfully!"
    
    # Verify installation
    $expoVersion = expo --version 2>$null
    if ($expoVersion) {
        Write-Host "Expo CLI version: $expoVersion"
    }
}

Write-Host "`nInstallation complete!"