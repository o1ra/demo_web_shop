import random
import string


def generate_random_email():
    login = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'mail.com']
    domain = random.choice(domains)

    email = f"{login}@{domain}"

    return email


random_email = generate_random_email()
