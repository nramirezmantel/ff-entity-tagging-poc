"""
Runs evaluation on a trained model, 
Or a trained model + matcher
"""
import pickle
import spacy
from spacy.training.example import Example

# working with raw pickle files produced by feature engineering
with open("TEST-ic-mrc-arc-large-batch.pkl", "rb") as f:
    TEST_DATA = pickle.load(f)

with open("TRAIN-ic-mrc-arc-large-batch.pkl", "rb") as f:
    TRAIN_DATA = pickle.load(f)

# load the best performing model from the output directory (directory specified by --output kwarg above)
trained_model = spacy.load("output/model-best")
examples = []

# PUT below into a function so it applies to train and test
for text, annots in TEST_DATA:
    doc = trained_model.make_doc(text)
    examples.append(Example.from_dict(doc, annots))
test_performance_dict = trained_model.evaluate(examples) # evaluate the best performing model's performance on test data
# load the best performing model from the output directory (directory specified by --output kwarg above)
train_examples = []
for text, annots in TRAIN_DATA:
    doc = trained_model.make_doc(text)
    examples.append(Example.from_dict(doc, annots))
train_performance_dict = trained_model.evaluate(examples) # evaluate the best performing model's performance on test data