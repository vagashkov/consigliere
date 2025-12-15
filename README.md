# consigliere
Company knowledge analysis and sharing service for both internal and external users

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
- download and install Hoockdeck CLI;
- launch Hoockdeck CLI, sign in and create new connection using <code>listen</code> command:
<code>hookdeck listen <port_numbnner> <source_name></code>
- do not forget to configure webhook URL in consigliere .env file
