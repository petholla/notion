from pprint import pprint
from lib.notion import Notion

def main():
    notion = Notion()
    databases = notion.get_databases()
    for database in databases:
        for page in database.get_pages():
            print(page.title)


if __name__ == "__main__":
    main()