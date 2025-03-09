"""
Actually trains the spaCy model
"""

from spacy.tokens import DocBin

# we first have to binarise our train and test datasets into .spacy files each (train.spacy, valid.spacy)
# PUT THE BELOW INTO A FUNCTION, so it applies to train and test
db = DocBin()
nlp = spacy.load("en_core_web_sm") #small, medium, large, xl, tf/BERT architecture
for text, annotations in TRAIN_DATA:
    entity_annotations = annotations['entities']
    for annotation in entity_annotations:
        doc = nlp(text)
        ents = []
        start, end, label = annotation
        span = doc.char_span(start, end, label=label)
        ents.append(span)
        doc.ents = ents
        print(f"text: {text}, ents: {ents}")
        db.add(doc)
db.to_disk("./train.spacy")

db = DocBin()
nlp = spacy.load("en_core_web_sm")
for text, annotations in TEST_DATA:
    entity_annotations = annotations['entities']
    for annotation in entity_annotations:
        doc = nlp(text)
        ents = []
        start, end, label = annotation
        span = doc.char_span(start, end, label=label)
        ents.append(span)
        doc.ents = ents
        print(f"text: {text}, ents: {ents}")
        db.add(doc)
db.to_disk("./valid.spacy")

# CLI command
!python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./valid.spacy