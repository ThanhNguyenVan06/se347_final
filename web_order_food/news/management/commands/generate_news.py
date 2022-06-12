from django.core.management.base import BaseCommand
from tqdm import tqdm
from news.models import news
from faker import Faker
import json
import sqlite3
mock_data =[
    {
        'title': 'Thưởng thức ngay các món ăn việt Nam ngon nức tiếng',
        'link_seemore': 'https://go2joy.vn/blog/cac-mon-an-viet-nam-ngon-va-noi-tieng-nhat/',
        'image': 'https://go2joy.s3.ap-southeast-1.amazonaws.com/blog/wp-content/uploads/2022/04/14172249/mon-an-viet-nam.jpg'
    }
]
class Command(BaseCommand):
    help = "generate mock mock news"
    def handle(self, *args, **kwargs):
        for data in mock_data:
            news.objects.create(
                title=data['title'],
                link_seemore=data['link_seemore'],
                image_new=data['image'],
            ).save()