import random
import string


def generate_random_verification_code(length:int=6):
    code="".join(random.choices(string.digits,k=length))
    return code