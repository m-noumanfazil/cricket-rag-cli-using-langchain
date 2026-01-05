import os
from dotenv import load_dotenv
from Classes import RAGAssistant

load_dotenv()
PDF_PATHS = ["./data/laws_of_cricket_2017_MCC.pdf"]

def main():
    assistant = RAGAssistant()

    # Add documents only if DB is empty
    assistant.add_documents(PDF_PATHS)

    print("\nCricket Rules RAG Assistant is ready. Type 'quit' to exit.\n")
    while True:
        query = input("Enter a question: ")
        if query.lower() == "quit":
            break
        response = assistant.query(query)
        print("Answer: ")
        print(response)

if __name__ == "__main__":
    main()
