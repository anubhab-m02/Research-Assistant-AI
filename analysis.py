import streamlit as st
from google.api_core import exceptions as google_exceptions
from typing import List, Dict, Any

def analyze_research_paper(chat_session, prompt: str) -> str:
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except google_exceptions.GoogleAPIError as e:
        st.error(f"An error occurred while analyzing the paper: {str(e)}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

def analyze_papers(chat_session, papers: List[Dict[str, Any]], focus_areas: List[str], output_format: str) -> List[Dict[str, Any]]:
    analysis_results = []
    progress_bar = st.progress(0)
    for i, paper in enumerate(papers):
        with st.spinner(f"Analyzing {paper['name']}..."):
            analysis_prompt = f"Analyze the following research paper content. Focus on: {', '.join(focus_areas)}. Format the output as {output_format}."
            analysis = analyze_research_paper(chat_session, f"{analysis_prompt}\n\n{paper['content']}")
            if analysis:
                analysis_results.append({"name": paper['name'], "analysis": analysis, "content": paper['content']})
        progress_bar.progress((i + 1) / len(papers))
    return analysis_results

def compare_papers(chat_session, analysis_results: List[Dict[str, Any]]) -> str:
    comparative_prompt = f"Compare the following research papers, highlighting their key aspects, similarities, differences, and potential research areas: {', '.join([r['name'] for r in analysis_results])}"
    return analyze_research_paper(chat_session, comparative_prompt)

def ask_question(chat_session, question: str) -> str:
    try:
        response = chat_session.send_message(question)
        return response.text
    except google_exceptions.GoogleAPIError as e:
        st.error(f"An error occurred while answering the question: {str(e)}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None
