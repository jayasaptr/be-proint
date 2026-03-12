import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Connect to database using environment variables
    conn = pymssql.connect(
        server=os.getenv("DB_SQLSERVER_HOST", "localhost"),
        user=os.getenv("DB_SQLSERVER_USERNAME", ""),
        password=os.getenv("DB_SQLSERVER_PASSWORD", ""),
        database=os.getenv("DB_SQLSERVER_DATABASE", "").strip('"'),
        port=os.getenv("DB_SQLSERVER_PORT", "1433")
    )

    cursor = conn.cursor()

    # Search for tables with 'Vacant' in the name
    query = """
    SELECT
        s.name AS SchemaName,
        t.name AS TableName
    FROM sys.tables t
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE t.name LIKE '%Vacant%'
       OR t.name LIKE '%VacantPos%'
       OR t.name LIKE '%RCE%'
    ORDER BY s.name, t.name
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        print("Tables found matching 'Vacant' or 'RCE':")
        print("-" * 60)
        for schema, table in rows:
            print(f"{schema}.{table}")
    else:
        print("No tables found matching 'Vacant' or 'RCE' pattern")
        print("\nLet me check all RCE tables:")

        cursor.execute("""
        SELECT s.name, t.name
        FROM sys.tables t
        INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE t.name LIKE 'RCE%'
        ORDER BY t.name
        """)

        rce_tables = cursor.fetchall()
        if rce_tables:
            print("RCE tables found:")
            for schema, table in rce_tables:
                print(f"  {schema}.{table}")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error connecting to database: {e}")
    print("\nPlease check your .env file configuration")
