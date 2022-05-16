from functools import lru_cache
from menu.models import category


class category_service:
    @staticmethod
    @lru_cache
    def get_category_dict() -> dict:
        """
        Function return the dict with key is category and value is 0
        """
        category_dict={}
        query_set= category.objects.all()
        for query in query_set:
            category_dict[query.category]=0
        return category_dict