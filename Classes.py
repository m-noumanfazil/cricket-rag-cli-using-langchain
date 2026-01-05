import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

class VectorDB:
    def __init__(self, collection_name: str = "cricket_rules", embedding_model: str = None):
        """Initialize Chroma vector store with HuggingFace embeddings."""
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model or "sentence-transformers/all-mpnet-base-v2"
        self.embedding_engine = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        self.persist_directory = "./chroma_cricket_db"

        # Initialize Chroma store
        self.store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embedding_engine,
            persist_directory=self.persist_directory
        )

        # Text splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " "]
        )
        print(f"[INFO] VectorDB initialized with collection '{self.collection_name}'.")

    def add_documents(self, paths: List[str]):
        """Load PDFs and embed only if database is empty."""
        # Check if DB is empty
        if len(self.store.get()["documents"]) > 0:
            print("[INFO] ChromaDB already has documents. Skipping re-embedding.")
            return

        all_chunks = []
        for path in paths:
            loader = PyPDFLoader(path)
            documents = loader.load()
            chunks = self.splitter.split_documents(documents)
            all_chunks.extend(chunks)

        self.store.add_documents(all_chunks)
        print(f"[INFO] {len(all_chunks)} chunks added to VectorDB.")


class RAGAssistant:
    def __init__(self):
        """Initialize RAG Assistant with retriever + Groq LLM + prompt."""
        self.llm = self._initialize_llm()
        self.vector_db = VectorDB()

        system_msg = SystemMessagePromptTemplate.from_template(
        """You are an expert assistant on Cricket Rules. 
        Answer ONLY using the context chunks provided. 
        If the answer is not contained in the context, respond exactly: 
        'I don't know. No relevant information found.' 
        Do NOT make guesses, assumptions, or add information not present in the context. 
        Do NOT hallucinate. Do NOT infer. Treat the context as the sole authority."""
        )

        human_msg = HumanMessagePromptTemplate.from_template(
            "Question: {question}\nContext: {context}"
        )

        self.prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])
        self.chain = self.prompt | self.llm

        print("[INFO] RAGAssistant initialized successfully.")

    def _initialize_llm(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Groq API key not found in environment variables!")

        return ChatGroq(
            model="qwen/qwen3-32b",
            temperature=0,
            reasoning_format="hidden",
            max_retries=2
        )

    def add_documents(self, paths: List[str]):
        self.vector_db.add_documents(paths)

    def query(self, question: str, n_results: int = 5):
        """RAG query: retrieve + LLM answer, also print relevant chunks."""
        # Step 1: Retrieve relevant chunks
        docs = self.vector_db.store.similarity_search(question, k=n_results)
    
        if not docs:
            print("[INFO] No relevant chunks found for this question.")
            return "I don't know. No relevant information found."
    
        # Step 2: Print the retrieved chunks
        print("[INFO] Retrieved relevant chunks for this query:")
        print("-" * 40)
        for i, doc in enumerate(docs, 1):
            print(f"Chunk {i}:\n{doc.page_content}\n{'-'*40}")
    
        # Step 3: Prepare context for LLM
        context = "\n\n".join(doc.page_content for doc in docs)
    
        # Step 4: Pass to LLM
        response = self.chain.invoke({"question": question, "context": context})
        return response.content


    def show_relevant_chunks(self, question: str, n_results: int = 3):
        """Just print relevant chunks without passing to LLM."""
        docs = self.vector_db.store.similarity_search(question, k=n_results)
        if not docs:
            print("[INFO] No relevant chunks found for this question.")
            return

        print("[INFO] Retrieved relevant chunks:")
        print("-" * 40)
        for i, doc in enumerate(docs, 1):
            print(f"Chunk {i}:\n{doc.page_content}\n{'-'*40}")
