import mysql.connector
import pytest


DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "root",
    "database": "StudentDB"
}


@pytest.fixture(scope="module")
def db_connection():

    conn = mysql.connector.connect(**DB_CONFIG)

    yield conn

    conn.close()


def get_tables(cursor):

    cursor.execute("SHOW TABLES")
    return {row[0].lower() for row in cursor.fetchall()}


def get_columns(cursor, table_name):

    cursor.execute(f"DESCRIBE {table_name}")

    return {
        row[0].lower(): {
            "type": row[1],
            "key": row[3],
            "extra": row[5]
        }
        for row in cursor.fetchall()
    }


def get_foreign_keys(cursor, table_name):

    query = """
        SELECT
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
          AND REFERENCED_TABLE_NAME IS NOT NULL
    """

    cursor.execute(query, (table_name,))

    return cursor.fetchall()


# ------------------------------------------------------------
# TEST 1 - Required tables
# ------------------------------------------------------------

def test_required_tables(db_connection):

    cursor = db_connection.cursor()

    tables = get_tables(cursor)

    required_tables = {
        "student",
        "course",
        "faculty",
        "department"
    }

    assert required_tables.issubset(tables), (
        "Required tables Student, Course, Faculty and Department "
        "must be created."
    )

    cursor.close()


# ------------------------------------------------------------
# TEST 2 - Student table structure
# ------------------------------------------------------------

def test_student_table(db_connection):

    cursor = db_connection.cursor()

    columns = get_columns(cursor, "Student")

    required_columns = {
        "studentid",
        "studentname",
        "courseid"
    }

    assert required_columns.issubset(columns.keys())

    assert columns["studentid"]["key"] == "PRI"

    cursor.close()


# ------------------------------------------------------------
# TEST 3 - Course table structure
# ------------------------------------------------------------

def test_course_table(db_connection):

    cursor = db_connection.cursor()

    columns = get_columns(cursor, "Course")

    required_columns = {
        "courseid",
        "coursename",
        "facultyid"
    }

    assert required_columns.issubset(columns.keys())

    assert columns["courseid"]["key"] == "PRI"

    cursor.close()


# ------------------------------------------------------------
# TEST 4 - Faculty table structure
# ------------------------------------------------------------

def test_faculty_table(db_connection):

    cursor = db_connection.cursor()

    columns = get_columns(cursor, "Faculty")

    required_columns = {
        "facultyid",
        "facultyname",
        "departmentid"
    }

    assert required_columns.issubset(columns.keys())

    assert columns["facultyid"]["key"] == "PRI"

    cursor.close()


# ------------------------------------------------------------
# TEST 5 - Department table structure
# ------------------------------------------------------------

def test_department_table(db_connection):

    cursor = db_connection.cursor()

    columns = get_columns(cursor, "Department")

    required_columns = {
        "departmentid",
        "departmentname"
    }

    assert required_columns.issubset(columns.keys())

    assert columns["departmentid"]["key"] == "PRI"

    cursor.close()


# ------------------------------------------------------------
# TEST 6 - Student -> Course foreign key
# ------------------------------------------------------------

def test_student_course_fk(db_connection):

    cursor = db_connection.cursor()

    foreign_keys = get_foreign_keys(cursor, "Student")

    assert any(
        str(row[0]).lower() == "courseid"
        and str(row[1]).lower() == "course"
        and str(row[2]).lower() == "courseid"
        for row in foreign_keys
    ), "Student.CourseID must reference Course.CourseID"

    cursor.close()


# ------------------------------------------------------------
# TEST 7 - Course -> Faculty foreign key
# ------------------------------------------------------------

def test_course_faculty_fk(db_connection):

    cursor = db_connection.cursor()

    foreign_keys = get_foreign_keys(cursor, "Course")

    assert any(
        str(row[0]).lower() == "facultyid"
        and str(row[1]).lower() == "faculty"
        and str(row[2]).lower() == "facultyid"
        for row in foreign_keys
    ), "Course.FacultyID must reference Faculty.FacultyID"

    cursor.close()


# ------------------------------------------------------------
# TEST 8 - Faculty -> Department foreign key
# ------------------------------------------------------------

def test_faculty_department_fk(db_connection):

    cursor = db_connection.cursor()

    foreign_keys = get_foreign_keys(cursor, "Faculty")

    assert any(
        str(row[0]).lower() == "departmentid"
        and str(row[1]).lower() == "department"
        and str(row[2]).lower() == "departmentid"
        for row in foreign_keys
    ), "Faculty.DepartmentID must reference Department.DepartmentID"

    cursor.close()


# ------------------------------------------------------------
# TEST 9 - No redundant original columns in Student
# ------------------------------------------------------------

def test_no_redundant_columns(db_connection):

    cursor = db_connection.cursor()

    columns = get_columns(cursor, "Student")

    unwanted_columns = {
        "coursename",
        "facultyname",
        "departmentname"
    }

    found = unwanted_columns.intersection(columns.keys())

    assert not found, (
        "Student table should not contain CourseName, "
        "FacultyName or DepartmentName in the 3NF design."
    )

    cursor.close()


# ------------------------------------------------------------
# TEST 10 - Sample data can be inserted
# ------------------------------------------------------------

def test_insert_sample_data(db_connection):

    cursor = db_connection.cursor()

    try:

        cursor.execute(
            "SELECT COUNT(*) FROM Department"
        )

        department_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Faculty"
        )

        faculty_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Course"
        )

        course_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Student"
        )

        student_count = cursor.fetchone()[0]

        assert department_count >= 1, \
            "Department table should contain sample data."

        assert faculty_count >= 1, \
            "Faculty table should contain sample data."

        assert course_count >= 1, \
            "Course table should contain sample data."

        assert student_count >= 1, \
            "Student table should contain sample data."

    finally:

        cursor.close()
