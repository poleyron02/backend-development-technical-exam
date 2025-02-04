# Running the FastAPI Server and Watcher Service (Windows Guide)

This guide explains how to run both the FastAPI server and the file watcher service concurrently on Windows.

## Prerequisites
Ensure you have the following installed:
- Python 3.8 or later
- Pip
- MongoDB (running locally or remotely)

## Installation

1. Clone the repository or navigate to the project directory.
```sh
cd your_project_directory
```

2. Install required dependencies.
```sh
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your MongoDB connection string:
```
MONGO_URL=your_mongodb_connection_string
```

## Running the FastAPI Server

1. Navigate to the `api` directory.
```sh
cd api
```
2. Run the FastAPI server.
```sh
fastapi dev .\main.py
```
or
```sh
py -m fastapi dev .\main.py
```

The server will start on `http://127.0.0.1:8000`.
You can access the API documentation at `http://127.0.0.1:8000/docs`.
## Running the Watcher Service

1. Open a new terminal.
2. Navigate to the `service` directory.
```sh
cd service
```
3. Run the watcher service.
```sh
py watcher.py
```
The watcher will monitor the upload directory and process new CSV files.

## Installing MongoDB Locally

To install MongoDB locally, follow these steps:

1. Download the MongoDB Community Edition from the [official MongoDB website](https://www.mongodb.com/products/self-managed/community-edition).
2. Follow the installation instructions for your specific Windows version.
3. After installation, start the MongoDB server from the MongoDB Compass or as a Windows service.
4. Verify that MongoDB is running by connecting to the MongoDB shell using MongoDB Compass or another MongoDB client.
## Creating a MongoDB Connection String

1. Open MongoDB Compass or your preferred MongoDB client.
2. Create a new connection by providing the necessary details such as hostname, port, and authentication.
3. Once connected, copy the connection string provided by the client.

Example connection string format:
```
mongodb://username:password@hostname:port/database
```

4. Paste the copied connection string into the `.env` file created earlier:
```
MONGO_URL=mongodb://username:password@hostname:port/database
```
Now you have a local MongoDB server running and can proceed with the rest of the setup.
