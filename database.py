import psycopg2
from psycopg2 import pool


# def connect():
#     return psycopg2.connect(
#                 user='postgres', password='Mysql#123', database='learning', host='localhost')

class Database:
    __connection_pool = None


    @classmethod
    def initialize(cls, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1,
                                                          10,
                                                         **kwargs)

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        return cls.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()


class CursorConnectionFromPool:
    def __init__(self):
        self.connection_pool = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
        self.connection.commit()
        Database.return_connection(self.connection)
