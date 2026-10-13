import re
import spacy

nlp = spacy.load("en_core_web_sm")


def detect_sensitive_data(prompt: str):

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    phone_pattern = r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"

    emails = re.findall(email_pattern, prompt)
    phones = re.findall(phone_pattern, prompt)

    doc = nlp(prompt)

    names = []
    locations = []
    organizations = []

    for entity in doc.ents:

        if entity.label_ == "PERSON":
            names.append(entity.text)

        elif entity.label_ == "GPE":
            locations.append(entity.text)

        elif entity.label_ == "ORG":
            organizations.append(entity.text)

    return {
        "emails": emails,
        "phones": phones,
        "names": names,
        "locations": locations,
        "organizations": organizations
    }