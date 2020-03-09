import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add_student(student):
    if not student.last_name:
        return 'Student is missing last name', 405
    if not student.first_name:
        return 'Student is missing first name', 405

    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)

    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    bla = student.to_dict()
    doc_id = student_db.insert(bla)
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return None

    student = Student.from_dict(student)
    if not subject:
        return student

    if subject not in student.grades:
        return None

    return student


def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id

def get_student_by_last_name(last_name):
    queries = []
    query = Query()
    queries.append(query.last_name == last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if not res:
        return 'Queried student does not exist', 404

    student = res[0]
    return student
