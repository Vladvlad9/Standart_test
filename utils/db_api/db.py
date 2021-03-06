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

    async def get_users(self, user_id: int):
        result = f'SELECT * FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchall()

    async def get_id_users(self, user_id: int):
        result = f'SELECT is_passet FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchone()

    async def get_first_question_users(self, user_id: int):
        result = f'SELECT first_question FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchone()

    async def update_first_question_users(self, first_question: int, id_user: int):
        """ADD """
        self.__cur.execute('''
                                UPDATE users
                                SET first_question = ?
                                WHERE user_id = ?
                            ''', (first_question, id_user))
        self.__conn.commit()

    async def get_percent_users(self, user_id: int):
        result = f'SELECT percent FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchone()

    async def add_user(self, user_id, f_name: str, l_name: str, restaurant: str,
                       is_passet: str, correct_answer: int):
        try:
            self.__cur.execute('''
                        INSERT INTO
                        users(
                            user_id,
                            f_name,
                            l_name,
                            restaurant,
                            is_passet,
                            correct_answer
                        )
                        VALUES(?, ?, ?, ?, ?, ?)
                    ''', (user_id, f_name, l_name, restaurant, is_passet, correct_answer))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    async def update_percent_user(self, percent: int, id_user: int):
        """ADD CORRECT_ANSWER"""
        self.__cur.execute('''
                                UPDATE users
                                SET percent = ?
                                WHERE user_id = ?
                            ''', (percent, id_user))
        self.__conn.commit()

    async def get_answered_question_users(self, user_id: int):
        result = f'SELECT answered_question FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchall()

    async def update_answered_question_user(self, answered_question: str, id_user: int):
        """ADD CORRECT_ANSWER"""
        self.__cur.execute('''
                                UPDATE users
                                SET answered_question = ?
                                WHERE user_id = ?
                            ''', (answered_question, id_user))
        self.__conn.commit()



    ##################QESTIONS#######################################################

    async def add_questions(self, photo: str, answer: str) -> bool:
        try:
            self.__cur.execute('''
                        INSERT INTO
                        questions(
                            img,
                            answer
                        )
                        VALUES(?, ?)
                    ''', (photo, answer))
            self.__conn.commit()
        except IntegrityError:
            return False
        else:
            return True

    async def get_questions(self, id: int):
        result = f'SELECT * FROM questions Where id = {id}'
        return self.__cur.execute(result).fetchall()

    async def get_questions_id(self):
        result = f'SELECT id FROM questions'
        return self.__cur.execute(result).fetchall()

    async def get_questions2(self, id: int):
        result = f'SELECT * FROM test_questions Where id = {id}'
        return self.__cur.execute(result).fetchall()

    async def get_all_questions(self):
        result = f'SELECT count(id) FROM questions'
        return self.__cur.execute(result).fetchone()

    async def update_question(self, img: str, id_question: int):
        """ADD """
        self.__cur.execute('''
                                UPDATE questions
                                SET img = ?
                                WHERE id = ?
                            ''', (img, id_question))
        self.__conn.commit()

    ##################ANSWER######################################

    async def get_answer(self):
        result = f'SELECT * FROM answer'
        return self.__cur.execute(result).fetchall()

    async def update_correct_answer(self, answer: int, id_user: int):
        """ADD CORRECT_ANSWER"""
        self.__cur.execute('''
                                UPDATE users
                                SET correct_answer = ?
                                WHERE user_id = ?
                            ''', (answer, id_user))
        self.__conn.commit()

    async def get_wrong_answers(self, id: int):
        result = f'SELECT wrong_answers FROM users Where user_id = {id}'
        return self.__cur.execute(result).fetchall()

    async def update_wrong_answer(self, answer: list, id_user: int):
        """ADD CORRECT_ANSWER"""
        self.__cur.execute('''
                                UPDATE users
                                SET wrong_answers = ?
                                WHERE user_id = ?
                            ''', (answer, id_user))
        self.__conn.commit()

    async def get_wrong_answer_selected(self, id: int):
        result = f'SELECT wrong_answer_selected FROM users Where user_id = {id}'
        return self.__cur.execute(result).fetchall()

    async def update_wrong_answer_selected(self, answer: list, id_user: int):
        """"""
        self.__cur.execute('''
                                UPDATE users
                                SET wrong_answer_selected = ?
                                WHERE user_id = ?
                            ''', (answer, id_user))
        self.__conn.commit()

    async def update_passet_answer(self, answer: int, id_user: int):
        """ADD """
        result = f'UPDATE users SET is_passet = "{answer}" WHERE user_id = {id_user}'
        self.__cur.execute(result)
        self.__conn.commit()

    async def get_correct_answer_users(self, user_id: int):
        result = f'SELECT correct_answer FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchone()

    async def get_wrong_answer_users(self, user_id: int):
        result = f'SELECT wrong_answers FROM users WHERE user_id = {user_id}'
        return self.__cur.execute(result).fetchone()



    async def create_all_database(self) -> None:
        """CREATE DATABASE"""
        await self.create_users_table()
