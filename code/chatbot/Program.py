import openai, os, requests

openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"

# Azure OpenAI setup
openai.api_base = "" # Add your endpoint here
openai.api_key = os.getenv("OPENAI_API_KEY") # Add your OpenAI API key here
deployment_id = "" # Add your deployment ID here

# Azure AI Search setup
search_endpoint = ""; # Add your Azure AI Search endpoint here
search_key = os.getenv("SEARCH_KEY"); # Add your Azure AI Search admin key here
search_index_name = ""; # Add your Azure AI Search index name here

def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

setup_byod(deployment_id)


message_text = [{"role": "user", "content": "What are the differences between Azure Machine Learning and Azure AI services?"}]

completion = openai.ChatCompletion.create(
    messages=message_text,
    deployment_id=deployment_id,
    data_sources=[  # camelCase is intentional, as this is the format the API expects
      {
  "type": "azure_search",
  "parameters": {
    "endpoint": "'$search_endpoint'",
    "index_name": "",
    "semantic_configuration": "default",
    "query_type": "simple",
    "fields_mapping": {},
    "in_scope": true,
    "role_information": "Your name is Vita. You are an AI assistant that helps people find information about Health. You must be kind and respectful to users.",
    "filter": null,
    "strictness": 3,
    "top_n_documents": 3,
    "authentication": {
      "type": "api_key",
      "key": ""
    },
    "key": "'$search_key'",
    "indexName": "'$search_index'"
  }
}
    ],
    temperature=0,
    top_p=1,
    max_tokens=800,
    stop=null,
    stream=true

)
print(completion)