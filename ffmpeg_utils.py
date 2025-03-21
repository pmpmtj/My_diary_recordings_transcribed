import os
import sys

def setup_ffmpeg_path():
    """Set up FFmpeg path for bundled executable"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = os.path.dirname(sys.executable)
        ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')
        
        # Add FFmpeg to PATH environment variable
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + base_path
        
        print(f"Using bundled FFmpeg at: {ffmpeg_path}")
        return ffmpeg_path
    else:
        # Running as script, assume FFmpeg is in PATH
        print("Using system FFmpeg")
        return 'ffmpeg' 