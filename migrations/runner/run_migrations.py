import os, glob
import psycopg
from psycopg.rows import tuple_row

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise SystemExit("DATABASE_URL não definido")

sql_files = sorted(glob.glob("/runner/sql/*.sql"))

print(f"Aplicando migrations em {DATABASE_URL} ...")
with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor(row_factory=tuple_row) as cur:
        for path in sql_files:
            print(f"-> Executando {os.path.basename(path)}")
            with open(path, "r", encoding="utf-8") as f:
                cur.execute(f.read())
        conn.commit()
print("Migrations aplicadas com sucesso.")
