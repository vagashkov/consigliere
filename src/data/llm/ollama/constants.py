from src.config import settings

# Define LLM provider endpoints list
BASE_URL = "{}://{}:{}".format(
    settings.LLM_PROVIDER_SCHEMA,
    settings.LLM_PROVIDER_HOST,
    settings.LLM_PROVIDER_PORT
)
LIST_ALL_MODELS_URL = "{}/api/tags".format(BASE_URL)
LIST_ACTIVE_MODELS_URL = "{}/api/ps".format(BASE_URL)
PULL_MODEL_URL = "{}/api/pull".format(BASE_URL)
DELETE_MODEL_URL = "{}/api/delete".format(BASE_URL)
MODEL_GENERATE_URL = "{}/api/generate".format(BASE_URL)
MODEL_CHAT_URL = "{}/api/chat".format(BASE_URL)
