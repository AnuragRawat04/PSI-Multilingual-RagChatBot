# PSI-Multilingual-RagChatBot

A **Multilingual RAG Assistant Chatbot** that enables seamless communication across multiple Indian and international languages. Users can upload documents in [translate:Marathi], [translate:Assamese], [translate:Urdu], [translate:Telugu], [translate:Kannada], [translate:Malayalam], [translate:Odia], or English. The chatbot automatically translates content to English, retrieves relevant information, and generates context-aware responses—all while maintaining the semantic meaning of your documents.

## 📺 Demo & Deployment Note

⚠️ **Deployment Status**: Due to recent changes in LangChain documentation and API compatibility issues, a fully deployed version is currently unavailable. However, you can run the application locally using the quick start guide above.

**Multip-rag.py**:This is the primary file implementing our project with Streamlit. To run the application, use the command:  
`streamlit run multi-rag.py`
**Fastapi.py**:This file contains a FastAPI implementation of the project that exposes the core functionality as an API. During the deployment process, I encountered challenges with the deployment, so I created this FastAPI alternative to ensure successful deployment and better scalability.

**Watch the Project Demo**: Check out our YouTube demo showcasing the full functionality: https://youtu.be/s71MUQZU93Q
We are actively working on resolving the deployment issues and will update this repository with a live link as soon as possible.

---
## ⚡ Quick Start

### Installation & Running

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AnuragRawat04/PSI-Multilingual-RagChatBot.git
   cd PSI-Multilingual-RagChatBot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run multi-rag.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

That's it! The app will launch with a user-friendly interface.

---

## 📝 Supported Languages

- [translate:मराठी] (Marathi)
- [translate:অসমীয়া] (Assamese)
- [translate:اردو] (Urdu)
- [translate:తెలుగు] (Telugu)
- [translate:ಕನ್ನಡ] (Kannada)
- [translate:മലയാളം] (Malayalam)
- [translate:ଓଡ଼ିଆ] (Odia)
- English

---

## 🚀 How It Works

1. **Upload Document**: Select a PDF/text file in any of the 8 supported languages
2. **Automatic Translation**: Content is translated to English for uniform processing
3. **Indexing**: Document is split into chunks and embedded into a vector database
4. **Query**: Ask questions in any of the supported languages
5. **Retrieval**: Relevant document chunks are retrieved using semantic search
6. **Response**: The chatbot generates accurate answers based on the retrieved context

---
## 📂 Project Structure

```
PSI-Multilingual-RagChatBot/
├── README.md
├── requirements.txt
├── multi-rag.py              # Main Streamlit app
├── .env                       # API keys (create this)
└── data/                      # Sample documents (optional)
```

---

## 🔧 Configuration

Set up your `.env` file with required API keys:

```env
GOOGLE_API_KEY=your_google_api_key
```

---

## 💡 Use Cases

- Customer support in multiple Indian languages
- Multilingual document Q&A systems
- Educational assistants supporting Indian languages
- Business knowledge bases with language flexibility
- Legal and healthcare document analysis



