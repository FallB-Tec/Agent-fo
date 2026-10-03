from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from pathlib import Path
import os


#function to load_documents
def load_document(docs_path ="./Companies_10k_filing"):
    print(f"Loading documents from {docs_path}")
    
    if not os.path.exists(docs_path):
        raise FileNotFoundError(
            f"The directory {docs_path} does not exist. "
            "Please create it and add your company files"
        )
        
    #Loading all .txt files from the directory
    Loader = DirectoryLoader(
        path=docs_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )
    
    documents = Loader.load()
    
    #checking if there is any pdfs
    if len(documents) == 0:
        raise ValueError(
            f"No .pdf files found in {docs_path}"
            "Please Add files in Companies_10k_filing"
        )
        
    return documents
    
#Making chunks
def split_documents(documents,chunk_size=800,chunk_overlap=0):
    print(f"Splitting documents into chunks documents:{documents}")
    
    #Split the document
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""]
    )
    
    chunks = text_splitter.split_documents(documents=documents)
    
    print(f"Chunks created: {len(chunks)}")
    
    #Add metadata
    
    for chunk in chunks:
        path = Path(chunk.metadata["source"])
        
        company = path.parent.name
        filename = path.stem
        filing_year = filename.split("-")[-1]
        
        chunk.metadata["document_type"] = "10-K"
        chunk.metadata["company"] = company
        chunk.metadata["filing_year"] = int(filing_year)
        chunk.metadata["filing"] = filename
        
    return chunks

#Embedding the chunks than store in vectorDatabase
def create_vectorstore(chunks,embedding_model_name="sentence-transformers/all-MiniLM-L6-v2",persist_directory="db/chroma_db"):
    
    print(f"Creating embeddings and storing in vectorstore with embedding model: {embedding_model_name}")
    
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space":"cosine"})
    
    print(f"Vectorstore created and persisted at {persist_directory}")
    
    return vectorstore
 
  
#separate function to create or update the vector database 
def vector_db_create_update():
     #Load the documents
    documents = load_document(docs_path="C:\\Users\\PcSuu\\OneDrive\\Desktop\\Companies_10k_filing")
        
    # print(f"Documents loaded: {len(documents)}")
        
     #Split the documents into chunks
    chunks = split_documents(documents)
        
    # print(f"Chunks created: {len(chunks)}")
    print(f"First chunk: {chunks[0].page_content}")
        
    vectorstore = create_vectorstore(chunks)
    print(f"Vectorstore created with {vectorstore._collection.count()} vectors")  
