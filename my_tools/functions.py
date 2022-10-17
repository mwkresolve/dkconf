from random import choice, randrange
import string

def ip_generator():
    return str(".".join([str(randrange(0, 255)),
                         str(randrange(0, 255)),
                         str(randrange(0, 255)),
                         str(randrange(1, 255))]))


def pwd_generator(size=8, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(choice(chars) for x in range(size))

