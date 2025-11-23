# src/models/Users.py
from ..config.Conection import Conection

async def create_users_table():
    db = Conection()
    try:
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
        print("Tabla 'users' verificada/creada exitosamente.")
    except Exception as e:
        print(f"Error al crear la tabla 'users': {e}")
    finally:
        # Cerrar la conexión para evitar advertencias de aiohttp
        await db.close()