# Rubix Bridge - Create Distributed Identifier (DID) and Data Token APIs

This Flask-based API server provides endpoints for managing Distributed Identifiers (DIDs) and Data Tokens. It interacts with multiple backend nodes, each associated with a specific application or service.

## Table of Contents
- [Endpoints](#endpoints)
- [Dependencies](#dependencies)
- [MongoDB Configuration](#mongodb-configuration)
- [Usage](#usage)

## Endpoints

### 1. Create Parent DID

- **Route:** `/api/createparentdid`
- **Method:** GET
- **Description:** Creates a parent DID for a specified application.

**Request Parameters**
- `app` (Query Parameter): Specifies the application for which the parent DID is created (e.g., "AM" or "ISK").

**Response**
- If successful, it returns a JSON response with information about the created parent DID.
- If unsuccessful, it returns an error message in JSON format.

### 2. Create Child DID

- **Route:** `/api/createchilddid`
- **Method:** GET
- **Description:** Creates a child DID for a specified application, linked to a parent DID.

**Request Parameters**
- `app` (Query Parameter): Specifies the application for which the child DID is created (e.g., "AM" or "ISK").

**Response**
- If successful, it returns a JSON response with information about the created child DID.
- If unsuccessful, it returns an error message in JSON format.

### 3. Get All DIDs

- **Route:** `/api/getalldid`
- **Method:** GET
- **Description:** Retrieves all DIDs associated with a specified application.

**Request Parameters**
- `app` (Query Parameter): Specifies the application for which DIDs should be retrieved (e.g., "AM" or "ISK").

**Response**
- If successful, it returns a JSON response containing a list of DIDs and associated information.

### 4. Create Data Token

- **Route:** `/api/createdt`
- **Method:** GET
- **Description:** Creates a Data Token.

**Response**
- If successful, it returns a JSON response with information about the created Data Token.

### 5. Commit Data Token

- **Route:** `/api/commitdt`
- **Method:** GET
- **Description:** Commits a Data Token.

**Response**
- If successful, it returns a JSON response indicating the success of the operation.

### 6. Shutdown All Nodes

- **Route:** `/api/shutdownall`
- **Method:** GET
- **Description:** Shuts down all backend nodes associated with different applications.

**Response**
- Returns a JSON response indicating the status of each node's shutdown operation.

### 7. Test All Nodes

- **Route:** `/api/testallnodes`
- **Method:** GET
- **Description:** Tests the connectivity of all backend nodes associated with different applications.

**Response**
- Returns a JSON response indicating the status of each node's connectivity test.

## Dependencies

- Flask: A web framework for Python.
- requests: A library for making HTTP requests.
- pymongo: A Python driver for MongoDB.
- geocoder: A library for geocoding IP addresses.
- flask_cors: A Flask extension for handling Cross-Origin Resource Sharing (CORS).

## MongoDB Configuration

- MongoDB Host: "localhost"
- MongoDB Port: 27017
- MongoDB Database: "jm"

## Usage

1. Ensure that MongoDB is running with the specified configuration.
2. Start the Flask API server by running the script. It will listen on host '0.0.0.0' and port 5050.
