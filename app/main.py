from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from gmail_reader import read_latest_emails
from langchain_agent import extract_tasks_and_reply
from send_reply import send_reply
import os

load_dotenv()
app = Flask(__name__)

# ✅ Home (Landing)
@app.route('/')
def home():
    return "<h2>🤖 AutoMate.AI – Task Automation Agent is Live!</h2><p><a href='/generate-reply'>Try Safe Auto-Reply</a></p>"

# ✅ Safe auto-reply preview
@app.route("/generate-reply", methods=["GET"])
def generate_reply():
    emails = read_latest_emails(1)  # Read latest 1 email
    if not emails:
        return "📭 No unread emails found."

    email = emails[0]
    result = extract_tasks_and_reply(email["subject"], email["body"])

    return render_template(
        "reply_preview.html",
        subject=email["subject"],
        body=email["body"],
        sender=email["sender"],
        thread_id=email["threadId"],
        auto_reply=result.get("auto_reply", "")
    )

# ✅ Send only after manual confirmation
@app.route("/send-reply", methods=["POST"])
def send_reply_route():
    reply_text = request.form["reply_text"]
    to = request.form["to"]
    thread_id = request.form["thread_id"]

    result = send_reply(to, reply_text, thread_id)

    if "error" in result:
        return f"❌ Error: {result['error']}"
    return f"✅ Reply sent to {to}:<br><pre>{reply_text}</pre>"

# 🔁 Placeholder agent trigger
@app.route('/run-agent')
def run_agent():
    return jsonify({"status": "Agent triggered – logic coming soon!"})

if __name__ == '__main__':
    app.run(debug=True)
