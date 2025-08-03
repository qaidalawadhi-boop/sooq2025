from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import SellerModel, SellerCreate, ProductModel
from database import sellers_collection, products_collection, get_paginated_results

router = APIRouter(prefix="/sellers", tags=["sellers"])

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

@router.get("/", response_model=List[SellerModel])
async def get_sellers():
    """Get all sellers"""
    sellers = await sellers_collection.find({}).sort("rating", -1).to_list(100)
    return [SellerModel(**seller) for seller in sellers]

@router.get("/{seller_id}", response_model=SellerModel)
async def get_seller(seller_id: str):
    """Get a specific seller"""
    seller = await sellers_collection.find_one({"id": seller_id})
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return SellerModel(**seller)

@router.get("/{seller_id}/products")
async def get_seller_products(
    seller_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=100)
):
    """Get products from a specific seller"""
    
    # Check if seller exists
    seller = await sellers_collection.find_one({"id": seller_id})
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    filter_dict = {"sellerId": seller_id}
    return await get_paginated_results(products_collection, filter_dict, page, limit)

@router.post("/", response_model=SellerModel)
async def create_seller(seller: SellerCreate):
    """Create a new seller"""
    seller_dict = seller.dict()
    seller_obj = SellerModel(**seller_dict)
    
    await sellers_collection.insert_one(seller_obj.dict())
    return seller_obj

@router.put("/{seller_id}", response_model=SellerModel)
async def update_seller(seller_id: str, seller: SellerCreate):
    """Update a seller"""
    existing_seller = await sellers_collection.find_one({"id": seller_id})
    if not existing_seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    seller_dict = seller.dict()
    seller_dict["id"] = seller_id
    seller_dict["createdAt"] = existing_seller["createdAt"]
    seller_obj = SellerModel(**seller_dict)
    
    await sellers_collection.replace_one({"id": seller_id}, seller_obj.dict())
    return seller_obj

@router.delete("/{seller_id}")
async def delete_seller(seller_id: str):
    """Delete a seller"""
    result = await sellers_collection.delete_one({"id": seller_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Seller not found")
    return {"message": "Seller deleted successfully"}