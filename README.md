# consigliere
Company knowledge analysis and sharing service for both internal and external users

## Local LLM configuration
- create docker volume ollama_data to store models etc. (Be aware that models can be really large so choose host destination carefully):
<code>docker volume create ollama_data --opt type=none --opt device=<host_destination> --opt o=bind</code>
