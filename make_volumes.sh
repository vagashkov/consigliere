#!/bin/dash

echo "Creating Docker volumes..."

docker volume create knowledge_data --opt type=none --opt device="<host_path>" --opt o=bind

docker volume create postgres_data --opt type=none --opt device="<host_path>" --opt o=bind

docker volume create hookdeck_data --opt type=none --opt device="<host_path>" --opt o=bind

docker volume create nginx_data --opt type=none --opt device="<host_path>" --opt o=bind

echo "...done"
