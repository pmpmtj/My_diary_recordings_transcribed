# Troubleshooting Guide

## Common Errors and Solutions

### 1. "No such file or directory: 'credentials.json'"

**Problem**: The script cannot find the credentials.json file required for OAuth authentication.

**Solution**:
- Make sure you've created the credentials.json file as described in the README.md
- Ensure the file is named exactly "credentials.json" (check for typos)
- Place the file in the same directory as the script
- Verify that the file path is correct if you're running the script from a different directory

### 2. "The client secrets were invalid"

**Problem**: The credentials.json file format is incorrect or corrupted.

**Solution**:
- Ensure you've downloaded the correct OAuth 2.0 credentials (Desktop app type)
- Try re-downloading the credentials from the Google Cloud Console
- Make sure you haven't modified the JSON file content

### 3. Browser doesn't open for authentication

**Problem**: The script couldn't open a browser for the OAuth flow.

**Solution**:
- Make sure you have a default browser set on your system
- Try running the script with a different browser open
- Check if any firewall or security software is blocking browser access

### 4. "File not found in your Google Drive"

**Problem**: The script couldn't find the specified file in your Google Drive.

**Solution**:
- Check if the file name is exactly correct, including capitalization and file extension
- Make sure the file is in your My Drive (not shared with you)
- Verify that the file isn't in the trash
- If the file has a special character in the name, try modifying the script to handle it

### 5. Import errors (ModuleNotFoundError)

**Problem**: Required Python packages are missing.

**Solution**:
- Make sure you've installed all the required packages:
  ```
  pip install -r requirements.txt
  ```
- If using a virtual environment, ensure it's activated
- Try reinstalling the packages if they appear to be corrupted

### 6. Permission issues during download

**Problem**: The script has permission errors when creating or writing to local files.

**Solution**:
- Make sure you have write permissions in the directory where the script is running
- Try running the script as administrator/with elevated privileges
- Check if antivirus software is blocking file operations

### 7. "Access Not Configured" error

**Problem**: The Google Drive API hasn't been properly enabled for your project.

**Solution**:
- Go to the Google Cloud Console
- Navigate to "APIs & Services" > "Library"
- Search for "Google Drive API" and make sure it's enabled for your project
- If it shows as enabled, try disabling and re-enabling it

### 8. Authentication timeout

**Problem**: The OAuth authentication process timed out.

**Solution**:
- Ensure you have a stable internet connection
- Complete the authentication process more quickly
- Try again with a fresh credentials.json file

## If All Else Fails

1. Delete the token.pickle file (if it exists) and try again
2. Create a new project in Google Cloud Console and set up new credentials
3. Verify your Google account has access to the file you're trying to download
4. Check if Google Drive API has any service disruptions 