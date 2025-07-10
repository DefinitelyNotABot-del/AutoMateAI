import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.6
)

# Use a clean JSON-safe prompt with no variable conflicts
prompt_template = PromptTemplate.from_template(
    """You are an intelligent email assistant.

Given the subject and body of an email, extract the following:
1. A list of tasks (if any), each with due dates and urgency (high, medium, low).
2. A professional auto-reply the user can send back.

Respond in this **EXACT JSON format**:
{{
  "tasks": [
    {{
      "task": "...",
      "due": "...",
      "urgency": "high/medium/low"
    }}
  ],
  "auto_reply": "..."
}}

Email Subject: {subject}

Email Body:
{body}
"""
)

# New chain format (prompt | llm)
chain = prompt_template | llm

# Function to run Gemini on a single email
def extract_tasks_and_reply(subject, body):
    print("🧠 Gemini processing...")
    try:
        output = chain.invoke({"subject": subject, "body": body})
        response_text = output.content.strip()

        # Remove triple backticks if present
        if response_text.startswith("```json"):
            response_text = response_text.removeprefix("```json").removesuffix("```").strip()

        parsed = json.loads(response_text)
        return parsed
    except Exception as e:
        return {
            "error": "Failed to parse Gemini output",
            "raw_output": response_text if 'response_text' in locals() else None,
            "exception": str(e)
        }



# Test run
if __name__ == "__main__":
    subject = "URGENT: Submit Project Report by Friday"
    body = """Hi Abhinav, please submit the final project report by this Friday (July 12). 
Let me know if you need an extension. Thanks – Professor Rao"""
    
    result = extract_tasks_and_reply(subject, body)
    print(json.dumps(result, indent=2))
