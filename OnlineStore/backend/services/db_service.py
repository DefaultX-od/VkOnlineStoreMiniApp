import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

class DataBase:
    def __init__(self):
        self.__db_name = os.getenv('db_name')
        self.__db_user = os.getenv('db_user')
        self.__db_user_pswd = os.getenv('db_user_pswd')
        self.__db_host_name = os.getenv('db_host_name')
        self.__con_str = f"mysql+mysqlconnector://{self.__db_user}:{self.__db_user_pswd}@{self.__db_host_name}:3306/{self.__db_name}"
        self.__engine = create_engine(self.__con_str)
        self.__session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.__engine
        )

    def get_session(self) -> Session:
        return self.__session()
