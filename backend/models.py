from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class CategoryModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    nameEn: str
    icon: str
    subCategories: List[str] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    isActive: bool = True

class CategoryCreate(BaseModel):
    name: str
    nameEn: str
    icon: str
    subCategories: List[str] = []
    isActive: bool = True

class ProductSpecification(BaseModel):
    key: str
    value: str

class SellerPolicy(BaseModel):
    shipping: str
    returns: str
    warranty: str

class ProductModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    titleEn: str
    price: float
    originalPrice: float
    currency: str = "ر.س"
    rating: float = 0.0
    reviewCount: int = 0
    image: str
    images: List[str] = []
    categoryId: str
    sellerId: str
    description: str
    specifications: List[ProductSpecification] = []
    inStock: bool = True
    stockQuantity: int = 0
    discount: float = 0.0
    isNew: bool = False
    isFeatured: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    title: str
    titleEn: str
    price: float
    originalPrice: float
    currency: str = "ر.س"
    image: str
    images: List[str] = []
    categoryId: str
    sellerId: str
    description: str
    specifications: List[ProductSpecification] = []
    inStock: bool = True
    stockQuantity: int = 0
    discount: float = 0.0
    isNew: bool = False
    isFeatured: bool = False

class SellerModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    nameEn: str
    rating: float = 0.0
    reviewCount: int = 0
    location: str
    joinDate: datetime = Field(default_factory=datetime.utcnow)
    logo: str
    banner: str
    description: str
    categories: List[str] = []
    productCount: int = 0
    isVerified: bool = False
    policies: SellerPolicy
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class SellerCreate(BaseModel):
    name: str
    nameEn: str
    location: str
    logo: str
    banner: str
    description: str
    categories: List[str] = []
    isVerified: bool = False
    policies: SellerPolicy

class ReviewModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    productId: str
    userId: str
    userName: str
    rating: int = Field(ge=1, le=5)
    comment: str
    date: datetime = Field(default_factory=datetime.utcnow)
    helpful: int = 0
    verified: bool = False

class ReviewCreate(BaseModel):
    productId: str
    userId: str
    userName: str
    rating: int = Field(ge=1, le=5)
    comment: str
    verified: bool = False

class BannerModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    image: str
    cta: str
    link: str
    isActive: bool = True
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class ProductFilter(BaseModel):
    categoryId: Optional[str] = None
    sellerId: Optional[str] = None
    minPrice: Optional[float] = None
    maxPrice: Optional[float] = None
    inStock: Optional[bool] = None
    isNew: Optional[bool] = None
    isFeatured: Optional[bool] = None
    search: Optional[str] = None

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=12, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    totalPages: int