import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pyperclip

# ---------------- UI ----------------
st.set_page_config(page_title="AI Translator")
st.title("🌍 AI Language Translation Tool")
st.markdown("---")

# ---------------- LANGUAGES ----------------
languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-cn",
    "Arabic": "ar",
    "Malayalam": "ml",
    "Telugu": "te",
    "Kannada": "kn"
}

# ---------------- SESSION STATE ----------------
if "translated" not in st.session_state:
    st.session_state.translated = ""

# ---------------- LANGUAGE SELECTORS (moved above text area) ----------------
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", list(languages.keys()))
with col2:
    target_lang = st.selectbox("Target Language", list(languages.keys()), index=1)

# ---------------- INPUT UI ----------------
text = st.text_area("Enter text to translate", height=120)
st.markdown("---")

# ---------------- TRANSLATE BUTTON ----------------
if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text!")
    else:
        try:
            st.session_state.translated = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.translated = ""

# ---------------- OUTPUT ----------------
if st.session_state.translated:
    st.success("Translated Text")

    st.text_area(
        "Result",
        st.session_state.translated,
        height=150
    )

    # ---------------- COPY BUTTON ----------------
    if st.button("Copy"):
        try:
            pyperclip.copy(st.session_state.translated)
            st.success("Copied to clipboard!")
        except Exception as e:
            st.error(f"Copy failed: {e}")

    # ---------------- TEXT TO SPEECH ----------------
    st.markdown("Listen")
    try:
        tts = gTTS(
            text=st.session_state.translated,
            lang=languages[target_lang]
        )
        audio_file = "translation.mp3"
        tts.save(audio_file)
        with open(audio_file, "rb") as audio:
            st.audio(audio.read(), format="audio/mp3")
    except Exception as e:
        st.error(f"TTS Error: {e}")
