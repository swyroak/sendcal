"""ETL utilities for loading data into the warehouse."""

from typing import Iterable
import csv
from sqlalchemy import create_engine


def load_csv(path: str) -> Iterable[dict]:
    """Load a CSV file and yield rows as dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def load_to_postgres(path: str, table: str, conn_str: str) -> int:
    """Load CSV rows into a PostgreSQL table using SQLAlchemy."""
    engine = create_engine(conn_str)
    rows = list(load_csv(path))
    if not rows:
        return 0
    # We rely on pandas for convenience if available
    try:
        import pandas as pd
    except Exception:
        raise RuntimeError("pandas is required for ETL operations")
    df = pd.DataFrame(rows)
    df.to_sql(table, engine, if_exists="replace", index=False)
    return len(df)
