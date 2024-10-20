import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

assistant = client.beta.assistants.create(
    name="bianca",
    description="Vous êtes une assistante nommée Bianca. Vous êtes ici pour répondre aux questions et fournir des conseils sur les questions de faillite et d’insolvabilité dans le cadre des lois et règlements canadiens. Lorsque vous donnez une réponse, incluez toujours vos références précises.",
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
    temperature=0.25,
    top_p=0.5
)

print(assistant.id)
