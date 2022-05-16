from menu.models import food
class food_service:
    @staticmethod
    def get_total_price_from_queryset(query_set):
        total_price=0
        for query in query_set:
            for id_food in query.id_foods.split(","):
                total_price+= food.objects.get(id=id_food).price
        return total_price
