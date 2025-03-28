""" 
This script is used to revise the annotations of the segments. It displays the image and plays the sound of the segment.
The user can listen to the sound and classify it as TRUE or FALSE. The user can also navigate through the segments using the arrow keys.
The user can clear all responses and start over. The user can also replay the sound using the <space> key.
Inputs:
    - segments_revised.csv: CSV file with the segments data and annotations.
    - segments folder: Folder containing the segment sounds and spectrograms.
Outputs:
    - segments_revised.csv: Updated CSV file with the user responses.
Usage:
    python revise_segments.py
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
import os
import threading
from tkinter import messagebox
import subprocess
import sys

# CSV file to store responses
csv_filename = os.path.normpath("../output/segments_revised.csv")  # Normalize path for cross-platform compatibility

# Function to play sound
def playsound(file_path):
    """
    Plays an audio file using the system's default sound player.

    This function detects the operating system and executes the appropriate command 
    to play the given audio file.

    Parameters
    ----------
    file_path : str
        Path to the audio file to be played.

    Raises
    ------
    FileNotFoundError
        If the specified audio file does not exist.
    subprocess.CalledProcessError
        If the system command fails to execute properly.

    Notes
    -----
    - On Windows, it uses PowerShell with `Media.SoundPlayer`.
    - On macOS, it uses the `afplay` command.
    - On Linux, it uses the `aplay` command.

    Examples
    --------
    Play a `.wav` file:

    >>> playsound("example.wav")
    """
    if sys.platform == "win32":
        subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{file_path}').PlaySync()"])
    elif sys.platform == "darwin":  # macOS
        subprocess.run(["afplay", file_path])
    else:  # Linux
        subprocess.run(["aplay", file_path])

# Function to load data from CSV
def load_data_from_csv():
    data = []
    if not os.path.exists(csv_filename):
        return data  # Return empty list if file does not exist

    with open(csv_filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'observationID' in row and 'scientificName' in row and 'segmentsFilePath' in row:
                sound = os.path.normpath(row['segmentsFilePath'])  # Normalize path
                image = os.path.normpath(os.path.splitext(sound)[0] + '.png')  # Normalize path
                species = row['scientificName']
                data.append({
                    "observationID": row['observationID'],
                    "classificationProbability": row['classificationProbability'],
                    "segmentsFilePath": sound,
                    "scientificName": species,
                    "userResponse": row['userResponse'],
                    "image": image,
                    "sound": sound,
                    "species": species
                })
    return data

# Load data from CSV
data = load_data_from_csv()

# Function to load existing annotations and find the first blank entry
def load_existing_annotations():
    if not os.path.exists(csv_filename):
        return {}  # No previous data
    
    annotations = {}
    with open(csv_filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            annotations[row['segmentsFilePath']] = row['userResponse']
    return annotations

# Function to initialize the CSV file if not present
def initialize_csv():
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["observationID", "classificationProbability", "segmentsFilePath", "scientificName", "userResponse"])
            writer.writeheader()

# Function to find the first unannotated sample index
def find_first_unannotated():
    for index, item in enumerate(data):
        if item["userResponse"] == "":
            return index
    return len(data)  # If everything is annotated, return end index

# Function to play sound in a separate thread
def play_sound():
    global current_index
    sound_file = os.path.normpath(data[current_index]["sound"])  # Normalize path
    threading.Thread(target=playsound, args=(sound_file,), daemon=True).start()

# Function to record response and move to the next sample
def record_response(response):
    global current_index
    data[current_index]["userResponse"] = response  # Save in data list

    # Update CSV file
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["observationID", "classificationProbability", "segmentsFilePath", "scientificName", "userResponse"])
        writer.writeheader()
        for item in data:
            writer.writerow({
                "observationID": item["observationID"],
                "classificationProbability": item["classificationProbability"],
                "segmentsFilePath": item["segmentsFilePath"],
                "scientificName": item["scientificName"],
                "userResponse": item["userResponse"]
            })

    # Move to next unannotated sample
    next_sample()

# Function to skip a sample without recording a response
def skip_sample():
    next_sample()

# Function to load the next unannotated sample
def next_sample():
    global current_index
    current_index += 1
    while current_index < len(data) and data[current_index]["userResponse"] != "":
        current_index += 1  # Skip annotated samples

    if current_index < len(data):
        update_image()
    else:
        root.quit()  # Exit when finished

# Function to navigate to the previous sample
def previous_sample():
    global current_index
    if current_index > 0:
        current_index -= 1
        update_image()

# Function to navigate to the next sample without recording a response
def next_sample_no_record():
    global current_index
    if current_index < len(data) - 1:
        current_index += 1
        update_image()

# Function to update the progress label
def update_progress_label():
    progress_label.config(text=f"{current_index + 1}/{len(data)}")

# Function to update the displayed image and text field
def update_image():
    global current_index
    try:
        img_path = os.path.normpath(data[current_index]["image"])  # Normalize path
        img = Image.open(img_path)
        img = img.resize((600, 500))
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep reference
        species_label.config(text=data[current_index]['species'].replace('_', ' '))  # Update species label
        actual_value_var.set(data[current_index]["userResponse"])  # Update text field with current value
        update_progress_label()  # Update progress label
        play_sound()  # Play sound automatically
    except Exception as e:
        print(f"Error loading image: {e}")
        skip_sample()  # Skip to the next sample if image loading fails

# Function to update the actual value from the text field
def update_actual_value(*args):
    global current_index
    data[current_index]["userResponse"] = actual_value_var.get()
    # Update CSV file immediately when text field changes
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["observationID", "classificationProbability", "segmentsFilePath", "scientificName", "userResponse"])
        writer.writeheader()
        for item in data:
            writer.writerow({
                "observationID": item["observationID"],
                "classificationProbability": item["classificationProbability"],
                "segmentsFilePath": item["segmentsFilePath"],
                "scientificName": item["scientificName"],
                "userResponse": item["userResponse"]
            })

# Function to clear all user responses
def clear_all_responses():
    global data, current_index
    if messagebox.askyesno("Confirmation", "Are you sure you want to clear all responses?"):
        for item in data:
            item["userResponse"] = ""
        # Update CSV file
        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["observationID", "classificationProbability", "segmentsFilePath", "scientificName", "userResponse"])
            writer.writeheader()
            for item in data:
                writer.writerow({
                    "observationID": item["observationID"],
                    "classificationProbability": item["classificationProbability"],
                    "segmentsFilePath": item["segmentsFilePath"],
                    "scientificName": item["scientificName"],
                    "userResponse": item["userResponse"]
                })
        current_index = find_first_unannotated()
        update_image()

# Function to handle key presses
def on_key_press(event):
    if event.keysym == "Right":  # Right arrow key → TRUE
        record_response("TRUE")
    elif event.keysym == "Left":  # Left arrow key → FALSE
        record_response("FALSE")
    elif event.keysym == "r":  # 'R' key → Replay sound
        play_sound()
    elif event.keysym == "Up":  # Up arrow key → Previous sample
        previous_sample()
    elif event.keysym == "Down":  # Down arrow key → Next sample
        next_sample_no_record()
    elif event.keysym == "Return":  # Enter key → Next sample
        next_sample_no_record()

# Initialize window
root = tk.Tk()
root.title("Auditivo")
root.geometry("600x800")  # Increase width to accommodate longer progress bar

# Color options
bg_color = "#2e2e2e"  # Dark background
fg_color = "#D3D3D3"  # Light text
button_bg_color = "#4d4d4d"  # Button background
button_fg_color = "#D3D3D3"  # Button text
button_active_bg_color = "#666666"  # Button active background
progress_label_fg_color = "#808080"  # Progress label text

root.configure(bg=bg_color)

# Load annotations and find first unannotated sample
initialize_csv()
annotations = load_existing_annotations()
current_index = find_first_unannotated()

# Image display
image_label = tk.Label(root, bg=bg_color)  # Dark background
image_label.pack(pady=10)

# Species label
species_label = tk.Label(root, text="", bg=bg_color, fg=fg_color, font=("Helvetica", 14, "italic"))  # Dark background, light text, italics
species_label.pack(pady=5)

# Text field for actual value
actual_value_var = tk.StringVar()
actual_value_var.trace_add("write", update_actual_value)
actual_value_entry = tk.Entry(root, textvariable=actual_value_var, font=("Helvetica", 14), width=50, bg=button_bg_color, fg=fg_color)  # Dark background, light text
actual_value_entry.pack(pady=10)

# Buttons frame
buttons_frame = tk.Frame(root, bg=bg_color)  # Dark background
buttons_frame.pack(pady=5)

# Style configuration
style = ttk.Style()
style.theme_use('clam')  # Use a theme that allows custom styling
style.configure("Rounded.TButton", 
                font=("Helvetica", 12), padding=3, background=button_bg_color, foreground=button_fg_color, borderwidth=1, relief="solid", bordercolor=button_bg_color)
style.map("Rounded.TButton", background=[("active", button_active_bg_color)])  # Lighter grey when active

# Buttons
true_button = ttk.Button(buttons_frame, text="TRUE → ", command=lambda: record_response("TRUE"), style="Rounded.TButton")
false_button = ttk.Button(buttons_frame, text="← FALSE", command=lambda: record_response("FALSE"), style="Rounded.TButton")
replay_button = ttk.Button(buttons_frame, text="PLAY ", command=play_sound, style="Rounded.TButton")
prev_button = ttk.Button(buttons_frame, text="BACK ↑", command=previous_sample, style="Rounded.TButton")
next_button = ttk.Button(buttons_frame, text="NEXT ↓", command=next_sample_no_record, style="Rounded.TButton")
clear_all_button = ttk.Button(buttons_frame, text="Clear All", command=clear_all_responses, style="Rounded.TButton")

replay_button.grid(row=1, column=1, padx=5, pady=5)
prev_button.grid(row=0, column=1, padx=5, pady=5)
next_button.grid(row=2, column=1, padx=5, pady=5)
false_button.grid(row=1, column=0, padx=5, pady=5)
true_button.grid(row=1, column=2, padx=5, pady=5)
clear_all_button.grid(row=3, column=1, padx=5, pady=5)

# Progress label
progress_label = tk.Label(root, text="", bg=bg_color, fg=progress_label_fg_color, font=("Helvetica", 10))
progress_label.pack(pady=10, padx=100, fill='x')  # Align to the right

# Bind keys for quick actions
root.bind("<Left>", on_key_press)   # FALSE
root.bind("<Right>", on_key_press)  # TRUE
root.bind("<space>", on_key_press)  # Play Sound
root.bind("<Up>", on_key_press)     # Previous Sample
root.bind("<Down>", on_key_press)   # Next Sample
root.bind("<Return>", on_key_press) # Enter key → Next Sample

# Load first image and sound
if current_index < len(data):
    update_image()
else:
    print("All samples are annotated. Exiting.")
    root.quit()

# Run the GUI loop
root.mainloop()