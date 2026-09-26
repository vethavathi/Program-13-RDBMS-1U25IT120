-- Write your 3NF SQL DDL Statements below.
-- Define Primary Keys and Foreign Keys appropriate for 3NF.

CREATE TABLE Course (
    -- Add columns and primary key here
);

CREATE TABLE Student (
    -- Add columns, primary key, and foreign key here
);

CREATE TABLE Course (
    CourseName VARCHAR(100) PRIMARY KEY,
    FacultyName VARCHAR(100) NOT NULL,
    DepartmentName VARCHAR(100) NOT NULL
);

CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    StudentName VARCHAR(100) NOT NULL,
    CourseName VARCHAR(100) NOT NULL,
    FOREIGN KEY (CourseName) REFERENCES Course(CourseName)
);
