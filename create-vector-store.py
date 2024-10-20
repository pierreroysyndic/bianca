import os
import urllib.request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)

references = {
    'lfi': "https://canlii.ca/t/ckh9",
    'lfi-regles': "https://canlii.ca/t/cljw",
    'lfi-paiement-methodique-regles': "https://canlii.ca/t/cljx",
    'lacc': "https://canlii.ca/t/ckj7",
    'lacc-regles': "https://canlii.ca/t/d9t2",
    'lpps': "https://canlii.ca/t/cl3n",
    'lpps-regles': "https://canlii.ca/t/cq3b",
    'lpps-service-canada-apercu': "https://www.canada.ca/fr/emploi-developpement-social/services/protection-salaries/syndic.html",
    'lpps-service-canada-admissibilite': "https://www.canada.ca/fr/emploi-developpement-social/services/protection-salaries/syndic/abmissibilite.html",
    'lpps-service-canada-inscription': "https://www.canada.ca/fr/emploi-developpement-social/services/protection-salaries/syndic/inscription.html",
    'lpps-service-canada-preuve-reclamation': "https://www.canada.ca/fr/emploi-developpement-social/services/protection-salaries/syndic/preuve-reclamation.html",
    'lpps-service-canada-soumettre': "https://www.canada.ca/fr/emploi-developpement-social/services/protection-salaries/syndic/soumettre.html",
    'lpps-service-canada-apres-demande': "https://www.canada.ca/fr/emploi-developpement-social/services/protection-salaries/syndic/apres-demande.html",
    'lpps-service-canada-paiement': "https://www.canada.ca/fr/emploi-developpement-social/services/protection-salaries/syndic/paiement.html",
    'bsf-instruction-1r8': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-1r8-consultations-matiere-dinsolvabilite",
    'bsf-instruction-2r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-2r",
    'bsf-instruction-3': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-3",
    'bsf-instruction-4r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-4r-entree-vigueur-18-septembre-2009",
    'bsf-instruction-5r7': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-5r7",
    'bsf-instruction-6r7': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/linstruction-no-6r7-evaluation-dun-debiteur-particulier",
    'bsf-instruction-7': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-7",
    'bsf-instruction-8r22': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-8r22-formulaires-loi-faillite-linsolvabilite",
    'bsf-instruction-9r3': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-9r3",
    'bsf-instruction-10r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-10r",
    'bsf-instruction-11r2': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-11r2-2024-revenu-excedentaire",
    'bsf-instruction-13r8': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-13r8-delivrance-licences-syndic",
    'bsf-instruction-14': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-14-entree-vigueur-18-septembre-2009",
    'bsf-instruction-15': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-15",
    'bsf-instruction-16': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-16",
    'bsf-instruction-17': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-17-entree-vigueur-18-septembre-2009",
    'bsf-instruction-18': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-18-entree-vigueur-18-septembre-2009",
    'bsf-instruction-19r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-19r",
    'bsf-instruction-20': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-20",
    'bsf-instruction-21r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-21r",
    'bsf-instruction-22r4': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/sites/default/files/documents/02-directive_22r4.pdf",
    'bsf-instruction-23': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-23",
    'bsf-instruction-24': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-24-entree-vigueur-18-septembre-2009",
    'bsf-instruction-25': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-25r",
    'bsf-instruction-26': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-26",
    'bsf-instruction-27r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-27r",
    'bsf-instruction-28r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-28r-bureaux-secondaires-syndics",
    'bsf-instruction-30': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-30",
    'bsf-instruction-31r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-31r",
    'bsf-instruction-32r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-32r-tenue-documents-electroniques-syndic",
    'bsf-instruction-33': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/instruction-no-33-designation-syndic-publicite-syndics",
    'bsf-instruction-34r': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/instruction-no-34r-formulaires-lies-delivrance-licences-sous-regime-paragraphe-131-larticle-131-loi",
    'bsf-circulaire-2r2': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/circulaire-no-2r2",
    'bsf-circulaire-3r3': "https://ised-isde.canada.ca/site/bureau-surintendant-faillites/fr/alintention-syndics-autorises-insolvabilite/instructions-circulaires/circulaire-no-3r3",
    'lir': "https://canlii.ca/t/ckfk",
    'llc': "https://canlii.ca/t/19hq",
    'llr': "https://canlii.ca/t/ckqq",
    'llr-contrats-financiers-admissibles-regles': "https://canlii.ca/t/cnbt",
    'code-civil-quebec': "https://canlii.ca/t/1b6h",
    'code-procedure-civile-quebec': "https://canlii.ca/t/dhqv",
}

streams = []

for name, url in references.items():
    path = f"references/{name}.html"

    if not os.path.exists(path):
        print(f"{name} not downloaded. Proceeding to fetch: {url}")

        with urllib.request.urlopen(url) as response:
            html = response.read()
            file = open(path, "wb")
            file.write(html)

    streams.append(open(path, "rb"))

vector_store = client.beta.vector_stores.create(name="bianca-vector-store")

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id,
    files=streams
)

print(vector_store.id)
