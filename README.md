# Cricket RAG CLI Assistant

A **CLI-based Retrieval-Augmented Generation (RAG) application** that answers cricket-related questions using **custom documents**. This project embeds the **MCC 2017 Laws of Cricket PDF** into a vector database with **Chroma** and leverages an LLM (**ChatGroq**) to provide precise answers based solely on the document content.

---

## Features

- Load a **single PDF** (MCC 2017 cricket rules) into a **vector database**  
- Perform **semantic search** to retrieve relevant content  
- Provide **accurate answers** without hallucination or assumptions  
- Interactive **CLI interface**; type `quit` to exit  
- Handles API keys securely via a `.env` file  
- Skips re-embedding if the database already contains documents  

---

## Project Structure

Project Root/
├── app.py # Main CLI application
├── Classes.py # RAGAssistant and VectorDB classes
├── data/ # PDF and related files
│ ├── laws_of_cricket_2017_MCC.pdf
│ └── laws_middle_pages.txt
├── chroma_cricket_db/ # Vector database (ignored in Git)
├── .env.example # Example environment variables
├── .gitignore
├── requirements.txt
└── README.md


## Setup

### 1. Clone the repository
### 2. Create and activate a virtual environment
### 3. Install dependencies
### 4. Configure environment variables

## Usage


### Usage4
This project is licensed under the MIT License.
