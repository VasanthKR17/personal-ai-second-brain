from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

# Load your secret API key
load_dotenv()

# Read all notes from the text file
with open("my_notes.txt", "r") as file:
    notes = [line.strip() for line in file.readlines() if line.strip()]

print(f"📄 Found {len(notes)} notes to remember.")

# Set up the embedding model (turns text into searchable "meaning")
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Build (or rebuild) a local vector database from your notes
db = Chroma.from_texts(
    texts=notes,
    embedding=embeddings,
    persist_directory="data"
)

print("✅ Your notes have been ingested into your Second Brain's memory!")