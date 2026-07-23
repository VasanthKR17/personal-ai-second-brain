from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

# Load your secret API key
load_dotenv()

# Set up the same embedding model used in ingest.py
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Load your existing notes memory (built by ingest.py)
db = Chroma(
    persist_directory="data",
    embedding_function=embeddings
)

# Connect to Gemini for answering
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Ask a question
question = "What do I know about AI?"

# Find the most relevant notes for this question
results = db.similarity_search(question, k=3)
context = "\n".join([doc.page_content for doc in results])

print("🔎 Relevant notes found:")
print(context)
print("-" * 40)

# Ask Gemini to answer using only those notes
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