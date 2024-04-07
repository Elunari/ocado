# DebtSimplifer

This application processes debt transactions between parties, calculates balances, and determines the minimum number of payments required to settle all debts. It interfaces with AWS S3 for data storage and SQS for message queueing.

## Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.12 or higher
- poetry for Python package and dependency management

### Configuration

The application is configured through environment variables. A sample `.env` file is provided with the necessary variables.

The application runs within docker container. Build it using `docker-compose up --build`

You can run pytest tests using cli command `python3 -m pytest test` from api or worker directory.

## Development decisions

### part 1
- use default python csv reader instead of pandas for simplicity and lightweight
- use logger to properly handle errors and provide crucial information
- keep app core in main function to facilitate testing
- use defaultdict to automatically add keys to dict

### part 2
- keep necessary logic from part 1 in `debts_simplifier.py` file
- reuse `aws.py` and `config.py` from api module to keep consistency of entire project
- use boto3 sdk to handle AWS connections
- use pytests instead of unittest to keep consistency of entire project