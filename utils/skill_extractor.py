from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch

# Load Hugging Face models
ner_model = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Optional: use Zero-shot if you want extra filtering
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_skills(resume_text):
    ner_results = ner_model(resume_text)

    skills = []
    names = []

    for ent in ner_results:
        if ent['entity_group'] == "PER":
            names.append((ent['word'], ent['score']))
        elif ent['entity_group'] in ["MISC", "ORG", "LOC"]:
            if len(ent['word']) > 2:
                skills.append(ent['word'].strip())

    name = sorted(names, key=lambda x: x[1], reverse=True)[0][0] if names else "Unknown"

    return name, list(set(skills))
