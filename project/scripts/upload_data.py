import csv
import sys
import os
from sqlmodel import create_engine,Session

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from app.models.companies import Acquisitions, Company, Ipos
from app.models.users import Users


DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# Define file paths for the CSV files located in the 'scripts' folder
company_csv = os.path.join(project_root, 'scripts', 'objects.csv')
acquisition_csv = os.path.join(project_root, 'scripts', 'filtered_acquisitions.csv')
ipo_csv = os.path.join(project_root, 'scripts', 'filtered_ipos.csv')
user_csv = os.path.join(project_root, 'scripts', 'users.csv')

def read_csv_file_generator(file_path):
    try:
        with open(file_path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                yield row
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def is_table_empty(model):
    with Session(engine) as session:
        count = session.query(model).count()
        return count == 0
    
def create_companies():
    with Session(engine) as session:
        for row in read_csv_file_generator(company_csv):
            company = Company(**row)
            session.add(company)
        session.commit()

def create_acquisitions():
    with Session(engine) as session:
        for row in read_csv_file_generator(acquisition_csv):
            acquisition = Acquisitions(**row)
            session.add(acquisition)
        session.commit()

def create_ipos():
    with Session(engine) as session:
        for row in read_csv_file_generator(ipo_csv):
            ipo = Ipos(**row)
            session.add(ipo)
        session.commit()

def create_users():
    with Session(engine) as session:
        for row in read_csv_file_generator(user_csv):
            users = Users(**row)
            session.add(users)
        session.commit()

if __name__ == "__main__":
    if is_table_empty(Company) and is_table_empty(Acquisitions) and is_table_empty(Ipos):
        print("Tables are empty. Uploading data.")
        # Call the data upload functions here (create_companies, create_acquisitions, create_ipos)
        create_companies()
        create_acquisitions()
        create_ipos()
    if is_table_empty(Users):
        create_users()
    else:
        print("Tables are not empty. Skipping data upload.")
