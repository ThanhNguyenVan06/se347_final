from django.core.management.base import BaseCommand
from django.dispatch import receiver
from faker import Faker
from tqdm import tqdm
from uuid import uuid4
from menu.models import cart
import sqlite3
import random
def get_random_food():
    """
    return a list contain sets
    a set contain (id,price)
    """
    conn= sqlite3.connect("./db.sqlite3")
    c= conn.cursor()
    sql= "SELECT id, price from menu_food where active=1"
    c.execute(sql)
    foods= c.fetchall()
    conn.close()
    return foods
def get_random_food_ids_price(foods):
    food_bought_number= random.randrange(1, len(foods))
    food_bought=random.choices(foods,k= food_bought_number)
    food_ids=[]
    total_price=0
    for i in food_bought:
        food_ids.append(str(i[0]))
        total_price+= i[1]
    return ",".join(f for f in food_ids), total_price
def get_random_bill_choice():
    statement_bill_choice= random.randrange(1,3)
    return str(statement_bill_choice)
def get_random_receiver(faker):
    is_empty= bool(random.getrandbits(1))
    if is_empty:
        return ""
    else:
        return faker.name()
def get_random_paid_bill():
    return bool(random.getrandbits(1))
def get_random_active_choice():
    return random.randrange(0,1)
def get_random_coupon_code():
    """
    We have 4 type of coupon code:
    - empty 
    - 100
    - 101
    - 102
    """
    code= random.choice(["","100","101","102"])
    return code

# remember to generate food before generate cart
class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("number", type=int, default=50)
    def handle(self,*args, **kwargs):
        number= kwargs['number']
        faker= Faker()
        foods=get_random_food()
        for _ in tqdm(range(number)):
            id_foods, total_price= get_random_food_ids_price(foods)
            cart.objects.create(
                user_name= faker.name(),
                id_foods= id_foods,
                bill_code= str(uuid4()),
                active= get_random_active_choice(),
                address_ship= faker.address(),
                number_telephone= faker.phone_number(),
                receiver= get_random_receiver(faker),
                coupon_code= get_random_coupon_code(),
                raw_price= total_price,
                final_price= total_price,
                statement_bill= get_random_bill_choice(),
                paid_bill= get_random_paid_bill()
            ).save()