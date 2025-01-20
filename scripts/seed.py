import random
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Student, Group, Teacher, Subject, Grade
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

faker = Faker()
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

try:
    logger.info("Adding groups...")
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)

    logger.info("Adding teachers...")
    teachers = [Teacher(name=faker.name()) for _ in range(5)]
    session.add_all(teachers)

    logger.info("Adding subjects...")
    subjects = [Subject(name=faker.word(), teacher=random.choice(teachers)) for _ in range(8)]
    session.add_all(subjects)

    logger.info("Adding students...")
    students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(50)]
    session.add_all(students)

    logger.info("Adding grades...")
    grades = [
        Grade(
            student=random.choice(students),
            subject=random.choice(subjects),
            date_received=faker.date_this_year(),
            grade=random.uniform(1, 10)
        )
        for _ in range(1000)
    ]
    session.add_all(grades)

    logger.info("Committing changes to database...")
    session.commit()
    logger.info("Data successfully added!")
except Exception as e:
    logger.error(f"An error occurred: {e}")
    session.rollback()
finally:
    session.close()
