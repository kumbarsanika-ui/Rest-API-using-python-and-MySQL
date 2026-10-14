# Employee Management REST API

A beginner-friendly REST API built with Python, FastAPI, MySQL, and Uvicorn. It provides employee CRUD/search endpoints and sandboxed text-file operations. The detailed endpoint reference, package explanations, built-ins, and interview questions are in [PythonAPIS.md](PythonAPIS.md).

## Current Features

- Add, list, get, update, delete, and search employees in MySQL.
- Create, write, append, read, check, rename, copy, delete, and measure text files inside `uploads/text`.
- Validate employee inputs and return HTTP errors for common database and file errors.
- Keep database settings in a local `.env` file, which is ignored by Git.

CSV import/export, JSON file operations, and upload/download endpoints are planned, but are not implemented yet.

## Requirements

- Python 3.11 or newer
- MySQL Server
- Visual Studio Code (recommended)
- Postman (for API testing)

## Setup on Windows

Open the project folder in VS Code and create a virtual environment in PowerShell:

```powershell
py --version
py -m venv .venv
```

Install the packages listed in `requirements.txt`:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Using the interpreter path directly avoids relying on PowerShell activation. Alternatively, activate the environment with `.\.venv\Scripts\Activate.ps1` and then use `python` commands. In VS Code, select the interpreter inside `.venv` with **Python: Select Interpreter**.

## Create the MySQL Database

Start MySQL Server and run this SQL in MySQL Workbench:

```sql
CREATE DATABASE IF NOT EXISTS employee_management;
USE employee_management;

CREATE TABLE IF NOT EXISTS employees (
		id INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(100) NOT NULL,
		email VARCHAR(255) NOT NULL UNIQUE,
		department VARCHAR(100) NOT NULL,
		salary DECIMAL(10, 2) NOT NULL
);
```

The primary key uniquely identifies each employee. The unique constraint prevents duplicate email addresses.

## Configure Database Access

Open the local `.env` file and set the MySQL username and password used by your local MySQL installation:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=employee_management
```

Keep real credentials private. Do not commit `.env` or paste its contents into chat. To test the connection, run:

```powershell
.\.venv\Scripts\python.exe database.py
```

## Run the API

Start the development server from the project folder:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open the interactive API docs at <http://127.0.0.1:8000/docs>. Stop the server with **Ctrl+C** in its terminal. The root URL `/` has no route and may return `404`; use `/docs` to explore the API.

## Test with Postman

Set the base URL to `http://127.0.0.1:8000`. For POST and PUT requests, select **Body → raw → JSON**.

Example employee body:

```json
{
	"name": "Ava Chen",
	"email": "ava.chen@example.com",
	"department": "Engineering",
	"salary": 85000
}
```

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/employees` | Add an employee. |
| `GET` | `/employees` | List employees. |
| `GET` | `/employees/{employee_id}` | Get an employee by ID. |
| `PUT` | `/employees/{employee_id}` | Replace an employee's details. |
| `DELETE` | `/employees/{employee_id}` | Delete an employee. |
| `GET` | `/employees/search?name=Ava` | Search by name and/or department. |
| `POST` | `/files/text/notes.txt` | Create an empty text file. |
| `PUT` | `/files/text/notes.txt` | Write text using JSON body `{"content":"..."}`. |
| `POST` | `/files/text/notes.txt/append` | Append text using JSON body `{"content":"..."}`. |
| `GET` | `/files/text/notes.txt` | Read the complete file. |
| `GET` | `/files/text/notes.txt/lines` | Read the file as a list of lines. |
| `GET` | `/files/text/notes.txt/exists` | Check whether the file exists. |
| `POST` | `/files/text/notes.txt/rename` | Rename with JSON body `{"new_filename":"new.txt"}`. |
| `POST` | `/files/text/notes.txt/copy` | Copy with JSON body `{"new_filename":"copy.txt"}`. |
| `DELETE` | `/files/text/notes.txt` | Delete the text file. |
| `GET` | `/files/text/notes.txt/size` | Get file size in bytes. |

Search example: `GET /employees/search?department=Engineering`. Employee endpoints require a working MySQL connection. Text-file endpoints only accept `.txt` filenames and operate inside `uploads/text`; they do not allow paths to arbitrary files.

## Project Structure

```text
.
├── main.py               # FastAPI application and route handlers
├── database.py           # MySQL connection using environment variables
├── employee_queries.py   # Parameterized employee SQL functions
├── file_operations.py    # Sandboxed text-file functions
├── requirements.txt      # Python dependencies
├── .env                  # Local database settings; ignored by Git
├── uploads/              # Application-managed files (text folder is created as needed)
├── reports/              # Reserved for future CSV/JSON reports
├── PythonAPIS.md         # Detailed API and learning reference
└── README.md             # Setup and run instructions
```

`reports/` and the CSV/JSON/upload features are part of the planned learning stages and may not exist until implemented. For endpoint response details, package descriptions, built-ins, and 30 interview questions, see [PythonAPIS.md](PythonAPIS.md).