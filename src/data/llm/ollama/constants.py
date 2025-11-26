from src.config import settings

# Define LLM provider endpoints list
BASE_URL = "{}://{}:{}".format(
    settings.LLM_PROVIDER_SCHEMA,
    settings.LLM_PROVIDER_HOST,
    settings.LLM_PROVIDER_PORT
)
LIST_ALL_MODELS_URL = "{}/api/tags".format(BASE_URL)
LIST_ACTIVE_MODELS_URL = "{}/api/ps".format(BASE_URL)
