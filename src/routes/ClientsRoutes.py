from fastapi import APIRouter, HTTPException, status
from typing import List
from ..database.Clients_Schema import Client, ClientCreate, ClientUpdate
from ..controllers import ClientController

router_clients = APIRouter(prefix="/clients", tags=["clients"])


# Crear un cliente
@router_clients.post("/create", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client_route(data: ClientCreate):
    """
    Crea un nuevo cliente.
    """
    try:
        return await ClientController.create_client(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear cliente: {str(e)}")


# Obtener todos los clientes
@router_clients.get("/", response_model=List[Client])
async def get_all_clients_route():
    """
    Obtiene todos los clientes.
    """
    try:
        return await ClientController.get_all_clients()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener cliente por ID
@router_clients.get("/{client_id}", response_model=Client)
async def get_client_by_id_route(client_id: int):
    """
    Obtiene un cliente por su ID.
    """
    client = await ClientController.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client


# Actualizar cliente
@router_clients.put("/update/{client_id}", response_model=Client)
async def update_client_route(client_id: int, data: ClientUpdate):
    """
    Actualiza un cliente existente.
    """
    try:
        updated = await ClientController.update_client(client_id, data)
        if not updated:
            raise HTTPException(status_code=404, detail="Cliente no encontrado o no actualizado")
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Eliminar cliente
@router_clients.delete("/delete/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client_route(client_id: int):
    """
    Elimina un cliente por su ID.
    """
    deleted = await ClientController.delete_client(client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return  # Devuelve 204 No Content por defecto
