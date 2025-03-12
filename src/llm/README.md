# FutureFund Document Extraction and Tagging POC

## Local Development

### Prerequisites: 

From your Azure Document Intelligence portal, get these keys and set them in a `.env` file in the root of the project:

**For using a custom extractor**, you need to create a custom extraction model [here](https://documentintelligence.ai.azure.com/studio/custommodel/projects).

```sh
# Azure Document Intelligence
AZURE_ENDPOINT=https://future-fund-poc.cognitiveservices.azure.com/
AZURE_API_KEY_PRIMARY=
AZURE_API_KEY_SECONDARY=
```
**For the OpenAI runner**, you need to create a model deployment [here](https://oai.azure.com/resource/deployments), and set the endpoint, API key and model version in the `.env` file's below sections, copying .env.example from this directory as a template:

```sh
# Azure OpenAI
AZURE_GPT_ENDPOINT=
AZURE_GPT_API_KEY=
AZURE_GPT_MODEL=
AZURE_GPT_API_VERSION=
```

## Running Locally

Create a virtual environment (tested on python 3.10) and install dependencies in `requirements.txt`

To run all components:

```sh
./auto/run.sh
```

To run specific components, run the runner files directly:

```sh
python src/runners/ee-openai_runner.py
```

## References

[Free tier limits](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/service-limits?view=doc-intel-3.1.0&viewFallbackFrom=doc-intel-4.0.0)

[Which prebuilt model to use?](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept/choose-model-feature?view=doc-intel-3.1.0)

### Repository Authors
Creator: Sanjay Kumar (Sanjay.Kumar@futurefund.gov.au)
Contributor: Nicole Ramirez (Nicole.Ramirez@futurefund.gov.au)