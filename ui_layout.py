import streamlit as st
from citation import extract_citations, format_citation
from analysis import analyze_papers, compare_papers, ask_question, summarize_paper, find_related_papers
from pdf_utils import extract_text_from_pdf
from semantic_search import perform_semantic_search, highlight_text
import time

def render_sidebar():
    with st.sidebar:
        st.title("📚 Research Assistant")
        api_key = st.text_input("Enter your Google API Key:", type="password", value=st.session_state.api_key, key="api_key_input")
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            st.experimental_rerun()
        
        st.markdown("---")
        st.subheader("About")
        st.info(
            "This app helps you analyze research papers, extract citations, "
            "perform semantic searches, and ask questions about the content."
        )
        
        st.markdown("---")
        st.subheader("Future Features (Let's Collaborate!)")
        st.markdown(
            """
            <div style="background-color: #004333; color: #b0e892; padding: 10px; border-radius: 5px;">
            • Reference management integration (Zotero, Mendeley)<br>
            • Automated literature review generation<br>
            • Plagiarism detection and similarity checking<br>
            • Integration with academic databases (e.g., PubMed, arXiv)<br>
            • Collaborative research workspace<br>
            • Custom AI model fine-tuning for specific research domains<br>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        st.subheader("Settings")

        # AI Model Temperature
        if 'ai_temperature' not in st.session_state:
            st.session_state.ai_temperature = 0.7
        ai_temperature = st.slider("AI Creativity (Temperature)", 0.0, 2.0, st.session_state.ai_temperature, 0.1)
        if ai_temperature != st.session_state.ai_temperature:
            st.session_state.ai_temperature = ai_temperature
            st.success(f"AI temperature set to {ai_temperature}. This will affect the creativity of AI-generated content.")

        # Max Token Limit
        if 'max_tokens' not in st.session_state:
            st.session_state.max_tokens = 1024
        max_tokens = st.number_input("Max Output Tokens", 256, 4096, st.session_state.max_tokens, 128)
        if max_tokens != st.session_state.max_tokens:
            st.session_state.max_tokens = max_tokens
            st.success(f"Max output tokens set to {max_tokens}. This will limit the length of AI-generated responses.")

        # Citation Style
        if 'default_citation_style' not in st.session_state:
            st.session_state.default_citation_style = 'APA'
        citation_style = st.selectbox("Default Citation Style", ['APA', 'MLA', 'Chicago'], index=['APA', 'MLA', 'Chicago'].index(st.session_state.default_citation_style))
        if citation_style != st.session_state.default_citation_style:
            st.session_state.default_citation_style = citation_style
            st.success(f"Default citation style set to {citation_style}.")

        if st.button("Clear All Data", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("All data cleared. The app will refresh momentarily.")
            st.experimental_rerun()

        st.markdown("---")
        st.markdown("Version 1.1.0")
        st.markdown("[Report a bug](https://github.com/anubhab-m02/Research-Assistant-AI/issues)")
        st.markdown("[Suggest a feature](https://github.com/anubhab-m02/Research-Assistant-AI/issues)")

def render_main_content():
    st.title("Enhanced Research Paper Analysis Assistant")

    # Paper input section
    st.header("Input Research Paper(s)")
    st.markdown("Upload your research papers or paste their content for analysis.")
    input_method = st.radio("Choose input method:", ("Upload PDF", "Paste Text"))

    if input_method == "Upload PDF":
        st.markdown("Upload one or more PDF files of research papers you want to analyze.")
        uploaded_files = st.file_uploader("Upload research paper(s) (PDF)", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            st.session_state.paper_contents = []
            for uploaded_file in uploaded_files:
                with st.spinner(f"Extracting text from {uploaded_file.name}..."):
                    content = extract_text_from_pdf(uploaded_file)
                    st.session_state.paper_contents.append({"name": uploaded_file.name, "content": content})
    else:
        st.markdown("Paste the text content of a research paper you want to analyze.")
        paper_content = st.text_area("Paste your research paper content here:", height=300)
        if paper_content:
            st.session_state.paper_contents = [{"name": "Pasted Content", "content": paper_content}]

    if st.session_state.paper_contents:
        st.write(f"Number of papers loaded: {len(st.session_state.paper_contents)}")

    # Functionality selection
    st.header("Choose Functionality")
    functionality = st.selectbox("Select what you want to do:", 
                                 ["Analyze Papers", "Extract Citations", "Semantic Search", "Ask Questions", "Find Related Papers", "Summarize Paper"])

    if functionality == "Analyze Papers":
        render_analysis_options()
    elif functionality == "Extract Citations":
        render_extract_citations()
    elif functionality == "Semantic Search":
        render_semantic_search()
    elif functionality == "Ask Questions":
        render_ask_questions()
    elif functionality == "Find Related Papers":
        render_find_related_papers()
    elif functionality == "Summarize Paper":
        render_summarize_paper()

def render_analysis_options():
    st.subheader("Analysis Options")
    tab1, tab2 = st.tabs(["Output Format", "Focus Areas"])
    with tab1:
        output_format = st.radio("Select output format:", ("Text", "Bullet Points", "Table", "JSON"))
    with tab2:
        focus_areas = st.multiselect("Select focus areas:", 
            ["Research Question", "Methodology", "Sample Size", "Key Findings", "Limitations", "Implications"],
            default=["Research Question", "Key Findings"]
        )

    if st.button("🔍 Analyze Paper(s)", key="analyze_button"):
        if st.session_state.paper_contents:
            st.session_state.analysis_results = []  # Clear previous results
            total_papers = len(st.session_state.paper_contents)
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, paper in enumerate(st.session_state.paper_contents):
                status_text.text(f"Analyzing paper {i+1} of {total_papers}: {paper['name']}")
                try:
                    result = analyze_papers(st.session_state.chat_session, [paper], focus_areas, output_format)
                    st.session_state.analysis_results.extend(result)
                except Exception as e:
                    st.error(f"Error analyzing {paper['name']}: {str(e)}")
                progress_bar.progress((i + 1) / total_papers)

            status_text.text("Analysis complete!")
            time.sleep(1)  # Give users a moment to see the "complete" message
            status_text.empty()
            progress_bar.empty()
        else:
            st.warning("Please input at least one research paper before analyzing.")

    # Display analysis results
    if st.session_state.analysis_results:
        render_analysis_results(st.session_state.analysis_results, st.session_state.chat_session)

        # Save analysis button
        if st.button("💾 Save Analysis", key="save_analysis_button", use_container_width=True):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"analysis_results_{timestamp}.txt"
            with open(filename, "w") as f:
                for result in st.session_state.analysis_results:
                    f.write(f"Analysis of {result['name']}:\n")
                    f.write(result['analysis'])
                    f.write("\n\n")
            st.download_button(label="Download Analysis", data=open(filename, "rb"), file_name=filename, mime="text/plain", key="download_analysis_button")
    else:
        st.info("No analysis results to display. Please analyze papers first.")

def render_analysis_results(analysis_results, chat_session):
    for i, result in enumerate(analysis_results):
        with st.expander(f"Analysis of {result['name']}", expanded=True):
            st.markdown(result['analysis'])

    # Comparative analysis
    if len(analysis_results) >= 2:
        with st.expander("Comparative Analysis", expanded=True):
            st.subheader("Comparative Analysis")
            comparative_analysis = compare_papers(chat_session, analysis_results)
            
            if isinstance(comparative_analysis, str):
                st.write(comparative_analysis)
            else:
                for section, content in comparative_analysis.items():
                    if content:
                        st.markdown(f"### {section.capitalize()}")
                        st.write(content)

def render_semantic_search():
    st.subheader("Semantic Search")
    st.markdown("Search for specific information across all uploaded papers using natural language queries.")
    search_query = st.text_input("Enter your search query:")
    if search_query and st.session_state.paper_contents:
        corpus = [paper['content'] for paper in st.session_state.paper_contents]
        search_results = perform_semantic_search(search_query, corpus)
        st.subheader("Top Matching Papers")
        for result in search_results:
            paper = st.session_state.paper_contents[result['corpus_id']]
            st.markdown(f"- **{paper['name']}** (Relevance: {result['score']:.2f})")
            highlighted_text = highlight_text(paper['content'], search_query)
            st.markdown(highlighted_text, unsafe_allow_html=True)

def render_ask_questions():
    st.subheader("Ask Questions")
    st.markdown("Ask specific questions about the content of the uploaded paper(s) and get AI-generated answers.")
    for q, a in st.session_state.chat_history:
        st.text_input("Question:", value=q, disabled=True)
        st.text_area("Answer:", value=a, disabled=True)
    
    question = st.text_input("Ask a new question about the paper(s):")
    if st.button("🤔 Ask Question", key="ask_question_button"):
        if question and st.session_state.chat_session:
            with st.spinner("Generating answer..."):
                answer = ask_question(st.session_state.chat_session, question)
            if answer:
                st.markdown(f"**Answer:** {answer}")
                st.session_state.chat_history.append((question, answer))
        elif not question:
            st.warning("Please enter a question before submitting.")
        else:
            st.warning("Please analyze a paper first before asking questions.")

def render_extract_citations():
    st.subheader("Extract Citations")
    if st.session_state.paper_contents:
        for i, paper in enumerate(st.session_state.paper_contents):
            with st.expander(f"Citations from {paper['name']}", expanded=True):
                citations = extract_citations(paper['content'])
                if citations:
                    citation_style = st.selectbox(f"Select citation style for {paper['name']}:", 
                                                  ("APA", "MLA", "Chicago"), 
                                                  index=["APA", "MLA", "Chicago"].index(st.session_state.default_citation_style),
                                                  key=f"citation_style_{i}")
                    formatted_citations = [format_citation(c, citation_style) for c in citations]
                    for j, fc in enumerate(formatted_citations):
                        st.markdown(f"{j+1}. {fc}")
                else:
                    st.write("No citations found in this paper.")
    else:
        st.warning("Please upload or paste paper content before extracting citations.")

def render_find_related_papers():
    st.subheader("Find Related Papers")
    if st.session_state.analysis_results:
        with st.spinner("Finding related papers based on your analysis..."):
            try:
                related_papers = find_related_papers(st.session_state.chat_session, st.session_state.analysis_results)
                
                if related_papers:
                    st.write("Related Papers:")
                    for paper in related_papers:
                        st.markdown(f"- [{paper['title']}]({paper['url']})")
                else:
                    st.warning("No related papers found. The AI model might not have generated suggestions in the expected format.")
            except Exception as e:
                st.error(f"An error occurred while finding related papers: {str(e)}")
    else:
        st.warning("Please analyze papers first before finding related papers.")

def render_summarize_paper():
    st.subheader("Summarize Paper")
    if st.session_state.paper_contents:
        # Create a list of paper names
        paper_names = [paper['name'] for paper in st.session_state.paper_contents]
        
        # Let the user select which paper to summarize
        selected_paper_name = st.selectbox("Select a paper to summarize:", paper_names)
        
        # Find the selected paper in the session state
        selected_paper = next((paper for paper in st.session_state.paper_contents if paper['name'] == selected_paper_name), None)
        
        if selected_paper:
            if st.button(f"Summarize {selected_paper_name}", key=f"summarize_{selected_paper_name}"):
                with st.spinner(f"Summarizing {selected_paper_name}..."):
                    summary = summarize_paper(st.session_state.chat_session, selected_paper['content'])
                    st.markdown(f"**Summary of {selected_paper_name}:**")
                    st.write(summary)
        else:
            st.error("Selected paper not found. Please try again.")
    else:
        st.warning("Please upload or paste paper content before summarizing.")