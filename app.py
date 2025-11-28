# Import necessary libraries
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from summarizer import chunk_text, summarize_chunk, consolidate_and_summarize, SummarizationError

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
    model = genai.GenerativeModel('gemini-2.0-flash')
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
    # Chunking / performance options
    enable_chunking = st.checkbox("Enable chunked summarization (recommended for long text)", value=True)
    chunk_size = st.number_input("Approx. characters per chunk:", min_value=1000, max_value=20000, value=4000, step=500)
    quick_mode = st.checkbox("Quick mode (faster, less detailed)", value=False)

# Main content area
input_text = st.text_area("Enter the text to summarize:", height=300, placeholder="Paste your article, notes, or document here...")

summarize_button = st.button("Summarize Text", type="primary", use_container_width=True)


# --- Logic for Summarization and Output ---
if summarize_button and input_text:
    with st.spinner("Gemini is working its magic..."):
        try:
            # Decide whether to chunk
            chunks = [input_text]
            if enable_chunking and len(input_text) > chunk_size:
                chunks = chunk_text(input_text, chunk_size)

            total = len(chunks)
            progress = st.progress(0)
            status_text = st.empty()

            intermediate_summaries = []
            for i, c in enumerate(chunks, start=1):
                status_text.info(f"Summarizing chunk {i} of {total}...")
                bullet = summary_tone == "Bullet Points"
                chunk_summary = summarize_chunk(c, model, summary_tone, max(1, summary_length), bullet=bullet, quick=quick_mode)
                intermediate_summaries.append(chunk_summary)
                progress.progress(int((i / total) * 100))

            status_text.info("Combining chunk summaries into a final concise summary...")
            # Combine intermediate summaries and ask for a final consolidated summary
            final_summary = consolidate_and_summarize(intermediate_summaries, model, summary_tone, summary_length)

            progress.progress(100)
            status_text.success("Done — final summary ready.")

            with st.expander("✅ **View Your Summary**", expanded=True):
                st.markdown(final_summary)

        except SummarizationError as e:
            st.error(f"Summarization failed: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif summarize_button and not input_text:
    st.warning("Please enter some text to summarize.")
