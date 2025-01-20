import argparse
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from cli import DatabaseCLI
from my_select import select_1, select_2, select_3, select_4, select_5, select_6, select_7, select_8, select_9, \
    select_10

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()


def execute_query(query_name, **kwargs):
    """Виконання вибірки з бази даних."""
    try:
        if query_name == "select_1":
            logger.info("Знайти 5 студентів із найбільшим середнім балом з усіх предметів:")
            result = select_1(session)
            logger.info(result)
        elif query_name == "select_2":
            logger.info("Знайти студента із найвищим середнім балом з певного предмета:")
            result = select_2(session, subject_id=kwargs.get("subject_id", 1))
            logger.info(result)
        elif query_name == "select_3":
            logger.info("Знайти середній бал у групах з певного предмета:")
            result = select_3(session, subject_id=kwargs.get("subject_id", 1))
            logger.info(result)
        elif query_name == "select_4":
            logger.info("Знайти середній бал на потоці (по всій таблиці оцінок):")
            result = select_4(session)
            logger.info(result)
        elif query_name == "select_5":
            logger.info("Знайти які курси читає певний викладач:")
            result = select_5(session, teacher_id=kwargs.get("teacher_id", 1))
            logger.info(result)
        elif query_name == "select_6":
            logger.info("Знайти список студентів у певній групі:")
            result = select_6(session, group_id=kwargs.get("group_id", 1))
            logger.info(result)
        elif query_name == "select_7":
            logger.info("Знайти оцінки студентів у окремій групі з певного предмета:")
            result = select_7(session, group_id=kwargs.get("group_id", 1), subject_id=kwargs.get("subject_id", 1))
            logger.info(result)
        elif query_name == "select_8":
            logger.info("Знайти середній бал, який ставить певний викладач зі своїх предметів:")
            result = select_8(session, teacher_id=kwargs.get("teacher_id", 1))
            logger.info(result)
        elif query_name == "select_9":
            logger.info("Знайти список курсів, які відвідує певний студент:")
            result = select_9(session, student_id=kwargs.get("student_id", 1))
            logger.info(result)
        elif query_name == "select_10":
            logger.info("Список курсів, які певному студенту читає певний викладач:")
            result = select_10(session, student_id=kwargs.get("student_id", 1), teacher_id=kwargs.get("teacher_id", 1))
            logger.info(result)
        else:
            logger.error("Невідомий запит.")
    except Exception as e:
        logger.error(f"Помилка при виконанні запиту: {e}")


def main():
    """Парсер для делегування CLI-команд та виконання запитів."""
    parser = argparse.ArgumentParser(description="CLI для роботи з базою даних та запитами.")
    parser.add_argument("-a", "--action", help="Дія: create, list, update, remove, query")
    parser.add_argument("-m", "--model", help="Модель: Teacher, Group, Student, Subject, Grade")
    parser.add_argument("--query", help="Назва запиту для виконання (select_1, select_2, ...)")
    parser.add_argument("--name", help="Ім'я для створення або оновлення")
    parser.add_argument("--id", type=int, help="ID для оновлення або видалення")
    parser.add_argument("--group_id", type=int, help="ID групи (для студентів)")
    parser.add_argument("--teacher_id", type=int, help="ID викладача (для предметів)")
    parser.add_argument("--subject_id", type=int, help="ID предмета (для оцінок)")
    parser.add_argument("--student_id", type=int, help="ID студента (для оцінок)")
    parser.add_argument("--grade", type=float, help="Оцінка (для оцінок)")
    args = parser.parse_args()

    if args.action:
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

    elif args.query:
        execute_query(args.query, subject_id=args.subject_id, teacher_id=args.teacher_id, group_id=args.group_id,
                      student_id=args.student_id)
    else:
        logger.error("Помилка: Необхідно вказати --action або --query.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Невідома помилка: {e}")
    finally:
        session.close()
