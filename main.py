from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load your secret API key from .env file
load_dotenv()

# Connect to Google Gemini AI
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Ask your first question to AI!
print("🧠 Asking AI your first question...")
print("-" * 40)

response = llm.invoke("What is Machine Learning? Explain in 3 simple lines.")
for block in response.content_blocks:
    if block["type"] == "text":
        print(block["text"])

print("-" * 40)
print("✅ Your AI is working!")