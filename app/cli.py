import argparse
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Student, Group, Teacher, Subject, Grade

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()


class DatabaseCLI:
    """Клас для виконання CRUD-операцій над усіма моделями."""

    # Teacher
    def create_teacher(self, name: str):
        teacher = Teacher(name=name)
        session.add(teacher)
        session.commit()
        logger.info(f"Викладач '{name}' створений успішно.")

    def list_teachers(self):
        teachers = session.query(Teacher).all()
        if teachers:
            logger.info("Список викладачів:")
            for teacher in teachers:
                logger.info(f"ID: {teacher.id}, Ім'я: {teacher.name}")
        else:
            logger.info("Список викладачів порожній.")

    def update_teacher(self, teacher_id: int, name: str):
        teacher = session.query(Teacher).get(teacher_id)
        if teacher:
            teacher.name = name
            session.commit()
            logger.info(f"Дані викладача з ID {teacher_id} оновлено на '{name}'.")
        else:
            logger.error(f"Викладача з ID {teacher_id} не знайдено.")

    def remove_teacher(self, teacher_id: int):
        teacher = session.query(Teacher).get(teacher_id)
        if teacher:
            session.delete(teacher)
            session.commit()
            logger.info(f"Викладача з ID {teacher_id} успішно видалено.")
        else:
            logger.error(f"Викладача з ID {teacher_id} не знайдено.")

    # Group
    def create_group(self, name: str):
        group = Group(name=name)
        session.add(group)
        session.commit()
        logger.info(f"Група '{name}' створена успішно.")

    def list_groups(self):
        groups = session.query(Group).all()
        if groups:
            logger.info("Список груп:")
            for group in groups:
                logger.info(f"ID: {group.id}, Назва: {group.name}")
        else:
            logger.info("Список груп порожній.")

    def update_group(self, group_id: int, name: str):
        group = session.query(Group).get(group_id)
        if group:
            group.name = name
            session.commit()
            logger.info(f"Дані групи з ID {group_id} оновлено на '{name}'.")
        else:
            logger.error(f"Групу з ID {group_id} не знайдено.")

    def remove_group(self, group_id: int):
        group = session.query(Group).get(group_id)
        if group:
            session.delete(group)
            session.commit()
            logger.info(f"Групу з ID {group_id} успішно видалено.")
        else:
            logger.error(f"Групу з ID {group_id} не знайдено.")

    # Student
    def create_student(self, name: str, group_id: int):
        student = Student(name=name, group_id=group_id)
        session.add(student)
        session.commit()
        logger.info(f"Студента '{name}' створено успішно в групі з ID {group_id}.")

    def list_students(self):
        students = session.query(Student).all()
        if students:
            logger.info("Список студентів:")
            for student in students:
                logger.info(f"ID: {student.id}, Ім'я: {student.name}, Група ID: {student.group_id}")
        else:
            logger.info("Список студентів порожній.")

    def update_student(self, student_id: int, name: str):
        student = session.query(Student).get(student_id)
        if student:
            student.name = name
            session.commit()
            logger.info(f"Дані студента з ID {student_id} оновлено на '{name}'.")
        else:
            logger.error(f"Студента з ID {student_id} не знайдено.")

    def remove_student(self, student_id: int):
        student = session.query(Student).get(student_id)
        if student:
            session.delete(student)
            session.commit()
            logger.info(f"Студента з ID {student_id} успішно видалено.")
        else:
            logger.error(f"Студента з ID {student_id} не знайдено.")

    # Subject
    def create_subject(self, name: str, teacher_id: int):
        subject = Subject(name=name, teacher_id=teacher_id)
        session.add(subject)
        session.commit()
        logger.info(f"Предмет '{name}' створено успішно з викладачем ID {teacher_id}.")

    def list_subjects(self):
        subjects = session.query(Subject).all()
        if subjects:
            logger.info("Список предметів:")
            for subject in subjects:
                logger.info(f"ID: {subject.id}, Назва: {subject.name}, Викладач ID: {subject.teacher_id}")
        else:
            logger.info("Список предметів порожній.")

    def update_subject(self, subject_id: int, name: str):
        subject = session.query(Subject).get(subject_id)
        if subject:
            subject.name = name
            session.commit()
            logger.info(f"Дані предмета з ID {subject_id} оновлено на '{name}'.")
        else:
            logger.error(f"Предмета з ID {subject_id} не знайдено.")

    def remove_subject(self, subject_id: int):
        subject = session.query(Subject).get(subject_id)
        if subject:
            session.delete(subject)
            session.commit()
            logger.info(f"Предмет з ID {subject_id} успішно видалено.")
        else:
            logger.error(f"Предмета з ID {subject_id} не знайдено.")

    # Grade
    def create_grade(self, student_id: int, subject_id: int, grade: float):
        grade_entry = Grade(student_id=student_id, subject_id=subject_id, grade=grade)
        session.add(grade_entry)
        session.commit()
        logger.info(f"Оцінку {grade} створено для студента ID {student_id} з предмета ID {subject_id}.")

    def list_grades(self):
        grades = session.query(Grade).all()
        if grades:
            logger.info("Список оцінок:")
            for grade in grades:
                logger.info(
                    f"ID: {grade.id}, Студент ID: {grade.student_id}, Предмет ID: {grade.subject_id}, Оцінка: {grade.grade}")
        else:
            logger.info("Список оцінок порожній.")


def main():
    parser = argparse.ArgumentParser(description="CLI для роботи з базою даних.")
    parser.add_argument("-a", "--action", required=True, help="Дія: create, list, update, remove")
    parser.add_argument("-m", "--model", required=True, help="Модель: Teacher, Group, Student, Subject, Grade")
    parser.add_argument("--name", help="Ім'я для створення або оновлення")
    parser.add_argument("--id", type=int, help="ID для оновлення або видалення")
    parser.add_argument("--group_id", type=int, help="ID групи (для студентів)")
    parser.add_argument("--teacher_id", type=int, help="ID викладача (для предметів)")
    parser.add_argument("--subject_id", type=int, help="ID предмета (для оцінок)")
    parser.add_argument("--student_id", type=int, help="ID студента (для оцінок)")
    parser.add_argument("--grade", type=float, help="Оцінка (для оцінок)")
    args = parser.parse_args()

    cli = DatabaseCLI()

    if args.action == "create":
        if args.model == "Teacher" and args.name:
            cli.create_teacher(args.name)
        elif args.model == "Group" and args.name:
            cli.create_group(args.name)
        elif args.model == "Student" and args.name and args.group_id:
            cli.create_student(args.name, args.group_id)
        elif args.model == "Subject" and args.name and args.teacher_id:
            cli.create_subject(args.name, args.teacher_id)
        elif args.model == "Grade" and args.student_id and args.subject_id and args.grade:
            cli.create_grade(args.student_id, args.subject_id, args.grade)
        else:
            logger.error("Помилка: Перевірте аргументи для створення.")

    elif args.action == "list":
        if args.model == "Teacher":
            cli.list_teachers()
        elif args.model == "Group":
            cli.list_groups()
        elif args.model == "Student":
            cli.list_students()
        elif args.model == "Subject":
            cli.list_subjects()
        elif args.model == "Grade":
            cli.list_grades()
        else:
            logger.error("Помилка: Невідома модель для переліку.")

    elif args.action == "update":
        if args.model == "Teacher" and args.id and args.name:
            cli.update_teacher(args.id, args.name)
        elif args.model == "Group" and args.id and args.name:
            cli.update_group(args.id, args.name)
        elif args.model == "Student" and args.id and args.name:
            cli.update_student(args.id, args.name)
        elif args.model == "Subject" and args.id and args.name:
            cli.update_subject(args.id, args.name)
        else:
            logger.error("Помилка: Перевірте аргументи для оновлення.")

    elif args.action == "remove":
        if args.model == "Teacher" and args.id:
            cli.remove_teacher(args.id)
        elif args.model == "Group" and args.id:
            cli.remove_group(args.id)
        elif args.model == "Student" and args.id:
            cli.remove_student(args.id)
        elif args.model == "Subject" and args.id:
            cli.remove_subject(args.id)
        else:
            logger.error("Помилка: Перевірте аргументи для видалення.")
    else:
        logger.error("Помилка: Невідома дія або модель.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Невідома помилка: {e}")
    finally:
        session.close()
