from ..config.Conection import Conection
from ..database.Product_Categories_schema import Product_Category
from typing import List, Optional

async def create_category(category_name: str) -> Product_Category: #el Product_Create se importa desde el schema y se usa para validar los datos de entrada
    db = Conection()
    try:
        insert_result = await db.execute(
            "INSERT INTO product_categories (category) VALUES (?)",
            [category_name]
        )
        
        new_id = insert_result.last_insert_rowid
        if new_id is None:
             raise Exception("No se pudo obtener el ID de la categoría.")

        result = await db.execute(
            "SELECT id, category, created_at, updated_at FROM product_categories WHERE id = ?",
            [new_id]
        )

        category_dict = dict(zip(result.columns, result.rows[0])) #se crea el diccionario a partir de las columnas y la fila
        return Product_Category(**category_dict) #los 2 asteriscos descomprimen el diccionario en argumentos de palabra clave es decir, key=value
    finally:
        await db.close()

async def get_all_categories() -> List[Product_Category]:
    db = Conection()
    try:
        result = await db.execute("SELECT id, category, created_at, updated_at FROM product_categories")
        
        return [
            Product_Category(**dict(zip(result.columns, row)))
            for row in result.rows
        ]
    finally:
        await db.close()

async def get_category_by_id(category_id: int) -> Optional[Product_Category]:
    db = Conection()
    try:
        result = await db.execute(
            "SELECT id, category, created_at, updated_at FROM product_categories WHERE id = ?",
            [category_id]
        )
        
        if not result.rows:
            return None
            
        category_dict = dict(zip(result.columns, result.rows[0]))
        return Product_Category(**category_dict)
    
    finally:
        await db.close()

async def update_category(category_id: int, new_category_name: str) -> Optional[Product_Category]:
    db = Conection()
    try:
        update_sql = "UPDATE product_categories SET category = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        update_result = await db.execute(
            update_sql,
            [new_category_name, category_id]
        )
        
        if update_result.rows_affected == 0:
            return None # Categoría no encontrada

        #se recupera el objeto actualizado
        return await get_category_by_id(category_id)
        
    finally:
        await db.close()

async def delete_category(category_id: int) -> bool:
    db = Conection()
    try:
        #no se puede eliminar si hay productos asociados
        result = await db.execute(
            "DELETE FROM product_categories WHERE id = ?",
            [category_id]
        )
        # este return devuelve True si se eliminó al menos una fila
        return result.rows_affected > 0
    finally:
        await db.close()
