import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

initial_query = sys.argv[1]

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": initial_query
        },
        {
            "role": "user",
            "content": "Veuillez réviser, retravailler (au besoin) et améliorer votre réponse en vous basant sur l'ensemble de documents à votre disposition. Assurez-vous de conserver les références et citations."
        },
        {
            "role": "user",
            "content": "Veuillez réviser votre réponse pour vous assurer quelle soit claire et concise. Assurez-vous de conserver les références et citations."
        }
    ],
    tool_resources={
        "file_search": {
            "vector_store_ids": [os.getenv('OPENAI_VECTOR_STORE_ID')]
        }
    }
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=os.getenv('OPENAI_ASSISTANT_ID')
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

message_content = messages[0].content[0]

message_text = message_content.text

annotations = message_text.annotations

citations = []

for index, annotation in enumerate(annotations):
    message_text.value = message_text.value.replace(annotation.text, f"[{index}]")

    if file_citation := getattr(annotation, "file_citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}] {cited_file.filename}")

response = message_text.value + "\n" + "\n".join(citations)

print(response)
