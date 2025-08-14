# Gemini AI Text Summarizer ✍️

A simple yet powerful web application that uses the Google Gemini API to summarize long pieces of text. This project is built with Python and Streamlit, providing a clean and interactive user interface.

# 🌟 Features:
- AI-Powered Summarization: Leverages the power of Google's Gemini model to generate high-quality, coherent summaries.

- Customizable Output: Easily adjust the desired length of the summary (in sentences or bullet points).

- Tone Selection: Choose the tone of the summary, from Formal and Professional to Casual or a simple Bullet Points list.

- User-Friendly Interface: A clean and simple UI built with Streamlit, making it easy for anyone to use.

- Loading Indicator: Provides user feedback while the AI is processing the request.

# 🛠️ Tech Stack:

- Language: Python

- Web Framework: Streamlit

- AI Model: Google Gemini API (gemini-1.5-flash-latest)

# 🚀 Getting Started
Follow these instructions to get a local copy up and running.

Prerequisites
Python 3.8 or higher

A Google AI Studio API Key

1. Clone the Repository
First, clone the repository to your local machine:

git clone https://github.com/YOUR_USERNAME/gemini-text-summarizer.git
cd gemini-text-summarizer

2. Create and Activate a Virtual Environment
It's best practice to create a virtual environment to manage project dependencies.

### Create the virtual environment
python -m venv venv

### Activate it (Windows)
venv\Scripts\activate

### Activate it (macOS/Linux)
source venv/bin/activate

3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

pip install -r requirements.txt

4. Set Up Your API Key
The application requires a Google Gemini API key to function.

Create a file named .env in the root of your project folder.

Inside the .env file, add your API key in the following format:

GOOGLE_API_KEY="AIza...YourSecretGoogleApiKey"

Note: The .env file is listed in the .gitignore file, so your secret key will not be committed to GitHub.

5. Run the Application
You are now ready to run the Streamlit application!

streamlit run app.py

A new tab should open in your web browser with the application running.
