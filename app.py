# Import necessary libraries
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Function to Load CSS ---
def load_css(file_name):
    """A function to load and inject a local CSS file."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini AI Summarizer",
    page_icon="✍️",
    layout="wide", # Use wide layout for a more spacious feel
    initial_sidebar_state="expanded"
)

# --- Load Custom CSS ---
load_css("style.css")


# --- Gemini API Configuration ---
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error("API key not found or invalid. Please check your .env file.")
    st.stop()


# --- Header and Title ---
st.title(" Gemini AI Text Summarizer")
st.markdown("##### Paste any text below, choose your desired summary style, and let Gemini do the rest!")


# --- Layout Configuration (Main Area and Sidebar) ---

# Sidebar for customization options
with st.sidebar:
    st.header("⚙️ Customization")
    summary_length = st.slider("Summary Length (sentences):", min_value=1, max_value=10, value=3, step=1)
    summary_tone = st.selectbox("Summary Tone:", ["Formal", "Casual", "Professional", "Bullet Points"])

# Main content area
input_text = st.text_area("Enter the text to summarize:", height=300, placeholder="Paste your article, notes, or document here...")

summarize_button = st.button("Summarize Text", type="primary", use_container_width=True)

# --- Logic for Summarization and Output ---
if summarize_button and input_text:
    with st.spinner("Gemini is working its magic..."):
        try:
            # --- Prompt Engineering ---
            if summary_tone == "Bullet Points":
                 prompt = f"""
                    You are an expert summarizer. Your task is to summarize the following text into a concise list of bullet points.
                    The summary should capture the key ideas and be exactly {summary_length} bullet points long.
                    Text to Summarize:
                    ---
                    {input_text}
                    ---
                    """
            else:
                prompt = f"""
                    You are an expert summarizer. Your task is to summarize the following text in a {summary_tone} tone.
                    The summary should capture the main points and be exactly {summary_length} sentences long.
                    Text to Summarize:
                    ---
                    {input_text}
                    ---
                    """

            # Make the API call
            response = model.generate_content(prompt)

            # Display the summary inside a collapsible expander
            with st.expander("✅ **View Your Summary**", expanded=True):
                st.markdown(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif summarize_button and not input_text:
    st.warning("Please enter some text to summarize.")
