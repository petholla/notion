import logging
from pprint import pprint
from datetime import datetime, timedelta
from lib.notion import Notion
from lib.common import get_logger

logger = get_logger()
logger.setLevel(logging.INFO)

def get_next_days(days):
    next_days = []
    for day in range(days):
        dt = datetime.now() + timedelta(days=day)
        next_days.append(dt.strftime("%Y-%m-%d %a").upper())
    return next_days

def get_daily_pages():
    notion = Notion()
    databases = notion.get_databases()
    daily_pages = []
    for database in databases:
#        database.add_page("xxx")
        pprint(database)
        for page in database.get_pages():
            daily_pages.append(page.title)

    return daily_pages

def main():
    notion = Notion()
    database = notion.get_database("Journal 2025")
    print(database)

    return


    next_days = get_next_days(7)
    daily_pages = get_daily_pages()

    for day in next_days:
        if day in daily_pages:
            print(f"{day} found.")
        else:
            print(f"{day} is missing.")

if __name__ == "__main__":
    main()