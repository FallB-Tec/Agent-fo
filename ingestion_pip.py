from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
import os


#function to load_documents
def load_document(docs_path ="Companies_10k_filing"):
    print(f"Loading documents from {docs_path}")
    
    if not os.path.exists(docs_path):
        raise FileNotFoundError(
            f"The directory {docs_path} does not exist. "
            "Please create it and add your company files"
        )
        
    #Loading all .txt files from the directory
    Loader = DirectoryLoader(
        path=docs_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )
    
    documents = Loader.load()
    
    #checking if there is any pdfs
    if len(documents) == 0:
        f"No .pdf files found in {docs_path}"
        "Please Add files in Companies_10k_filing"
        
        return documents
    
