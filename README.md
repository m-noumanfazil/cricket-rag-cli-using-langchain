# Cricket RAG CLI Assistant

A simple CLI-based Retrieval-Augmented Generation (RAG) application that answers cricket-related questions using custom documents. This project demonstrates how to build a small RAG system using a PDF of the MCC 2017 Laws of Cricket, embedding it into a vector database with Chroma, and querying it with an LLM (ChatGroq).

--
# Features

-> Load a single PDF document (MCC 2017 cricket rules) into a vector database.

-> Perform semantic search to retrieve relevant chunks of the document.

-> Answer cricket-related questions using the retrieved context without hallucinations.

-> CLI interface – ask questions interactively, quit anytime with quit.

-> Safe API key handling using a .env file.

-> Skips re-embedding if the vector database already contains documents.

--
# Project Structure
```md
Project Root/
├── app.py                  # Main CLI application
├── Classes.py              # RAGAssistant and VectorDB classes
├── data/                   # Folder containing MCC 2017 PDF
│   ├── laws_of_cricket_2017_MCC.pdf
│   └── laws_middle_pages.txt
├── chroma_cricket_db/      # Vector database folder (ignored in Git)
├── .env.example            # Example environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

# Setup Instructions
### 1. Clone the repository
Run thses commands:

```cmd
git clone https://github.com/YOUR_USERNAME/cricket-rag-cli-using-langchain.git
cd cricket-rag-cli-using-langchain
```

### 2. Create and activate a virtual environment using uv

```cmd
# Windows PowerShell
uv venv environment
.\environment\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv environment
source environment/bin/activate
```
### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy .env.example to .env:
```cmd
copy .env.example .env   # Windows
cp .env.example .env     # Linux/macOS
```

Add your Groq API key in .env:

```cmd
GROQ_API_KEY=your_api_key_here
```

### 5. Run the application

```cmd
python app.py
```

The app will automatically embed the PDF if the vector database is empty.

Type your questions in the CLI.

Type quit to exit.

#### Example:
```cmd
Enter a question: How long is a Test match?
Answer: A Test match is played over five days...
```
# License

MIT License

### Notes
- Currently supports only one PDF: `laws_of_cricket_2017_MCC.pdf`
- Re-running the program does not re-embed the PDF if the ChromaDB already contains documents
- Designed as a minimal, safe RAG demonstration for educational purposes


