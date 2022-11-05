import random
from .random_animal import generate_name_animal
from .random_food import generate_name_food

def generate_random_name():
    sample = random.randint(0, 1)
    if sample == 1:
        return generate_name_animal()
    else:
        return generate_name_food()