import mysql.connector
from fastapi import Body, FastAPI, HTTPException

import employee_queries
import file_operations

app = FastAPI(title="Employee Management API")


def handle_database_error(error):
    if isinstance(error, mysql.connector.IntegrityError):
        raise HTTPException(
            status_code=409,
            detail="An employee with this email already exists.",
        ) from error

    raise HTTPException(
        status_code=503,
        detail="Database unavailable. Check the MySQL server and connection settings.",
    ) from error


def run_file_operation(operation, *args):
    try:
        return operation(*args)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="Text file not found.") from error
    except FileExistsError as error:
        raise HTTPException(status_code=409, detail="Text file already exists.") from error
    except PermissionError as error:
        raise HTTPException(status_code=500, detail="File permission denied.") from error
    except OSError as error:
        raise HTTPException(status_code=500, detail="File operation failed.") from error


@app.post("/employees", status_code=201)
def create_employee(
    name: str = Body(..., min_length=1, max_length=100),
    email: str = Body(
        ...,
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    ),
    department: str = Body(..., min_length=1, max_length=100),
    salary: float = Body(..., ge=0),
):
    try:
        employee_id = employee_queries.add_employee(name, email, department, salary)
        return employee_queries.get_employee_by_id(employee_id)
    except (mysql.connector.Error, ValueError) as error:
        handle_database_error(error)


@app.get("/employees")
def list_employees():
    try:
        return employee_queries.get_all_employees()
    except (mysql.connector.Error, ValueError) as error:
        handle_database_error(error)


@app.get("/employees/search")
def find_employees(name: str = None, department: str = None):
    if not name and not department:
        raise HTTPException(
            status_code=400,
            detail="Provide a name or department to search.",
        )

    try:
        return employee_queries.search_employees(name, department)
    except (mysql.connector.Error, ValueError) as error:
        handle_database_error(error)


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    try:
        employee = employee_queries.get_employee_by_id(employee_id)
    except (mysql.connector.Error, ValueError) as error:
        handle_database_error(error)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found.")

    return employee


@app.put("/employees/{employee_id}")
def replace_employee(
    employee_id: int,
    name: str = Body(..., min_length=1, max_length=100),
    email: str = Body(
        ...,
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    ),
    department: str = Body(..., min_length=1, max_length=100),
    salary: float = Body(..., ge=0),
):
    try:
        employee = employee_queries.get_employee_by_id(employee_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found.")

        employee_queries.update_employee(
            employee_id,
            name,
            email,
            department,
            salary,
        )
        return employee_queries.get_employee_by_id(employee_id)
    except (mysql.connector.Error, ValueError) as error:
        handle_database_error(error)


@app.delete("/employees/{employee_id}")
def remove_employee(employee_id: int):
    try:
        deleted_count = employee_queries.delete_employee(employee_id)
    except (mysql.connector.Error, ValueError) as error:
        handle_database_error(error)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found.")

    return {"message": "Employee deleted."}


@app.post("/files/text/{filename}", status_code=201)
def create_text_file(filename: str):
    created_filename = run_file_operation(file_operations.create_text_file, filename)
    return {"filename": created_filename, "message": "Text file created."}


@app.put("/files/text/{filename}")
def write_text_file(filename: str, content: str = Body(..., embed=True)):
    written_filename = run_file_operation(
        file_operations.write_text_file,
        filename,
        content,
    )
    return {"filename": written_filename, "message": "Text file written."}


@app.post("/files/text/{filename}/append")
def append_text_file(filename: str, content: str = Body(..., embed=True)):
    appended_filename = run_file_operation(
        file_operations.append_text_file,
        filename,
        content,
    )
    return {"filename": appended_filename, "message": "Text added to file."}


@app.get("/files/text/{filename}/lines")
def read_text_file_lines(filename: str):
    lines = run_file_operation(file_operations.read_text_file_lines, filename)
    return {"filename": filename, "lines": lines}


@app.get("/files/text/{filename}/exists")
def check_text_file_exists(filename: str):
    exists = run_file_operation(file_operations.text_file_exists, filename)
    return {"filename": filename, "exists": exists}


@app.post("/files/text/{filename}/rename")
def rename_text_file(filename: str, new_filename: str = Body(..., embed=True)):
    renamed_filename = run_file_operation(
        file_operations.rename_text_file,
        filename,
        new_filename,
    )
    return {"filename": renamed_filename, "message": "Text file renamed."}


@app.post("/files/text/{filename}/copy", status_code=201)
def copy_text_file(filename: str, new_filename: str = Body(..., embed=True)):
    copied_filename = run_file_operation(
        file_operations.copy_text_file,
        filename,
        new_filename,
    )
    return {"filename": copied_filename, "message": "Text file copied."}


@app.delete("/files/text/{filename}")
def delete_text_file(filename: str):
    deleted_filename = run_file_operation(file_operations.delete_text_file, filename)
    return {"filename": deleted_filename, "message": "Text file deleted."}


@app.get("/files/text/{filename}/size")
def get_text_file_size(filename: str):
    size = run_file_operation(file_operations.get_text_file_size, filename)
    return {"filename": filename, "size_bytes": size}


@app.get("/files/text/{filename}")
def read_text_file(filename: str):
    content = run_file_operation(file_operations.read_text_file, filename)
    return {"filename": filename, "content": content}