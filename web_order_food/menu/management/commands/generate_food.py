from unicodedata import category
from django.core.management.base import BaseCommand
from tqdm import tqdm
from menu.models import food
from faker import Faker
data = [
    {
        "name_food": "chicken",
        "category": "chicken",
        "description": "chicken",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "combo_chicken",
        "category": "chicken",
        "description": "combo_chicken",
        "image": "..asd",
        "price":100,
        "active":1,
    },
    {
        "name_food": "fried-chicken",
        "category": "chicken",
        "description": "fried-chicken",
        "image": "..asd",
        "price":150,
        "active":1,
    },
    {
        "name_food": "nuggest",
        "category": "chicken",
        "description": "nuggest",
        "image": "..asd",
        "price":200,
        "active":1,
    },
    {
        "name_food": "whole-chicken",
        "category": "chicken",
        "description": "whole-chicken",
        "image": "..asd",
        "price":150,
        "active":1,
    },
    {
        "name_food": "cereal",
        "category": "dessert",
        "description": "cereal",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "chocolate-cake",
        "category": "dessert",
        "description": "chocolate-cake",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "cupcake",
        "category": "dessert",
        "description": "cupcake",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "dessert",
        "category": "dessert",
        "description": "dessert",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "ice-cream",
        "category": "dessert",
        "description": "ice-cream",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "pancake",
        "category": "dessert",
        "description": "pancake",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "waffles",
        "category": "dessert",
        "description": "waffles",
        "image": "..asd",
        "price":50,
        "active":1,
    },
    {
        "name_food": "drinks",
        "category": "drinks",
        "description": "drinks",
        "image": "..asd",
        "price":20,
        "active":1,
    },
    {
        "name_food": "orange-juices",
        "category": "dessert",
        "description": "orange-juices",
        "image": "..asd",
        "price":30,
        "active":1,
    }
]
class Command(BaseCommand):
    help = "generate mock food"
    def handle(self, *args, **kwargs):
        for i in tqdm(data):
            food.objects.create(
                name_food=i['name_food'],
                category=i['category'],
                description=i['description'],
                image=i['image'],
                price=i['price'],
                active=i['active'],
            ).save()