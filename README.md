# Audio Extraction and Procedure Generation

This project provides a pipeline for extracting audio from a video file, transcribing the audio content, generating a step-by-step procedure in the specified language, and saving the procedure to a file.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [File Descriptions](#file-descriptions)
4. [License](#license)

## Installation

To set up the project locally:

1. **Clone this repository:**

```bash
git clone <repository-url>
cd <repository-directory>
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install the required dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

   Create a `.env` file and add the necessary OpenAI credentials:

```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

To run the script and generate a procedure from a video file:

```bash
python extracao-audio.py <video_path> <procedure_path> [language]
```

- `<video_path>`: Path to the input video file.
- `<procedure_path>`: Path where the generated procedure will be saved.
- `[language]` (optional): Language for the generated procedure. Defaults to "Portuguese".

For example:

```bash
python extracao-audio.py -v example_video.mp4 -o output_procedure.txt -l English
```

## File Descriptions

- **extracao-audio.py**:
  - `handle_audio_files(video_path)`: Extracts audio from the given video.
  - `get_openai_client()`: Initializes the OpenAI client using environment variables.
  - `transcribe_video(client, video_path)`: Transcribes the audio of the given video.
  - `generate_procedure(client, transcription, language="Portuguese")`: Generates a step-by-step procedure from the transcription.
  - `save_to_file(content, filepath)`: Saves the generated procedure to the specified file.
  - `main(video_path, procedure_path, language="Portuguese")`: Main function orchestrating the steps from video transcription to procedure file generation.


## LICENSE

The project is licensed under the MIT License. For more details, refer to the LICENSE file included in this repository.