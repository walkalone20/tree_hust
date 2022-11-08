import random
from .random_animal import generate_name_animal
from .random_food import generate_name_food

def generate_random_name(post_id, user_id):
    random.seed(post_id + user_id)
    sample = random.randint(0, 1)
    if sample == 1:
        return generate_name_animal(post_id, user_id)
    else:
        return generate_name_food(post_id, user_id)
