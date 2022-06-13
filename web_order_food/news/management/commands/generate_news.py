from django.core.management.base import BaseCommand
from tqdm import tqdm
from news.models import news
from faker import Faker
import json
import sqlite3
mock_data =[
    {'title':"Mì Quảng",
'context': "Món ăn này là đặc sản của tỉnh Quảng Nam nhưng được ưa chuộng trên khắp cả nước. Nguyên liệu gồm sợi mì, đậu phộng, bánh đa, thịt lợn quay và nước dùng có màu vàng của nghệ. Không ít du khách quốc tế khi được thưởng thức mì Quảng khi đến Việt Nam đã ca ngợi đây là món ăn hoàn hảo.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/1-1565953389-845-width1440height960.jpg"},

{'title':"Phở",
'context': "Mỗi ngày ở Việt Nam có hàng triệu bát phở được phục vụ. Đây luôn được coi là món ăn nổi tiếng nhất và hấp dẫn nhất của nền ẩm thực Việt trong mắt du khách quốc tế.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/2-1565953389-205-width1440height960.jpg"},

{'title':"Gỏi cuốn",
'context': "Đây là món ăn nhẹ hoàn hảo của Việt Nam, với các thành phần chính như tôm, miến, thịt lợn và rau xanh rất tốt cho sức khỏe được bọc trong lớp bánh tráng mỏng, dai.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/3-1565953389-541-width1440height953.jpg"},

{'title':"Bò kho",
'context': "Món ăn này được đặc biệt yêu thích vào bữa sáng hoặc trưa. Đầu bếp có thể thay thế thịt bò bằng bất kỳ loại thịt nào khác, ninh trong lửa nhỏ với nước mắm, đường và nước dừa tươi, cà rốt, hành tây và rau mùi.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/4-1565953389-213-width1440height1080.jpg"},

{'title':"Bún chả",
'context': "Bún chả là một đại diện của phong cách ẩm thực Hà Nội. Các thành phần chính gồm bún gạo, thịt lợn nướng, nước mắm và rất nhiều loại gia vị và rau thơm ăn kèm.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/5-1565953389-440-width1440height1080.jpg"},

{'title':"Chả giò",
'context':"Những chiếc nem được làm từ thịt lợn băm, trứng, nấm tai mèo và các loại rau củ được gói trong bánh tráng rồi chiên giòn ngập dầu.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/6-1565953389-571-width1440height1080.jpg"},

{'title':"Bún mắm",
'context': "Món ăn này được người dân địa phương biến tấu với nhiều nguyên liệu khác nhau, tùy theo từng vùng miền.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/7-1565953389-416-width1440height965.jpg"},

{'title':"Gà nướng",
'context': "Gà nướng sả cũng tương tự như các món bún nổi tiếng khác của Việt Nam, chỉ khác là nguyên liệu chính từ thịt gà ướp sả, nướng thơm phức vô cùng hấp dẫn.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/8-1565953389-535-width1440height960.jpg"},

{'title':"Cơm tấm",
'context': "Đây là bữa trưa vô cùng phổ biến ở Sài Gòn, với đĩa cơm tấm ăn kèm với thịt lợn hoặc sườn lợn nướng, dưa muối chua và một số loại rau gia vị.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/9-1565953389-330-width1440height1080.jpg"},

{'title':"Mực chiên",
'context': "Mực ống được sắt miếng vừa phải và tẩm bột chiên giòn. Món ăn này được mọi lứa tuổi và vùng miền yêu thích vì rất dễ ăn.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/10-1565953389-469-width1440height969.jpg"},

{'title':"Bún bò Huế",
'context': "Ẩm thực cố đô Huế nổi tiếng với hương vị hài hòa giữa cay, chua, mặn và ngọt - và Bún bò Huế là một ví dụ tuyệt vời.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/11-1565953389-274-width1440height965.jpg"},

{'title':"Bánh mì",
'context': "Hàng triệu ổ bánh mì được nướng mỗi ngày, không chỉ ngon, giá rẻ mà còn đầy đủ chất dinh dưỡng và cơ động cho một bữa sáng vội vàng.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/12-1565953389-847-width1440height1080.jpg"},

{'title':"Cá kho tộ",
'context': "Cá được đun sôi liên tục trong dầu ăn, nước hàng, tỏi, hành, muối, nước mắm và nước dừa bên trong nồi đất sét nung tạo nên hương vị vô cùng hấp dẫn.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/13-1565953389-177-width1440height1080.jpg"},

{'title':"Bánh xèo",
'context': "Bột bánh xèo được làm từ bột gạo và bột nghệ, tráng mỏng, giòn, phần nhân làm từ thịt bò, tôm, giá đỗ ăn kèm với các loại rau thơm, chấm nước mắm chua ngọt vô cùng hấp dẫn.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/14-1565953389-659-width1440height958.jpg"},

{'title':"Gỏi",
'context': "Các món nộm/ gỏi thường có nguyên liệu chính từ đu đủ xanh bào sợ, bắp cải thái chỉ,... kèm với các loại thịt lợn, thịt gà, đậu phộng, ",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/15-1565953389-669-width1440height1080.jpg"},

{'title':"Cao lầu",
'context': "Món cao lầu là đặc sản của Hội An. Dù được biến tấu theo nhiều phong cách và hương vị khác nhau, nhưng món ăn này chỉ hấp dẫn nhất khi được thưởng thức tại quê hương của nó.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/17-1565953389-305-width1440height965.jpg"},

{'title':"muống xào",
'context': "Rau muống xanh mướt được xào với tỏi và dầu ăn béo ngậy. Ngay cả những người không thích ăn rau xanh cũng dễ “xiêu lòng” với món ăn dân dã này.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/16-1565953389-8-width1440height1080.jpg"},

{'title':"Chả cá",
'context': "Cá được ướp với bột nghệ, gừng, tỏi và nước mắm. Khi ăn, thực khách sẽ chiên nó trên chảo với rau thì là và hành lá, ăn kèm với bún gạo. ",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/18-1565953389-74-width1440height960.jpg"},

{'title':"Ốc",
'context': "Người Việt rất thích ăn ốc và các loại ốc ở đây cũng vô cùng đa dạng cả về chủng loại và cách chế biến",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/19-1565953389-361-width594height440.jpg"},

{'title':"Bột chiên",
'context': "Bột chiên giòn với trứng và hành lá là món ăn sáng khá hấp dẫn. Món ăn này thường được bày bán trên các xe đẩy ở đường phố miền Nam Việt Nam.",
'link_seemore': "https://www.24h.com.vn/am-thuc/20-mon-an-ngon-nhat-viet-nam-duoc-bao-tay-vi-nhu-huong-vi-thien-duong-c460a1075365.html",
'image_new':"https://icdn.24h.com.vn/upload/3-2019/images/2019-08-16/20-1565953389-257-width1440height995.jpg"},






]
class Command(BaseCommand):
    help = "generate mock mock news"
    def handle(self, *args, **kwargs):
        for data in mock_data:
            news.objects.create(
                title=data['title'],
                link_seemore=data['link_seemore'],
                context=data['context'],
                image_new=data['image_new'],
            ).save()