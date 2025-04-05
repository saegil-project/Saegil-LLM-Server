import requests
import os

def test_text_to_speech_api():
    """
    Test the text-to-speech API by sending a request and saving the response to a file.
    """
    # API endpoint
    url = "http://localhost:8000/text-to-speech"
    
    # Text to convert to speech
    text = "안녕하세요, 이것은 텍스트를 음성으로 변환하는 API 테스트입니다."
    
    # Send POST request to the API
    response = requests.post(
        url,
        json={"text": text}
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful!")
        
        # Save the audio to a file
        with open("test_output.mp3", "wb") as f:
            f.write(response.content)
        
        print(f"Audio saved to {os.path.abspath('test_output.mp3')}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    print("Testing the text-to-speech API...")
    print("Make sure the API is running (python api.py) before running this test.")
    test_text_to_speech_api()