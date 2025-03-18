""" 
Structures the segments CSV file to have the required columns for annotation.
Intended to add compatibility with a PAMFLOW. 
Run only once to create the annotation file.
"""
import pandas as pd

# Load the CSV file
df = pd.read_csv('../segments/segments.csv')

# Replace spaces with underscores in the 'scientificName' column
df['scientificName'] = df['scientificName'].str.replace(' ', '_')

# Modify the 'segmentsFilePath' column to have a relative path
df['segmentsFilePath'] = df.apply(lambda row: f"../segments/{row['scientificName']}/{row['segmentsFilePath']}", axis=1)

# Initialize the 'userResponse' column with empty strings
df['userResponse'] = ''

# Save the modified CSV file with the required columns
df[['observationID', 'classificationProbability', 'segmentsFilePath', 'scientificName', 'userResponse']].to_csv('../output/segments_revised.csv', index=False)