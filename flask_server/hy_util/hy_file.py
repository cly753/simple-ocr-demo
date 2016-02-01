import os


def save_byte(b, dest):
    if not os.path.exists(dest):
        os.makedirs(dest, exist_ok=True)

    with open(dest, 'wb') as f:
        f.write(b)

    return True
