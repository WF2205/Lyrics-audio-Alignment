import os
import re

def clean_filename(name):
    """
    Remove emojis, special characters, and leading/trailing spaces from the filename.
    """
    # Remove all non-alphanumeric characters except spaces and hyphens
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s\-\:]', '', name)
    # Replace multiple spaces with a single space
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
    return cleaned_name

def rename_files_in_directory(directory):
    """
    Rename all files in the specified directory by cleaning their filenames.
    """
    song_count = 0
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        
        # Ensure we are working with files only
        if os.path.isfile(old_path):
            # Extract the base name and extension
            base, ext = os.path.splitext(filename)
            
            # Clean the base name
            cleaned_name = clean_filename(base)
            
            # Construct the new file name
            new_filename = f"{cleaned_name}{ext}"
            new_path = os.path.join(directory, new_filename)
            
            # Rename the file
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: '{filename}' -> '{new_filename}'")
                song_count += 1
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")
            
    print(f"\nTotal number of songs: {song_count}")

def find_files_with_author_title(directory, output_file):
    """
    Find files containing '-' or ':' in their names and save to a txt file.
    """
    matching_files = []
    for filename in os.listdir(directory):
        if '-' in filename or ':' in filename:  # chech names contain "-" or ":"
            matching_files.append(filename)
    
    # Save matching file names to the output txt file
    with open(output_file, 'w', encoding='utf-8') as f:
        for file in matching_files:
            f.write(file + '\n')
    
    print(f"\nFound {len(matching_files)} files containing '-' or ':'. Saved to {output_file}")

# Directory containing the downloaded audio files
audio_directory = os.path.abspath('dataset/DALI/audio')
output_file = os.path.join(audio_directory, "files_with_author_title.txt")

# Run the renaming function
rename_files_in_directory(audio_directory)

# Find and save files with '-' or ':' in their names
find_files_with_author_title(audio_directory, output_file)
