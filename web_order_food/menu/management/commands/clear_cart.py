import sqlite3
from django.core.management.base import BaseCommand
class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        conn= sqlite3.connect("./db.sqlite3")
        c= conn.cursor()
        sql="DELETE FROM menu_food"
        c.execute(sql)
        conn.commit()
        conn.close()
        print("Deleted all data from cart")