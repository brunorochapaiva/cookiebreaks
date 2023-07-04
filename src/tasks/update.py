from src.config import parse_config
from src.database import insert_missing_breaks


def update():
    config = parse_config()
    insert_missing_breaks(config)


if __name__ == "__main__":
    update()
