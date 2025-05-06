from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import torch

# Load Hugging Face models
ner_model = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Optional: Zero-shot classifier (you can use this later for filtering)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_name_heuristic(resume_text):
    lines = resume_text.strip().split('\n')
    for line in lines[:5]:  # Look at the top 5 lines
        clean_line = line.strip()
        if 2 <= len(clean_line.split()) <= 4:
            if all(word[0].isupper() for word in clean_line.split() if word[0].isalpha()):
                return clean_line
    return "Unknown"

def extract_skills(resume_text):
    # Optional: log first few lines for debugging
    print("First 5 lines of resume:")
    print("\n".join(resume_text.strip().split('\n')[:5]))

    ner_results = ner_model(resume_text)

    skills = []
    names = []

    for ent in ner_results:
        word = ent['word'].strip()
        if ent['entity_group'] == "PER":
            names.append((word, ent['score']))
        elif ent['entity_group'] in ["MISC", "ORG", "LOC"]:
            if len(word) > 2 and not word.lower().startswith("http"):
                skills.append(word)

    if names:
        name = sorted(names, key=lambda x: x[1], reverse=True)[0][0]
    else:
        name = extract_name_heuristic(resume_text)

    return name, sorted(set(skills))
