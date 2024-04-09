from create_db import create_db
from datetime import datetime
from faker import Faker
from random import randint, choice
import sqlite3

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_COURSES = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 1000


def generate_fake_data(number_students, number_teachers, number_grades) -> tuple():
    fake_students = []
    fake_groups = ["OMT-96-1", "OMT-99-2", "PTM-12-1"]
    fake_courses = [
        "Бази даних",
        "Креслення",
        "Матан",
        "Українська мова",
        "Англійська мова",
        "Економіка",
        "Теормех",
        "Металографія",
    ]
    fake_teachers = []
    fake_grades = []

    fake_data = Faker("uk_UA")
    Faker.seed(0)

    # generate students
    for _ in range(number_students):
        fake_students.append(
            fake_data.first_name_nonbinary() + " " + fake_data.last_name_nonbinary()
        )

    # generate teachers
    for _ in range(number_teachers):
        fake_teachers.append(
            fake_data.first_name_nonbinary() + " " + fake_data.last_name_nonbinary()
        )

    # generate grades
    for _ in range(number_grades):
        fake_grades.append(randint(1, 10))

    return fake_students, fake_groups, fake_courses, fake_teachers, fake_grades


def prepare_data(students, groups, courses, teachers, grades) -> tuple():
    for_groups = []
    for group in groups:
        for_groups.append((group,))

    for_teachers = []
    for teacher in teachers:
        for_teachers.append((teacher,))

    for_students = []
    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPS)))

    for_studyes = []
    for course in courses:
        for_studyes.append((course, randint(1, NUMBER_TEACHERS)))

    for_grades = []
    for grade in grades:
        for_grades.append(
            (
                grade,
                datetime(2023, randint(1, 12), randint(1, 28)).date(),
                randint(1, NUMBER_STUDENTS),
                randint(1, NUMBER_COURSES),
            )
        )

    return for_students, for_groups, for_studyes, for_teachers, for_grades


def insert_data_to_db(students, groups, courses, teachers, grades) -> None:
    with sqlite3.connect("university.db") as con:
        cur = con.cursor()

        sql_to_groups = """INSERT INTO groups(name)
                               VALUES (?)"""
        cur.executemany(sql_to_groups, groups)

        sql_to_teachers = """INSERT INTO teachers(name)
                               VALUES (?)"""
        cur.executemany(sql_to_teachers, teachers)

        sql_to_studyes = """INSERT INTO studyes(name, teacher_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_studyes, courses)

        sql_to_students = """INSERT INTO students(name, group_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_students, students)

        sql_to_grades = """INSERT INTO grades(grade, date, student_id, study_id)
                               VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_grades, grades)

        con.commit()


def execute_query(sql_file: str) -> list:
    with open(sql_file, "r") as f:
        sql = f.read()

    with sqlite3.connect("university.db") as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


if __name__ == "__main__":
    create_db()
    students, groups, courses, teachers, grades = prepare_data(
        *generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_GRADES)
    )
    insert_data_to_db(students, groups, courses, teachers, grades)
