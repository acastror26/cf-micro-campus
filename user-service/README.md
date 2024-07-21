# FastAPI Microservice

This is a FastAPI microservice for managing users and authentication.

## Features

- CRUD operations for users
- Token-based authentication
- Easily deployable to AWS with Terraform
- Docker configuration for containerization
- Unit tests

## Running the application

### Requirements

- Docker
- Docker Compose

### Running with Docker

1. Build the Docker image:

```sh
docker-compose build
```

2. Start the container

```sh
docker-compose up
```

### API documentation

One the application is running you can access the documentation at `http://localhost:8000/docs`.

### Running tests

```sh
pytest
```

### Deplying to AWS with Terraform

```sh
cd terraform
terraform init
terraform apply
```