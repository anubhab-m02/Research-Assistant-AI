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
        st.write(f"Analyzing paper: {paper['name']}")
        st.write(f"Paper content length: {len(paper['content'])} characters")
        with st.spinner(f"Analyzing {paper['name']}..."):
            analysis_prompt = f"Analyze the following research paper content. Focus on: {', '.join(focus_areas)}. Format the output as {output_format}."
            analysis = analyze_research_paper(chat_session, f"{analysis_prompt}\n\n{paper['content'][:1000]}...")  # Limit content for logging
            if analysis:
                analysis_results.append({"name": paper['name'], "analysis": analysis, "content": paper['content']})
                st.success(f"Analysis complete for {paper['name']}")
            else:
                st.warning(f"No analysis generated for {paper['name']}")
        progress_bar.progress((i + 1) / len(papers))
    return analysis_results

def compare_papers(chat_session, analysis_results):
    if len(analysis_results) < 2:
        return "At least two papers are required for comparison."

    paper_titles = [result['name'] for result in analysis_results]
    prompt = f"""Compare and contrast the following papers: {', '.join(paper_titles)}. 
    Provide a brief overview of each paper, then discuss:
    1. Key similarities between the papers
    2. Notable differences between the papers
    3. Potential areas for future research based on these papers
    
    Format your response with clear headings for each section, but do not repeat the headings at the end."""

    comparison = analyze_research_paper(chat_session, prompt)

    # Split the comparison into sections
    sections = comparison.split('\n\n')
    result = {
        "overview": "",
        "similarities": "",
        "differences": "",
        "future_research": ""
    }

    current_section = "overview"
    for section in sections:
        if "Key similarities" in section:
            current_section = "similarities"
        elif "Notable differences" in section:
            current_section = "differences"
        elif "Potential areas for future research" in section:
            current_section = "future_research"
        
        result[current_section] += section + "\n\n"

    # Remove any trailing newlines and spaces
    for key in result:
        result[key] = result[key].strip()

    return result

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

@st.cache_data
def summarize_paper(_chat_session, paper_content: str) -> str:
    summary_prompt = "Provide a concise summary of the following research paper, highlighting the main research question, methodology, key findings, and conclusions:"
    return analyze_research_paper(_chat_session, f"{summary_prompt}\n\n{paper_content}")

def find_related_papers(chat_session, analysis_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    # Combine all analyses into one context
    combined_analysis = "\n\n".join([f"Paper: {r['name']}\nAnalysis: {r['analysis']}" for r in analysis_results])
    
    prompt = f"""Based on the following analysis of research papers, suggest 5 related research papers that would be relevant for further reading. For each suggestion, provide the title and a URL where it can be found (use Google Scholar links if available).

    {combined_analysis}

    Please format your response as a list, with each item in the following format:
    - [Paper Title](URL)
    """
    
    response = analyze_research_paper(chat_session, prompt)
    
    # Parse the response to extract paper titles and URLs
    related_papers = []
    for line in response.split('\n'):
        if line.strip().startswith('-'):
            parts = line.split('](')
            if len(parts) == 2:
                title = parts[0].strip('- [')
                url = parts[1].strip(')')
                related_papers.append({"title": title, "url": url})
    
    return related_papers
