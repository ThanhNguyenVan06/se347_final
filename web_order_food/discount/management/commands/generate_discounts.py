from django.core.management.base import BaseCommand
from tqdm import tqdm
from discount.models import discounts
mock_data =[{
    'title': 'Voucher Bún bò',
    'percent': 0.1,
    'image': 'https://go2joy.s3.ap-southeast-1.amazonaws.com/blog/wp-content/uploads/2022/04/14172249/mon-an-viet-nam.jpg'
}]
class Command(BaseCommand):
    help = "generate mock discounts"
    def handle(self, *args, **kwargs):
        for data in mock_data:
            discounts.objects.create(
                title=data['title'],
                percent=data['percent'],
                image_discount=data['image'],
            ).save()