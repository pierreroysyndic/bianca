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
            "content": "Retravaillez votre réponse afin de mentionner clairement de quels textes vous prenez votre source. Si applicable, mentionnez les articles de loi pertinents directement dans le texte de la réponse."
        },
        {
            "role": "user",
            "content": "Veuillez réviser, retravailler (au besoin) et améliorer votre réponse en vous basant sur l'ensemble de documents à votre disposition. Assurez-vous de conserver les références et citations."
        },
        {
            "role": "user",
            "content": "Pouvez-vous vous assurer que votre réponse est complète, véridique et réellement conforme à la loi? Si vous n'êtes pas certain, veuillez retirer la partie de la réponse concernée.",
        },
        {
            "role": "user",
            "content": "Veuillez réviser votre réponse pour vous assurer qu'elle soit claire et concise. Assurez-vous de conserver les références et citations."
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

citations = []

for index, annotation in enumerate(message_text.annotations):
    message_text.value = message_text.value.replace(annotation.text, f"[{index}]")

    if file_citation := getattr(annotation, "file_citation", None):
        cited_file = client.files.retrieve(file_citation.file_id)
        citations.append(f"[{index}] {cited_file.filename}")

response = message_text.value + "\n" + "\n".join(citations)

print(response)
