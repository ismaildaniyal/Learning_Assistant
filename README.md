Real-time Language Learning Assistant

Overview

The Real-time Language Learning Assistant is a Streamlit-based web application that enables users to:

- Record or Upload Audio: Record real-time speech or upload an audio file.

- Transcribe Speech: Convert spoken words into text using the Deepgram API.

- Check Grammar: Detect and correct grammar mistakes using the LanguageTool API.

- Analyze Pronunciation: Compare the transcription against expected pronunciation to provide feedback.

- Visualize Audio Waveform: Display a real-time waveform of the recorded speech.

Features

- Multi-language support (English, Spanish, French, German, etc.).

- Real-time recording with waveform visualization.

- Deepgram API integration for speech-to-text transcription.

- Grammar checking using LanguageTool.

- Pronunciation analysis based on text similarity.

- Streamlit UI for an interactive user experience.

Installation

Prerequisites

Ensure you have Python installed (Python 3.7+ recommended).

Steps

1. Clone this repository:

git clone https://github.com/your-repo/language-learning-assistant.git
cd language-learning-assistant

2. Install dependencies:

pip install -r requirements.txt

3. Run the application:

streamlit run app.py

Dependencies

The project relies on the following Python libraries:

- streamlit (for UI development)

- requests (for API communication)

- language_tool_python (for grammar checking)

- pyaudio, wave (for audio recording)

- numpy, matplotlib (for waveform visualization)

- pydub (for audio processing)

- difflib (for pronunciation comparison)

Usage

1. Select a Language

Choose the language you want to transcribe and analyze.

2. Provide Audio Input

- Record in real-time: Press and hold the record button to capture your voice.

- Upload an audio file: Upload an .mp3, .wav, or .ogg file.

3. Get Feedback

- View the transcription of your speech.

- Receive grammar corrections.

- Get pronunciation feedback based on text similarity.

- See a real-time waveform of your recorded audio.

Configuration

API Key

Replace DEEPGRAM_API_KEY in app.py with your Deepgram API key:

DEEPGRAM_API_KEY = "your-api-key-here"

Future Enhancements

- Add more languages for transcription and grammar checking.

- Improve pronunciation feedback using phonetic analysis.

- Enhance UI with additional visualization features.

License

This project is licensed under the MIT License. Feel free to modify and distribute it as needed.

Contributors

- Your Name (@yourGitHubHandle)

Contact

For questions or support, reach out to: [ismailsarfraz9345@gmail.com]

