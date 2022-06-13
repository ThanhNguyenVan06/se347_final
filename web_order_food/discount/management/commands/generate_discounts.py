from django.core.management.base import BaseCommand
from tqdm import tqdm
from discount.models import discounts
mock_data =[
{'title':'Vocher: món Bò',
'percent':'5',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Phở',
'percent':'35',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Gà',
'percent':'20',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Nướng',
'percent':'40',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Bún bò',
'percent':'35',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Bún chả giò',
'percent':'30',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Bún mắm',
'percent':'50',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Mì cay',
'percent':'25',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Phở trộn',
'percent':'20',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Thịt xiên',
'percent':'15',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Bún mắm',
'percent':'45',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Mì cay',
'percent':'20',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Phở trộn',
'percent':'20',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

{'title':'Vocher: món Thịt xiên',
'percent':'15',
'image_discount':'https://bestpac.lk/wp-content/uploads/2021/09/voucher.png'},

]
class Command(BaseCommand):
    help = "generate mock discounts"
    def handle(self, *args, **kwargs):
        for data in mock_data:
            discounts.objects.create(
                title=data['title'],
                percent=data['percent'],
                image_discount=data['image_discount'],
            ).save()