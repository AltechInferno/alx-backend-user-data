#!/usr/bin/env python3
""" Connect to secure database, Read and filter data """
import os
import re
from typing import List
import logging
import mysql.connector

""" this contains the fields from user_data that are PII"""
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ our constructor """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log  """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """ returns the log message """
    for item in fields:
        message = re.sub(fr'{item}=.+?{separator}',
                         f'{item}={redaction}{separator}', message)
    return message


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a db connector """
    return mysql.connector.connect(
                    host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
                    database=os.environ.get('PERSONAL_DATA_DB_NAME', 'root'),
                    user=os.environ.get('PERSONAL_DATA_DB_USERNAME'),
                    password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''))


def get_logger() -> logging.Logger:
    """ returns logging.Logger obj """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger

def main():
    """ estabish db connection using get_db and retrieve all rows in the
        users table and display each row under a filtered format """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()
    for row in result:
        message = f"name={row[0]}; " + \
                  f"email={row[1]}; " + \
                  f"phone={row[2]}; " + \
                  f"ssn={row[3]}; " + \
                  f"password={row[4]};"
        print(message)
        log_record = logging.LogRecord("my_logger", logging.INFO,
                                       None, None, message, None, None)
        formatter = RedactingFormatter(PII_FIELDS)
        formatter.format(log_record)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
