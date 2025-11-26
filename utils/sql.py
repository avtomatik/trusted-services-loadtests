from pathlib import Path


def load_sql(name: str) -> str:
    sql_path = Path(__file__).parents[1] / 'sql' / name
    return sql_path.read_text()
