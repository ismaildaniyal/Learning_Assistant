import streamlit as st
import requests
import io
import json
import language_tool_python
import difflib
import pyaudio
import wave
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from io import BytesIO
from pydub import AudioSegment

# Deepgram API Key (Replace with your own)
DEEPGRAM_API_KEY = "2639cacaad008c296faec98375c783987d058fa4"

# Initialize LanguageTool for grammar check
tool = language_tool_python.LanguageToolPublicAPI('en-US')

# Language mapping
LANGUAGES = {
    'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Italian': 'it',
    'Portuguese': 'pt', 'Russian': 'ru', 'Chinese': 'zh'
}

# Function to transcribe audio using Deepgram API
# Function to transcribe audio using Deepgram API
def transcribe_audio_deepgram(audio_data, language='en', retries=3):
    url = f"https://api.deepgram.com/v1/listen?model=general&language={language}"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }
    
    try:
        # Convert the audio to WAV format
        audio = AudioSegment.from_file(audio_data)
        audio = audio.set_channels(1).set_frame_rate(16000)  # Mono, 16kHz sample rate
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        if wav_io.getbuffer().nbytes == 0:
            st.error("Converted audio is empty. Check file format.")
            return None

        files = {"audio": wav_io.getvalue()}
    except Exception as e:
        st.error(f"Error converting audio to WAV: {e}")
        return None

    attempt = 0
    while attempt < retries:
        try:
            response = requests.post(url, headers=headers, data=files["audio"])
            if response.status_code == 200:
                return response.json()['results']['channels'][0]['alternatives'][0]['transcript']
            else:
                st.error(f"Deepgram API Error: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {e}")
            time.sleep(2)  # Retry after a short delay
        except Exception as e:
            st.error(f"Error: {e}")
            return None
        attempt += 1

    return None


# Function to provide grammar feedback
def check_grammar(text, language='en-US'):
    tool.language = language
    matches = tool.check(text)
    return [match.ruleId + ": " + match.message for match in matches]

# Function to check pronunciation feedback
def check_pronunciation(reference_text, user_text):
    similarity = difflib.SequenceMatcher(None, reference_text, user_text).ratio()
    return "Your pronunciation needs improvement. Try speaking more clearly!" if similarity < 0.7 else "Great pronunciation!"

# Function to record audio
class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.stream = None
        self.p = pyaudio.PyAudio()

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        threading.Thread(target=self.record).start()

    def record(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)
        
    def stop_recording(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()

        # Convert audio to WAV format
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(self.frames))
        
        wav_io.seek(0)
        return wav_io  # Return the WAV formatted audio

    def get_live_data(self):
        """Return the latest audio frame data for visualization."""
        data = self.stream.read(1024)
        return np.frombuffer(data, dtype=np.int16)

# Streamlit UI Setup
st.title('🎙️ Real-time Language Learning Assistant')
st.write("Speak in any language, and get **instant transcription, grammar correction, and pronunciation feedback.**")

# Language Selection
selected_language = st.selectbox('🌍 Select your language:', list(LANGUAGES.keys()))
language_code = LANGUAGES[selected_language]

# Audio Recording Option
option = st.radio("🎤 Choose how to provide audio:", ('Upload Audio File', 'Record Audio in Real-time'))

# Add visualization of waveform
if option == 'Record Audio in Real-time':
    st.write("Press and hold the button below to record your voice. Release to process audio.")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        record_button = st.button("🔴 Hold to Record", key="record")

    # Create a figure for plotting waveform
    fig, ax = plt.subplots()
    ax.set_ylim(-32000, 32000)  # Limit the y-axis to the range of audio data
    line, = ax.plot([], [], lw=2)

    ax.set_title("Real-time Audio Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    # Update function for animation
    def update_plot(frame):
        audio_data = recorder.get_live_data()
        line.set_ydata(audio_data)
        line.set_xdata(np.arange(len(audio_data)))
        return line,

    # Recorder and visualization loop
    recorder = AudioRecorder()
    if record_button:
        st.write("Recording... Hold the button!")
        recorder.start_recording()

        # Animate the waveform in real-time
        ani = FuncAnimation(fig, update_plot, blit=True, interval=50)

        st.pyplot(fig)

        time.sleep(3)  # Simulating holding button for recording

        # Stop recording after 3 seconds
        audio_data = recorder.stop_recording()

        with st.spinner('Processing audio...'):
            transcription = transcribe_audio_deepgram(audio_data, language=language_code)
            if transcription:
                st.subheader("**📝 Transcription:**")
                st.write(transcription)
                grammar_feedback = check_grammar(transcription, language=language_code)
                if grammar_feedback:
                    st.subheader("**✍️ Grammar Feedback:**")
                    for feedback in grammar_feedback:
                        st.write(f"- {feedback}")
                st.subheader("**🗣 Pronunciation Feedback:**")
                st.write(check_pronunciation(transcription, transcription))

elif option == 'Upload Audio File':
    audio_file = st.file_uploader("📂 Upload an audio file", type=["mp3", "wav", "ogg"])
    if audio_file:
        st.audio(audio_file, format="audio/wav")
        with st.spinner('Processing audio...'):
            audio_data = io.BytesIO(audio_file.read())
            transcription = transcribe_audio_deepgram(audio_data, language=language_code)
            if transcription:
                st.subheader("**📝 Transcription:**")
                st.write(transcription)
                grammar_feedback = check_grammar(transcription, language=language_code)
                if grammar_feedback:
                    st.subheader("**✍️ Grammar Feedback:**")
                    for feedback in grammar_feedback:
                        st.write(f"- {feedback}")
                st.subheader("**🗣 Pronunciation Feedback:**")
                st.write(check_pronunciation(transcription, transcription))
