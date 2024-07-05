#!/usr/bin/env python3

# %%
import os
import logging
from datetime import datetime
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
import argparse

# %%
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# %%
def handle_audio_files(video_path):
    logging.info(f"Extracting audio from video: {video_path}")
    audio_from_video = AudioSegment.from_file(video_path, format="mp4")
    audio_path = "./temp_audio.mp3"
    audio_data = audio_from_video.export(audio_path, format="mp3")
    logging.info(f"Audio extracted and saved to: {audio_path}")
    return (audio_path, audio_data)

# %%
def get_openai_client():
    logging.info("Loading environment variables and initializing OpenAI client")
    load_dotenv()
    return OpenAI()

# %%
def transcribe_video(client, video_path):
    logging.info(f"Starting transcription for video: {video_path}")
    (audio_path, audio_file) = handle_audio_files(video_path)
    
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    logging.info("Transcription completed")
    
    os.remove(audio_path)
    logging.info(f"Temporary audio file removed: {audio_path}")
    return transcription.text

# %%
def generate_procedure(client, transcription, language="Portuguese"):
    logging.info("Generating step-by-step procedure from transcription")
    prompt = f"""
            You are a helpful assistant. Using the provided transcription, generate a step-by-step procedure of the explained process.
            Make sure that the procedure was written in {language}. Return only the procedure, without any explanation or additional information.
            Transcription:
            """
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": transcription},
    ]
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    logging.info("Procedure generation completed")
    return response.choices[0].message.content

# %%
def save_to_file(content, filepath):
    logging.info(f"Saving procedure to file: {filepath}")
    with open(filepath, 'w') as file:
        file.write(content)
    logging.info("Procedure saved successfully")

# %%
def main(video_path, procedure_path, language):
    client = get_openai_client()
    transcription = transcribe_video(client, video_path)
    procedure = generate_procedure(client, transcription, language)

    save_to_file(procedure, procedure_path)
    
    print(f"Procedure:\n\n{procedure}", end="\n\n")
    print(f"Procedure saved to {procedure_path}")

# %%
if __name__ == "__main__":
    default_language = "Portuguese"
    default_viodeo_path = "./data/video.mp4"
    default_procedure_path = f"./data/procedure-{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

    parser = argparse.ArgumentParser(description="Process a video and generate a procedural text file.")
    parser.add_argument('-v','--video', dest='video_path', type=str, default=default_viodeo_path, help='Path to the video file')
    parser.add_argument('-o','--output', dest='procedure_path', type=str, default=default_procedure_path, help='Path to save the procedure file')
    parser.add_argument('-l','--language', dest='language', type=str, default=default_language, help='Language of the procedure')

    args, unknown = parser.parse_known_args()
    main(args.video_path, args.procedure_path, args.language)
