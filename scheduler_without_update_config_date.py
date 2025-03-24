"""
Automated Audio Pipeline Scheduler

This script runs two operations sequentially every minute:
1. download-from-gdrive.py - Downloads audio files from Google Drive
2. local_whisper.py - Transcribes the downloaded audio files

Author: [Your Name]
Date: [Current Date]
"""

import subprocess
import time
import logging
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_scheduler.log'),
        logging.StreamHandler()
    ]
)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the scripts to run (use absolute paths for reliability)
DOWNLOAD_SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'download-from-gdrive.py')
WHISPER_SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'local_whisper.py')

# Get the path to the Python executable that's running this script
# This ensures we use the same Python environment with all installed packages
PYTHON_EXECUTABLE = sys.executable

# Interval in seconds (60 seconds = 1 minute)
INTERVAL = 60

def run_script(script_path, script_name):
    """Execute a script as a subprocess and log the result."""
    try:
        logging.info(f"Starting {script_name} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run the script using the same Python interpreter that's running this script
        result = subprocess.run([PYTHON_EXECUTABLE, script_path], 
                               capture_output=True, 
                               text=True, 
                               check=False)
        
        if result.returncode == 0:
            logging.info(f"{script_name} executed successfully")
            if result.stdout:
                logging.info(f"Output: {result.stdout.strip()}")
            return True
        else:
            logging.error(f"{script_name} failed with return code {result.returncode}")
            if result.stderr:
                logging.error(f"Error: {result.stderr.strip()}")
            if result.stdout:
                logging.info(f"Output: {result.stdout.strip()}")
            return False
                
    except Exception as e:
        logging.error(f"Failed to run {script_name}: {str(e)}")
        return False

def run_pipeline_cycle():
    """Run the complete pipeline sequence: download files, then transcribe them."""
    # Step 1: Download files from Google Drive
    download_success = run_script(DOWNLOAD_SCRIPT_PATH, "Google Drive download script")
    
    # Step 2: Transcribe audio files (even if download failed, there might be files from previous runs)
    whisper_success = run_script(WHISPER_SCRIPT_PATH, "Whisper transcription script")
    
    return download_success, whisper_success

def main():
    """Main function to run the scheduler."""
    logging.info("Starting Audio Pipeline Scheduler")
    logging.info(f"Will run pipeline every {INTERVAL} seconds")
    logging.info(f"Using Python executable: {PYTHON_EXECUTABLE}")
    logging.info(f"Download script: {DOWNLOAD_SCRIPT_PATH}")
    logging.info(f"Transcription script: {WHISPER_SCRIPT_PATH}")
    
    try:
        while True:
            # Run the full pipeline cycle
            download_success, whisper_success = run_pipeline_cycle()
            
            # Log the cycle summary
            if download_success and whisper_success:
                logging.info("Pipeline cycle completed successfully")
            elif not download_success and not whisper_success:
                logging.warning("Both download and transcription failed in this cycle")
            elif not download_success:
                logging.warning("Download failed but transcription completed in this cycle")
            else:
                logging.warning("Download succeeded but transcription failed in this cycle")
            
            logging.info(f"Waiting {INTERVAL} seconds until next pipeline cycle...")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Scheduler encountered an error: {str(e)}")
        raise

if __name__ == "__main__":
    main() 