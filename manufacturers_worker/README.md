# Manufacturers Worker Microservice

This microservice subscribes to a Google Cloud Pub/Sub topic called "commands_to_manufactures" and processes batches of manufacturer records to be stored in a PostgreSQL database.

## Features

- Subscribes to Pub/Sub topic
- Processes manufacturer data in batches
- Validates manufacturer data
- Stores valid manufacturers in PostgreSQL
- Records validation errors in an errors table
- Acknowledges processed messages

## Environment Variables

- `DB_NAME` - PostgreSQL database name
- `DB_HOST` - PostgreSQL host
- `DB_PORT` - PostgreSQL port
- `DB_USER` - PostgreSQL user
- `DB_PASSWORD` - PostgreSQL password
- `PROJECT_ID` - GCP project ID
- `SUBSCRIPTION_ID` - Pub/Sub subscription ID

## Running the service

```
python -m src.main
```