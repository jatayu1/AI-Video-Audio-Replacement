import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip
from google.cloud import speech, texttospeech
import requests
import tempfile
import json
import os
import subprocess

# Google Cloud credentials for Speech-to-Text and Text-to-Speech services
gcp_key = st.secrets["google_cloud"]["gcp_key"]

# Create a temporary file to store the GCP key JSON
with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_gcp_key_file:
    temp_gcp_key_file.write(gcp_key.encode())  # Write the key as a string
    gcp_key_path = temp_gcp_key_file.name

# Set the environment variable to the path of the temporary GCP key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key_path

# Azure OpenAI connection details for transcription correction
azure_openai_key = st.secrets["azure_openai"]["azure_openai_key"]
azure_openai_endpoint = st.secrets["azure_openai"]["azure_openai_endpoint"]

# Streamlit interface for uploading video and inputting parameters
st.title("AI Video Audio Replacement")

# Upload a video and provide context keywords for better transcription accuracy
uploaded_video = st.file_uploader("Upload a Video with improper audio", type=["mp4", "mov"])
context_keywords = st.text_input("Enter context keywords (comma-separated):")
words_per_minute = st.number_input("Enter desired words per minute (WPM):", min_value=50, max_value=300, value=150)

# Function to safely remove files if they already exist
def remove_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# Process the video when the user clicks the button
if st.button("Process Video"):
    if uploaded_video:
        # Remove any existing files before starting the process
        remove_if_exists("extracted_audio.wav")
        remove_if_exists("mono_audio.wav")
        remove_if_exists("synthesized_audio.wav")
        remove_if_exists("final_video.mp4")

        # Function to extract and resample the audio from the video
        def extract_audio(video_clip, output_audio_path, target_sample_rate=16000):
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(output_audio_path)
            
            # Convert audio to mono and set the target sample rate
            mono_audio_path = "mono_audio.wav"
            subprocess.run([
                "ffmpeg", "-i", output_audio_path, "-ac", "1", "-ar", str(target_sample_rate), mono_audio_path
            ], check=True)
            
            return mono_audio_path

        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(uploaded_video.read())
            video_path = temp_video.name

        video_clip = VideoFileClip(video_path)
        audio_path = "extracted_audio.wav"
        mono_audio_path = extract_audio(video_clip, audio_path)

        st.write("Original Audio:")
        st.audio(mono_audio_path)

        # Function to transcribe audio using Google Speech-to-Text
        def transcribe_audio(audio_file):
            client = speech.SpeechClient()
            with open(audio_file, "rb") as audio:
                audio_content = audio.read()

            audio = speech.RecognitionAudio(content=audio_content)
            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
                enable_automatic_punctuation=True,
                use_enhanced=True,
                model="video",
                speech_contexts=[{"phrases": context_keywords.split(",")}],  # Add context keywords for better recognition
            )
            
            response = client.recognize(config=config, audio=audio)
            return response.results[0].alternatives[0].transcript if response.results else ""

        # Transcribe the extracted audio
        transcription = transcribe_audio(mono_audio_path)
        st.write("Original Transcription:")
        st.text(transcription)

        # Function to correct transcription using Azure OpenAI GPT-4
        def correct_transcription(transcription):
            if azure_openai_key and azure_openai_endpoint:
                try:
                    prompt = f"Please correct the following transcription for grammar and clarity:\n\n{transcription}"
                    headers = {
                        "Content-Type": "application/json",
                        "api-key": azure_openai_key
                    }
                    data = {
                        "messages": [
                            {"role": "system", "content": "You are a helpful assistant that corrects grammar and clarity."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": 300
                    }
                    
                    response = requests.post(azure_openai_endpoint, headers=headers, json=data)
                    if response.status_code == 200:
                        result = response.json()
                        return result["choices"][0]["message"]["content"].strip()
                    else:
                        st.error(f"Failed to connect or retrieve response: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect or retrieve response: {str(e)}")

        # Get the corrected transcription using GPT-4
        corrected_transcription = correct_transcription(transcription)
        st.write("Corrected Transcription:")
        st.text(corrected_transcription)

        # Function to synthesize speech from corrected transcription using Google Text-to-Speech
        def synthesize_speech(text, output_audio_path, wpm):
            client = texttospeech.TextToSpeechClient()
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Calculate the speaking rate based on the desired words per minute (WPM)
            speaking_rate = wpm / 150.0  # Adjust according to average WPM of 150
            speaking_rate = max(0.25, min(4.0, speaking_rate))  # Keep within valid range

            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", name="en-US-Wavenet-J"  # Journey voice
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate=speaking_rate
            )

            # Synthesize the corrected transcription into audio
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            # Save the synthesized audio
            with open(output_audio_path, "wb") as out:
                out.write(response.audio_content)

        # Synthesize the corrected transcription to audio
        output_audio_path = "synthesized_audio.wav"
        synthesize_speech(corrected_transcription, output_audio_path, words_per_minute)

        # Function to replace the original audio in the video with the synthesized audio
        def replace_audio_in_video(video_path, new_audio_path, output_video_path):
            video_clip = VideoFileClip(video_path)
            video_clip_duration = video_clip.duration

            new_audio = AudioFileClip(new_audio_path)
            
            # Replace the video’s audio with the new synthesized audio
            final_clip = video_clip.set_audio(new_audio)
            final_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
            st.write(f"Video with replaced audio saved to {output_video_path}")

        # Generate the final video with replaced audio
        output_video_path = "final_video.mp4"
        replace_audio_in_video(video_path, output_audio_path, output_video_path)

        # Display the final video
        st.video(output_video_path)
    else:
        st.error("Please upload a video file before processing.")
