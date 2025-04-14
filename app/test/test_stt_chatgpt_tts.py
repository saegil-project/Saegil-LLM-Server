import os

import requests


def test_stt_chatgpt_tts_upload_api():
    """
    Test the STT-ChatGPT-TTS upload API by sending an audio file and saving the response to a file.
    """
    # API endpoint
    url = "http://localhost:9090/stt-chatgpt-tts/upload"

    # Path to an audio file for testing
    # Replace this with the path to a real audio file on your system
    audio_file_path = "path/to/your/audio.mp3"

    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
        print("Please update the script with the path to a real audio file.")
        return

    # Send POST request to the API with the audio file
    with open(audio_file_path, "rb") as f:
        files = {"file": (os.path.basename(audio_file_path), f, "audio/mpeg")}
        response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")

        # Save the audio response to a file
        output_file = "stt_chatgpt_tts_response.mp3"
        with open(output_file, "wb") as f:
            f.write(response.content)

        print(f"Audio response saved to {os.path.abspath(output_file)}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")


def test_stt_chatgpt_tts_upload_json_api():
    """
    Test the STT-ChatGPT-TTS upload JSON API by sending an audio file and printing the JSON response.
    """
    # API endpoint
    url = "http://localhost:9090/stt-chatgpt-tts/upload/json"

    # Path to an audio file for testing
    # Replace this with the path to a real audio file on your system
    audio_file_path = "path/to/your/audio.mp3"

    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
        print("Please update the script with the path to a real audio file.")
        return

    # Send POST request to the API with the audio file
    with open(audio_file_path, "rb") as f:
        files = {"file": (os.path.basename(audio_file_path), f, "audio/mpeg")}
        response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")

        # Print the JSON response
        json_response = response.json()
        print("JSON Response:")
        print(f"Text: {json_response.get('text')}")
        print(f"Response: {json_response.get('response')}")
        print(f"Audio URL: {json_response.get('audio_url')}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")


if __name__ == "__main__":
    print("Testing the STT-ChatGPT-TTS API...")
    print("Make sure the API is running (python -m app.main) before running this test.")
    print("Also, update the audio_file_path variable with the path to a real audio file.")

    print("\nTesting the STT-ChatGPT-TTS upload API (returns audio):")
    test_stt_chatgpt_tts_upload_api()

    print("\nTesting the STT-ChatGPT-TTS upload JSON API (returns JSON):")
    test_stt_chatgpt_tts_upload_json_api()
