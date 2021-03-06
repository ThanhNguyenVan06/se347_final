import datetime
from typing import List
class time_service:
    @staticmethod
    def get_all_weekday_to_now() -> List:
        week_day=datetime.datetime.now().isocalendar()[2]
        # Calculates Starting date (Sunday) for this case by subtracting current date with time delta of the day of the week
        start_date=datetime.datetime.now() - datetime.timedelta(days=week_day)
        # Prints the list of dates in a current week
        dates=[int((start_date + datetime.timedelta(days=i)).date().strftime("%d")) for i in range(1,8)]
        return dates
    @staticmethod
    def get_month_ab(curr_month: int) -> List:
        months= ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ab_month=[]
        for i in range(1,curr_month):
            ab_month.append(months[curr_month])
        return ab_month