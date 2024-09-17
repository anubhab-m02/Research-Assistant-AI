import streamlit as st
from typing import Tuple, List, Dict, Any
from citation import extract_citations, format_citation
from analysis import compare_papers

def render_analysis_options() -> Tuple[str, List[str]]:
    st.subheader("Analysis Options")
    tab1, tab2 = st.tabs(["Output Format", "Focus Areas"])
    with tab1:
        output_format = st.radio("Select output format:", ("Text", "Bullet Points", "Table", "JSON"))
    with tab2:
        focus_areas = st.multiselect("Select focus areas:", 
            ["Research Question", "Methodology", "Sample Size", "Key Findings", "Limitations", "Implications"],
            default=["Research Question", "Key Findings"]
        )
    return output_format, focus_areas

def render_analysis_results(analysis_results, chat_session):
    for i, result in enumerate(analysis_results):
        st.subheader(f"Analysis of {result['name']}")
        st.markdown(result['analysis'])
        
        # Extract and display citations
        citations = extract_citations(result['content'])
        if citations:
            citation_style = st.selectbox(
                "Select citation style:", 
                ("APA", "MLA", "Chicago"), 
                key=f"citation_style_{i}"
            )
            formatted_citations = [format_citation(c, citation_style) for c in citations]
            st.subheader("Citations")
            for fc in formatted_citations:
                st.write(fc)
        
        st.markdown("---")  # Add a separator between paper analyses

    # Comparative analysis
    if len(analysis_results) >= 2:
        st.subheader("Comparative Analysis")
        comparative_analysis = compare_papers(chat_session, analysis_results)
        
        if isinstance(comparative_analysis, str):
            st.write(comparative_analysis)
        else:
            st.markdown("### Overview")
            st.write(comparative_analysis["overview"])
            
            st.markdown("### Key Similarities")
            st.write(comparative_analysis["similarities"])
            
            st.markdown("### Notable Differences")
            st.write(comparative_analysis["differences"])
            
            st.markdown("### Potential Areas for Future Research")
            st.write(comparative_analysis["future_research"])
