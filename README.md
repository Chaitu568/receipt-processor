# Receipt Processor

A simple FastAPI-based application for processing receipts. This application calculates points for receipts based on a set of rules and exposes two endpoints:
- **POST /receipts/process** – Accepts a receipt JSON payload and returns a unique ID.
- **GET /receipts/{id}/points** – Retrieves the points for a receipt by its ID.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Running Locally with Pipenv](#running-locally-with-pipenv)
  - [Using Docker](#using-docker)
- [API Endpoints](#api-endpoints)
- [Automated Testing](#automated-testing)
- [Debugging](#debugging)
- [Notes](#notes)

## Requirements
- Python 3.12
- [Pipenv](https://pipenv.pypa.io/en/latest/)
- Docker (optional, for containerized deployment)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Chaitu568/receipt-processor.git
   cd receipt-processor
   ```

2. **Install Dependencies with Pipenv:**
   ```bash
   pipenv install
   ```
   This will create a virtual environment and install all required packages (FastAPI, Uvicorn, etc.).

## Running the Application

### Running Locally with Pipenv

1. **Activate the Virtual Environment:**
   ```bash
   pipenv shell
   ```

2. **Start the Application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API Documentation:**
   Open your browser and visit http://localhost:8000/docs to explore the interactive API docs.

### Using Docker

A Dockerfile is provided for containerized deployment.

1. **Build the Docker Image:**
   ```bash
   docker build -t receipt-processor .
   ```

2. **Run the Docker Container:**
   ```bash
   docker run -p 8000:8000 receipt-processor
   ```

3. **Verify the Application:**
   Access http://localhost:8000/docs in your browser to view the API documentation.

## API Endpoints

1. **Process Receipt**
   * **Endpoint:** `POST /receipts/process`
   * **Description:** Submits a receipt for processing.
   * **Request Body Example:**
     ```json
     {
       "retailer": "M&M Corner Market",
       "purchaseDate": "2022-01-01",
       "purchaseTime": "13:01",
       "items": [
         {
           "shortDescription": "Mountain Dew 12PK",
           "price": "6.49"
         },
         {
           "shortDescription": "Emils Cheese Pizza",
           "price": "12.25"
         },
         {
           "shortDescription": "Knorr Creamy Chicken",
           "price": "1.26"
         },
         {
           "shortDescription": "Doritos Nacho Cheese",
           "price": "3.35"
         },
         {
           "shortDescription": "Klarbrunn 12-PK 12 FL OZ",
           "price": "12.00"
         }
       ],
       "total": "35.35"
     }
     ```
   * **Response Example:**
     ```json
     {
       "id": "adb6b560-0eef-42bc-9d16-df48f30e89b2"
     }
     ```

2. **Retrieve Receipt Points**
   * **Endpoint:** `GET /receipts/{id}/points`
   * **Description:** Returns the points for the receipt with the given ID.
   * **Response Example:**
     ```json
     {
       "points": 100
     }
     ```

## Automated Testing

Automated tests have been written using pytest and FastAPI's TestClient. To run the tests locally:

1. **Activate your virtual environment (if not already activated):**
   ```bash
   pipenv shell
   ```

2. **Run the tests:**
   ```bash
   pipenv run pytest
   ```

### Running Tests Inside Docker

To run tests inside a Docker container, you can override the container's command:
```bash
docker run --rm -e PYTHONPATH=. receipt-processor pipenv run pytest
```

## Debugging

If your application isn't behaving as expected:

1. **View Container Logs:**
   ```bash
   docker logs <container_id_or_name>
   ```

2. **Open a Shell Inside the Running Container:**
   ```bash
   docker exec -it <container_id_or_name> /bin/bash
   ```

3. **Check the Application:** Verify that Uvicorn is running on port 8000 and your files are in place.

## Notes

* Each POST request to `/receipts/process` creates a new receipt, generating a unique ID even if only the numbers in the payload change.
* This application uses in-memory storage for receipts. In a production environment, consider using a persistent database.
* Ensure your environment variables such as `PYTHONPATH` are set properly during testing if needed.

Happy Testing!