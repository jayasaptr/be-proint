import pymssql
from app.config import Config

# Connect to database
conn = pymssql.connect(
    server=Config.DB_SERVER,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME
)

cursor = conn.cursor()

# Check for tables with 'Vacant' or 'Pos' in the name
query = """
SELECT TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
AND (TABLE_NAME LIKE '%Vacant%' OR TABLE_NAME LIKE '%Pos%' OR TABLE_NAME LIKE '%RCE%')
ORDER BY TABLE_SCHEMA, TABLE_NAME
"""

cursor.execute(query)
rows = cursor.fetchall()

print("Tables found:")
for row in rows:
    print(f"  {row[0]}.{row[1]}")

cursor.close()
conn.close()
