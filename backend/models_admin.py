from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Admin User Models
class AdminUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    password_hash: str
    full_name: str
    role: str = "admin"  # admin, super_admin
    is_active: bool = True
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str = "admin"

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_info: Dict[str, Any]

# Order Models
class OrderStatus(BaseModel):
    pending: str = "pending"
    confirmed: str = "confirmed" 
    processing: str = "processing"
    shipped: str = "shipped"
    delivered: str = "delivered"
    cancelled: str = "cancelled"
    refunded: str = "refunded"

class OrderItem(BaseModel):
    product_id: str
    product_title: str
    product_image: str
    quantity: int
    price: float
    total: float

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: Dict[str, str]
    billing_address: Dict[str, str]
    items: List[OrderItem]
    subtotal: float
    tax: float = 0.0
    shipping_cost: float = 0.0
    discount: float = 0.0
    total: float
    status: str = "pending"
    payment_method: str
    payment_status: str = "pending"  # pending, paid, failed, refunded
    seller_id: str
    notes: Optional[str] = None
    tracking_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: Dict[str, str]
    billing_address: Dict[str, str]
    items: List[OrderItem]
    payment_method: str
    seller_id: str
    notes: Optional[str] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = None

# Analytics Models
class DashboardStats(BaseModel):
    total_orders: int
    total_revenue: float
    total_customers: int
    total_products: int
    total_sellers: int
    orders_today: int
    revenue_today: float
    pending_orders: int
    low_stock_products: int

class SalesData(BaseModel):
    date: str
    sales: float
    orders: int

class TopProduct(BaseModel):
    id: str
    title: str
    image: str
    sales_count: int
    revenue: float

class AnalyticsData(BaseModel):
    dashboard_stats: DashboardStats
    sales_chart: List[SalesData]
    top_products: List[TopProduct]
    recent_orders: List[Order]

# System Settings Models
class SystemSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    site_name: str = "منصة بازاري"
    site_description: str = "منصة التجارة الإلكترونية الرائدة في المملكة العربية السعودية"
    logo_url: str = "/images/logo.png"
    favicon_url: str = "/images/favicon.ico"
    primary_color: str = "#3B82F6"
    secondary_color: str = "#F59E0B"
    contact_email: str = "info@bazari.com"
    contact_phone: str = "+966501234567"
    social_links: Dict[str, str] = {}
    payment_methods: List[str] = ["credit_card", "bank_transfer", "cash_on_delivery"]
    shipping_methods: List[Dict[str, Any]] = []
    tax_rate: float = 0.15
    currency: str = "ر.س"
    language: str = "ar"
    timezone: str = "Asia/Riyadh"
    maintenance_mode: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SystemSettingsUpdate(BaseModel):
    site_name: Optional[str] = None
    site_description: Optional[str] = None
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None
    payment_methods: Optional[List[str]] = None
    shipping_methods: Optional[List[Dict[str, Any]]] = None
    tax_rate: Optional[float] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    maintenance_mode: Optional[bool] = None

# Notification Models
class NotificationModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # new_order, low_stock, new_seller, system_alert
    title: str
    message: str
    is_read: bool = False
    priority: str = "normal"  # low, normal, high, urgent
    related_id: Optional[str] = None  # Related order, product, seller ID
    created_at: datetime = Field(default_factory=datetime.utcnow)

class NotificationCreate(BaseModel):
    type: str
    title: str
    message: str
    priority: str = "normal"
    related_id: Optional[str] = None