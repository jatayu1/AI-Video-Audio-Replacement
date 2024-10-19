# AI Video Audio Replacement

This application allows you to replace the audio in a video file with AI-generated voice audio. It utilizes Google Cloud services for speech recognition and synthesis, as well as Azure OpenAI for transcription correction.

## Features

- Upload a video with improper audio.
- Automatically transcribe the audio using Google Speech-to-Text.
- Correct the transcription using Azure OpenAI GPT-4.
- Synthesize speech from the corrected transcription using Google Text-to-Speech.
- Replace the original audio in the video with the synthesized audio.

## Prerequisites

To run this application, you need to install the following dependencies and set up your Google Cloud and Azure OpenAI services:

1. **Python 3.7 or later**
2. **Google Cloud SDK** - Follow the [installation guide](https://cloud.google.com/sdk/docs/install).
3. **Azure OpenAI Service** - Sign up and create a resource in the [Azure portal](https://portal.azure.com/).
4. **ffmpeg** - A tool for handling multimedia files like video and audio. Install `ffmpeg` by following the instructions below.

### Installing `ffmpeg`

- On macOS (using Homebrew):
  ```bash
  brew install ffmpeg

- On Ubuntu/Debian:
    ```bash
    sudo apt update
    sudo apt install ffmpeg

- On Windows:
    Download the latest release from the official ffmpeg website and follow the installation instructions. Ensure the ffmpeg binary is added to your system’s PATH.
    
## Setup Instructions

1. **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

2. **Install required Python packages:**
    ```bash
    pip install streamlit moviepy google-cloud-speech google-cloud-texttospeech requests

3. **Set up Google Cloud credentials:**
    Replace the 'your-service-account-file' values in code with your google cloud's service account JSON key file's path:
    ```bash
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./<your-service-account-file>.json"

4. **Set up Azure OpenAI connection:**
    Replace the azure_openai_key and azure_openai_endpoint values in your code with your actual key and endpoint:
    ```bash
    azure_openai_key = "<your-azure-openai-key>"
    azure_openai_endpoint = "<your-azure-openai-endpoint>"

5. **To run the application:**
    ```bash
    streamlit run <your-python-file>.py



