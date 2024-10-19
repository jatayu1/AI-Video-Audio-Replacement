# AI Video Audio Replacement

This Streamlit-based application allows users to upload a video file with improper audio, transcribe the audio using AI, correct the transcription, and replace the original audio with an AI-generated voice. The application uses:

- **Google Cloud Speech-to-Text** for audio transcription.
- **Azure OpenAI GPT-4** for transcription correction.
- **Google Cloud Text-to-Speech** for AI-generated audio replacement.
- **MoviePy** for video editing and audio replacement.

## Features

- **Upload Video**: Upload a video with improper or low-quality audio.
- **Transcribe Audio**: Automatically transcribe the audio using Google Speech-to-Text.
- **Correct Transcription**: Use Azure OpenAI GPT-4 to correct and improve the transcription for clarity and grammar.
- **AI Audio Replacement**: Generate a new audio track using Google's Text-to-Speech service.
- **Replace Audio in Video**: Replace the original video’s audio with the new AI-generated audio.
- **Customize Speech**: Set the desired speaking rate with words per minute (WPM) input.

## Prerequisites

### Python Libraries

Install the required Python libraries via pip:

```bash
pip install streamlit moviepy google-cloud-speech google-cloud-texttospeech requests
```


### Additional Tools
- FFmpeg: Required for audio processing (converting to mono and resampling). Install FFmpeg by following the instructions at FFmpeg Download.
Cloud Services

### Google Cloud:
- Enable the Speech-to-Text and Text-to-Speech APIs in your Google Cloud project.
Create a Google Cloud service account and download the JSON key file.

### Azure OpenAI:
- Obtain the API key and endpoint for Azure OpenAI GPT-4.


## Setup

1. Clone this repository:

```
    git clone https://github.com/yourusername/AI-Video-Audio-Replacement.git
    cd AI-Video-Audio-Replacement
```
2. Create a .streamlit/secrets.toml file in the project directory and add your Google Cloud and Azure OpenAI credentials:

```
    [google_cloud]
    gcp_key = '''{
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "your-private-key",
        "client_email": "your-client-email",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-client-email"
    }'''

    [azure_openai]
    azure_openai_key = "your-azure-openai-key"
    azure_openai_endpoint = "your-azure-openai-endpoint"
```

3. Install the dependencies and run the Streamlit app:

``` bash
    streamlit run audio-replacer.py
```