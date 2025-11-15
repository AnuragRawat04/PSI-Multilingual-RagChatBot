from langchain_community.document_loaders import PyPDFLoader
import easyocr
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from dotenv import load_dotenv
import base64
from googletrans import Translator

#To display the pdf page
def display_pdf_page(file_path, page_number):
    base64_pdf = base64.b64encode(open(file_path, "rb").read()).decode("utf-8")
    return f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}#page={page_number}" 
            width="700" height="500" type="application/pdf"></iframe>
    """

load_dotenv()

# HuggingFace embeddings (Labse Model)
hugging_api_key = os.getenv("HuggingFace")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/LaBSE",
    model_kwargs={"device": "cpu"}  
)

st.title("BharatDocs Chat")
st.write("Upload PDFs in any Indian language and chat in English with document-aware answers.")

# Groq API Key
api_key = st.text_input("Enter your Groq API KEY:", type="password")
#api_key="ikdjbfnjk"
if api_key:
    # llm = ChatGroq(groq_api_key=api_key, model="openai/gpt-oss-120b")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=os.getenv("GOOGLE_API_KEY"))
    translator = Translator()

    uploaded_files = st.file_uploader("📂 Upload PDFs", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        # LUser can select the labguage of pdf which they want to be translated
        language_option = st.selectbox(
            "Please select the language of the PDF:",
            options=[
                "Marathi",
                "Assamese",
                "Urdu",
                "Telugu",
                "Kannada",
                "Malayalam",
                "Odia",
                "English"
            ]
        )
        lang_map = {
            "Marathi": ['mr', 'en'],
            "Assamese": ['as', 'en'],
            "Urdu": ['ur', 'en'],
            "Telugu": ['te','en'],
            "Kannada": ['kn','en'],
            "Malayalam": ['ml','en'],
            "Odia": ['or','en'],
            "English": ['en']
        }

        reader = easyocr.Reader(lang_map[language_option], download_enabled=True)
        documents = []

        for uploaded_file in uploaded_files:
            temp_path = f"./{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            loader = PyPDFLoader(temp_path)
            docs = loader.load()

            for i, page in enumerate(docs):
                page.metadata["source"] = uploaded_file.name
                page.metadata["path"] = temp_path
                page.metadata["page"] = i

                if not page.page_content.strip():
                    ocr_text = ""
                    images = page.images if hasattr(page, "images") else []
                    for img in images:
                        ocr_result = reader.readtext(img, detail=0)
                        ocr_text += " ".join(ocr_result) + "\n"

                    # Translate to English
                    page.page_content = translator.translate(ocr_text, src='auto', dest='en').text

            documents.extend(docs)

        # Split the document into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        splits = splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(splits, embedding=embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an assistant. The retrieved context can be in any Indian language or English. "
             "Translate all retrieved context to English and answer the user's question in English. "
             "Keep the answer concise and accurate from the pdf(max 5 sentences).\n\n{context}"),
            ("human", "{input}")
        ])
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        #Streamlit 
        user_input = st.text_input("💬 Your Question:")
        if user_input:
            response = rag_chain.invoke({"input": user_input})
            st.write("🤖 Assistant:")
            st.write(response["answer"])

            # Show sources
            if "context" in response:
                st.write("📌 Sources:")
                for doc in response["context"]:
                    file_name = doc.metadata.get("source", "Unknown file")
                    page_num = doc.metadata.get("page", 0) + 1
                    file_path = doc.metadata.get("path", None)

                    st.markdown(f"**📄 {file_name}** - Page {page_num}")
                    if file_path:
                        with st.expander(f"🔍 Preview Page {page_num} from {file_name}"):
                            st.markdown(display_pdf_page(file_path, page_num), unsafe_allow_html=True)

            # Clean up temp files
            for uploaded_file in uploaded_files:
                temp_path = f"./{uploaded_file.name}"
                if os.path.exists(temp_path):
                    os.remove(temp_path)

else:
    st.warning("⚠️ Please enter your Groq API key.")





