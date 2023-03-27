import random
import string

def generate_string():
    this_string = ''

    for _ in range(random.randint(1, 100)):
        this_string += random.choice(list(string.ascii_lowercase + '0123456789'))

    return (this_string)