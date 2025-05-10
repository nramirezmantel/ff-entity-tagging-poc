# ff-entity-tagging-poc

This repository contains proof of concept code for training and applying an entity tagging and matching model

The key files and folders are as follows:

```
data/                       # where we store data
|   |--raw_input_docs/      # input data      
|   |--raw_input_labels/    # input labels
|   |--matching_data/       # MDM extracts
model/                      # where we store the model weights and files
|   |--output/
|       |--model-best/      # best performing model
|       |--model-last/      # most recently trained model
base_config.cfg             # spaCy base config template
config.cfg                  # spaCy config that we use to train the model, modified from above
inference.ipynb             # notebook for model inference (tagging and matching)
README.md
requirements-dev.txt        # required packages for training and inference
src-train.ipynb             # notebook for training
```


## Model Inference

Follow the notebook `inference.ipynb`. Execute cells from top to bottom

## Model Training

Follow the notebook `src-train.ipynb`. Execute cells from top to bottom