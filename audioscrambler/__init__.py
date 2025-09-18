__package__ = "audioscrambler"
__version__ = "0.1.0"

from .Scrambler import Scrambler

import os
from local_ffmpeg import is_installed, install

# Check if FFmpeg is already installed
if not is_installed():
    # Install FFmpeg if not found
    success, message = install()
    if success:
        print(message)  # FFmpeg installed successfully
    else:
        print(f"Error: {message}")

if is_installed():
    # Add FFmpeg to PATH
    os.environ["PATH"] += os.pathsep + os.path.abspath('ffmpeg')