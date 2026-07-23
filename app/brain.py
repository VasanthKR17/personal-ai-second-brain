from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

# Set up embeddings (for searching notes) and the chat model (for answering)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

db = Chroma(
    persist_directory="data",
    embedding_function=embeddings
)


def save_note(note):
    # Save to the plain text file, like before
    with open("my_notes.txt", "a") as file:
        file.write(note + "\n")

    # ALSO add it directly to the searchable memory right away
    db.add_texts([note])
    print("✅ Note saved and remembered!")


def ask_question(question):
    results = db.similarity_search(question, k=3)
    context = "\n".join([doc.page_content for doc in results])

    prompt = f"""Answer the question using only the notes below.

Notes:
{context}

Question: {question}
"""
    response = llm.invoke(prompt)

    for block in response.content_blocks:
        if block["type"] == "text":
            print("🧠 Answer:")
            print(block["text"])


def main():
    print("🧠 Welcome to your Personal AI Second Brain!")
    while True:
        print("\nWhat would you like to do?")
        print("1. Save a note")
        print("2. Ask a question")
        print("3. Exit")
        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":
            note = input("Type your note: ")
            save_note(note)
        elif choice == "2":
            question = input("Ask your question: ")
            ask_question(question)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("Please type 1, 2, or 3.")


if __name__ == "__main__":
    main()