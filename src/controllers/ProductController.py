from ..config.Conection import Conection
from ..database.Products_schema import Product, ProductCreate, ProductUpdate
from typing import List, Optional
#crud de productos

async def create_product(data: ProductCreate) -> Product:
    db = Conection()
    try:
        insert_result = await db.execute(
            "INSERT INTO products (name, price, cost, stock, category_id) VALUES (?, ?, ?, ?, ?)",
            [data.name, data.price, data.cost, data.stock, data.category_id]
        )
        
        new_id = insert_result.last_insert_rowid
        if new_id is None:
             raise Exception("No se pudo obtener el ID del producto.")

        #aqui se recupera el objeto completo
        result = await db.execute(
            "SELECT id, name, price, cost, stock, category_id, created_at, updated_at FROM products WHERE id = ?",
            [new_id]
        )
            
        product_dict = dict(zip(result.columns, result.rows[0]))
        return Product(**product_dict)
    
    finally:
        await db.close()
        
async def get_all_products() -> List[Product]:
    db = Conection()
    try:
        result = await db.execute(
            "SELECT id, name, price, cost, stock, category_id, created_at, updated_at FROM products"
        )
        
        return [
            Product(**dict(zip(result.columns, row)))
            for row in result.rows
        ]
    finally:
        await db.close()

async def get_product_by_id(product_id: int) -> Optional[Product]:
    db = Conection()
    try:
        result = await db.execute(
            "SELECT id, name, price, cost, stock, category_id, created_at, updated_at FROM products WHERE id = ?",
            [product_id]
        )
        
        if not result.rows:
            return None
            
        product_dict = dict(zip(result.columns, result.rows[0]))
        return Product(**product_dict)
    
    finally:
        await db.close()

async def update_product(product_id: int, data: ProductUpdate) -> Optional[Product]:
    db = Conection()
    try:
        #se obtiene el producto existente
        existing_product = await get_product_by_id(product_id)
        if existing_product is None:
            return None

        # 2. Construir la lista de campos a actualizar
        updates = []
        params = []
        
        # Mapear los campos de Pydantic a SQL
        update_fields = data.model_dump(exclude_unset=True)

        for key, value in update_fields.items():
            if key in ["name", "price", "cost", "stock", "category_id"]:
                updates.append(f"{key} = ?")
                params.append(value)

        if not updates:
            return existing_product #si no hay cambios, devuelve el objeto existente

        #Ejecuta el UPDATE
        params.append(product_id)
        
        update_sql = f"UPDATE products SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        await db.execute(update_sql, params)

        return await get_product_by_id(product_id)
        
    finally:
        await db.close()

async def delete_product(product_id: int) -> bool:
    db = Conection()
    try:
        result = await db.execute(
            "DELETE FROM products WHERE id = ?",
            [product_id]
        )

        return result.rows_affected > 0
    finally:
        await db.close()
