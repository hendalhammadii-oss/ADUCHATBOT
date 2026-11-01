import hashlib
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "students.db"


def pin_hash(pin):
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()  # This setup script rebuilds the demo database.
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE students (
        student_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        program TEXT NOT NULL,
        pin_sha256 TEXT NOT NULL
    );

    CREATE TABLE attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL REFERENCES students(student_id),
        course_code TEXT NOT NULL,
        course_name TEXT NOT NULL,
        semester TEXT NOT NULL,
        absences INTEGER NOT NULL CHECK (absences >= 0)
    );

    CREATE TABLE fees (
        student_id TEXT PRIMARY KEY REFERENCES students(student_id),
        total_due REAL NOT NULL CHECK (total_due >= 0),
        amount_paid REAL NOT NULL CHECK (amount_paid >= 0),
        payment_deadline TEXT,
        currency TEXT NOT NULL DEFAULT 'SAR'
    );

    CREATE TABLE exam_requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL REFERENCES students(student_id),
        course_code TEXT NOT NULL,
        course_name TEXT NOT NULL,
        status TEXT NOT NULL,
        professor_name TEXT,
        professor_email TEXT,
        contact_deadline TEXT,
        instructions TEXT
    );
    """)

    students = [
        ("STU1001", "Ahmed Hassan", "ahmed@example.test", "Computer Science", pin_hash("1234")),
        ("STU1002", "Sara Ali", "sara@example.test", "Business Administration", pin_hash("2468")),
        ("STU1003", "Omar Ibrahim", "omar@example.test", "Engineering", pin_hash("1357")),
    ]
    conn.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?)", students)

    attendance = [
        ("STU1001", "CS101", "Introduction to Programming", "Fall 2026", 4),
        ("STU1001", "MATH120", "Calculus I", "Fall 2026", 2),
        ("STU1001", "ENG105", "Academic English", "Fall 2026", 1),
        ("STU1002", "BUS210", "Principles of Management", "Fall 2026", 3),
        ("STU1002", "ECON101", "Introduction to Economics", "Fall 2026", 1),
        ("STU1003", "ENG220", "Engineering Materials", "Fall 2026", 5),
        ("STU1003", "MATH240", "Applied Mathematics", "Fall 2026", 2),
    ]
    conn.executemany(
        """INSERT INTO attendance
           (student_id, course_code, course_name, semester, absences)
           VALUES (?, ?, ?, ?, ?)""",
        attendance,
    )

    fees = [
        ("STU1001", 5000.00, 2000.00, "2026-11-15", "SAR"),
        ("STU1002", 7500.00, 7500.00, "2026-11-15", "SAR"),
        ("STU1003", 6200.00, 1200.00, "2026-11-12", "SAR"),
    ]
    conn.executemany("INSERT INTO fees VALUES (?, ?, ?, ?, ?)", fees)

    exams = [
        ("STU1001", "CS101", "Introduction to Programming", "Approved",
         "Dr. Lina Mansour", "lina.mansour@example.test", "2026-11-05",
         "Email the professor to confirm the resit schedule."),
        ("STU1001", "MATH120", "Calculus I", "Pending",
         "Dr. Samir Nasser", "samir.nasser@example.test", "2026-11-07",
         "Wait for the department's decision before making arrangements."),
        ("STU1002", "BUS210", "Principles of Management", "Rejected",
         "Dr. Huda Saleh", "huda.saleh@example.test", None,
         "Contact the academic affairs office if you need clarification."),
        ("STU1003", "ENG220", "Engineering Materials", "Approved",
         "Dr. Faisal Karim", "faisal.karim@example.test", "2026-11-08",
         "Contact the professor to confirm the exam time and location."),
    ]
    conn.executemany(
        """INSERT INTO exam_requests
           (student_id, course_code, course_name, status, professor_name,
            professor_email, contact_deadline, instructions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        exams,
    )
    conn.commit()
    conn.close()
    print(f"Created demo database: {DB_PATH}")
    print("All records are fictional. Demo logins:")
    print("  STU1001 / 1234")
    print("  STU1002 / 2468")
    print("  STU1003 / 1357")


if __name__ == "__main__":
    main()
