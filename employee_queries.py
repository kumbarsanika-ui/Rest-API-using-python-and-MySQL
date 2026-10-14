from database import create_connection


def run_read_query(query, values=(), fetch_one=False):
    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, values)

        if fetch_one:
            return cursor.fetchone()
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def run_write_query(query, values=()):
    connection = create_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return cursor.rowcount, cursor.lastrowid
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_all_employees():
    query = """
        SELECT id, name, email, department, salary
        FROM employees
        ORDER BY id
    """
    return run_read_query(query)


def get_employee_by_id(employee_id):
    query = """
        SELECT id, name, email, department, salary
        FROM employees
        WHERE id = %s
    """
    return run_read_query(query, (employee_id,), fetch_one=True)


def add_employee(name, email, department, salary):
    query = """
        INSERT INTO employees (name, email, department, salary)
        VALUES (%s, %s, %s, %s)
    """
    _, employee_id = run_write_query(query, (name, email, department, salary))
    return employee_id


def update_employee(employee_id, name, email, department, salary):
    query = """
        UPDATE employees
        SET name = %s, email = %s, department = %s, salary = %s
        WHERE id = %s
    """
    run_write_query(query, (name, email, department, salary, employee_id))


def delete_employee(employee_id):
    query = "DELETE FROM employees WHERE id = %s"
    row_count, _ = run_write_query(query, (employee_id,))
    return row_count


def search_employees(name=None, department=None):
    query = """
        SELECT id, name, email, department, salary
        FROM employees
    """
    conditions = []
    values = []

    if name:
        conditions.append("name LIKE %s")
        values.append(f"%{name}%")

    if department:
        conditions.append("department LIKE %s")
        values.append(f"%{department}%")

    query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY id"

    return run_read_query(query, tuple(values))