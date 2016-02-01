import os


def save_byte(b, dest):
    with open(dest, 'wb') as f:
        f.write(b)

    return True
