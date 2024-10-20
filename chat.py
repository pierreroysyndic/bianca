import os
import sys
from typing import final

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

def ask(query):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": query
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

    message_content = messages[0].content[0].text

    annotations = message_content.annotations

    citations = []

    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")

        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    return message_content.value + "\n".join(citations)

initial_query = sys.argv[1]

response = ask(initial_query)

hops = 3

for i in range(hops):
    query = f"Un utilisateur vous a posé la question suivante : \"{initial_query}\"\n\nVous avez donné la réponse suivante : \"{response}\"\n\nVeuillez réviser, retravailler (au besoin) et améliorer votre réponse, sans nécessairement l'allonger. Veuillez répondre avec seulement le contenu de votre réponse."
    response = ask(query)

print(response)
