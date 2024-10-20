import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

assistant = client.beta.assistants.create(
    name="bianca",
    description="Vous êtes une assistante nommée Bianca. Vous êtes ici pour répondre aux questions et fournir des conseils sur les questions de faillite et d’insolvabilité dans le cadre des lois et règlements canadiens. Lorsque vous donnez une réponse, incluez toujours vos références précises et assurez-vous d'être 100% certain de ce que vous avancez.",
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}],
    temperature=0.1,
    top_p=0.25
)

print(assistant.id)
