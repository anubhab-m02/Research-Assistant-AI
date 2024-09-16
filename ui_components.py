import streamlit as st
from typing import Tuple, List, Dict, Any
from citation import extract_citations, format_citation
from visualization import create_chart
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

def render_analysis_results(analysis_results: List[Dict[str, Any]], chat_session):
    st.subheader("Analysis Results:")
    for result in analysis_results:
        with st.expander(f"Analysis of {result['name']}"):
            st.write(result['analysis'])

            # Citation extraction and formatting
            citations = extract_citations(result['content'])
            if citations:
                st.subheader("Extracted Citations:")
                citation_style = st.selectbox("Select citation style:", ("APA", "MLA", "Chicago"))
                formatted_citations = [format_citation(c, citation_style) for c in citations]
                for fc in formatted_citations:
                    st.write(fc)

    # Comparative analysis for multiple papers
    if len(analysis_results) > 1:
        st.subheader("Comparative Analysis")
        comparative_analysis = compare_papers(chat_session, analysis_results)
        st.write(comparative_analysis)

    # Data visualization
    st.subheader("Data Visualization")
    chart_type = st.selectbox("Select chart type:", ("Bar", "Pie", "Histogram"))
    data_to_visualize = st.text_input("Enter comma-separated values to visualize:")
    if data_to_visualize:
        try:
            data = [float(x.strip()) for x in data_to_visualize.split(',')]
            fig = create_chart(data, chart_type)
            if fig:
                st.pyplot(fig)
        except ValueError:
            st.warning("Invalid data format. Please enter numeric values separated by commas.")
