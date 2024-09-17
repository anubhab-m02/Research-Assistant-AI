import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from pdf_utils import extract_text_from_pdf
from analysis import analyze_papers, compare_papers, ask_question, summarize_paper, find_related_papers
from citation import extract_citations, format_citation
from semantic_search import perform_semantic_search, highlight_text
from ui_layout import render_sidebar, render_main_content
import time

# Page configuration
st.set_page_config(layout="wide", page_title="Research Paper Analysis Assistant", page_icon="📚")

# Initialize session state variables if they don't exist
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'paper_contents' not in st.session_state:
    st.session_state.paper_contents = []
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar for API key input and app information
render_sidebar()

# Main app logic
if st.session_state.api_key:
    genai.configure(api_key=st.session_state.api_key)

    try:
        if st.session_state.chat_session is None:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": st.session_state.ai_temperature,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": st.session_state.max_tokens,
                },
            )
            st.session_state.chat_session = model.start_chat(history=[])

        # Main content area
        render_main_content()

    except google_exceptions.GoogleAPIError as e:
        st.error(f"An error occurred while setting up the model: {str(e)}")
        st.info("Please check your API key and try again. If the problem persists, the service might be temporarily unavailable.")
        if st.button("Retry"):
            st.experimental_rerun()

else:
    st.warning("Please enter your Google API Key in the sidebar to use the application.")