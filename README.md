# AutoMate.AI - Task Agent Project 
```
# 🤖 AutoMateAI

AutoMateAI is a smart email assistant that reads Gmail messages, extracts tasks and urgency using Gemini 1.5 Flash, and lets you safely send professional replies through a Flask UI.

---

📦 Features:
- Gmail API to read latest emails
- Gemini 1.5 Flash to extract:
  - 📌 Tasks (with due dates & urgency)
  - ✉️ Suggested professional replies
- Manual UI for safe human-approved sending
- Flask frontend
- Future: Google Calendar + Sheets integrations

---

🛠 Tech:
- Python 3.10
- Flask
- LangChain + Gemini
- Gmail API
- Google OAuth2

---

▶ How to run:

1. Clone the repo:
   git clone https://github.com/DefinitelyNotABot-del/AutoMateAI.git

2. Add your Gemini key to `.env`:
   GEMINI_API_KEY=your_key_here

3. Install dependencies:
   pip install -r app/requirements.txt

4. Add Gmail API `credentials.json` in `/credentials/`

5. Run it:
   cd app
   python main.py

Then open: http://localhost:5000/generate-reply

---

✅ Example output:
{
  "tasks": [
    {
      "task": "Submit report",
      "due": "July 12",
      "urgency": "high"
    }
  ],
  "auto_reply": "Thank you, I'll submit it on time."
}

---

By: github.com/DefinitelyNotABot-del
```
