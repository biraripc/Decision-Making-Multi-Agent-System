from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document as LangchainDocument

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.db = None
    
    def add_documents(self, documents):
        # Convert our Document objects to Langchain Documents
        langchain_docs = []
        for doc in documents:
            langchain_doc = LangchainDocument(
                page_content=doc.content,
                metadata=doc.metadata
            )
            langchain_docs.append(langchain_doc)
        
        self.db = FAISS.from_documents(langchain_docs, self.embeddings)
    
    def similarity_search(self, query, k=5):
        if self.db is None:
            return []
        return self.db.similarity_search(query, k=k)
