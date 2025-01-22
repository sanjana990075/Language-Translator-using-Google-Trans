import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import speech_recognition as sr
import os

# Custom CSS for a fully colorful theme
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #ff758c, #6a8eae);
        color: white;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .stApp {
        background: linear-gradient(to bottom, #ff9a9e, #fad0c4, #6a8eae);
    }
    .stTextInput > label {
        color: white;
        font-size: 18px;
    }
    .stSelectbox > label {
        color: white;
        font-size: 18px;
    }
    .stRadio > label {
        color: white;
        font-size: 18px;
    }
    .stButton > button {
        background-color: #ff7eb3;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        border: 2px solid white;
    }
    .stButton > button:hover {
        background-color: #ff758c;
        color: black;
    }
    .stAlert {
        background-color: rgba(255, 255, 255, 0.3) !important;
        border: 1px solid white;
        color: white;
    }
    h1, h2, h3 {
        text-align: center;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
    }
    .stMarkdown {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the translator
translator = Translator()

# Title of the app
st.title("🌍 Multimodal Translator: Audio & Text 🌐")

# Input method selection
st.header("🔍 Select Your Input Method")
input_method = st.radio("Choose one:", ("Text", "Audio"))

# Initialize user input variable
user_input = None

if input_method == "Text":
    # Text input
    st.subheader("✍️ Enter Text")
    user_input = st.text_input("Type here:")

elif input_method == "Audio":
    # Audio input using the microphone
    recognizer = sr.Recognizer()
    st.subheader("🎤 Speak Into the Microphone")
    st.info("Click the button below to start speaking.")
    if st.button("🎙️ Record Audio"):
        with sr.Microphone() as source:
            st.info("🎙️ Recording... Please speak now.")
            recognizer.adjust_for_ambient_noise(source)  # Adjusts for ambient noise
            audio_data = recognizer.listen(source)
            st.info("✅ Recording stopped.")
            try:
                # Recognize speech using Google Web Speech API
                user_input = recognizer.recognize_google(audio_data)
                st.success(f"Recognized Text: {user_input}")
            except sr.UnknownValueError:
                st.error("⚠️ Couldn't recognize the speech. Please try again.")
            except sr.RequestError:
                st.error("⚠️ Error with the speech recognition service. Check your connection.")

# Populate language dropdown with valid language codes
st.header("🌐 Select Target Language")
language_options = {v: k for k, v in LANGUAGES.items()}
target_language = st.selectbox("Choose a language:", list(language_options.keys()))

# Translate and display result
if user_input:
    try:
        translation = translator.translate(user_input, dest=language_options[target_language])
        
        # Display translated text
        st.header("📜 Translated Text")
        st.markdown(f"### {translation.text}")
        
        # Generate speech for the translation
        tts = gTTS(translation.text, lang=language_options[target_language])
        tts.save("output.mp3")
        
        # Play the audio
        audio_file_path = "output.mp3"
        st.audio(audio_file_path, format="audio/mp3")

    except Exception as e:
        st.error(f"❌ An error occurred while translating: {e}")

# Clean up the saved file after execution
if os.path.exists("output.mp3"):
    os.remove("output.mp3")