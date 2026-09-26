# Homework: Database Normalization (Up to 3NF)

## Problem Statement
You are given an unnormalized table structure for a university record system:

**Unnormalized Table:**
`Student(StudentID, StudentName, CourseName, FacultyName, DepartmentName)`

### Assumptions & Functional Dependencies:
1. `StudentID` uniquely identifies `StudentName` and `CourseName`.
2. `CourseName` uniquely identifies `FacultyName` and `DepartmentName`.

## Tasks
1. Identify functional dependencies and transitive dependencies in the unnormalized table.
2. Normalize the design step-by-step to **First Normal Form (1NF)**, **Second Normal Form (2NF)**, and **Third Normal Form (3NF)**.
3. Write your final SQL DDL code in `schema.sql`.

## Instructions
- Edit `submission.txt` to provide your step-by-step normalization explanation.
- Edit `schema.sql` to include the final 3NF database schema (table definitions, Primary Keys, and Foreign Keys).
- Commit and push your changes to run autograding tests.
