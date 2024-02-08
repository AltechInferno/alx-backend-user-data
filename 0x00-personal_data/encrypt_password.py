#!/usr/bin/env python3
""" Encrypt passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """ 1 string arg name password, returns a salted,
        hashed password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ 2 arguments, returns a boolean. """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
