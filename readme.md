# Research Assistant AI

## Overview

This application is a Research Assistant AI built using Streamlit. It allows users to upload research papers in PDF format or paste their content, and then perform various analyses such as extracting citations, performing semantic searches, asking questions, and summarizing the papers. The application leverages Google Generative AI for natural language processing tasks.

## Features

- **Upload and Analyze Research Papers**: Upload PDF files or paste text content for analysis.
- **Extract Citations**: Extract and format citations from the research papers.
- **Semantic Search**: Perform semantic searches across the uploaded papers.
- **Ask Questions**: Ask specific questions about the content of the papers and get AI-generated answers.
- **Summarize Papers**: Generate concise summaries of the research papers.
- **Find Related Papers**: Suggest related research papers based on the analysis.

## Prerequisites

- Python 3.10 or higher
- Google API Key for accessing Google Generative AI

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/anubhab-m02/Research-Assistant-AI.git
    cd research-paper-analysis-assistant
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. **Set up your Google API Key**:
    - Obtain an API key from Google Cloud Platform.

## Running the Application

1. **Start the Streamlit application**:
    ```sh
    streamlit run app.py
    ```

2. **Open your web browser** and navigate to `http://localhost:8501` to access the application.

## Code Structure

- **app.py**: Main entry point of the application. Configures the Streamlit page and handles the main logic.
  ```python:app.py
  startLine: 1
  endLine: 60
  ```

- **ui_layout.py**: Contains functions to render the sidebar and main content layout.
  ```python:ui_layout.py
  startLine: 1
  endLine: 283
  ```

- **analysis.py**: Functions for analyzing research papers, comparing papers, and summarizing content.
  ```python:analysis.py
  startLine: 1
  endLine: 114
  ```

- **pdf_utils.py**: Utility functions for extracting text from PDF files.
  ```python:pdf_utils.py
  startLine: 1
  endLine: 19
  ```

- **citation.py**: Functions for extracting and formatting citations.
  ```python:citation.py
  startLine: 1
  endLine: 22
  ```

- **semantic_search.py**: Functions for performing semantic searches and highlighting text.
  ```python:semantic_search.py
  startLine: 1
  endLine: 29
  ```

- **reference_management.py**: Functions for managing references using Zotero.
  ```python:reference_management.py
  startLine: 1
  endLine: 20
  ```

## Potential Vulnerabilities

1. **API Key Exposure**: Ensure that the Google API key is kept secure and not exposed in the code or version control.

2. **Input Validation**: The application does not perform extensive validation on user inputs, which could lead to issues such as injection attacks or processing of malformed data.

3. **Error Handling**: While the application includes basic error handling, it could be improved to handle more specific cases and provide more informative error messages.

4. **PDF Extraction**: The text extraction from PDFs relies on PyPDF2, which may not handle all PDF formats correctly, especially scanned or protected PDFs.

5. **Session State Management**: The use of Streamlit's session state is convenient but may lead to issues if not managed properly, especially with concurrent users.

## Contributing

1. **Fork the repository**.
2. **Create a new branch** for your feature or bugfix:
    ```sh
    git checkout -b feature-name
    ```
3. **Commit your changes**:
    ```sh
    git commit -m "Description of your changes"
    ```
4. **Push to the branch**:
    ```sh
    git push origin feature-name
    ```
5. **Create a pull request**.

For any issues or feature requests, please open an issue on the [GitHub repository](https://github.com/anubhab-m02/Research-Assistant-AI/issues).
