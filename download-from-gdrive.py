import os
import io
import pickle
import sys
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Set stdout to use utf-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# If modifying these scopes, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/drive']  # Changed to full access for deletion
CREDENTIALS_FILE = 'credentials.json'
FOLDER_NAME = 'a-daily-log'  # Your Google Drive folder name

def check_credentials_file():
    """Check if credentials.json exists and provide help if not."""
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERROR: '{CREDENTIALS_FILE}' file not found!")
        print("\nTo create your credentials file:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project or select an existing one")
        print("3. Enable the Google Drive API:")
        print("   - Navigate to 'APIs & Services' > 'Library'")
        print("   - Search for 'Google Drive API' and enable it")
        print("4. Create OAuth credentials:")
        print("   - Go to 'APIs & Services' > 'Credentials'")
        print("   - Click 'Create Credentials' > 'OAuth client ID'")
        print("   - Select 'Desktop app' as application type")
        print("   - Download the JSON file and rename it to 'credentials.json'")
        print("   - Place it in the same directory as this script")
        print("\nThen run this script again.")
        return False
    return True

def authenticate_google_drive():
    """Authenticate with Google Drive API using OAuth."""
    creds = None
    
    # The token.pickle file stores the user's access and refresh tokens
    # It is created automatically when the authorization flow completes for the first time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If no valid credentials are available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not check_credentials_file():
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return creds

def find_folder_by_name(service, folder_name):
    """Find a folder by name in Google Drive."""
    # Search for folders with the given name
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        return None
    else:
        # Return the first matching folder
        return items[0]

def find_file_by_name_in_folder(service, file_name, folder_id):
    """Find a file by name in a specific Google Drive folder."""
    # Search for files with the given name in the specified folder
    query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name, mimeType)'
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        return None
    else:
        # Return the first matching file
        return items[0]

def list_files_in_folder(service, folder_id):
    """List all files in a specific Google Drive folder."""
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name, mimeType)'
    ).execute()
    
    return results.get('files', [])

def download_file(service, file_id, file_name):
    """Download a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    
    # Create a BytesIO stream to store the downloaded file
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    
    # Download the file
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download progress: {int(status.progress() * 100)}%")
    
    # Save the file
    file_stream.seek(0)
    with open(file_name, 'wb') as f:
        f.write(file_stream.read())
    
    print(f"File '{file_name}' downloaded successfully!")

def delete_file(service, file_id, file_name):
    """Delete a file from Google Drive."""
    try:
        service.files().delete(fileId=file_id).execute()
        print(f"File '{file_name}' deleted successfully from Google Drive.")
        return True
    except Exception as e:
        print(f"Error deleting file '{file_name}': {str(e)}")
        return False

def download_all_files(service, files):
    """Download all files from the list."""
    print(f"\nDownloading all {len(files)} files from folder...")
    
    # Create a downloads directory if it doesn't exist
    download_dir = 'downloads'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory: {download_dir}")
    
    # Keep track of successfully downloaded files
    downloaded_files = []
    
    # Download each file
    for i, file in enumerate(files, 1):
        file_name = file['name']
        file_id = file['id']
        
        # Skip Google Docs, Sheets, etc. that need export
        mime_type = file.get('mimeType', '')
        if 'google-apps' in mime_type and mime_type != 'application/vnd.google-apps.folder':
            print(f"Skipping Google Workspace file: {file_name} (requires export)")
            continue
        
        # Create path for downloaded file
        file_path = os.path.join(download_dir, file_name)
        
        print(f"\nDownloading file {i}/{len(files)}: {file_name}")
        try:
            # Download the file
            request = service.files().get_media(fileId=file_id)
            
            # Create a BytesIO stream to store the downloaded file
            file_stream = io.BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)
            
            # Download the file
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download progress: {int(status.progress() * 100)}%")
            
            # Save the file
            file_stream.seek(0)
            with open(file_path, 'wb') as f:
                f.write(file_stream.read())
            
            print(f"File '{file_name}' downloaded successfully!")
            downloaded_files.append(file)
        except Exception as e:
            print(f"Error downloading '{file_name}': {str(e)}")
    
    print(f"\nDownload complete! All files saved to the '{download_dir}' directory.")
    return downloaded_files

def delete_files_without_confirmation(service, downloaded_files):
    """Delete files from Google Drive without asking for confirmation."""
    if not downloaded_files:
        print("No files were successfully downloaded, so none will be deleted.")
        return
    
    print("\nAutomatically deleting files from Google Drive...")
    deleted_count = 0
    
    for file in downloaded_files:
        file_name = file['name']
        file_id = file['id']
        
        if delete_file(service, file_id, file_name):
            deleted_count += 1
    
    print(f"\nDeletion complete! {deleted_count} out of {len(downloaded_files)} files were deleted from Google Drive.")

def main():
    print(f"Authenticating with Google Drive...")
    
    try:
        creds = authenticate_google_drive()
        service = build('drive', 'v3', credentials=creds)
        
        # Find the 'a-daily-log' folder
        print(f"Searching for folder: {FOLDER_NAME}")
        folder = find_folder_by_name(service, FOLDER_NAME)
        
        if not folder:
            print(f"Folder '{FOLDER_NAME}' not found in your Google Drive.")
            return
            
        print(f"Folder found! ID: {folder['id']}")
        
        # List all files in the folder
        print(f"Listing files in '{FOLDER_NAME}' folder:")
        files = list_files_in_folder(service, folder['id'])
        
        if not files:
            print(f"No files found in '{FOLDER_NAME}' folder.")
            return
            
        print("\nFiles in folder:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file['name']} ({file.get('mimeType', 'unknown type')})")
        
        # Download all files and get list of successfully downloaded files
        downloaded_files = download_all_files(service, files)
        
        # Automatically delete the downloaded files without asking
        delete_files_without_confirmation(service, downloaded_files)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure you have:")
        print("1. Installed all required packages (pip install -r requirements.txt)")
        print("2. Set up proper Google Drive API credentials")
        print("3. Enabled the Google Drive API in your Google Cloud project")

if __name__ == '__main__':
    main()
