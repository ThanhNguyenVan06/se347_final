from django.core.management.base import BaseCommand
from faker import Faker
from tqdm import tqdm
from uuid import uuid4
from menu.models import cart
import sqlite3
import random
def get_random_food():
    conn= sqlite3.connect("./db.sqlite3")
    c= conn.cursor()
    sql= "SELECT id from menu_food"
    c.execute(sql)
    foods= c.fetchall()
    conn.close()
    while True:
        yield random.choice(foods) 
# remember to generate food before generate cart
class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("number", type=int, default=50)
    def handle(self,*args, **kwargs):
        number= kwargs['number']
        faker= Faker()
        random_food_generator= get_random_food()
        for i in tqdm(range(number)):
            id_food= next(random_food_generator)[0]
            cart.objects.create(
                user_name= faker.name(),
                id_foods= id_food,
                bill_code= str(uuid4()),
                active= 1,
                address_ship= faker.address(),
            ).save()