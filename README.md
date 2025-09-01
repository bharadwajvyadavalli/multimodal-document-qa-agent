# 📄 Multimodal Document QA Assistant

Simple Q&A assistant for PDFs containing text, tables, and charts.

## ✨ Features
- Extract and understand text, tables, and images from PDFs
- Answer questions using GPT-4 (text) and GPT-4V (images/charts)
- Highlight source locations in the original document
- Simple, clean codebase (~500 lines)

## 🚀 Quick Start

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the app:
```bash
streamlit run app.py
```

### 3. Add your OpenAI API key in the sidebar

### 4. Upload a PDF and ask questions!

## 📊 Example Questions
- "What is the revenue in Q3?" (reads from tables)
- "What trend does the sales chart show?" (analyzes images)
- "Summarize the key findings" (combines multiple sources)
- "What are the main conclusions?" (extracts from text)

## 🛠️ Tech Stack
- **PyMuPDF** - PDF processing and text extraction
- **OpenAI GPT-4/GPT-4V** - Natural language understanding and vision analysis
- **Streamlit** - Web interface
- **Pillow** - Image processing

## 📁 Project Structure
```
multimodal-doc-qa/
├── app.py                 # Streamlit UI
├── requirements.txt       # Dependencies
├── src/
│   ├── pdf_processor.py   # PDF content extraction
│   ├── qa_engine.py       # Question answering logic
│   └── visualizer.py      # Source highlighting
├── examples/
│   └── sample_report.pdf  # Demo PDF (add your own)
└── README.md             # This file
```

## 🔧 How It Works

1. **PDF Processing**: Extracts text, identifies tables, and captures images from uploaded PDFs
2. **Content Analysis**: Finds relevant content based on the question using keyword matching
3. **Answer Generation**: 
   - Uses GPT-3.5/4 for text and table-based questions
   - Uses GPT-4 Vision for chart and image analysis
4. **Source Attribution**: Highlights the exact location in the PDF where the answer was found

## 💡 Future Improvements
- Add semantic search using embeddings for better content matching
- Support for multiple PDF uploads and cross-document QA
- Export answers with citations
- Add support for more document formats (Word, Excel)
- Implement local LLM option for privacy-sensitive documents

## 📝 License
MIT License - Feel free to use and modify

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.