from django.test import TestCase

# Create your tests here.

import requests

response = requests.post("http://127.0.0.1:8000", params={"search": "asd"})

print(response.text)