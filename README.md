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

## Running the Watcher Service

1. Open a new terminal.
2. Navigate to the `services` directory.
```sh
cd services
```
3. Run the watcher service.
```sh
py watcher.py
```
The watcher will monitor the upload directory and process new CSV files.
