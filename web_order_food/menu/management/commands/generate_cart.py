from django.core.management.base import BaseCommand
from faker import Faker
from tqdm import tqdm
from uuid import uuid4
import pytz
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

def get_random_bill_choice(active):
    """
    based on the active
    active =1 -> delivering or delivered
    active =0 -> pending
    """
    if active ==1:
        return random.choices([1,2], weights=[1,2], k=1)[0]
    return 0

def get_random_receiver(faker):
    is_empty= bool(random.getrandbits(1))
    if is_empty:
        return ""
    else:
        return faker.name()

def get_random_paid_bill(active):
    """
    an inactive cart can be paid1
    """
    if active ==0:
        return False
    return random.choices([False,True], weights=[1,2])[0]

def get_random_active_choice():
    return random.choices([0,1], weights=[2,8], k=1)[0]

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
        """
        you should disable the auto_now_add=True before generate mock data
        """
        number= kwargs['number']
        faker= Faker()
        foods=get_random_food()
        for _ in tqdm(range(number)):
            id_foods, total_price= get_random_food_ids_price(foods)
            # paid bill and statement_bill depend on cart_active
            cart_active= get_random_active_choice()
            utc = pytz.timezone('UTC')
            cart.objects.create(
                user_name= faker.name(),
                id_foods= id_foods,
                bill_code= str(uuid4()),
                active= cart_active,
                address_ship= faker.address(),
                number_telephone= faker.phone_number(),
                receiver= get_random_receiver(faker),
                coupon_code= get_random_coupon_code(),
                date_created=faker.date_time_between(start_date='-3y', end_date='now',tzinfo=utc),
                raw_price= total_price,
                final_price= total_price,
                statement_bill= get_random_bill_choice(cart_active),
                paid_bill= get_random_paid_bill(cart_active)
            ).save()
        print("WARNING: you must disable the auto_now_add = True in menu order, otherwise the cart will be created with the now datetime")