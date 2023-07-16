# Insurance Premium Calculation API

This is a FastAPI application that provides endpoints to manage and use tariffs for insurance premium calculation. The tariffs are used to calculate insurance costs based on a given declared value.

## Installation

### Prerequisites

Before you start, ensure you have installed:

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/insurance-premium-api.git
   ```

   Replace `yourusername` with your actual GitHub username if you've forked this repository to your account.

2. Navigate to the project directory:

   ```bash
   cd smit_api
   ```

3. Build the Docker image:

   ```bash
   docker-compose build
   ```

4. Start the Docker container:
   ```bash
   docker-compose up
   ```

The FastAPI application should now be up and running at `http://localhost:8000`.

## Usage

FastAPI provides automatic interactive API documentation. Once the application is running, you can go to `http://localhost:8000/docs` in your web browser to see and interact with your API.

The available endpoints are:

- `/tariffs/` (GET): Fetch all tariffs.
- `/tariffs/{id}` (GET): Fetch a tariff by its ID.
- `/load_tariffs/` (POST): Load tariffs from a provided JSON payload.
- `/calculate_insurance/{id}` (POST): Calculate insurance cost using the tariff with the given ID and a declared value from the request body.
- `/update_tariff/{id}` (PUT): Update a tariff by its ID from the JSON payload in the request body.
- `/delete_tariff/{id}` (DELETE): Delete a tariff by its ID.

Remember to replace `{id}` with the actual ID of the tariff you want to interact with.

## Testing

You can test each endpoint and its functionality directly in the interactive API documentation at `http://localhost:8000/docs`.
