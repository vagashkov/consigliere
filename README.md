# consigliere
Company knowledge analysis and sharing service for both internal and external users

## Create Docker volumes
You can create docker volumes manually (see below) or use make_volumes.sh script to create them automatically.
Just do not forget to change the host destinations in every command.

## Knowledge base configuration
- create docker volume knowledge_data to store system prompt, documents etc.
<code>docker volume create knowledge_data --opt type=none --opt device=<host_destination*> --opt o=bind</code>
  (* - see /data/knowledge folder for details)

## Postgres DB configuration
- create docker volume postgres_data to store database files etc:
<code>docker volume create postgres_data --opt type=none --opt device=<host_destination> --opt o=bind</code>

## Local LLM configuration
- create docker volume ollama_data to store models etc. (Be aware that models can be really large so choose host destination carefully):
<code>docker volume create ollama_data --opt type=none --opt device=<host_destination> --opt o=bind</code>

## webhooks configuration
Consigliere uses webhooks to receive events from external services (e.g. Telegram etc).
To configure webhooks, you need to set up a webhook in the external service and configure the webhook URL in the consigliere settings.
To enable webhooks for local development, you can use ngrok or similar tools.
In case of using https://hookdeck.com/:
- [optionally] register using your email or GitHub/Google account;
- [optionally] create new source in dashboard Sources section and copy the source URL;
- create docker volume postgres_data to store database files etc:
<code>docker volume create hookdeck_data --opt type=none --opt device=<host_destination**> --opt o=bind</code>
- fill config.toml with hookdeck data provided by Hookdeck;
  (** - see /data/hookdeck folder for details)
- do not forget to configure webhook URL in consigliere .env file

## Launch routine
- use docker-compose-local-llm.yml to launch consigliere with local LLM (via Ollama)
- use docker-compose-remote-llm.yml to launch consigliere with remote OpenAI API-compatible LLM (e.g. via OpenRouter)