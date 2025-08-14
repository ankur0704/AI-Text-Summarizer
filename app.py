# Import necessary libraries
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Page Configuration ---
# Set the page title, icon, and layout for a better user experience.
st.set_page_config(
    page_title="Gemini AI Summarizer",
    page_icon="✍️",
    layout="centered"
)

# --- Gemini API Configuration ---
# Configure the generative AI model with the API key from the environment variables.
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    # Initialize the GenerativeModel
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    # If the API key is not found or invalid, display an error and stop the app.
    st.error("API key not found or invalid. Please check your .env file.")
    st.stop()


# --- Main Application UI ---

# Display the main title and a brief description of the app.
st.title("✨ Gemini AI Text Summarizer")
st.write("Paste any text below, choose your desired summary style, and let Gemini do the rest!")

# --- User Input and Customization Options ---

# Create a text area for the user to input the text they want to summarize.
# The height is set to 250 pixels to provide ample space.
input_text = st.text_area("Enter the text to summarize:", height=250, placeholder="Paste your article, notes, or document here...")

# Create a sidebar for customization options to keep the main interface clean.
with st.sidebar:
    st.header("Customization")
    # A slider to select the desired length of the summary in sentences.
    summary_length = st.slider("Summary Length (sentences):", min_value=1, max_value=10, value=3, step=1)
    # A selectbox to choose the tone or style of the summary.
    summary_tone = st.selectbox("Summary Tone:", ["Formal", "Casual", "Professional", "Bullet Points"])

# Create a button to trigger the summarization process.
summarize_button = st.button("Summarize Text", type="primary")


# --- Logic for Summarization ---

# Check if the "Summarize Text" button was clicked and if there is text to summarize.
if summarize_button and input_text:
    # Use a spinner to show a loading message while the API call is in progress.
    with st.spinner("Gemini is summarizing the text..."):
        try:
            # --- Prompt Engineering ---
            # Create a detailed prompt for the AI model.
            # This prompt is engineered to be specific, telling the model its role, the task,
            # the input text, and the desired output format (length and tone).
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

            # Make the API call to generate the content.
            response = model.generate_content(prompt)

            # Display the generated summary.
            st.subheader("✅ Summary Complete")
            st.markdown(response.text) # Using markdown to properly format bullet points

        except Exception as e:
            # If any error occurs during the API call, display an error message.
            st.error(f"An error occurred: {e}")

# If the button is clicked but the text area is empty, show a warning.
elif summarize_button and not input_text:
    st.warning("Please enter some text to summarize.")
