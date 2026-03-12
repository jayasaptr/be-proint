import pymssql
from app.config import Config

try:
    # Connect to database
    conn = pymssql.connect(
        server=Config.DB_SERVER,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )

    cursor = conn.cursor()

    # List all tables
    query = """
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE = 'BASE TABLE'
    ORDER BY TABLE_NAME
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print("All tables in database:")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]}.{row[1]}")

    print("\n" + "="*60)
    print("Tables with 'Vacant' in name:")
    print("-" * 60)
    for row in rows:
        if 'vacant' in row[1].lower():
            print(f"{row[0]}.{row[1]}")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
