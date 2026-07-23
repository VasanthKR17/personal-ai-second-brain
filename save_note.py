# This is the first real piece of your Second Brain!
# It saves a note and reads it back

def save_note(note):
    with open("my_notes.txt", "a") as file:
        file.write(note + "\n")
    print("✅ Note saved to your brain!")

def read_notes():
    print("\n📖 All your saved notes:")
    with open("my_notes.txt", "r") as file:
        notes = file.readlines()
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note.strip()}")

# Save some notes
save_note("Machine learning is a subset of AI")
save_note("Python is the best language for AI projects")
save_note("My project is Personal AI Second Brain")

# Read them back
read_notes()