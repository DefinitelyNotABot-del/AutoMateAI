from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64

def send_reply(to, reply_text, thread_id):
    creds = Credentials.from_authorized_user_file("credentials/token.json", ["https://www.googleapis.com/auth/gmail.modify"])
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(reply_text)
    message["to"] = to
    message["subject"] = "Re: (Auto Reply)"
    message["In-Reply-To"] = thread_id

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {
        "raw": raw,
        "threadId": thread_id
    }

    try:
        send = service.users().messages().send(userId="me", body=body).execute()
        return send
    except Exception as e:
        return {"error": str(e)}
