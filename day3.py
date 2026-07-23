from datetime import date

# Dictionary - storing a note with extra info
note = {
    "content": "Machine learning is amazing",
    "type": "text",
    "date": str(date.today())
}

print("📝 My note:", note["content"])
print("📁 Type:", note["type"])
print("📅 Date:", note["date"])

print("\n--- All note details ---")
for key, value in note.items():
    print(f"{key} → {value}")

# If/else - making decisions
print("\n--- Smart Brain Decisions ---")

source = "youtube"

if source == "text":
    print("✅ Saving a text note...")
elif source == "youtube":
    print("🎥 Saving a YouTube video...")
elif source == "pdf":
    print("📄 Saving a PDF file...")
else:
    print("❌ Unknown source type!")

# Combining both - save multiple notes as dictionaries
notes_list = []

def save_smart_note(content, source_type):
    note = {
        "content": content,
        "type": source_type,
        "date": str(date.today())
    }
    notes_list.append(note)
    print(f"✅ Saved {source_type} note!")

def show_all_notes():
    print(f"\n🧠 Your brain has {len(notes_list)} notes:")
    for i, note in enumerate(notes_list, 1):
        print(f"{i}. [{note['type']}] {note['content']} ({note['date']})")

# Save different types of notes
save_smart_note("Machine learning is a subset of AI", "text")
save_smart_note("https://youtube.com/watch?v=abc123", "youtube")
save_smart_note("college_notes.pdf", "pdf")

# Show all
show_all_notes()