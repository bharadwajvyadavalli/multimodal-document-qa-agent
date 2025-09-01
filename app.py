import streamlit as st
from src.pdf_processor import PDFProcessor
from src.qa_engine import QAEngine
from src.visualizer import PDFVisualizer
import os

# Page config
st.set_page_config(page_title="Document QA Assistant", page_icon="📄")
st.title("📄 Multimodal Document QA Assistant")
st.caption("Ask questions about PDFs with text, tables, and charts")

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = None
    st.session_state.qa_engine = None

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    st.info("Uses GPT-4 Vision for chart/image understanding")

# File upload
uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])

if uploaded_file:
    # Process PDF
    with st.spinner("Processing PDF..."):
        # Save uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process the PDF
        processor = PDFProcessor("temp.pdf")
        content = processor.extract_all()
        
        # Initialize QA engine
        qa_engine = QAEngine(content)
        
        # Store in session state
        st.session_state.processor = processor
        st.session_state.qa_engine = qa_engine
        
    # Show PDF info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pages", content['num_pages'])
    with col2:
        st.metric("Tables", len(content['tables']))
    with col3:
        st.metric("Images", len(content['images']))
    
    # Question input
    st.divider()
    question = st.text_input("💬 Ask a question about the document:")
    
    if question and st.button("Get Answer", type="primary"):
        with st.spinner("Finding answer..."):
            # Get answer
            answer, source = st.session_state.qa_engine.answer(question)
            
            # Display answer
            st.success("**Answer:**")
            st.write(answer)
            
            # Show source
            if source:
                st.info(f"📍 Source: {source['type']} on page {source['page']}")
                
                # Visualize source in PDF
                if source['type'] != 'general':
                    visualizer = PDFVisualizer("temp.pdf")
                    img = visualizer.highlight_area(
                        source['page'] - 1, 
                        source.get('bbox', None)
                    )
                    st.image(img, caption=f"Page {source['page']}")

else:
    st.info("👆 Please upload a PDF to start")

# Cleanup
if os.path.exists("temp.pdf"):
    os.remove("temp.pdf")