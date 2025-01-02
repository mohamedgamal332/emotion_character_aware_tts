import json
import os
import requests
import base64


def make_api_call(prompt, content, speaker, api_url='http://localhost:5000/predictions'):
    """
    Makes an API call with the specified parameters.

    Args:
      prompt: The text prompt for the API.
      content: The content for the API call.
      speaker: The speaker ID for the API call.
      api_url: URL to call the endpoint

    Returns:
      dict: The JSON response from the API, or None on error.
    """

    data = {
        "input": {
            "prompt": prompt,
            "content": content,
            "speaker": speaker,
            "language": "English"
        }
    }

    try:
        response = requests.post(
           api_url,
            headers={"Content-Type": "application/json"},
            json=data
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return None


def get_audio_from_api_output(api_output_json):
    """
    Extracts and saves the audio from an API response's 'output' field.

    Args:
      api_output_json: The JSON response from the API, or a Python dictionary

    Returns:
        tuple:  The decoded audio data as bytes object, or None if fails
                and the output filename (without extension) or None if fails
    """
    try:
        # Load JSON from the string if it's not already a dict
        if isinstance(api_output_json, str):
           api_output = json.loads(api_output_json)
        else:
            api_output=api_output_json

        output_data_uri = api_output.get("output")
        if not output_data_uri:
            print("Error: 'output' field not found in the API response.")
            return None,None


        # Remove the data URI prefix
        prefix = "data:audio/mpeg;base64,"
        if output_data_uri.startswith(prefix):
            base64_audio = output_data_uri[len(prefix):]

        else:
            print("Error: Output is not a data URI. Not starting with ", prefix )
            return None,None

        try:
            # Decode the base64 string into bytes
            decoded_audio = base64.b64decode(base64_audio, validate = True)
        except base64.binascii.Error as e:
            print(f"Error decoding base64 audio data: {e}")
            return None,None

        output_file_prefix = api_output.get("output_file_prefix")
        if output_file_prefix:
             output_filename = output_file_prefix
        else:
            output_filename = 'output'
        return decoded_audio, output_filename
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None,None
    except Exception as e:
         print(f"An error occurred: {e}")
         return None,None
    

def save_audio(audio_data, filename, output_dir, num):
    """Saves the audio bytes to a file

    Args:
      audio_data: The decoded audio data as a byte object
      filename: the filename to store the file (without extension)
      output_dir: The directory to save the file in

    Returns:
      none
    """
    if not audio_data:
        print("no audio data")
        return
    if not filename:
         filename='output'
    output_path = os.path.join(output_dir, filename + f"{num}" + ".mp3")

    try:
        with open(output_path, 'wb') as f:
          f.write(audio_data)
          print(f"Audio file saved to {output_path}")
    except Exception as e:
        print(f"Error saving audio to file: {e}")



def automate_audio_creation(output_dir, prompt, content, speaker, num):
    """
    Automates the process of making API calls and saving the audio output.

    Args:
      output_dir: The directory where audio files should be saved.
      prompt: The text prompt for the API.
      content: The content for the API call.
      speaker: The speaker ID for the API call.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)


    api_response = make_api_call(prompt, content, speaker)


    if api_response:

        audio_data, output_filename = get_audio_from_api_output(api_response)

        if audio_data:
          save_audio(audio_data, output_filename, output_dir, num)

    else:
        print("Failed to get audio from the API.")

import json

if __name__ == "__main__":
    output_directory = ".."  # Specify your desired directory
    file_path = os.path.join("..", "temp", "tts_input.json")
    

    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
        for i in range(len(data)):
            prompt_text = data[i][1]  # Change your prompt
            content_text = data[i][0][0]  # Change your content
            speaker_id = data[i][0][1]  # Change your speaker id

            automate_audio_creation(output_directory, prompt_text, content_text, speaker_id, i)