from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import CategoryModel, CategoryCreate, ProductModel
from database import categories_collection, products_collection, get_paginated_results

router = APIRouter(prefix="/categories", tags=["categories"])

def convert_objectid(data):
    """Convert MongoDB ObjectId to string recursively"""
    if isinstance(data, dict):
        if "_id" in data:
            data.pop("_id", None)  # Remove MongoDB _id field
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    else:
        return data

@router.get("/", response_model=List[CategoryModel])
async def get_categories():
    """Get all categories"""
    categories = await categories_collection.find({"isActive": True}).to_list(100)
    cleaned_categories = convert_objectid(categories)
    return [CategoryModel(**category) for category in cleaned_categories]

@router.get("/{category_id}", response_model=CategoryModel)
async def get_category(category_id: str):
    """Get a specific category"""
    category = await categories_collection.find_one({"id": category_id, "isActive": True})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    cleaned_category = convert_objectid(category)
    return CategoryModel(**cleaned_category)

@router.get("/{category_id}/products")
async def get_category_products(
    category_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100)
):
    """Get products in a specific category"""
    
    # Check if category exists
    category = await categories_collection.find_one({"id": category_id, "isActive": True})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    filter_dict = {"categoryId": category_id}
    result = await get_paginated_results(products_collection, filter_dict, page, limit)
    result["items"] = convert_objectid(result["items"])
    
    return result

@router.post("/", response_model=CategoryModel)
async def create_category(category: CategoryCreate):
    """Create a new category"""
    category_dict = category.dict()
    category_obj = CategoryModel(**category_dict)
    
    await categories_collection.insert_one(category_obj.dict())
    return category_obj

@router.put("/{category_id}", response_model=CategoryModel)
async def update_category(category_id: str, category: CategoryCreate):
    """Update a category"""
    existing_category = await categories_collection.find_one({"id": category_id})
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_dict = category.dict()
    category_dict["id"] = category_id
    category_dict["createdAt"] = existing_category["createdAt"]
    category_obj = CategoryModel(**category_dict)
    
    await categories_collection.replace_one({"id": category_id}, category_obj.dict())
    return category_obj

@router.delete("/{category_id}")
async def delete_category(category_id: str):
    """Delete a category"""
    result = await categories_collection.delete_one({"id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}