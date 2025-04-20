#!/bin/bash

# Get the installed version of Chrome
chrome_version=$(google-chrome-stable --version | sed 's/Google Chrome //')

# Echo the version
echo "Using fixed Chrome version: $chrome_version"

# Construct the download URL
chromedriver_url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${chrome_version}/linux64/chromedriver-linux64.zip"

# Download ChromeDriver
echo "Downloading ChromeDriver from: $chromedriver_url"
wget -q "$chromedriver_url" -O /tmp/chromedriver_linux64.zip

# Check if download was successful
if [ ! -f /tmp/chromedriver_linux64.zip ]; then
  echo "Failed to download ChromeDriver"
  exit 1
fi

# Unzip and move to path
unzip /tmp/chromedriver_linux64.zip -d /tmp/chromedriver_extracted
mv /tmp/chromedriver_extracted/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver

# Cleanup
rm -rf /tmp/chromedriver_linux64.zip /tmp/chromedriver_extracted
