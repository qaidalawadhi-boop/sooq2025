from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models import ProductModel, ProductCreate, PaginationParams, PaginatedResponse
from database import products_collection, get_paginated_results
import re

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=dict)
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
    categoryId: Optional[str] = None,
    sellerId: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    inStock: Optional[bool] = None,
    isNew: Optional[bool] = None,
    isFeatured: Optional[bool] = None,
    search: Optional[str] = None
):
    """Get products with filtering and pagination"""
    
    # Build filter
    filter_dict = {}
    
    if categoryId:
        filter_dict["categoryId"] = categoryId
    if sellerId:
        filter_dict["sellerId"] = sellerId
    if minPrice is not None:
        filter_dict["price"] = {"$gte": minPrice}
    if maxPrice is not None:
        if "price" in filter_dict:
            filter_dict["price"]["$lte"] = maxPrice
        else:
            filter_dict["price"] = {"$lte": maxPrice}
    if inStock is not None:
        filter_dict["inStock"] = inStock
    if isNew is not None:
        filter_dict["isNew"] = isNew
    if isFeatured is not None:
        filter_dict["isFeatured"] = isFeatured
    if search:
        filter_dict["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    return await get_paginated_results(products_collection, filter_dict, page, limit)

@router.get("/featured", response_model=List[ProductModel])
async def get_featured_products():
    """Get featured products"""
    products = await products_collection.find({"isFeatured": True}).to_list(20)
    return [ProductModel(**product) for product in products]

@router.get("/new", response_model=List[ProductModel])
async def get_new_products():
    """Get new products"""
    products = await products_collection.find({"isNew": True}).to_list(20)
    return [ProductModel(**product) for product in products]

@router.get("/trending", response_model=List[ProductModel])
async def get_trending_products():
    """Get trending products (highest rated)"""
    products = await products_collection.find({}).sort("rating", -1).limit(8).to_list(8)
    return [ProductModel(**product) for product in products]

@router.get("/search")
async def search_products(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100),
    categoryId: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None
):
    """Search products"""
    
    filter_dict = {
        "$or": [
            {"title": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"titleEn": {"$regex": q, "$options": "i"}}
        ]
    }
    
    if categoryId:
        filter_dict["categoryId"] = categoryId
    if minPrice is not None:
        filter_dict["price"] = {"$gte": minPrice}
    if maxPrice is not None:
        if "price" in filter_dict:
            filter_dict["price"]["$lte"] = maxPrice
        else:
            filter_dict["price"] = {"$lte": maxPrice}
    
    return await get_paginated_results(products_collection, filter_dict, page, limit)

@router.get("/{product_id}", response_model=ProductModel)
async def get_product(product_id: str):
    """Get a specific product"""
    product = await products_collection.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductModel(**product)

@router.post("/", response_model=ProductModel)
async def create_product(product: ProductCreate):
    """Create a new product"""
    product_dict = product.dict()
    product_obj = ProductModel(**product_dict)
    
    await products_collection.insert_one(product_obj.dict())
    return product_obj

@router.put("/{product_id}", response_model=ProductModel)
async def update_product(product_id: str, product: ProductCreate):
    """Update a product"""
    existing_product = await products_collection.find_one({"id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_dict = product.dict()
    product_dict["id"] = product_id
    product_dict["createdAt"] = existing_product["createdAt"]
    product_obj = ProductModel(**product_dict)
    
    await products_collection.replace_one({"id": product_id}, product_obj.dict())
    return product_obj

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    """Delete a product"""
    result = await products_collection.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}