# Audita - Species Annotation Tool

This script provides a graphical user interface (GUI) for quickly annotating audio segments from a CSV file. It allows users to review spectrograms and sounds associated with species observations, record responses, and navigate through the dataset.

## Features

- **Image and Sound Display**: Displays an image and plays a sound associated with each observation.
- **Keyboard Shortcuts**: Navigate and annotate quickly using keyboard keys.
- **CSV Integration**: Reads data from a CSV file and updates it with user responses in real-time.

## Requirements

- Python 3.10, 3.11, 3.12
- Required Python libraries:
  - **Native libraries**:
    - `tkinter`
    - `csv`
    - `os`
    - `threading`
  - **Non-native libraries**:
    - `Pillow`
    - `playsound`

## Installation

1. Clone or download this repository.
2. Install the required Python libraries using pip:
   ```bash
   pip install pillow playsound
   ```
3. On MacOSx, install PyObjC to ensure compatibility with `playsound`:
   ```bash
   pip install pyobjc
   ```
## Usage
Set inputs:
  - segments_revised.csv: CSV file with the segments data and annotations.
  - segments folder: Folder containing the segment sounds and spectrograms.

Run:
  ```bash
  python revise_segments.py
  ```

Outputs:
  - segments_revised.csv: Updated CSV file with the user responses.
