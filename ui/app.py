import streamlit as st
import tempfile
import os
import sys

# Add parent directory to path to enable imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from data_processing.ingest import load_csv
from data_processing.vector_store import VectorStore
from agents.option_finder import OptionFinderAgent
from agents.pros_cons import ProsConsAgent
from agents.decision import DecisionAgent
from workflow.orchestrator import build_workflow
from llm.gemini_wrapper import GeminiLLMWrapper
from config import GOOGLE_API_KEY

st.title("Multi-Agent Decision System")

uploaded = st.file_uploader("Upload CSV", type='csv')
query = st.text_input("Describe your objective/query:")

if uploaded and query:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
        tmp_file.write(uploaded.getvalue())
        tmp_file_path = tmp_file.name
    
    try:
        # Process the data
        with st.spinner("Loading and processing data..."):
            docs = load_csv(tmp_file_path)
            vs = VectorStore()
            vs.add_documents(docs)
        
        # Initialize LLM and agents
        with st.spinner("Initializing AI agents..."):
            llm = GeminiLLMWrapper(api_key=GOOGLE_API_KEY)
            option_finder = OptionFinderAgent(vs)
            pros_cons = ProsConsAgent(llm)
            decision = DecisionAgent(llm)

        # Build and run workflow
        with st.spinner("Analyzing options and generating recommendation..."):
            workflow = build_workflow(option_finder, pros_cons, decision)
            state = {"query": query}
            result = workflow.invoke(state)
        
        # Display results
        st.subheader("Found Options")
        if 'candidates' in result:
            for i, candidate in enumerate(result['candidates']):
                st.write(f"**Option {i+1}:** {candidate.page_content}")
        
        st.subheader("Analysis")
        if 'analyses' in result:
            for analysis in result['analyses']:
                with st.expander(f"Analysis for: {analysis['option'][:50]}..."):
                    st.write(analysis['analysis'])
        
        st.subheader("Final Recommendation")
        st.write(result['recommendation'])
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
