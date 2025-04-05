# Text-to-Speech Web Application

A web application with a REST API built with FastAPI that converts text queries to speech using the ElevenLabs API.

## Prerequisites

- Python 3.7+
- ElevenLabs API key

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your ElevenLabs API key as an environment variable:

```bash
export ELEVENLABS_API_KEY="your-api-key-here"
```

Alternatively, you can create a `.env` file in the project root with the following content:

```
ELEVENLABS_API_KEY=your-api-key-here
```

## Running the Application

Start the server:

```bash
python api.py
```

The web application will be available at http://localhost:8000.

You can also access the interactive API documentation at http://localhost:8000/docs.

## Using the Web Interface

1. Open your browser and navigate to http://localhost:8000
2. Enter the text you want to convert to speech in the text area
3. Click the "Convert to Speech" button
4. Wait for the conversion to complete
5. The audio will be played automatically in the browser
6. You can download the MP3 file by clicking the "Download MP3" button

## API Endpoints

### GET /

Serves the web application interface.

### POST /text-to-speech

Converts text to speech and returns the audio file.

**Request Body:**

```json
{
  "text": "Text to convert to speech"
}
```

**Response:**

Audio file (MP3 format)

## Testing the API

A test script is provided to demonstrate how to use the API:

```bash
# Make sure the API server is running in another terminal
python test_api.py
```

This will send a request to the API with a sample text and save the resulting audio to `test_output.mp3`.

## Implementation Details

- The application uses FastAPI for handling HTTP requests and serving the web interface
- Text-to-speech conversion is performed using the ElevenLabs API
- The audio is streamed back to the client as an MP3 file
- The web interface is built with HTML, CSS, and JavaScript
- Jinja2 templates are used for rendering the HTML
- The application uses static file serving for CSS and JavaScript files
