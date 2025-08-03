#!/usr/bin/env python3
"""
Backend API Testing for Bazari E-commerce Platform
Tests all API endpoints as specified in the review request
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE_URL = f"{BACKEND_URL}/api"

class BazariAPITester:
    def __init__(self):
        self.session = None
        self.test_results = []
        self.failed_tests = []
        self.admin_token = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success:
            self.failed_tests.append(test_name)
        print()
    
    async def make_request(self, method: str, endpoint: str, **kwargs) -> tuple[bool, Any, str]:
        """Make HTTP request and return success status, data, and error message"""
        try:
            url = f"{API_BASE_URL}{endpoint}"
            print(f"Making {method} request to: {url}")
            
            async with self.session.request(method, url, **kwargs) as response:
                try:
                    data = await response.json()
                except:
                    data = await response.text()
                
                if response.status >= 200 and response.status < 300:
                    return True, data, ""
                else:
                    return False, data, f"HTTP {response.status}: {data}"
                    
        except Exception as e:
            return False, None, f"Request failed: {str(e)}"
    
    async def test_basic_api(self):
        """Test basic API endpoints"""
        print("=== Testing Basic API Endpoints ===")
        
        # Test GET /api/ (health check)
        success, data, error = await self.make_request("GET", "/")
        if success and isinstance(data, dict) and "message" in data:
            self.log_test("GET /api/ (health check)", True, f"Message: {data.get('message', '')}")
        else:
            self.log_test("GET /api/ (health check)", False, error, data)
        
        # Test GET /api/health
        success, data, error = await self.make_request("GET", "/health")
        if success and isinstance(data, dict) and data.get("status") == "healthy":
            self.log_test("GET /api/health", True, f"Status: {data.get('status', '')}")
        else:
            self.log_test("GET /api/health", False, error, data)
    
    async def test_categories_api(self):
        """Test Categories API endpoints"""
        print("=== Testing Categories API ===")
        
        # Test GET /api/categories (all categories)
        success, data, error = await self.make_request("GET", "/categories")
        categories_data = None
        if success and isinstance(data, list) and len(data) > 0:
            categories_data = data
            self.log_test("GET /api/categories", True, f"Found {len(data)} categories")
        else:
            self.log_test("GET /api/categories", False, error, data)
            return
        
        # Get first category ID for further testing
        category_id = categories_data[0].get("id") if categories_data else None
        
        if category_id:
            # Test GET /api/categories/{id} (specific category)
            success, data, error = await self.make_request("GET", f"/categories/{category_id}")
            if success and isinstance(data, dict) and data.get("id") == category_id:
                self.log_test(f"GET /api/categories/{category_id}", True, f"Category: {data.get('name', '')}")
            else:
                self.log_test(f"GET /api/categories/{category_id}", False, error, data)
            
            # Test GET /api/categories/{id}/products (category products)
            success, data, error = await self.make_request("GET", f"/categories/{category_id}/products")
            if success and isinstance(data, dict) and "items" in data:
                items_count = len(data.get("items", []))
                total = data.get("total", 0)
                self.log_test(f"GET /api/categories/{category_id}/products", True, 
                            f"Found {items_count} products (total: {total})")
            else:
                self.log_test(f"GET /api/categories/{category_id}/products", False, error, data)
        
        # Test non-existent category
        success, data, error = await self.make_request("GET", "/categories/nonexistent")
        if not success and "404" in str(error):
            self.log_test("GET /api/categories/nonexistent (404 test)", True, "Correctly returned 404")
        else:
            self.log_test("GET /api/categories/nonexistent (404 test)", False, 
                        "Should return 404 for non-existent category")
    
    async def test_products_api(self):
        """Test Products API endpoints"""
        print("=== Testing Products API ===")
        
        # Test GET /api/products (all products with pagination)
        success, data, error = await self.make_request("GET", "/products")
        products_data = None
        if success and isinstance(data, dict) and "items" in data:
            products_data = data
            items_count = len(data.get("items", []))
            total = data.get("total", 0)
            page = data.get("page", 1)
            total_pages = data.get("totalPages", 1)
            self.log_test("GET /api/products", True, 
                        f"Page {page}/{total_pages}, {items_count} items, total: {total}")
        else:
            self.log_test("GET /api/products", False, error, data)
        
        # Test pagination
        success, data, error = await self.make_request("GET", "/products?page=1&limit=5")
        if success and isinstance(data, dict) and len(data.get("items", [])) <= 5:
            self.log_test("GET /api/products (pagination)", True, 
                        f"Pagination working, got {len(data.get('items', []))} items")
        else:
            self.log_test("GET /api/products (pagination)", False, error, data)
        
        # Test GET /api/products/featured
        success, data, error = await self.make_request("GET", "/products/featured")
        if success and isinstance(data, list):
            featured_count = len(data)
            self.log_test("GET /api/products/featured", True, f"Found {featured_count} featured products")
        else:
            self.log_test("GET /api/products/featured", False, error, data)
        
        # Test GET /api/products/new
        success, data, error = await self.make_request("GET", "/products/new")
        if success and isinstance(data, list):
            new_count = len(data)
            self.log_test("GET /api/products/new", True, f"Found {new_count} new products")
        else:
            self.log_test("GET /api/products/new", False, error, data)
        
        # Test GET /api/products/trending
        success, data, error = await self.make_request("GET", "/products/trending")
        if success and isinstance(data, list):
            trending_count = len(data)
            self.log_test("GET /api/products/trending", True, f"Found {trending_count} trending products")
        else:
            self.log_test("GET /api/products/trending", False, error, data)
        
        # Get first product ID for further testing
        product_id = None
        if products_data and products_data.get("items"):
            product_id = products_data["items"][0].get("id")
        
        if product_id:
            # Test GET /api/products/{id}
            success, data, error = await self.make_request("GET", f"/products/{product_id}")
            if success and isinstance(data, dict) and data.get("id") == product_id:
                self.log_test(f"GET /api/products/{product_id}", True, 
                            f"Product: {data.get('title', '')}")
            else:
                self.log_test(f"GET /api/products/{product_id}", False, error, data)
        
        # Test GET /api/products/search
        success, data, error = await self.make_request("GET", "/products/search?q=سامسونج")
        if success and isinstance(data, dict) and "items" in data:
            search_count = len(data.get("items", []))
            self.log_test("GET /api/products/search?q=سامسونج", True, 
                        f"Found {search_count} products matching 'سامسونج'")
        else:
            self.log_test("GET /api/products/search?q=سامسونج", False, error, data)
        
        # Test search with English query
        success, data, error = await self.make_request("GET", "/products/search?q=Samsung")
        if success and isinstance(data, dict) and "items" in data:
            search_count = len(data.get("items", []))
            self.log_test("GET /api/products/search?q=Samsung", True, 
                        f"Found {search_count} products matching 'Samsung'")
        else:
            self.log_test("GET /api/products/search?q=Samsung", False, error, data)
        
        # Test search with filters
        success, data, error = await self.make_request("GET", "/products/search?q=هاتف&minPrice=1000&maxPrice=5000")
        if success and isinstance(data, dict) and "items" in data:
            search_count = len(data.get("items", []))
            self.log_test("GET /api/products/search (with filters)", True, 
                        f"Found {search_count} products with price filter")
        else:
            self.log_test("GET /api/products/search (with filters)", False, error, data)
    
    async def test_sellers_api(self):
        """Test Sellers API endpoints"""
        print("=== Testing Sellers API ===")
        
        # Test GET /api/sellers
        success, data, error = await self.make_request("GET", "/sellers")
        sellers_data = None
        if success and isinstance(data, list) and len(data) > 0:
            sellers_data = data
            self.log_test("GET /api/sellers", True, f"Found {len(data)} sellers")
        else:
            self.log_test("GET /api/sellers", False, error, data)
            return
        
        # Get first seller ID for further testing
        seller_id = sellers_data[0].get("id") if sellers_data else None
        
        if seller_id:
            # Test GET /api/sellers/{id}
            success, data, error = await self.make_request("GET", f"/sellers/{seller_id}")
            if success and isinstance(data, dict) and data.get("id") == seller_id:
                self.log_test(f"GET /api/sellers/{seller_id}", True, 
                            f"Seller: {data.get('name', '')}")
            else:
                self.log_test(f"GET /api/sellers/{seller_id}", False, error, data)
            
            # Test GET /api/sellers/{id}/products
            success, data, error = await self.make_request("GET", f"/sellers/{seller_id}/products")
            if success and isinstance(data, dict) and "items" in data:
                items_count = len(data.get("items", []))
                total = data.get("total", 0)
                self.log_test(f"GET /api/sellers/{seller_id}/products", True, 
                            f"Found {items_count} products (total: {total})")
            else:
                self.log_test(f"GET /api/sellers/{seller_id}/products", False, error, data)
        
        # Test non-existent seller
        success, data, error = await self.make_request("GET", "/sellers/nonexistent")
        if not success and "404" in str(error):
            self.log_test("GET /api/sellers/nonexistent (404 test)", True, "Correctly returned 404")
        else:
            self.log_test("GET /api/sellers/nonexistent (404 test)", False, 
                        "Should return 404 for non-existent seller")
    
    async def test_reviews_api(self):
        """Test Reviews API endpoints"""
        print("=== Testing Reviews API ===")
        
        # First get a product ID to test reviews
        success, products_data, error = await self.make_request("GET", "/products?limit=1")
        product_id = None
        
        if success and isinstance(products_data, dict) and products_data.get("items"):
            product_id = products_data["items"][0].get("id")
        
        if product_id:
            # Test GET /api/reviews/products/{id}
            success, data, error = await self.make_request("GET", f"/reviews/products/{product_id}")
            if success and isinstance(data, list):
                reviews_count = len(data)
                self.log_test(f"GET /api/reviews/products/{product_id}", True, 
                            f"Found {reviews_count} reviews for product")
            else:
                self.log_test(f"GET /api/reviews/products/{product_id}", False, error, data)
        else:
            self.log_test("GET /api/reviews/products/{id}", False, "No products found to test reviews")
        
        # Test non-existent product reviews
        success, data, error = await self.make_request("GET", "/reviews/products/nonexistent")
        if not success and "404" in str(error):
            self.log_test("GET /api/reviews/products/nonexistent (404 test)", True, "Correctly returned 404")
        else:
            self.log_test("GET /api/reviews/products/nonexistent (404 test)", False, 
                        "Should return 404 for non-existent product")
    
    async def test_data_structure_validation(self):
        """Test that returned data structures are correct"""
        print("=== Testing Data Structure Validation ===")
        
        # Test category structure
        success, data, error = await self.make_request("GET", "/categories")
        if success and isinstance(data, list) and len(data) > 0:
            category = data[0]
            required_fields = ["id", "name", "nameEn", "icon", "subCategories", "isActive"]
            missing_fields = [field for field in required_fields if field not in category]
            
            if not missing_fields:
                self.log_test("Category data structure", True, "All required fields present")
            else:
                self.log_test("Category data structure", False, f"Missing fields: {missing_fields}")
        
        # Test product structure
        success, data, error = await self.make_request("GET", "/products")
        if success and isinstance(data, dict) and data.get("items"):
            product = data["items"][0]
            required_fields = ["id", "title", "price", "rating", "image", "categoryId", "sellerId"]
            missing_fields = [field for field in required_fields if field not in product]
            
            if not missing_fields:
                self.log_test("Product data structure", True, "All required fields present")
            else:
                self.log_test("Product data structure", False, f"Missing fields: {missing_fields}")
        
        # Test seller structure
        success, data, error = await self.make_request("GET", "/sellers")
        if success and isinstance(data, list) and len(data) > 0:
            seller = data[0]
            required_fields = ["id", "name", "rating", "location", "logo", "description"]
            missing_fields = [field for field in required_fields if field not in seller]
            
            if not missing_fields:
                self.log_test("Seller data structure", True, "All required fields present")
            else:
                self.log_test("Seller data structure", False, f"Missing fields: {missing_fields}")
    
    async def test_admin_authentication(self):
        """Test Admin Authentication APIs"""
        print("=== Testing Admin Authentication ===")
        
        # Test POST /api/admin/login
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        success, data, error = await self.make_request("POST", "/admin/login", json=login_data)
        if success and isinstance(data, dict) and "access_token" in data:
            self.admin_token = data["access_token"]
            admin_info = data.get("admin_info", {})
            self.log_test("POST /api/admin/login", True, 
                        f"Login successful, admin: {admin_info.get('username', '')}")
        else:
            self.log_test("POST /api/admin/login", False, error, data)
            return None
        
        # Test GET /api/admin/profile (requires authentication)
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        success, data, error = await self.make_request("GET", "/admin/profile", headers=headers)
        if success and isinstance(data, dict) and data.get("username") == "admin":
            self.log_test("GET /api/admin/profile", True, 
                        f"Profile retrieved: {data.get('full_name', '')}")
        else:
            self.log_test("GET /api/admin/profile", False, error, data)
        
        return self.admin_token
    
    async def test_admin_dashboard(self):
        """Test Admin Dashboard APIs"""
        print("=== Testing Admin Dashboard ===")
        
        if not hasattr(self, 'admin_token') or not self.admin_token:
            self.log_test("Admin Dashboard Tests", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/admin/dashboard/stats
        success, data, error = await self.make_request("GET", "/admin/dashboard/stats", headers=headers)
        if success and isinstance(data, dict):
            required_fields = ["total_orders", "total_revenue", "total_customers", "total_products", 
                             "total_sellers", "orders_today", "revenue_today", "pending_orders", "low_stock_products"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                self.log_test("GET /api/admin/dashboard/stats", True, 
                            f"Stats: {data.get('total_orders', 0)} orders, {data.get('total_products', 0)} products")
            else:
                self.log_test("GET /api/admin/dashboard/stats", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("GET /api/admin/dashboard/stats", False, error, data)
        
        # Test GET /api/admin/analytics
        success, data, error = await self.make_request("GET", "/admin/analytics", headers=headers)
        if success and isinstance(data, dict):
            required_fields = ["dashboard_stats", "sales_chart", "top_products", "recent_orders"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                sales_chart_count = len(data.get("sales_chart", []))
                top_products_count = len(data.get("top_products", []))
                recent_orders_count = len(data.get("recent_orders", []))
                self.log_test("GET /api/admin/analytics", True, 
                            f"Analytics: {sales_chart_count} sales data points, {top_products_count} top products, {recent_orders_count} recent orders")
            else:
                self.log_test("GET /api/admin/analytics", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("GET /api/admin/analytics", False, error, data)
    
    async def test_admin_orders_management(self):
        """Test Admin Orders Management APIs"""
        print("=== Testing Admin Orders Management ===")
        
        if not hasattr(self, 'admin_token') or not self.admin_token:
            self.log_test("Admin Orders Tests", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/admin/orders
        success, data, error = await self.make_request("GET", "/admin/orders", headers=headers)
        orders_data = None
        if success and isinstance(data, dict) and "items" in data:
            orders_data = data
            items_count = len(data.get("items", []))
            total = data.get("total", 0)
            self.log_test("GET /api/admin/orders", True, 
                        f"Found {items_count} orders (total: {total})")
        else:
            self.log_test("GET /api/admin/orders", False, error, data)
        
        # Test pagination
        success, data, error = await self.make_request("GET", "/admin/orders?page=1&limit=5", headers=headers)
        if success and isinstance(data, dict) and len(data.get("items", [])) <= 5:
            self.log_test("GET /api/admin/orders (pagination)", True, 
                        f"Pagination working, got {len(data.get('items', []))} items")
        else:
            self.log_test("GET /api/admin/orders (pagination)", False, error, data)
        
        # Test specific order if orders exist
        if orders_data and orders_data.get("items"):
            order_id = orders_data["items"][0].get("id")
            if order_id:
                # Test GET /api/admin/orders/{id}
                success, data, error = await self.make_request("GET", f"/admin/orders/{order_id}", headers=headers)
                if success and isinstance(data, dict) and data.get("id") == order_id:
                    self.log_test(f"GET /api/admin/orders/{order_id}", True, 
                                f"Order details: {data.get('order_number', '')}")
                else:
                    self.log_test(f"GET /api/admin/orders/{order_id}", False, error, data)
                
                # Test PUT /api/admin/orders/{id} (update order)
                update_data = {"status": "confirmed", "notes": "تم تأكيد الطلب من قبل الإدمن"}
                success, data, error = await self.make_request("PUT", f"/admin/orders/{order_id}", 
                                                             json=update_data, headers=headers)
                if success and isinstance(data, dict) and "message" in data:
                    self.log_test(f"PUT /api/admin/orders/{order_id}", True, "Order updated successfully")
                else:
                    self.log_test(f"PUT /api/admin/orders/{order_id}", False, error, data)
        else:
            self.log_test("Admin Orders Detail Tests", False, "No orders found to test specific operations")
    
    async def test_admin_products_management(self):
        """Test Admin Products Management APIs"""
        print("=== Testing Admin Products Management ===")
        
        if not hasattr(self, 'admin_token') or not self.admin_token:
            self.log_test("Admin Products Tests", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/admin/products
        success, data, error = await self.make_request("GET", "/admin/products", headers=headers)
        if success and isinstance(data, dict) and "items" in data:
            items_count = len(data.get("items", []))
            total = data.get("total", 0)
            self.log_test("GET /api/admin/products", True, 
                        f"Found {items_count} products (total: {total})")
        else:
            self.log_test("GET /api/admin/products", False, error, data)
    
    async def test_admin_categories_management(self):
        """Test Admin Categories Management APIs"""
        print("=== Testing Admin Categories Management ===")
        
        if not hasattr(self, 'admin_token') or not self.admin_token:
            self.log_test("Admin Categories Tests", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/admin/categories
        success, data, error = await self.make_request("GET", "/admin/categories", headers=headers)
        if success and isinstance(data, list) and len(data) > 0:
            self.log_test("GET /api/admin/categories", True, f"Found {len(data)} categories")
        else:
            self.log_test("GET /api/admin/categories", False, error, data)
    
    async def test_admin_sellers_management(self):
        """Test Admin Sellers Management APIs"""
        print("=== Testing Admin Sellers Management ===")
        
        if not hasattr(self, 'admin_token') or not self.admin_token:
            self.log_test("Admin Sellers Tests", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/admin/sellers
        success, data, error = await self.make_request("GET", "/admin/sellers", headers=headers)
        if success and isinstance(data, list) and len(data) > 0:
            self.log_test("GET /api/admin/sellers", True, f"Found {len(data)} sellers")
        else:
            self.log_test("GET /api/admin/sellers", False, error, data)
    
    async def test_admin_settings(self):
        """Test Admin Settings APIs"""
        print("=== Testing Admin Settings ===")
        
        if not hasattr(self, 'admin_token') or not self.admin_token:
            self.log_test("Admin Settings Tests", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/admin/settings
        success, data, error = await self.make_request("GET", "/admin/settings", headers=headers)
        settings_data = None
        if success and isinstance(data, dict):
            settings_data = data
            required_fields = ["site_name", "currency", "language", "tax_rate"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                self.log_test("GET /api/admin/settings", True, 
                            f"Settings: {data.get('site_name', '')}, currency: {data.get('currency', '')}")
            else:
                self.log_test("GET /api/admin/settings", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("GET /api/admin/settings", False, error, data)
        
        # Test PUT /api/admin/settings
        update_data = {
            "site_name": "منصة بازاري المحدثة",
            "contact_email": "admin@bazari-updated.com",
            "tax_rate": 0.16
        }
        success, data, error = await self.make_request("PUT", "/admin/settings", 
                                                     json=update_data, headers=headers)
        if success and isinstance(data, dict) and "message" in data:
            self.log_test("PUT /api/admin/settings", True, "Settings updated successfully")
        else:
            self.log_test("PUT /api/admin/settings", False, error, data)
    
    async def test_admin_notifications(self):
        """Test Admin Notifications APIs"""
        print("=== Testing Admin Notifications ===")
        
        if not hasattr(self, 'admin_token') or not self.admin_token:
            self.log_test("Admin Notifications Tests", False, "No admin token available")
            return
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # Test GET /api/admin/notifications
        success, data, error = await self.make_request("GET", "/admin/notifications", headers=headers)
        notifications_data = None
        if success and isinstance(data, dict) and "items" in data:
            notifications_data = data
            items_count = len(data.get("items", []))
            total = data.get("total", 0)
            self.log_test("GET /api/admin/notifications", True, 
                        f"Found {items_count} notifications (total: {total})")
        else:
            self.log_test("GET /api/admin/notifications", False, error, data)
        
        # Test specific notification if notifications exist
        if notifications_data and notifications_data.get("items"):
            notification_id = notifications_data["items"][0].get("id")
            if notification_id:
                # Test PUT /api/admin/notifications/{id}/read
                success, data, error = await self.make_request("PUT", f"/admin/notifications/{notification_id}/read", 
                                                             headers=headers)
                if success and isinstance(data, dict) and "message" in data:
                    self.log_test(f"PUT /api/admin/notifications/{notification_id}/read", True, 
                                "Notification marked as read")
                else:
                    self.log_test(f"PUT /api/admin/notifications/{notification_id}/read", False, error, data)
        else:
            self.log_test("Admin Notifications Detail Tests", False, "No notifications found to test specific operations")
    
    async def test_admin_authentication_security(self):
        """Test Admin Authentication Security"""
        print("=== Testing Admin Authentication Security ===")
        
        # Test accessing admin endpoint without token
        success, data, error = await self.make_request("GET", "/admin/profile")
        if not success and ("401" in str(error) or "403" in str(error)):
            self.log_test("Admin endpoint without token (security test)", True, "Correctly rejected unauthorized access")
        else:
            self.log_test("Admin endpoint without token (security test)", False, "Should reject unauthorized access")
        
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid-token-12345"}
        success, data, error = await self.make_request("GET", "/admin/profile", headers=headers)
        if not success and ("401" in str(error) or "403" in str(error)):
            self.log_test("Admin endpoint with invalid token (security test)", True, "Correctly rejected invalid token")
        else:
            self.log_test("Admin endpoint with invalid token (security test)", False, "Should reject invalid token")
        
        # Test login with wrong credentials
        wrong_login_data = {
            "username": "admin",
            "password": "wrongpassword"
        }
        success, data, error = await self.make_request("POST", "/admin/login", json=wrong_login_data)
        if not success and "401" in str(error):
            self.log_test("Admin login with wrong credentials (security test)", True, "Correctly rejected wrong credentials")
        else:
            self.log_test("Admin login with wrong credentials (security test)", False, "Should reject wrong credentials")

    async def run_all_tests(self):
        """Run all API tests"""
        print(f"Starting Bazari Backend API Tests")
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base URL: {API_BASE_URL}")
        print("=" * 60)
        
        try:
            # Test basic APIs first
            await self.test_basic_api()
            await self.test_categories_api()
            await self.test_products_api()
            await self.test_sellers_api()
            await self.test_reviews_api()
            await self.test_data_structure_validation()
            
            # Test Admin APIs (NEW)
            await self.test_admin_authentication()
            await self.test_admin_dashboard()
            await self.test_admin_orders_management()
            await self.test_admin_products_management()
            await self.test_admin_categories_management()
            await self.test_admin_sellers_management()
            await self.test_admin_settings()
            await self.test_admin_notifications()
            await self.test_admin_authentication_security()
            
        except Exception as e:
            print(f"Error during testing: {e}")
            self.log_test("Test execution", False, str(e))
        
        # Print summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = len(self.failed_tests)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%")
        
        if self.failed_tests:
            print("\nFailed Tests:")
            for test in self.failed_tests:
                print(f"  - {test}")
        
        return passed_tests, failed_tests, self.test_results

async def main():
    """Main test execution function"""
    async with BazariAPITester() as tester:
        passed, failed, results = await tester.run_all_tests()
        
        # Return appropriate exit code
        return 0 if failed == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)