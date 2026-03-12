"""
Script untuk melihat ukuran kolom sebenarnya di database SQL Server
"""
from app import create_app, db

app = create_app()

with app.app_context():
    # Query untuk mendapatkan ukuran kolom tabel RCECandidate
    query = """
    SELECT
        c.COLUMN_NAME,
        c.DATA_TYPE,
        c.CHARACTER_MAXIMUM_LENGTH,
        c.IS_NULLABLE
    FROM INFORMATION_SCHEMA.COLUMNS c
    WHERE c.TABLE_NAME = 'RCECandidate'
    AND c.TABLE_SCHEMA = 'dbo'
    ORDER BY c.ORDINAL_POSITION
    """

    result = db.session.execute(db.text(query))

    print("\n" + "="*80)
    print("UKURAN KOLOM TABEL RCECandidate DI DATABASE SQL SERVER:")
    print("="*80)
    print(f"{'Kolom':<30} {'Tipe':<15} {'Max Length':<12} {'Nullable'}")
    print("-"*80)

    for row in result:
        column_name, data_type, max_length, is_nullable = row
        max_len_str = str(max_length) if max_length else "N/A"
        print(f"{column_name:<30} {data_type:<15} {max_len_str:<12} {is_nullable}")

    print("="*80)
    print("\nField dengan ukuran KECIL yang perlu diperhatikan:")
    print("-"*80)

    result2 = db.session.execute(db.text(query))
    for row in result2:
        column_name, data_type, max_length, is_nullable = row
        if max_length and max_length < 20 and data_type in ['varchar', 'char', 'nvarchar', 'nchar']:
            print(f"  ⚠️  {column_name}: max hanya {max_length} chars!")

    print("="*80)
