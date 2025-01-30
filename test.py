from pprint import pprint
from lib.common import Notion

def main():
    notion = Notion()
    databases = notion.get_databases()
    pprint(databases)


if __name__ == "__main__":
    main()