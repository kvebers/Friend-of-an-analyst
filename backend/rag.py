import os
from typing import Callable
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config_class import Config, config
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import jsonify
from config_class import config


def get_retriever(config: Config) -> any:
    vectorstore = FAISS.load_local(
        config.vector_store_path,
        HuggingFaceEmbeddings(model_name=config.ebmedings_model_name),
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": config.search})
    return retriever

def split_documents(config: Config) -> any:
    all_documents = []
    try:
        text_splitter = CharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separator=" "
        )
        if os.path.exists(config.document_directiory) and os.path.isdir(config.document_directiory):
            for file_name in os.listdir(config.document_directiory):
                file_path = os.path.join(config.document_directiory, file_name)
                if os.path.isfile(file_path):
                    if file_path.endswith(".pdf"):
                        loader = PyPDFLoader(file_path=file_path)
                        documents = loader.load()
                        all_documents.extend(text_splitter.split_documents(documents))
                    else:
                        print("File That should not have been here is here")
        else:
            print(f"No directory {config.document_directiory}")
        return all_documents
    except Exception as e:
        print(f"Error: {e}")
        return []

def create_vector_embedings(config: Config):
    all_documents_splited = split_documents(config=config)
    if all_documents_splited:
        os.makedirs(config.vector_store_path, exist_ok=True)
        embeddings = HuggingFaceEmbeddings(model_name=config.ebmedings_model_name)
        vectorstore = FAISS.from_documents(all_documents_splited, embeddings)
        vectorstore.save_local(config.vector_store_path)


tokenizer = AutoTokenizer.from_pretrained(config.model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(config.model_name)
if (config.create_new_embedings):
    create_vector_embedings(config=config)
retriever = get_retriever(config=config)


def generate_answer_localy(query: str, context: list, max_length=512) -> str:
    """
    Generates the answer localy from query and context
    """
    prompt = f"""\
    Answer the question using only the context below. 
    If you do not know the answer, respond with 'I do not know'.

    Context: {context}

    Question: {query}

    Answer:
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=max_length)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

def rag(query: str):
    """
    Generates json for the api, on failure return json 
    """
    if not query:
        return jsonify({"results": config.error, "query": "None", "context": ["None"]})
    try:
        context = retriever.invoke(query)
        merged_context = [doc.page_content for doc in context]
        answer = generate_answer_localy(query=query, context=merged_context)
        return jsonify({"results": answer, "query": query, "context": merged_context})
    except:
        return jsonify({"results": config.default_error_message, "query": "None", "context": ["None"]})
