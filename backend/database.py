from motor.motor_asyncio import AsyncIOMotorClient
from models import CategoryModel, ProductModel, SellerModel, ReviewModel, BannerModel
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
categories_collection = db.categories
products_collection = db.products
sellers_collection = db.sellers
reviews_collection = db.reviews
banners_collection = db.banners

async def init_sample_data():
    """Initialize database with sample data"""
    
    # Check if data already exists
    if await categories_collection.count_documents({}) > 0:
        return
    
    print("Initializing sample data...")
    
    # Sample Categories
    categories = [
        {
            "id": "1",
            "name": "الإلكترونيات",
            "nameEn": "Electronics",
            "icon": "smartphone",
            "subCategories": ["هواتف ذكية", "حاسوب وتابلت", "اكسسوارات إلكترونية"],
            "createdAt": datetime.utcnow(),
            "isActive": True
        },
        {
            "id": "2",
            "name": "الأزياء",
            "nameEn": "Fashion",
            "icon": "shirt",
            "subCategories": ["ملابس رجالية", "ملابس نسائية", "أحذية", "حقائب واكسسوارات"],
            "createdAt": datetime.utcnow(),
            "isActive": True
        },
        {
            "id": "3",
            "name": "المنزل والحديقة",
            "nameEn": "Home & Garden",
            "icon": "home",
            "subCategories": ["أثاث", "ديكور المنزل", "أدوات المطبخ", "نباتات وحدائق"],
            "createdAt": datetime.utcnow(),
            "isActive": True
        },
        {
            "id": "4",
            "name": "الجمال والعناية",
            "nameEn": "Beauty & Care",
            "icon": "sparkles",
            "subCategories": ["مستحضرات التجميل", "العناية بالبشرة", "العطور", "العناية بالشعر"],
            "createdAt": datetime.utcnow(),
            "isActive": True
        },
        {
            "id": "5",
            "name": "الرياضة واللياقة",
            "nameEn": "Sports & Fitness",
            "icon": "dumbbell",
            "subCategories": ["معدات رياضية", "ملابس رياضية", "مكملات غذائية"],
            "createdAt": datetime.utcnow(),
            "isActive": True
        },
        {
            "id": "6",
            "name": "الكتب والتعليم",
            "nameEn": "Books & Education",
            "icon": "book",
            "subCategories": ["كتب", "أدوات مكتبية", "ألعاب تعليمية"],
            "createdAt": datetime.utcnow(),
            "isActive": True
        }
    ]
    
    # Sample Sellers
    sellers = [
        {
            "id": "1",
            "name": "متجر التقنية المتقدمة",
            "nameEn": "Advanced Tech Store",
            "rating": 4.9,
            "reviewCount": 1243,
            "location": "الرياض، السعودية",
            "joinDate": datetime(2021, 3, 15),
            "logo": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80",
            "banner": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80",
            "description": "متخصصون في بيع أحدث الأجهزة الإلكترونية والتقنية بأفضل الأسعار وضمان شامل.",
            "categories": ["الإلكترونيات", "اكسسوارات إلكترونية"],
            "productCount": 156,
            "isVerified": True,
            "policies": {
                "shipping": "شحن مجاني للطلبات أكثر من 500 ريال",
                "returns": "إرجاع مجاني خلال 30 يوم",
                "warranty": "ضمان شامل لجميع المنتجات"
            },
            "createdAt": datetime(2021, 3, 15)
        },
        {
            "id": "2",
            "name": "بوتيك الأناقة",
            "nameEn": "Elegance Boutique",
            "rating": 4.7,
            "reviewCount": 867,
            "location": "دبي، الإمارات",
            "joinDate": datetime(2020, 8, 22),
            "logo": "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=100&q=80",
            "banner": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80",
            "description": "أزياء نسائية راقية وحقائب وإكسسوارات من أفضل الماركات العالمية.",
            "categories": ["الأزياء", "حقائب واكسسوارات"],
            "productCount": 89,
            "isVerified": True,
            "policies": {
                "shipping": "شحن سريع خلال 24 ساعة",
                "returns": "إرجاع مجاني خلال 15 يوم",
                "warranty": "ضمان الجودة"
            },
            "createdAt": datetime(2020, 8, 22)
        }
    ]
    
    # Sample Products
    products = [
        {
            "id": "1",
            "title": "هاتف سامسونج جالاكسي S24",
            "titleEn": "Samsung Galaxy S24",
            "price": 3299,
            "originalPrice": 3599,
            "currency": "ر.س",
            "rating": 4.8,
            "reviewCount": 234,
            "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80",
            "images": [
                "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80"
            ],
            "categoryId": "1",
            "sellerId": "1",
            "description": "هاتف سامسونج جالاكسي S24 الجديد مع أحدث التقنيات وكاميرا عالية الجودة. يأتي مع ضمان لمدة عامين ومواصفات ممتازة للاستخدام اليومي.",
            "specifications": [
                {"key": "الشاشة", "value": "6.2 بوصة Dynamic AMOLED"},
                {"key": "المعالج", "value": "Snapdragon 8 Gen 3"},
                {"key": "الذاكرة", "value": "8GB RAM, 256GB"},
                {"key": "الكاميرا", "value": "50MP + 12MP + 10MP"},
                {"key": "البطارية", "value": "4000mAh"}
            ],
            "inStock": True,
            "stockQuantity": 15,
            "discount": 8,
            "isNew": True,
            "isFeatured": True,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "id": "2",
            "title": "فستان أنيق للسهرات",
            "titleEn": "Elegant Evening Dress",
            "price": 450,
            "originalPrice": 520,
            "currency": "ر.س",
            "rating": 4.6,
            "reviewCount": 89,
            "image": "https://images.unsplash.com/photo-1566479179817-1b8d14f5ca6b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80",
            "images": [
                "https://images.unsplash.com/photo-1566479179817-1b8d14f5ca6b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80",
                "https://images.unsplash.com/photo-1544441893-675973e31985?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80"
            ],
            "categoryId": "2",
            "sellerId": "2",
            "description": "فستان أنيق مثالي للسهرات والمناسبات الخاصة. مصنوع من أجود الأقمشة ومتوفر بألوان مختلفة.",
            "specifications": [
                {"key": "المقاس", "value": "S, M, L, XL"},
                {"key": "اللون", "value": "أزرق، أسود، أحمر"},
                {"key": "القماش", "value": "حرير طبيعي"},
                {"key": "العناية", "value": "غسيل جاف فقط"}
            ],
            "inStock": True,
            "stockQuantity": 8,
            "discount": 13,
            "isNew": False,
            "isFeatured": True,
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
    ]
    
    # Insert data
    await categories_collection.insert_many(categories)
    await sellers_collection.insert_many(sellers)
    await products_collection.insert_many(products)
    
    print("Sample data initialized successfully!")

# Utility functions
async def get_paginated_results(collection, filter_dict, page: int, limit: int, sort_field: str = "createdAt", sort_order: int = -1):
    """Get paginated results from a collection"""
    skip = (page - 1) * limit
    
    cursor = collection.find(filter_dict).sort(sort_field, sort_order).skip(skip).limit(limit)
    items = await cursor.to_list(limit)
    total = await collection.count_documents(filter_dict)
    total_pages = (total + limit - 1) // limit
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "totalPages": total_pages
    }