# Pink Timer Deluxe

Pink Timer Deluxe is a stylish, PyQt6-based desktop application that combines a countdown timer with music playback. Set a timer for a predefined duration (2, 10, or 15 minutes), and when it finishes, the app plays a random MP3 file from a user-selected folder. The app features a pink-themed UI, making it a delightful tool for time management or reminders with a musical twist.

## Features

- **Countdown Timer**: Choose from preset timers (2, 10, or 15 minutes) with a clear, bold display.
- **Music Playback**: Plays a random MP3 file from a selected folder when the timer completes, using PyQt6's `QMediaPlayer`.
- **User-Friendly Interface**: Pink-themed design with intuitive controls for starting, stopping, and resetting the timer.
- **Music Folder Selection**: Easily select a folder containing MP3 files via a file dialog.
- **Cross-Platform**: Runs on Windows, macOS, and Linux (with appropriate multimedia codecs).

## Screenshots

*Coming soon! Add screenshots of the app in action here.*

## Prerequisites

- **Python**: Version 3.8 or higher.
- **PyQt6**: Required for the GUI and multimedia playback.
- **Multimedia Codecs**: Ensure your system has MP3 playback support (usually included on Windows/macOS; may require `gstreamer1.0-plugins-good` on Linux).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/pink-timer-deluxe.git
   cd pink-timer-deluxe

Create a Virtual Environment (optional but recommended):
bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies:
bash

pip install PyQt6

Verify Multimedia Support:
On Linux, install MP3 codecs if needed:
bash

sudo apt-get install gstreamer1.0-plugins-good

Windows and macOS typically include MP3 support by default.

Usage
Run the Application:
bash

python pink_timer_deluxe.py

Select a Music Folder:
Click the " Select Music Folder" button and choose a folder containing MP3 files.

Set a Timer:
Click one of the preset buttons (2 min, 10 min, or 15 min) to start the countdown.

Timer Completion:
When the timer reaches zero, the app displays " Go! " and plays a random MP3 file from the selected folder.

Stop or Reset:
Click " Stop / Reset" to halt the timer or stop music playback and reset the app.

Close the App:
Close the window to stop any playing music and exit cleanly.

File Structure
pink_timer_deluxe.py: Main application script containing the PyQt6-based timer and music player logic.

README.md: This file, providing project documentation.

Troubleshooting
No Sound:
Ensure the selected folder contains valid MP3 files.

Verify that your system has MP3 codec support (see Prerequisites).

Check system audio settings and volume.

PyQt6 Errors:
Confirm PyQt6 is installed (pip show PyQt6).

Update PyQt6 to the latest version (pip install --upgrade PyQt6).

Linux Codec Issues:
Install additional GStreamer plugins: sudo apt-get install gstreamer1.0-plugins-ugly.

Contributing
Contributions are welcome! To contribute:
Fork the repository.

Create a new branch (git checkout -b feature/your-feature).

Make your changes and commit (git commit -m "Add your feature").

Push to your branch (git push origin feature/your-feature).

Open a Pull Request.

Please ensure your code follows the existing style and includes appropriate comments.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments
Built with PyQt6 for GUI and multimedia functionality.

Inspired by the need for a fun, music-driven timer application.

Contact
For questions or feedback, please open an issue on the GitHub repository or contact [your email or handle].

