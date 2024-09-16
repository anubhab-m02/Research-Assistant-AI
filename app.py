import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from pdf_utils import extract_text_from_pdf
from analysis import analyze_papers, compare_papers, ask_question
from citation import extract_citations, format_citation
from visualization import create_chart
from ui_components import render_analysis_options, render_analysis_results

st.set_page_config(layout="wide")
st.title("Enhanced Research Paper Analysis Assistant")

# API Key input
api_key = st.text_input("Enter your Google API Key:", type="password", help="Your API key is required to use the Gemini model. If you don't have one, please visit https://makersuite.google.com/app/apikey to obtain it.")

if api_key:
    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 1024,
            },
        )

        # Initialize chat session in session state
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])

        # File uploader for multiple PDFs
        uploaded_files = st.file_uploader("Upload research paper(s) (PDF)", type="pdf", accept_multiple_files=True)

        # Text area for paper content input
        paper_content = st.text_area("Or paste your research paper content here:", height=300)

        if uploaded_files:
            paper_contents = []
            for uploaded_file in uploaded_files:
                with st.spinner(f"Extracting text from {uploaded_file.name}..."):
                    content = extract_text_from_pdf(uploaded_file)
                    paper_contents.append({"name": uploaded_file.name, "content": content})
                    st.success(f"PDF text extracted successfully from {uploaded_file.name}!")

        # Render analysis options and get user inputs
        output_format, focus_areas = render_analysis_options()

        if st.button("Analyze Paper(s)"):
            if paper_contents or paper_content:
                analysis_results = analyze_papers(st.session_state.chat_session, paper_contents, focus_areas, output_format)
                render_analysis_results(analysis_results, st.session_state.chat_session)
            else:
                st.warning("Please upload a PDF or paste the research paper content before analyzing.")

        # Text input for questions
        question = st.text_input("Ask a question about the paper(s):")

        if st.button("Ask Question"):
            if question and "chat_session" in st.session_state:
                with st.spinner("Generating answer..."):
                    answer = ask_question(st.session_state.chat_session, question)
                if answer:
                    st.subheader("Answer:")
                    st.write(answer)
            elif not question:
                st.warning("Please enter a question before submitting.")
            else:
                st.warning("Please analyze a paper first before asking questions.")

    except google_exceptions.GoogleAPIError as e:
        st.error(f"An error occurred while setting up the model: {str(e)}")
        st.info("Please check your API key and try again. If the problem persists, the service might be temporarily unavailable.")

else:
    st.warning("Please enter your Google API Key to use the application.")

# Add information about advanced features (for future implementation)
st.sidebar.title("Coming Soon")
st.sidebar.info("""
Future enhancements:
- Semantic search across multiple papers
- Integration with reference management tools
- Advanced summarization capabilities
""")
