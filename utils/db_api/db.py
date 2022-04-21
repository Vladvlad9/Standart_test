from sqlite3 import *
from data.config import DATABASE


class DBApi(object):

    def __init__(self) -> None:
        self.__conn: Connection = connect(DATABASE)
        self.__cur: Cursor = self.__conn.cursor()

    async def create_users_table(self) -> None:
        """CREATE USER TABLES"""
        self.__cur.execute('''
            CREATE TABLE IF NOT EXISTS
            users(
                user_id INTEGER PRIMARY KEY,
                f_name Text,
                l_name Text,
                m_name Text,
                restaurant Text,
                role TEXT NOT NULL
            )
        ''')
        self.__conn.commit()

    async def get_id_users(self, user_id: int):
        result = f'SELECT is_passet FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchone()

    async def get_questions(self, id: int):
        result = f'SELECT * FROM questions Where id = {id}'
        return self.__cur.execute(result).fetchall()

    async def get_all_questions(self):
        result = f'SELECT count(id) FROM questions'
        return self.__cur.execute(result).fetchone()

    async def get_answer(self):
        result = f'SELECT * FROM answer'
        return self.__cur.execute(result).fetchall()


    async def create_all_database(self) -> None:
        """CREATE DATABASE"""
        await self.create_users_table()
