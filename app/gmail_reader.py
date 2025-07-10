import os
import base64
import email
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set required Gmail scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


# Get absolute-safe paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, '../credentials/credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'credentials/token.json')


def authenticate_gmail():
    creds = None

    # Load existing token or generate new one
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
        # Save token
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def extract_email_body(payload):
    try:
        # If the message has multiple parts
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain' and 'data' in part.get('body', {}):
                    data = part['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            # If the message is just one plain body
            body_data = payload.get('body', {}).get('data')
            if body_data:
                return base64.urlsafe_b64decode(body_data).decode('utf-8')
    except Exception as e:
        return f"(Error decoding body: {e})"
    return "(No body content)"


def read_latest_emails(max_results=5):
    service = authenticate_gmail()
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    print(f"📬 Emails fetched from Gmail: {len(messages)}")

    email_list = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        thread_id = msg_data.get('threadId', '')

        body = extract_email_body(payload)

        email_list.append({
            'subject': subject,
            'sender': sender,
            'threadId': thread_id,
            'body': body.strip()
        })

    return email_list


# 🚀 Entry point
if __name__ == '__main__':
    print("🚀 Running read_latest_emails()")
    emails = read_latest_emails()

    print(f"📬 Emails fetched: {len(emails)}")

    if not emails:
        print("⚠️ No emails returned. Check if Gmail inbox has messages.")

    for i, email_data in enumerate(emails, 1):
        print(f"\n📧 Email {i}")
        print(f"📌 Subject: {email_data['subject']}")
        print(f"📤 From: {email_data['sender']}")
        print(f"🧵 Thread ID: {email_data['threadId']}")
        print(f"📝 Body Preview: {email_data['body'][:200]}...")
        print("=" * 50)

