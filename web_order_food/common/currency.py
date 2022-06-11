import locale

class Currency:
    locale.setlocale(locale.LC_ALL, 'en_US')
    @staticmethod
    def convert_currency(number):
        return locale.format("%d", number, grouping=True)