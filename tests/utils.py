import random
import string


def get_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def get_random_weekday():
    return random.choice(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])


def get_random_colour():
    return random.choice(['red', 'green', 'white'])


class CallableMock:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self):
        return []
