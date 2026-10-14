# Python APIs and Project Guide

This document describes the code currently present in this project. It includes employee CRUD/search and sandboxed text-file endpoints. CSV, JSON, upload, and download endpoints are not implemented yet.

## What `requirements.txt` Contains

`requirements.txt` lists external Python packages that the project needs. Install them into the project virtual environment with:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Current direct dependencies:

| Requirement | Purpose |
|---|---|
| `fastapi` | Defines HTTP routes, validates request inputs, and creates OpenAPI documentation. |
| `uvicorn[standard]` | Runs the FastAPI application as a web server; `[standard]` installs optional performance and reload helpers. |
| `mysql-connector-python` | Connects Python to MySQL and executes SQL statements. |
| `python-multipart` | Supports multipart form uploads when file-upload endpoints are added. It is installed now but not used by current routes. |
| `python-dotenv` | Loads local settings from `.env` into environment variables. |

A requirements file usually lists one direct dependency per line. A project may pin versions, for example `fastapi==x.y.z`, to make installs more reproducible. This project's requirements are currently unpinned. Python's standard-library modules do not belong in this file.

## Python APIs Compared with Node.js APIs

Both can provide REST endpoints over HTTP and return JSON. The difference is the language runtime and common project tooling, not the meaning of REST.

| Topic | This Python project | Typical Node.js project |
|---|---|---|
| Runtime | Python interpreter | Node.js runtime |
| Common web framework | FastAPI | Express, Fastify, or NestJS |
| Dependencies | Listed in `requirements.txt` and installed in a virtual environment | Listed in `package.json` and installed with npm, pnpm, or Yarn |
| Isolation | A Python `venv`, such as `.venv` | Usually a project-local `node_modules` directory; Node version managers may also be used |
| Request validation/docs | FastAPI provides validation and OpenAPI docs from route declarations | Often added with framework features or libraries such as schema validators and OpenAPI tools |
| I/O style | This code uses regular `def` route functions and synchronous MySQL Connector calls | Node servers commonly use promises/`async` functions with an event loop |

Either ecosystem can build scalable APIs. FastAPI also supports `async def`, but asynchronous routes should be paired with suitable asynchronous libraries; this project deliberately uses simple synchronous functions.

## Virtual Environment

A virtual environment is an isolated Python environment for one project. It keeps this project's installed packages separate from other Python projects and system Python. Here, `.venv` is the environment directory. Activate it in PowerShell with:

```powershell
.\.venv\Scripts\Activate.ps1
```

This machine's VS Code terminals have not always resolved the `python` command consistently, so use `.\.venv\Scripts\python.exe` to run the project's interpreter reliably. The environment is not a copy of the whole Python installation; it mainly keeps a project-specific interpreter context and packages.

`requirements.txt` describes what to install; `.venv` is where those packages are installed. The `.env` file is different again: it stores local settings such as database credentials. `.env` is ignored by Git and must not be committed or shared.

## What FastAPI Is

FastAPI is a Python web framework for building HTTP APIs. In this project, decorators such as `@app.get(...)` and `@app.post(...)` connect URLs and HTTP methods to Python functions. Type hints and `Body(...)` constraints let FastAPI validate requests and generate interactive documentation. When the server is running, visit `http://127.0.0.1:8000/docs` to try the routes in Swagger UI.

## Project Files

| File or folder | Responsibility |
|---|---|
| `main.py` | Creates the FastAPI app, defines HTTP routes, validates inputs, and translates errors into HTTP responses. |
| `database.py` | Loads `.env` settings and creates a MySQL connection. |
| `employee_queries.py` | Runs parameterized SQL for employee reads and writes. |
| `file_operations.py` | Performs text-file operations only within `uploads/text`. |
| `uploads/` | Holds application-managed files. Text operations create `uploads/text` when first needed. |
| `reports/` | Reserved for future CSV/JSON reports; no report routes exist yet. |
| `requirements.txt` | Lists external Python dependencies. |
| `.env` | Local database settings; ignored by Git. Never put real credentials in source code or documentation. |
| `README.md` | Main project setup guide; can link to this detailed API guide. |
| `PythonAPIS.md` | This API and learning reference. |

## REST API Endpoints Currently Implemented

Base URL: `http://127.0.0.1:8000`. The employee endpoints require a working MySQL server, database, and `.env` settings. Text-file endpoints do not use MySQL.

### Employee Endpoints

| Method | Path | Input | Purpose and success response |
|---|---|---|---|
| `POST` | `/employees` | JSON: `name`, `email`, `department`, `salary` | Creates an employee; returns the employee with generated ID (`201`). |
| `GET` | `/employees` | None | Returns all employees (`200`). |
| `GET` | `/employees/search` | Query parameter `name`, `department`, or both (for example, `?name=Ava`) | Returns employees matching the supplied filters (`200`). At least one filter is required. |
| `GET` | `/employees/{employee_id}` | Integer path parameter | Returns one employee (`200`). |
| `PUT` | `/employees/{employee_id}` | All four employee fields as JSON | Replaces all employee details (`200`). |
| `DELETE` | `/employees/{employee_id}` | Integer path parameter | Deletes the employee (`200`). |

Example employee JSON body for POST and PUT:

```json
{
  "name": "Ava Chen",
  "email": "ava.chen@example.com",
  "department": "Engineering",
  "salary": 85000
}
```

### Text-File Endpoints

File names must be `.txt` names only. The code confines them to `uploads/text`; callers cannot supply folder paths or access arbitrary computer files.

| Method | Path | Input | Purpose and success response |
|---|---|---|---|
| `POST` | `/files/text/{filename}` | `.txt` filename in URL | Creates a new empty text file (`201`); existing destination returns `409`. |
| `PUT` | `/files/text/{filename}` | JSON: `{"content": "..."}` | Replaces the file contents (`200`). |
| `POST` | `/files/text/{filename}/append` | JSON: `{"content": "..."}` | Appends text to the file (`200`). |
| `GET` | `/files/text/{filename}` | `.txt` filename in URL | Returns the complete file content (`200`). |
| `GET` | `/files/text/{filename}/lines` | `.txt` filename in URL | Returns file lines as a JSON array (`200`). |
| `GET` | `/files/text/{filename}/exists` | `.txt` filename in URL | Returns whether the file exists (`200`). |
| `POST` | `/files/text/{filename}/rename` | JSON: `{"new_filename": "new.txt"}` | Renames the file (`200`). |
| `POST` | `/files/text/{filename}/copy` | JSON: `{"new_filename": "copy.txt"}` | Copies the file (`201`). |
| `DELETE` | `/files/text/{filename}` | `.txt` filename in URL | Deletes the file (`200`). |
| `GET` | `/files/text/{filename}/size` | `.txt` filename in URL | Returns file size in bytes (`200`). |

### Common Error Responses

- `400 Bad Request`: invalid file name or a search request without a name/department.
- `404 Not Found`: employee or text file does not exist.
- `409 Conflict`: duplicate employee email or a destination text file already exists.
- `422 Unprocessable Entity`: request values fail FastAPI's input validation.
- `500 Internal Server Error`: a local file operation fails, including a permission error.
- `503 Service Unavailable`: a database connection/query error.

CSV import/export, JSON file APIs, file upload/download, and a root (`/`) homepage are not implemented at this stage.

## Built-ins, Standard Library, and External Packages

### Python Built-ins Used

- Functions: `int()` converts the configured port to an integer; `isinstance()` checks whether a MySQL error is an integrity error; `print()` displays connection test results.
- Types and constructors: `str`, `int`, and `float` appear in type annotations; `tuple()` converts search values to a tuple for the connector.
- Exception classes: `ValueError`, `OSError`, `FileNotFoundError`, `FileExistsError`, `PermissionError`, and `Exception` are used to report or handle errors.
- `None` is used for an absent value or uninitialized cursor; `True` and `False` are boolean values.

The code uses `Path.open()` rather than calling the built-in `open()` directly. `Path`, `shutil`, and `os` below are standard-library facilities, not built-in functions.

### Standard-Library Modules

- `os`: reads environment variables with `os.getenv()`.
- `pathlib.Path`: builds, validates, and operates on paths and files.
- `shutil`: copies a text file with `shutil.copyfile()`.

### External Packages

The external packages are the five entries in `requirements.txt`: FastAPI, Uvicorn, MySQL Connector/Python, `python-multipart`, and `python-dotenv`. `mysql.connector` and `dotenv` are the import names used by the source for MySQL Connector/Python and python-dotenv. `python-multipart` is included for the later upload stage but current routes do not use it. MySQL Workbench and Postman are separate desktop tools, not Python packages.

## 30 Interview Questions and Answers

1. **What is a REST API?**
   **Answer:** A REST API exposes resources through HTTP methods and URL paths. A client sends a request, often with JSON data, and the server returns a response with a status code and usually JSON. For example, this project uses `POST /employees` to create an employee and `GET /employees` to list them.

2. **What does `requirements.txt` do?**
   **Answer:** It lists the external Python packages the project needs, usually one package per line. Running `python -m pip install -r requirements.txt` asks pip to install those packages into the selected Python environment.

3. **What is a virtual environment?**
   **Answer:** It is an isolated Python environment for one project. This project's `.venv` keeps its installed libraries separate from other projects, which helps avoid version conflicts.

4. **How is `requirements.txt` different from `.venv`?**
   **Answer:** `requirements.txt` describes which packages to install; `.venv` is the environment where Python and those packages are available for this project. You can recreate an environment from the requirements file without committing the environment folder.

5. **What is FastAPI?**
   **Answer:** FastAPI is a Python framework for building HTTP APIs. It maps decorated functions to routes, validates many inputs using type annotations, and generates an OpenAPI schema and interactive documentation at `/docs`.

6. **What does Uvicorn do?**
   **Answer:** Uvicorn is the web server that runs the FastAPI application. In this project, `uvicorn main:app --reload` imports the `app` object from `main.py` and restarts the development server when code changes.

7. **What is an endpoint?**
   **Answer:** An endpoint is an HTTP method and route handled by an application, such as `GET /employees/{employee_id}`. The method describes the requested operation, while the path identifies the resource.

8. **What does HTTP `GET` normally do?**
   **Answer:** `GET` retrieves information and should not change the resource. Here, `GET /employees/3` requests the employee whose ID is 3; a missing employee returns `404`.

9. **What does HTTP `POST` normally do?**
   **Answer:** `POST` submits data to create a resource or perform an operation. Here, `POST /employees` accepts employee fields in a JSON body and returns `201 Created` when the insert succeeds.

10. **What does HTTP `PUT` normally do?**
  **Answer:** `PUT` replaces a resource or its supplied representation. This project's employee update route expects all employee fields; a partial update would usually be modeled with `PATCH` instead.

11. **What does HTTP `DELETE` do?**
  **Answer:** `DELETE` requests removal of a resource. Here, `DELETE /employees/{employee_id}` removes one database row, while `DELETE /files/text/{filename}` removes one allowed text file.

12. **What does status `201` mean?**
  **Answer:** `201 Created` means the request created a resource successfully. This project returns it when creating an employee or an empty text file.

13. **What does status `404` mean?**
  **Answer:** `404 Not Found` means the requested resource does not exist. The employee lookup and text-file operations use it when the requested ID or file is missing.

14. **What does status `409` mean in this project?**
  **Answer:** `409 Conflict` means the request conflicts with existing state. Examples are inserting an employee with an email already in use or copying a file to a name that already exists.

15. **What does status `422` mean?**
  **Answer:** `422 Unprocessable Entity` means FastAPI received the request but its fields failed validation. For example, a missing required employee field or a negative salary is rejected before the route performs its database operation.

16. **Why does the employee table use a primary key?**
  **Answer:** A primary key uniquely identifies each row. The auto-incrementing `id` lets MySQL assign a distinct employee ID, which the API can use for lookups, updates, and deletes.

17. **Why is employee email unique?**
  **Answer:** The unique constraint prevents two employee rows from using the same email address. MySQL enforces this rule, and the API translates a duplicate-key error into a `409 Conflict` response.

18. **What is a parameterized SQL query?**
  **Answer:** It is a query whose values are passed separately from its SQL text. In this project, the connector's `%s` placeholders are paired with a tuple of values, such as the employee ID used in a `WHERE` clause.

19. **Why parameterize SQL values?**
  **Answer:** Parameterization helps keep input data separate from SQL commands, reducing SQL injection risk and avoiding manual quoting errors. User-provided values should not be concatenated into a query string.

20. **What does `connection.commit()` do?**
  **Answer:** It saves successful changes in the current database transaction. The write-query helper calls it after an insert, update, or delete so MySQL persists the change.

21. **Why call `rollback()` after a write error?**
  **Answer:** A rollback cancels uncommitted changes in the current transaction. The write helper rolls back if a query fails, then re-raises the error so the API can handle it.

22. **Why close a database cursor and connection?**
  **Answer:** Cursors and connections use resources in Python and MySQL. Closing them in `finally` blocks releases those resources even when a query raises an error.

23. **What does `load_dotenv()` do?**
  **Answer:** It reads key-value settings from the local `.env` file and makes them available as environment variables. `database.py` then uses `os.getenv()` to retrieve the MySQL host, user, password, database, and port.

24. **Why should `.env` not be committed?**
  **Answer:** It can contain passwords or other private settings. This project's `.gitignore` excludes `.env`, but that is not encryption; credentials should still be kept private and never added to source code or shared publicly.

25. **What does a FastAPI route type annotation do?**
  **Answer:** It declares the kind of value a function expects, such as an integer employee ID or string name. FastAPI uses annotations and constraints to validate requests and describe fields in the generated API documentation.

26. **What does `Body(..., ge=0)` mean?**
  **Answer:** `Body(...)` marks a required value in the request body, and `ge=0` means its numeric value must be greater than or equal to zero. The salary route uses this to reject negative salaries.

27. **What is `pathlib.Path` used for here?**
  **Answer:** `Path` represents filesystem paths and provides methods to create directories, open files, read or write text, rename, delete, and inspect file size. It also helps resolve paths before the code checks the allowed folder boundary.

28. **How does the text-file code prevent path traversal?**
  **Answer:** It rejects filenames containing path separators, accepts only `.txt` extensions, resolves the final path, and checks that the file remains directly inside `uploads/text`. This keeps requests from selecting arbitrary computer files.

29. **What is the difference between write and append file modes?**
  **Answer:** Writing replaces existing file contents, while appending adds text at the end without discarding existing content. In this project, `write_text_file()` replaces content and `append_text_file()` adds to it.

30. **Which requested features are not implemented yet?**
  **Answer:** The current code has employee endpoints and text-file endpoints. CSV import/export, JSON file operations, and file upload/download are planned for later stages and should not be described as available API routes yet.
