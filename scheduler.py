"""
Automated Audio Pipeline Scheduler

This script runs three operations sequentially every minute:
1. update_config_date.py - Updates the output filename with the current date
2. download-from-gdrive.py - Downloads audio files from Google Drive
3. local_whisper.py - Transcribes the downloaded audio files

Author: [Your Name]
Date: [Current Date]
"""

import subprocess
import time
import logging
import os
import sys
import traceback
from datetime import datetime
from update_config_date import update_output_filename

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
INTERVAL = 90

def run_pipeline():
    """Run the complete pipeline: update config date, download files, transcribe audio"""
    logging.info("Starting pipeline execution")
    
    # Step 1: Update config file with current date
    logging.info("Step 1: Updating config file date")
    if not update_output_filename():
        logging.error("Failed to update config date. Continuing with pipeline anyway.")
    
    # Step 2: Download files from Google Drive
    logging.info("Step 2: Downloading files from Google Drive")
    try:
        download_process = subprocess.run(
            [PYTHON_EXECUTABLE, DOWNLOAD_SCRIPT_PATH],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info(f"Download script output: {download_process.stdout}")
        if download_process.stderr:
            logging.warning(f"Download script errors: {download_process.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Download script failed with exit code {e.returncode}")
        logging.error(f"Error output: {e.stderr}")
        # Continue to transcription anyway - there might be previously downloaded files
    
    # Step 3: Transcribe downloaded audio files
    logging.info("Step 3: Transcribing audio files")
    try:
        whisper_process = subprocess.run(
            [PYTHON_EXECUTABLE, WHISPER_SCRIPT_PATH],
            check=True,
            capture_output=True,
            text=True
        )
        logging.info(f"Transcription script output: {whisper_process.stdout}")
        if whisper_process.stderr:
            logging.warning(f"Transcription script errors: {whisper_process.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Transcription script failed with exit code {e.returncode}")
        logging.error(f"Error output: {e.stderr}")
    
    logging.info("Pipeline execution completed")

def main():
    """Main function to run the scheduler"""
    logging.info("Audio Pipeline Scheduler started")
    
    try:
        while True:
            # Log start time for this cycle
            cycle_start = datetime.now()
            logging.info(f"Starting pipeline cycle at {cycle_start.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Run the pipeline
            run_pipeline()
            
            # Calculate time for next cycle
            elapsed = (datetime.now() - cycle_start).total_seconds()
            sleep_time = max(1, INTERVAL - elapsed)  # Ensure at least 1 second sleep
            
            logging.info(f"Cycle completed in {elapsed:.2f} seconds. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main() 