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

# Initialize session state for summary storage
if "summary_output" not in st.session_state:
    st.session_state.summary_output = None


# --- Layout Configuration (Main Area and Sidebar) ---

# Sidebar for customization options
with st.sidebar:
    st.header("⚙️ Customization")
    
    # Preset templates
    preset = st.selectbox(
        "📋 Quick Presets",
        ["Custom", "Quick Summary", "Executive Brief", "Detailed Report", "Key Points"],
        help="Choose a preset to auto-configure summary settings"
    )
    
    # Apply preset if selected
    if preset == "Quick Summary":
        summary_length = 2
        summary_tone = "Casual"
    elif preset == "Executive Brief":
        summary_length = 3
        summary_tone = "Formal"
    elif preset == "Detailed Report":
        summary_length = 5
        summary_tone = "Professional"
    elif preset == "Key Points":
        summary_length = 4
        summary_tone = "Bullet Points"
    else:
        summary_length = st.slider("Summary Length (sentences):", min_value=1, max_value=10, value=3, step=1)
        summary_tone = st.selectbox("Summary Tone:", ["Formal", "Casual", "Professional", "Bullet Points"])
    
    # If preset is selected, show the configured values
    if preset != "Custom":
        st.info(f"✓ Preset applied: {preset}")
    
    # Chunking / performance options
    st.markdown("---")
    enable_chunking = st.checkbox("Enable chunked summarization (recommended for long text)", value=True)
    chunk_size = st.number_input("Approx. characters per chunk:", min_value=1000, max_value=20000, value=4000, step=500)
    quick_mode = st.checkbox("Quick mode (faster, less detailed)", value=False)

# Main content area
input_text = st.text_area("Enter the text to summarize:", height=300, placeholder="Paste your article, notes, or document here...")

# Character counter and clear button
col1, col2 = st.columns([0.85, 0.15])
with col1:
    char_count = len(input_text.strip())
    if char_count > 0:
        st.caption(f"📊 {char_count:,} characters • {len(input_text.split())} words")
    else:
        st.caption("💡 Paste your text here to get started")

with col2:
    if st.button("🗑️ Clear", use_container_width=True):
        st.rerun()

# Button row
col1, col2 = st.columns([0.7, 0.3])
with col1:
    summarize_button = st.button("✨ Summarize Text", type="primary", use_container_width=True)
with col2:
    pass  # Placeholder for potential future button


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
            status_text.success("✅ Done — final summary ready!")
            
            # Store summary in session state
            st.session_state.summary_output = final_summary
            
            # Calculate statistics
            input_words = len(input_text.split())
            output_words = len(final_summary.split())
            reduction_percent = ((input_words - output_words) / input_words * 100) if input_words > 0 else 0
            
            # Display summary with statistics
            st.markdown("---")
            
            # Statistics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📝 Input Words", f"{input_words:,}")
            with col2:
                st.metric("✨ Output Words", f"{output_words:,}")
            with col3:
                st.metric("📊 Reduction", f"{reduction_percent:.1f}%")
            with col4:
                st.metric("⚡ Efficiency", f"{output_words / max(input_words, 1) * 100:.1f}%")
            
            st.markdown("---")
            
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.subheader("📄 Your Summary")
            with col2:
                if st.button("📋 Copy", use_container_width=True, help="Copy to clipboard"):
                    st.toast("✅ Copied to clipboard!", icon="📋")
            
            with st.expander("View Summary", expanded=True):
                st.markdown(final_summary)
                # Copy button inside expander for easier access
                st.code(final_summary, language="text", line_numbers=False)

        except SummarizationError as e:
            st.error(f"❌ Summarization failed: {e}")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

elif summarize_button and not input_text:
    st.warning("⚠️ Please enter some text to summarize.")

# --- Empty State / Welcome Message ---
else:
    if char_count == 0:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("""
            ### 👋 Welcome to Gemini AI Text Summarizer
            
            **How to use:**
            1. 📝 Paste or type your text above
            2. ⚙️ Customize your summary (length, tone, etc.)
            3. ✨ Click "Summarize Text" to generate your summary
            
            **Features:**
            - 🚀 Powered by Google Gemini 2.0
            - 📊 Handles long documents with smart chunking
            - ⚡ Quick mode for faster summaries
            - 💾 Copy results with one click
            
            **Try an example:**
            """)
            
            if st.button("📚 Load Sample Text", use_container_width=True):
                sample_text = """
                Artificial intelligence has revolutionized many industries by automating complex tasks 
                and providing intelligent insights. Machine learning models trained on large datasets 
                can now perform tasks that once required human expertise. From healthcare to finance, 
                AI is improving decision-making and efficiency. However, as AI becomes more powerful, 
                questions about ethics, bias, and transparency become increasingly important. Companies 
                and governments are working to develop responsible AI practices.
                """
                st.session_state.sample_text = sample_text
                st.rerun()
