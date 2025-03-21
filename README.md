# Audita - Segment Annotation Tool

This repository provides a graphical user interface (GUI) for quickly annotating audio segments from a CSV file. It allows users to review spectrograms and sounds associated with species observations, record responses, and navigate through the dataset.

## Features

- **Image and Sound Display**: Displays an image and plays a sound associated with each observation.
- **Keyboard Shortcuts**: Navigate and annotate quickly using keyboard keys.
- **CSV Integration**: Reads data from a CSV file and updates it with user responses in real-time.

## Requirements

- Python 3.10, 3.11, 3.12
- Only requires native Python libraries (no need to install packages)
    - `tkinter`
    - `csv`
    - `os`
    - `threading`
    - `sys`
    - `subprocess`

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
