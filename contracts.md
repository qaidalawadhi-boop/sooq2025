# عقود API لمنصة سوق إكسبرس

## نظرة عامة
هذا المستند يحدد عقود API بين Frontend (React) و Backend (FastAPI) لمنصة سوق إكسبرس.

## البيانات المُوكيد الحالية في mock/data.js
- `mockCategories`: أقسام المنتجات
- `mockProducts`: المنتجات مع تفاصيلها
- `mockSellers`: معلومات البائعين
- `mockReviews`: التقييمات والمراجعات
- `mockBanners`: البانرات الإعلانية

## نماذج البيانات المطلوبة

### 1. Category Model
```javascript
{
  id: string,
  name: string,
  nameEn: string,
  icon: string,
  subCategories: string[],
  createdAt: datetime,
  isActive: boolean
}
```

### 2. Product Model
```javascript
{
  id: string,
  title: string,
  titleEn: string,
  price: number,
  originalPrice: number,
  currency: string,
  rating: number,
  reviewCount: number,
  image: string,
  images: string[],
  categoryId: string,
  sellerId: string,
  description: string,
  specifications: [{key: string, value: string}],
  inStock: boolean,
  stockQuantity: number,
  discount: number,
  isNew: boolean,
  isFeatured: boolean,
  createdAt: datetime,
  updatedAt: datetime
}
```

### 3. Seller Model
```javascript
{
  id: string,
  name: string,
  nameEn: string,
  rating: number,
  reviewCount: number,
  location: string,
  joinDate: datetime,
  logo: string,
  banner: string,
  description: string,
  categories: string[],
  productCount: number,
  isVerified: boolean,
  policies: {
    shipping: string,
    returns: string,
    warranty: string
  },
  createdAt: datetime
}
```

### 4. Review Model
```javascript
{
  id: string,
  productId: string,
  userId: string,
  userName: string,
  rating: number,
  comment: string,
  date: datetime,
  helpful: number,
  verified: boolean
}
```

## API Endpoints المطلوبة

### Categories
- `GET /api/categories` - جلب جميع الأقسام
- `GET /api/categories/{id}` - جلب قسم محدد
- `GET /api/categories/{id}/products` - جلب منتجات قسم معين

### Products
- `GET /api/products` - جلب جميع المنتجات مع pagination و filters
- `GET /api/products/{id}` - جلب منتج محدد
- `GET /api/products/featured` - جلب المنتجات المميزة
- `GET /api/products/new` - جلب المنتجات الجديدة
- `GET /api/products/trending` - جلب المنتجات الأكثر طلباً
- `GET /api/products/search?q={query}` - البحث في المنتجات

### Sellers
- `GET /api/sellers` - جلب جميع البائعين
- `GET /api/sellers/{id}` - جلب بائع محدد
- `GET /api/sellers/{id}/products` - جلب منتجات بائع معين

### Reviews
- `GET /api/products/{id}/reviews` - جلب مراجعات منتج
- `POST /api/products/{id}/reviews` - إضافة مراجعة جديدة

### Search
- `GET /api/search?q={query}&category={id}&minPrice={price}&maxPrice={price}` - البحث المتقدم

## تغييرات Frontend المطلوبة

### 1. استبدال Mock Data
- إزالة استيراد `mock/data.js` من الـ components
- استبداله بـ API calls باستخدام axios
- إضافة loading states و error handling

### 2. إضافة API Service
- إنشاء `src/services/api.js` للتعامل مع API calls
- استخدام REACT_APP_BACKEND_URL environment variable

### 3. Components التي تحتاج تعديل
- `HomePage.js`: استخدام API calls بدلاً من mock data
- `Header.js`: ربط البحث بـ API
- المكونات المستقبلية: ProductPage, CategoryPage, SearchPage

## خطة التكامل

### المرحلة 1: Backend Development
1. إنشاء MongoDB models
2. تطوير API endpoints
3. إضافة sample data لقاعدة البيانات
4. اختبار APIs

### المرحلة 2: Frontend Integration
1. إنشاء API service layer
2. تعديل HomePage لاستخدام APIs
3. إضافة loading states
4. اختبار التكامل

### المرحلة 3: صفحات إضافية
1. صفحة المنتج
2. صفحة القسم
3. صفحة البحث
4. صفحة البائع

## متطلبات البيئة
- Backend: FastAPI + MongoDB + Motor (async)
- Frontend: React + Axios
- Database: MongoDB مع collections منفصلة لكل model