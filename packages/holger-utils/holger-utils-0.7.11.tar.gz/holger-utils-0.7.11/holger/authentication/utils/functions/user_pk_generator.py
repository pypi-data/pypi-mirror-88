import time
import random


def user_pk_generator():
    return F"usr{int(time.time() * 1000000)}-{random.randint(10000, 99999)}"
