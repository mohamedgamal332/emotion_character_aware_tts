import os
import re
from pydub import AudioSegment

def natural_sort_key(s):
    """
    Key for natural sorting of strings with numbers (e.g., "file10" comes after "file2").
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def merge_audio_files(input_directory, output_file):
    """
    Merges all MP3 files in the specified directory into a single MP3 file,
    ensuring they are merged in numerical order.

    Args:
        input_directory (str): The path to the directory containing the audio files.
        output_file (str): The path to the output MP3 file.
    """
    try:
        combined_audio = AudioSegment.empty()
        files_to_merge = []

        for filename in os.listdir(input_directory):
            if filename.lower().endswith(".mp3"):
                files_to_merge.append(filename)

        # Sort files using natural sort
        files_to_merge.sort(key=natural_sort_key)

        for filename in files_to_merge:
            file_path = os.path.join(input_directory, filename)
            try:
              audio_segment = AudioSegment.from_mp3(file_path)
              combined_audio += audio_segment
            except Exception as e:
                 print(f"Error loading audio segment {filename}: {e}")



        if combined_audio:
             combined_audio.export(output_file, format="mp3")
             print(f"Audio files successfully merged in order and saved to: {output_file}")
        else:
            print("No valid audio file to merge")


    except FileNotFoundError:
        print(f"Error: Directory not found at {input_directory}")
    except Exception as e:
        print(f"An unexpected error occurred during the merging process: {e}")

if __name__ == "__main__":
    input_directory = "../output"
    output_filename = "Audiobook.mp3"

    merge_audio_files(input_directory, output_filename)