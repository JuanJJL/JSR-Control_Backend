from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from ..database.Products_schema import Product, ProductCreate, ProductUpdate
from ..database.Product_Categories_schema import Product_Category, ProductCategoryCreate
from ..controllers import ProductController

router_products = APIRouter(prefix="/products", tags=["products"])

#rutas de categorias de productos

@router_products.post("/categories/create", response_model=Product_Category, status_code=status.HTTP_201_CREATED)
async def create_category_route(data: ProductCategoryCreate):
    """Crea una nueva categoría de producto."""
    try:
        return await ProductController.create_category(data.category)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear categoría: {str(e)}")

@router_products.get("/categories", response_model=List[Product_Category])
async def get_all_categories_route():
    """Obtiene todas las categorías de productos."""
    try:
        return await ProductController.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router_products.get("/categories/{category_id}", response_model=Product_Category)
async def get_category_by_id_route(category_id: int):
    """Obtiene una categoría por su ID."""
    category = await ProductController.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return category

@router_products.put("/categories/update/{category_id}", response_model=Product_Category)
async def update_category_route(category_id: int, data: ProductCategoryCreate):
    """Actualiza una categoría existente."""
    try:
        updated_category = await ProductController.update_category(category_id, data.category)
        if not updated_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada o no actualizada")
        return updated_category
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router_products.delete("/categories/delete/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_route(category_id: int):
    """Elimina una categoría por su ID."""
    try:
        success = await ProductController.delete_category(category_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        return # Devuelve 204 No Content por defecto
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al eliminar: {str(e)}. Verifique dependencias.")

#rutas de productos

@router_products.post("/Create", response_model=Product, status_code=status.HTTP_201_CREATED,)
async def create_product_route(data: ProductCreate):
    """Crea un nuevo producto."""
    try:
        return await ProductController.create_product(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error al crear producto: {str(e)}")

@router_products.get("/", response_model=List[Product])
async def get_all_products_route():
    """Obtiene todos los productos."""
    try:
        return await ProductController.get_all_products()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router_products.get("/{product_id}", response_model=Product)
async def get_product_by_id_route(product_id: int):
    """Obtiene un producto por su ID."""
    product = await ProductController.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product

@router_products.put("/update/{product_id}", response_model=Product)
async def update_product_route(product_id: int, data: ProductUpdate):
    """Actualiza campos de un producto existente."""
    try:
        updated_product = await ProductController.update_product(product_id, data)
        if not updated_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado o no actualizado")
        return updated_product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router_products.delete("/delete/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(product_id: int):
    """Elimina un producto por su ID."""
    success = await ProductController.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return # Devuelve 204 No Content por defecto