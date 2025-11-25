from typing import List, Optional
from ..config.Conection import Conection
from ..database.Clients_Schema import Client, ClientCreate, ClientUpdate

# Crear cliente
async def create_client(data: ClientCreate) -> Client:
    db = Conection()
    try:
        result = await db.execute(
            """
            INSERT INTO clients (name, email, age, details)
            VALUES (?, ?, ?, ?)
            """,
            [data.name, data.email, data.age, data.details]
        )

        new_id = result.last_insert_rowid
        if new_id is None:
            raise Exception("No se pudo obtener el ID del cliente.")

        # Obtener cliente recién creado
        result = await db.execute(
            "SELECT id, name, email, age, details, created_at, updated_at FROM clients WHERE id = ?",
            [new_id]
        )

        client_dict = dict(zip(result.columns, result.rows[0]))
        return Client(**client_dict)

    finally:
        await db.close()


# Obtener todos los clientes
async def get_all_clients() -> List[Client]:
    db = Conection()
    try:
        result = await db.execute(
            "SELECT id, name, email, age, details, created_at, updated_at FROM clients"
        )

        return [
            Client(**dict(zip(result.columns, row)))
            for row in result.rows
        ]

    finally:
        await db.close()


# Obtener cliente por ID
async def get_client_by_id(client_id: int) -> Optional[Client]:
    db = Conection()
    try:
        result = await db.execute(
            "SELECT id, name, email, age, details, created_at, updated_at FROM clients WHERE id = ?",
            [client_id]
        )

        if not result.rows:
            return None

        client_dict = dict(zip(result.columns, result.rows[0]))
        return Client(**client_dict)

    finally:
        await db.close()


# Actualizar cliente
async def update_client(client_id: int, data: ClientUpdate) -> Optional[Client]:
    db = Conection()
    try:
        existing = await get_client_by_id(client_id)
        if existing is None:
            return None

        updates = []
        params = []

        update_fields = data.model_dump(exclude_unset=True)

        for key, value in update_fields.items():
            updates.append(f"{key} = ?")
            params.append(value)

        if not updates:
            return existing

        params.append(client_id)

        update_sql = f"""
            UPDATE clients
            SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """

        await db.execute(update_sql, params)

        return await get_client_by_id(client_id)

    finally:
        await db.close()


# Eliminar cliente
async def delete_client(client_id: int) -> bool:
    db = Conection()
    try:
        result = await db.execute(
            "DELETE FROM clients WHERE id = ?",
            [client_id]
        )
        return result.rows_affected > 0

    finally:
        await db.close()
