from ..config.Conection import Conection

async def create_product_tables():
    db = Conection()
    try:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS product_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category VARCHAR(30) NOT NULL UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(30) NOT NULL,
                price INTEGER NOT NULL,
                cost INTEGER NOT NULL,
                stock INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (category_id) REFERENCES product_categories(id)
            );
        """)
        print("Tablas de productos verificadas/creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas de productos: {e}")
    finally:
        await db.close()