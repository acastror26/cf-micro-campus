# My Django Application

## Requirements

- Docker
- Docker Compose

## Running the Application

Build and run the Docker containers:
```sh
cd backend
docker-compose up --build
```

The application will be available at http://localhost:8000.

## Making Migrations

Access the web container:
```sh
docker-compose exec web bash
```
Run the following commands:
```sh
python manage.py makemigrations
python manage.py migrate
```

## Running Tests

Access the web container:
```sh
docker-compose exec web bash
```
Run the tests:
```sh
python manage.py test
```

## Terraform Deployment to AWS

Initialize Terraform and apply the Terraform configuration:

```sh
cd terraform
terraform init
terraform apply
```
Follow the prompts to confirm the deployment. The instance IP address will be displayed as output.

## API Documentation
The API documentation is available at http://localhost:8000/swagger/.

## User Service Integration
The application integrates with a user service at user-service.com for user creation and authentication. Ensure the user service is running and accessible.
