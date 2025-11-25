from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from ..database.Product_Categories_schema import Product_Category, ProductCategoryCreate
from ..controllers import ProductController

router_ProductsCategory = APIRouter(prefix="/products", tags=["products"])


@router_ProductsCategory.post("/categories/create", response_model=Product_Category, status_code=status.HTTP_201_CREATED)
async def create_category_route(data: ProductCategoryCreate):
    """Crea una nueva categoría de producto."""
    try:
        return await ProductController.create_category(data.category)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear categoría: {str(e)}")

@router_ProductsCategory.get("/categories", response_model=List[Product_Category])
async def get_all_categories_route():
    """Obtiene todas las categorías de productos."""
    try:
        return await ProductController.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router_ProductsCategory.get("/categories/{category_id}", response_model=Product_Category)
async def get_category_by_id_route(category_id: int):
    """Obtiene una categoría por su ID."""
    category = await ProductController.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return category

@router_ProductsCategory.put("/categories/update/{category_id}", response_model=Product_Category)
async def update_category_route(category_id: int, data: ProductCategoryCreate):
    """Actualiza una categoría existente."""
    try:
        updated_category = await ProductController.update_category(category_id, data.category)
        if not updated_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada o no actualizada")
        return updated_category
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router_ProductsCategory.delete("/categories/delete/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_route(category_id: int):
    """Elimina una categoría por su ID."""
    try:
        success = await ProductController.delete_category(category_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        return # Devuelve 204 No Content por defecto
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al eliminar: {str(e)}. Verifique dependencias.")
