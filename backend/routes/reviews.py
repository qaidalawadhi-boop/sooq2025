from fastapi import APIRouter, HTTPException, Query
from typing import List
from models import ReviewModel, ReviewCreate
from database import reviews_collection, products_collection

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/products/{product_id}", response_model=List[ReviewModel])
async def get_product_reviews(product_id: str):
    """Get all reviews for a specific product"""
    # Check if product exists
    product = await products_collection.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    reviews = await reviews_collection.find({"productId": product_id}).sort("date", -1).to_list(100)
    return [ReviewModel(**review) for review in reviews]

@router.post("/products/{product_id}", response_model=ReviewModel)
async def create_review(product_id: str, review: ReviewCreate):
    """Create a new review for a product"""
    # Check if product exists
    product = await products_collection.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create review
    review_dict = review.dict()
    review_dict["productId"] = product_id
    review_obj = ReviewModel(**review_dict)
    
    await reviews_collection.insert_one(review_obj.dict())
    
    # Update product rating and review count
    all_reviews = await reviews_collection.find({"productId": product_id}).to_list(1000)
    new_rating = sum(r["rating"] for r in all_reviews) / len(all_reviews)
    
    await products_collection.update_one(
        {"id": product_id},
        {
            "$set": {
                "rating": round(new_rating, 1),
                "reviewCount": len(all_reviews)
            }
        }
    )
    
    return review_obj

@router.put("/reviews/{review_id}/helpful")
async def mark_review_helpful(review_id: str):
    """Mark a review as helpful"""
    result = await reviews_collection.update_one(
        {"id": review_id},
        {"$inc": {"helpful": 1}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"message": "Review marked as helpful"}

@router.delete("/reviews/{review_id}")
async def delete_review(review_id: str):
    """Delete a review"""
    review = await reviews_collection.find_one({"id": review_id})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Delete review
    await reviews_collection.delete_one({"id": review_id})
    
    # Update product rating and review count
    product_id = review["productId"]
    remaining_reviews = await reviews_collection.find({"productId": product_id}).to_list(1000)
    
    if remaining_reviews:
        new_rating = sum(r["rating"] for r in remaining_reviews) / len(remaining_reviews)
        new_count = len(remaining_reviews)
    else:
        new_rating = 0
        new_count = 0
    
    await products_collection.update_one(
        {"id": product_id},
        {
            "$set": {
                "rating": round(new_rating, 1),
                "reviewCount": new_count
            }
        }
    )
    
    return {"message": "Review deleted successfully"}