from django.core.management.base import BaseCommand
from tqdm import tqdm
from menu.models import food
import sqlite3
class Command(BaseCommand):
    help = "generate mock food"
    def handle(self, *args, **kwargs):
        conn= sqlite3.connect("./db.sqlite3")
        c= conn.cursor()
        sql= "delete from menu_food" 
        c.execute(sql)
        conn.commit()
        conn.close()
        print("Deleted all data from food")