from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import bcrypt
from models_admin import (
    AdminUser, AdminUserCreate, AdminLogin, AdminToken,
    Order, OrderCreate, OrderUpdate, 
    DashboardStats, AnalyticsData, SalesData, TopProduct,
    SystemSettings, SystemSettingsUpdate,
    NotificationModel, NotificationCreate
)
from database import (
    categories_collection, products_collection, sellers_collection, 
    reviews_collection, get_paginated_results
)
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Admin collections
client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.environ.get('DB_NAME', 'bazari_db')]
admin_users_collection = db.admin_users
orders_collection = db.orders
settings_collection = db.settings
notifications_collection = db.notifications

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBearer()

# JWT Secret - in production, use environment variable
JWT_SECRET = "your-super-secret-jwt-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

def convert_objectid(data):
    """Convert MongoDB ObjectId to string recursively"""
    if isinstance(data, dict):
        if "_id" in data:
            data.pop("_id", None)
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    else:
        return data

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify admin JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        admin = await admin_users_collection.find_one({"username": username, "is_active": True})
        if admin is None:
            raise HTTPException(status_code=401, detail="Admin user not found")
        
        return convert_objectid(admin)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Initialize default admin user
async def init_default_admin():
    """Create default admin user if none exists"""
    admin_count = await admin_users_collection.count_documents({})
    if admin_count == 0:
        default_admin = {
            "id": "admin-001",
            "username": "admin",
            "email": "admin@bazari.com",
            "password_hash": hash_password("admin123"),
            "full_name": "مدير المنصة",
            "role": "super_admin",
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        await admin_users_collection.insert_one(default_admin)
        print("Default admin user created: admin/admin123")

# Authentication endpoints
@router.post("/login", response_model=AdminToken)
async def admin_login(login_data: AdminLogin):
    """Admin login"""
    admin = await admin_users_collection.find_one({"username": login_data.username, "is_active": True})
    if not admin or not verify_password(login_data.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update last login
    await admin_users_collection.update_one(
        {"id": admin["id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create token
    token = create_access_token({"username": admin["username"], "role": admin["role"]})
    
    admin_clean = convert_objectid(admin)
    admin_clean.pop("password_hash", None)
    
    return AdminToken(
        access_token=token,
        admin_info=admin_clean
    )

@router.get("/profile")
async def get_admin_profile(current_admin = Depends(verify_admin_token)):
    """Get current admin profile"""
    current_admin.pop("password_hash", None)
    return current_admin

# Dashboard & Analytics
@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_admin = Depends(verify_admin_token)):
    """Get dashboard statistics"""
    
    # Calculate stats
    total_orders = await orders_collection.count_documents({})
    total_products = await products_collection.count_documents({})
    total_sellers = await sellers_collection.count_documents({})
    total_customers = 0  # Will implement with user system
    
    # Revenue calculation
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$total"}}}
    ]
    revenue_result = await orders_collection.aggregate(pipeline).to_list(1)
    total_revenue = revenue_result[0]["total"] if revenue_result else 0.0
    
    # Today's stats
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    orders_today = await orders_collection.count_documents({"created_at": {"$gte": today}})
    
    # Today's revenue
    pipeline_today = [
        {"$match": {"created_at": {"$gte": today}}},
        {"$group": {"_id": None, "total": {"$sum": "$total"}}}
    ]
    revenue_today_result = await orders_collection.aggregate(pipeline_today).to_list(1)
    revenue_today = revenue_today_result[0]["total"] if revenue_today_result else 0.0
    
    # Pending orders
    pending_orders = await orders_collection.count_documents({"status": "pending"})
    
    # Low stock products (assuming stock < 10)
    low_stock_products = await products_collection.count_documents({"stockQuantity": {"$lt": 10}})
    
    return DashboardStats(
        total_orders=total_orders,
        total_revenue=total_revenue,
        total_customers=total_customers,
        total_products=total_products,
        total_sellers=total_sellers,
        orders_today=orders_today,
        revenue_today=revenue_today,
        pending_orders=pending_orders,
        low_stock_products=low_stock_products
    )

@router.get("/analytics", response_model=AnalyticsData)
async def get_analytics_data(current_admin = Depends(verify_admin_token)):
    """Get comprehensive analytics data"""
    
    # Dashboard stats
    stats = await get_dashboard_stats(current_admin)
    
    # Sales chart data (last 7 days)
    sales_data = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)
        
        # Daily orders count
        daily_orders = await orders_collection.count_documents({
            "created_at": {"$gte": date_start, "$lt": date_end}
        })
        
        # Daily revenue
        pipeline = [
            {"$match": {"created_at": {"$gte": date_start, "$lt": date_end}}},
            {"$group": {"_id": None, "total": {"$sum": "$total"}}}
        ]
        revenue_result = await orders_collection.aggregate(pipeline).to_list(1)
        daily_revenue = revenue_result[0]["total"] if revenue_result else 0.0
        
        sales_data.append(SalesData(
            date=date.strftime("%Y-%m-%d"),
            sales=daily_revenue,
            orders=daily_orders
        ))
    
    # Top products (mock data for now)
    products = await products_collection.find({}).sort("rating", -1).limit(5).to_list(5)
    products_clean = convert_objectid(products)
    top_products = [
        TopProduct(
            id=product["id"],
            title=product["title"],
            image=product["image"],
            sales_count=50,  # Mock data
            revenue=product["price"] * 50
        )
        for product in products_clean
    ]
    
    # Recent orders (mock some orders if none exist)
    recent_orders_data = await orders_collection.find({}).sort("created_at", -1).limit(5).to_list(5)
    if not recent_orders_data:
        # Create some mock orders for demo
        mock_orders = []
        for i in range(3):
            mock_order = Order(
                order_number=f"ORD-{1000 + i}",
                customer_name=f"عميل تجريبي {i + 1}",
                customer_email=f"customer{i + 1}@example.com",
                customer_phone="+966501234567",
                shipping_address={"city": "الرياض", "street": "شارع الملك فهد"},
                billing_address={"city": "الرياض", "street": "شارع الملك فهد"},
                items=[],
                subtotal=500.0,
                total=500.0,
                status="pending",
                payment_method="credit_card",
                seller_id="1"
            )
            mock_orders.append(mock_order.dict())
            await orders_collection.insert_one(mock_order.dict())
        recent_orders_data = mock_orders
    else:
        recent_orders_data = convert_objectid(recent_orders_data)
    
    recent_orders = [Order(**order) for order in recent_orders_data]
    
    return AnalyticsData(
        dashboard_stats=stats,
        sales_chart=sales_data,
        top_products=top_products,
        recent_orders=recent_orders
    )

# Orders management
@router.get("/orders")
async def get_all_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_admin = Depends(verify_admin_token)
):
    """Get all orders with pagination"""
    filter_dict = {}
    if status:
        filter_dict["status"] = status
    
    result = await get_paginated_results(orders_collection, filter_dict, page, limit, "created_at", -1)
    result["items"] = convert_objectid(result["items"])
    
    return result

@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(order_id: str, current_admin = Depends(verify_admin_token)):
    """Get specific order"""
    order = await orders_collection.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return Order(**convert_objectid(order))

@router.put("/orders/{order_id}")
async def update_order(order_id: str, order_update: OrderUpdate, current_admin = Depends(verify_admin_token)):
    """Update order"""
    update_data = {k: v for k, v in order_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await orders_collection.update_one(
        {"id": order_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order updated successfully"}

# Products management (using existing product endpoints with admin auth)
@router.get("/products")
async def admin_get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_admin = Depends(verify_admin_token)
):
    """Get all products for admin"""
    result = await get_paginated_results(products_collection, {}, page, limit)
    result["items"] = convert_objectid(result["items"])
    return result

# Categories management
@router.get("/categories")
async def admin_get_categories(current_admin = Depends(verify_admin_token)):
    """Get all categories for admin"""
    categories = await categories_collection.find({}).to_list(100)
    return convert_objectid(categories)

# Sellers management
@router.get("/sellers")
async def admin_get_sellers(current_admin = Depends(verify_admin_token)):
    """Get all sellers for admin"""
    sellers = await sellers_collection.find({}).to_list(100)
    return convert_objectid(sellers)

# Settings management
@router.get("/settings", response_model=SystemSettings)
async def get_system_settings(current_admin = Depends(verify_admin_token)):
    """Get system settings"""
    settings = await settings_collection.find_one({})
    if not settings:
        # Create default settings
        default_settings = SystemSettings()
        await settings_collection.insert_one(default_settings.dict())
        return default_settings
    
    return SystemSettings(**convert_objectid(settings))

@router.put("/settings")
async def update_system_settings(
    settings_update: SystemSettingsUpdate,
    current_admin = Depends(verify_admin_token)
):
    """Update system settings"""
    update_data = {k: v for k, v in settings_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await settings_collection.update_one(
        {},
        {"$set": update_data},
        upsert=True
    )
    
    return {"message": "Settings updated successfully"}

# Notifications
@router.get("/notifications")
async def get_notifications(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    unread_only: bool = Query(False),
    current_admin = Depends(verify_admin_token)
):
    """Get admin notifications"""
    filter_dict = {}
    if unread_only:
        filter_dict["is_read"] = False
    
    result = await get_paginated_results(
        notifications_collection, filter_dict, page, limit, "created_at", -1
    )
    result["items"] = convert_objectid(result["items"])
    
    return result

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_admin = Depends(verify_admin_token)
):
    """Mark notification as read"""
    result = await notifications_collection.update_one(
        {"id": notification_id},
        {"$set": {"is_read": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification marked as read"}