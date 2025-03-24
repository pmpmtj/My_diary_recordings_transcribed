"""
Config Date Updater

This script updates the output_file in config.json to reflect the current date in YYMMDD format.
It can be called independently or imported as a function for use in the scheduler.
"""

import json
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('config_updater.log'),
        logging.StreamHandler()
    ]
)

def update_output_filename():
    """
    Updates the output_file field in config.json to use current date in YYMMDD format.
    Returns True if successful, False otherwise.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    
    try:
        # Get current date in YYMMDD format
        current_date = datetime.now().strftime("%y%m%d")
        new_filename = f"{current_date}_daily.txt"
        
        # Read existing config
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        
        # Check if the filename already matches current date
        if config.get('output_file') == new_filename:
            logging.info(f"Config already using current date format: {new_filename}")
            return True
            
        # Update the output_file value
        old_filename = config.get('output_file', '')
        config['output_file'] = new_filename
        
        # Write updated config back to file
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=2)
            
        logging.info(f"Updated output_file in config from '{old_filename}' to '{new_filename}'")
        return True
        
    except Exception as e:
        logging.error(f"Failed to update config.json: {str(e)}")
        return False

# If run directly, update the config file
if __name__ == "__main__":
    result = update_output_filename()
    if result:
        print("Successfully updated config.json with current date.")
    else:
        print("Failed to update config.json. Check the logs for details.") 