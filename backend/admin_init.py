"""
Admin initialization script
Run this to set up admin collections and default data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import bcrypt

async def init_admin_data():
    """Initialize admin collections with sample data"""
    
    # MongoDB connection
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ.get('DB_NAME', 'bazari_db')]
    
    # Collections
    admin_users_collection = db.admin_users
    orders_collection = db.orders
    settings_collection = db.settings
    notifications_collection = db.notifications
    
    print("Initializing admin data...")
    
    # Check if admin user already exists
    admin_count = await admin_users_collection.count_documents({})
    if admin_count == 0:
        # Create default admin user
        password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        default_admin = {
            "id": "admin-001",
            "username": "admin",
            "email": "admin@souq-express.com",
            "password_hash": password_hash,
            "full_name": "مدير المنصة الرئيسي",
            "role": "super_admin",
            "is_active": True,
            "last_login": None,
            "created_at": datetime.utcnow()
        }
        
        await admin_users_collection.insert_one(default_admin)
        print("✅ Default admin user created:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@bazari.com")
    else:
        print("✅ Admin user already exists")
    
    # Create sample orders if none exist
    orders_count = await orders_collection.count_documents({})
    if orders_count == 0:
        sample_orders = [
            {
                "id": "order-001",
                "order_number": "ORD-2024-001",
                "customer_name": "أحمد محمد السعيد",
                "customer_email": "ahmed@example.com",
                "customer_phone": "+966501234567",
                "shipping_address": {
                    "city": "الرياض",
                    "district": "الملز",
                    "street": "شارع الملك فهد",
                    "building": "123",
                    "apartment": "45"
                },
                "billing_address": {
                    "city": "الرياض",
                    "district": "الملز", 
                    "street": "شارع الملك فهد",
                    "building": "123",
                    "apartment": "45"
                },
                "items": [
                    {
                        "product_id": "1",
                        "product_title": "هاتف سامسونج جالاكسي S24",
                        "product_image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9",
                        "quantity": 1,
                        "price": 3299.0,
                        "total": 3299.0
                    }
                ],
                "subtotal": 3299.0,
                "tax": 494.85,
                "shipping_cost": 0.0,
                "discount": 0.0,
                "total": 3793.85,
                "status": "confirmed",
                "payment_method": "credit_card",
                "payment_status": "paid",
                "seller_id": "1",
                "notes": "طلب من العميل VIP",
                "tracking_number": "TR123456789",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": "order-002",
                "order_number": "ORD-2024-002",
                "customer_name": "فاطمة علي الزهراني",
                "customer_email": "fatima@example.com",
                "customer_phone": "+966509876543",
                "shipping_address": {
                    "city": "جدة",
                    "district": "الحمراء",
                    "street": "شارع فلسطين",
                    "building": "789",
                    "apartment": "12"
                },
                "billing_address": {
                    "city": "جدة",
                    "district": "الحمراء",
                    "street": "شارع فلسطين", 
                    "building": "789",
                    "apartment": "12"
                },
                "items": [
                    {
                        "product_id": "2",
                        "product_title": "فستان أنيق للسهرات",
                        "product_image": "https://images.unsplash.com/photo-1566479179817-1b8d14f5ca6b",
                        "quantity": 2,
                        "price": 450.0,
                        "total": 900.0
                    }
                ],
                "subtotal": 900.0,
                "tax": 135.0,
                "shipping_cost": 50.0,
                "discount": 100.0,
                "total": 985.0,
                "status": "pending",
                "payment_method": "bank_transfer",
                "payment_status": "pending",
                "seller_id": "2",
                "notes": "العميل يفضل التسليم صباحاً",
                "tracking_number": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        await orders_collection.insert_many(sample_orders)
        print(f"✅ Created {len(sample_orders)} sample orders")
    else:
        print("✅ Orders already exist")
    
    # Create default settings if none exist
    settings_count = await settings_collection.count_documents({})
    if settings_count == 0:
        default_settings = {
            "id": "settings-001",
            "site_name": "منصة بازاري",
            "site_description": "أفضل منصة للتسوق الإلكتروني في العالم العربي",
            "logo_url": "https://via.placeholder.com/200x80?text=بازاري",
            "favicon_url": "https://via.placeholder.com/32x32?text=B",
            "primary_color": "#3B82F6",
            "secondary_color": "#F59E0B",
            "contact_email": "info@bazari.com",
            "contact_phone": "+966112345678",
            "social_links": {
                "facebook": "https://facebook.com/bazari",
                "twitter": "https://twitter.com/bazari",
                "instagram": "https://instagram.com/bazari",
                "youtube": "https://youtube.com/bazari"
            },
            "payment_methods": ["credit_card", "bank_transfer", "cash_on_delivery", "apple_pay", "stc_pay"],
            "shipping_methods": [
                {
                    "name": "توصيل عادي",
                    "cost": 25.0,
                    "delivery_time": "3-5 أيام عمل"
                },
                {
                    "name": "توصيل سريع",
                    "cost": 50.0,
                    "delivery_time": "24-48 ساعة"
                },
                {
                    "name": "توصيل فوري",
                    "cost": 100.0,
                    "delivery_time": "في نفس اليوم"
                }
            ],
            "tax_rate": 0.15,
            "currency": "ر.س",
            "language": "ar",
            "timezone": "Asia/Riyadh",
            "maintenance_mode": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await settings_collection.insert_one(default_settings)
        print("✅ Default system settings created")
    else:
        print("✅ System settings already exist")
    
    # Create sample notifications
    notifications_count = await notifications_collection.count_documents({})
    if notifications_count == 0:
        sample_notifications = [
            {
                "id": "notif-001",
                "type": "new_order",
                "title": "طلب جديد",
                "message": "تم استلام طلب جديد رقم ORD-2024-001",
                "is_read": False,
                "priority": "normal",
                "related_id": "order-001",
                "created_at": datetime.utcnow()
            },
            {
                "id": "notif-002",
                "type": "low_stock",
                "title": "مخزون منخفض",
                "message": "المنتج 'هاتف سامسونج جالاكسي S24' أصبح مخزونه أقل من 10 قطع",
                "is_read": False,
                "priority": "high",
                "related_id": "1",
                "created_at": datetime.utcnow()
            },
            {
                "id": "notif-003",
                "type": "new_seller",
                "title": "طلب بائع جديد",
                "message": "تم تسجيل بائع جديد ويحتاج للموافقة",
                "is_read": True,
                "priority": "normal",
                "related_id": "seller-new-001",
                "created_at": datetime.utcnow()
            }
        ]
        
        await notifications_collection.insert_many(sample_notifications)
        print(f"✅ Created {len(sample_notifications)} sample notifications")
    else:
        print("✅ Notifications already exist")
    
    client.close()
    print("\n🎉 Admin initialization completed successfully!")
    print("\n📝 Login Details:")
    print("   Admin Panel URL: /admin/login")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == "__main__":
    asyncio.run(init_admin_data())