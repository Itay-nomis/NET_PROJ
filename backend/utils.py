import hmac
import hashlib
import string
import random

salt = b'None'  # TODO add from configuration afterwards


def encrypt_password(password: str):
    """
    This function encrypts the password using hmac.
    :param password: the password to encrypt
    :return: encrypted password
    """
    return hmac.new(salt, password.encode(), hashlib.sha256).hexdigest()


def generate_random_string(length: int = 12):
    """
    Generate a random string of the specified length.

    :param length: Length of the random string (default is 12).
    :return: A random string consisting of letters and digits.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def encrypt_with_sha1():
    """
    Encrypt a string using SHA-1.
    :return: The SHA-1 hash of the string in hexadecimal format.
    """
    encrypted_string = hashlib.sha1(generate_random_string().encode())
    return encrypted_string.hexdigest()