from faker import Faker
import random

fake = Faker()

def generate_associated_username_email():
    base = fake.user_name()
    username = base + str(random.randint(10, 99))
    email = f"{base}@{fake.free_email_domain()}"

    return username, email

# Generate associated username and email
username, email = generate_associated_username_email()
print("Username:", username)
print("Email:", email)
