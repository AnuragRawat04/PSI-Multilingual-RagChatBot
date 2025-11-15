from fastapi import FastAPI,File,Form,UploadFile
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
import easyocr
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from googletrans import Translator
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import Chroma
api_key=os.getenv("GOOGLE_API_KEY")
print(api_key)
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=api_key)
hugging_api_key = os.getenv("HuggingFace")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/LaBSE",
    model_kwargs={"device": "cpu"}  
)


translator = Translator()
UPLOAD_DIRECTORY=r"Documnent"
app=FastAPI()
@app.post("/multilingual_chat_bot/")
async def multilingual_chat_bot(file:UploadFile=File(),doc_lang:str=Form(...),Final_language:str=Form(...),input_prompt:str=Form(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
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

    with open(file_location, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    print(doc_lang)
    reader = easyocr.Reader(lang_map[doc_lang], download_enabled=True)
    documents=[]
    loader = PyPDFLoader(file_location)
    docs = loader.load()
    for i, page in enumerate(docs):
        page.metadata["source"] = file.filename
        page.metadata["path"] = file_location
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
    response = rag_chain.invoke({"input": input_prompt})

    
    return {"response":response['answer'],"full_response":response}


