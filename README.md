# Google Drive File Downloader

This script allows you to download a specific file from your Google Drive. It is currently configured to download a file named "Estrada da Rocha.m4a".

## Prerequisites

1. Python 3.6 or higher
2. Google Drive API enabled in the Google Cloud Console
3. OAuth credentials (credentials.json file)

## Step-by-Step Setup Instructions

### 1. Install the required packages

```
pip install -r requirements.txt
```

### 2. Set up Google Drive API and OAuth credentials

1. **Go to Google Cloud Console**: 
   - Visit https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a new project**:
   - Click on the project dropdown at the top of the page
   - Click "NEW PROJECT"
   - Enter a name for your project and click "CREATE"
   - Wait for the project to be created and then select it

3. **Enable the Google Drive API**:
   - In the left sidebar, navigate to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click on "Google Drive API" in the results
   - Click "ENABLE"

4. **Create OAuth credentials**:
   - In the left sidebar, navigate to "APIs & Services" > "Credentials"
   - Click "CREATE CREDENTIALS" at the top and select "OAuth client ID"
   - If prompted to configure the consent screen, click "CONFIGURE CONSENT SCREEN"
     - Select "External" (if this is a personal account) and click "CREATE"
     - Fill in the required fields (App name, User support email, Developer contact information)
     - Click "SAVE AND CONTINUE" through the remaining steps and return to the dashboard
   - Back on the "Create OAuth client ID" screen:
     - Select "Desktop app" as the Application type
     - Enter a name for your OAuth client
     - Click "CREATE"
   - Download the JSON file by clicking the download icon (↓)
   - Rename the downloaded file to `credentials.json`
   - Place this file in the same directory as the script

### 3. Run the script

```
python download-from-gdrive.py
```

### 4. First-time authentication

- When you run the script for the first time, a browser window will open
- Select your Google account when prompted
- You may see a warning that the app isn't verified - click "Advanced" and then "Go to {Project Name} (unsafe)"
- Click "Allow" to grant the necessary permissions
- The browser will show "The authentication flow has completed. You may close this window."
- The script will continue running and download your file

## Notes

- After the first successful authentication, a `token.pickle` file will be created for future use
- If you want to change the file to download, edit the `file_name` variable in the `main()` function
- The script will download the file to the current directory with its original name

## Features

- Searches for the file by name in your Google Drive
- Downloads the file to the current directory
- Shows download progress
- Handles authentication using OAuth 2.0 