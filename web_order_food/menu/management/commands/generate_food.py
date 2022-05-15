from django.core.management.base import BaseCommand
from tqdm import tqdm
from menu.models import food, category
from faker import Faker
import json
file= open("category.json")
data= json.load(file)
def generate_category():
    category.objects.create(id=1,category="pizza").save()
    category.objects.create(id=2,category="other").save()
    category.objects.create(id=3,category="drink").save()
    category.objects.create(id=4,category="dessert").save()
    category.objects.create(id=5,category="chicken").save()
    print("generated category")
class Command(BaseCommand):
    help = "generate mock food"
    def handle(self, *args, **kwargs):
        if category.objects.count() == 0:
            print("generate category")
            generate_category()
        for i in tqdm(data):
            try:
                food.objects.get(name_food=i['name_food'])
            except food.DoesNotExist:
                food.objects.create(
                    name_food=i['name_food'],
                    category_food_id=i['category_food_id'],
                    description=i['description'],
                    image=i['image'],
                    price=i['price'],
                    active=i['active'],
                ).save()