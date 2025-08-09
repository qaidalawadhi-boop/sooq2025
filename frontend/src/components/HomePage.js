import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Star, Heart, ShoppingCart, Eye, Zap, TrendingUp, Gift, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { categoriesAPI, productsAPI } from '../services/api';

const HomePage = () => {
  const [currentBanner, setCurrentBanner] = useState(0);
  const [categories, setCategories] = useState([]);
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [newProducts, setNewProducts] = useState([]);
  const [trendingProducts, setTrendingProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mock banners for now (can be moved to API later)
  const mockBanners = [
    {
      id: '1',
      title: 'تخفيضات الجمعة البيضاء',
      subtitle: 'خصومات تصل إلى 70% على جميع المنتجات',
      image: 'https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
      cta: 'تسوق الآن',
      link: '/categories'
    },
    {
      id: '2',
      title: 'إلكترونيات جديدة',
      subtitle: 'اكتشف أحدث الأجهزة والتقنيات',
      image: 'https://images.unsplash.com/photo-1498049794561-7780e7231661?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80',
      cta: 'استكشف',
      link: '/categories/electronics'
    }
  ];

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        // Load real data from APIs
        const [categoriesData, featuredData, newData, trendingData] = await Promise.all([
          categoriesAPI.getAll(),
          productsAPI.getFeatured(),
          productsAPI.getNew(),
          productsAPI.getTrending()
        ]);
        
        setCategories(categoriesData || []);
        setFeaturedProducts(featuredData || []);
        setNewProducts(newData || []);
        setTrendingProducts(trendingData || []);
        
        setError(null);
      } catch (err) {
        setError('حدث خطأ في تحميل البيانات');
        console.error('Error loading homepage data:', err);
        
        // Fallback to mock data on error
        try {
          const { mockCategories, mockProducts } = await import('../mock/data');
          setCategories(mockCategories || []);
          setFeaturedProducts(mockProducts.filter(product => product.isFeatured) || []);
          setNewProducts(mockProducts.filter(product => product.isNew) || []);
          setTrendingProducts(mockProducts.slice(0, 4) || []);
        } catch (fallbackErr) {
          console.error('Error loading mock data:', fallbackErr);
        }
      } finally {
        setLoading(false);
      }
    };

    loadData();

    // Auto-rotate banner
    const interval = setInterval(() => {
      setCurrentBanner((prev) => (prev + 1) % mockBanners.length);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const nextBanner = () => {
    setCurrentBanner((prev) => (prev + 1) % mockBanners.length);
  };

  const prevBanner = () => {
    setCurrentBanner((prev) => (prev - 1 + mockBanners.length) % mockBanners.length);
  };

  const ProductCard = ({ product }) => (
    <Card className="group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 border-0 shadow-md">
      <CardContent className="p-0">
        <div className="relative overflow-hidden rounded-t-lg">
          <img
            src={product.image}
            alt={product.title}
            className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-500"
          />
          {product.discount > 0 && (
            <Badge className="absolute top-3 right-3 bg-red-500 hover:bg-red-600 text-white">
              -{product.discount}%
            </Badge>
          )}
          {product.isNew && (
            <Badge className="absolute top-3 left-3 bg-green-500 hover:bg-green-600 text-white">
              جديد
            </Badge>
          )}
          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
            <div className="flex space-x-2 space-x-reverse">
              <Button size="sm" variant="secondary" className="rounded-full p-2">
                <Eye className="h-4 w-4" />
              </Button>
              <Button size="sm" variant="secondary" className="rounded-full p-2">
                <Heart className="h-4 w-4" />
              </Button>
              <Button size="sm" variant="secondary" className="rounded-full p-2">
                <ShoppingCart className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
        
        <div className="p-4">
          <div className="mb-2">
            <h3 className="font-semibold text-sm mb-1 line-clamp-2 text-gray-900 group-hover:text-blue-600 transition-colors">
              {product.title}
            </h3>
            <p className="text-xs text-gray-500">{product.category || 'منتج'}</p>
          </div>
          
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-1 space-x-reverse">
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
              <span className="text-sm font-medium text-gray-700">{product.rating}</span>
              <span className="text-xs text-gray-500">({product.reviewCount})</span>
            </div>
            <div className="text-left">
              <div className="flex items-center space-x-1 space-x-reverse">
                <span className="text-lg font-bold text-blue-600">{product.price}</span>
                <span className="text-sm text-gray-500">{product.currency}</span>
              </div>
              {product.originalPrice > product.price && (
                <span className="text-xs text-gray-400 line-through">
                  {product.originalPrice} {product.currency}
                </span>
              )}
            </div>
          </div>
          
          <Button className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg py-2 transition-all duration-300">
            <ShoppingCart className="h-4 w-4 ml-2" />
            أضف للسلة
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">جارٍ تحميل المنصة...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
            <p className="text-red-600 mb-2">حدث خطأ في تحميل البيانات</p>
            <p className="text-sm text-red-500">{error}</p>
          </div>
          <Button 
            onClick={() => window.location.reload()} 
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            إعادة المحاولة
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Banner */}
      <section className="relative bg-gradient-to-r from-blue-900 via-blue-800 to-purple-900 overflow-hidden">
        <div className="absolute inset-0 bg-black bg-opacity-30"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div className="text-white">
              <div className="flex items-center space-x-2 space-x-reverse mb-4">
                <Zap className="h-6 w-6 text-yellow-400" />
                <span className="text-yellow-400 font-semibold">منصة سوق إكسبرس</span>
              </div>
              <h1 className="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
                أفضل وجهة للتسوق
                <span className="block text-yellow-400">الإلكتروني</span>
              </h1>
              <p className="text-xl mb-8 text-gray-200 leading-relaxed">
                اكتشف آلاف المنتجات من أفضل المتاجر العربية. جودة عالية، أسعار منافسة، وتسليم سريع.
              </p>
              <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 sm:space-x-reverse">
                <Link to="/categories">
                  <Button size="lg" className="w-full sm:w-auto bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white font-semibold px-8 py-3 rounded-lg shadow-lg transform hover:scale-105 transition-all duration-300">
                    ابدأ التسوق الآن
                    <ChevronLeft className="mr-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/sellers">
                  <Button size="lg" variant="outline" className="w-full sm:w-auto border-2 border-white text-white hover:bg-white hover:text-blue-900 px-8 py-3 rounded-lg font-semibold transition-all duration-300">
                    انضم كبائع
                  </Button>
                </Link>
              </div>
            </div>
            <div className="hidden lg:block">
              <div className="relative">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-4">
                    {featuredProducts.slice(0, 2).map((product, index) => (
                      <div key={product.id} className={`bg-white rounded-xl p-4 shadow-xl transform ${index === 0 ? 'rotate-3' : '-rotate-2'} hover:rotate-0 transition-transform duration-500`}>
                        <img src={product.image} alt="منتج" className="w-full h-24 object-cover rounded-lg mb-2" />
                        <p className="text-sm font-semibold text-gray-800">{product.title}</p>
                      </div>
                    ))}
                  </div>
                  <div className="space-y-4 mt-8">
                    {featuredProducts.slice(2, 4).map((product, index) => (
                      <div key={product.id} className={`bg-white rounded-xl p-4 shadow-xl transform ${index === 0 ? 'rotate-2' : '-rotate-1'} hover:rotate-0 transition-transform duration-500`}>
                        <img src={product.image} alt="منتج" className="w-full h-24 object-cover rounded-lg mb-2" />
                        <p className="text-sm font-semibold text-gray-800">{product.title}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1200 120" preserveAspectRatio="none" className="relative block w-full h-12 fill-gray-50">
            <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25"></path>
            <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5"></path>
            <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z"></path>
          </svg>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">تسوق حسب الأقسام</h2>
            <p className="text-gray-600 max-w-2xl mx-auto">اكتشف مجموعة واسعة من المنتجات في مختلف الأقسام</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category) => (
              <Link
                key={category.id}
                to={`/categories/${category.id}`}
                className="group"
              >
                <Card className="text-center hover:shadow-lg transition-all duration-300 border-0 shadow-md hover:-translate-y-2">
                  <CardContent className="p-6">
                    <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                      <span className="text-white text-2xl">📱</span>
                    </div>
                    <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {category.name}
                    </h3>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">المنتجات المميزة</h2>
              <p className="text-gray-600">أفضل المنتجات المختارة خصيصاً لك</p>
            </div>
            <Link to="/categories">
              <Button variant="outline" className="flex items-center space-x-2 space-x-reverse hover:bg-blue-50 hover:border-blue-300">
                <span>عرض المزيد</span>
                <ChevronLeft className="h-4 w-4" />
              </Button>
            </Link>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.length > 0 ? (
              featuredProducts.map((product) => (
                <Link key={product.id} to={`/products/${product.id}`}>
                  <ProductCard product={product} />
                </Link>
              ))
            ) : (
              <div className="col-span-4 text-center py-8">
                <p className="text-gray-500">لا توجد منتجات مميزة متاحة حالياً</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* New Products */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-12">
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="bg-green-500 p-2 rounded-lg">
                <Gift className="h-6 w-6 text-white" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-gray-900">المنتجات الجديدة</h2>
                <p className="text-gray-600">أحدث المنتجات في السوق</p>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {newProducts.length > 0 ? (
              newProducts.map((product) => (
                <Link key={product.id} to={`/products/${product.id}`}>
                  <ProductCard product={product} />
                </Link>
              ))
            ) : (
              <div className="col-span-4 text-center py-8">
                <p className="text-gray-500">لا توجد منتجات جديدة متاحة حالياً</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Trending Products */}
      <section className="py-16 bg-gradient-to-r from-gray-100 to-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-12">
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="bg-orange-500 p-2 rounded-lg">
                <TrendingUp className="h-6 w-6 text-white" />
              </div>
              <div>
                <h2 className="text-3xl font-bold text-gray-900">الأكثر طلباً</h2>
                <p className="text-gray-600">المنتجات الأكثر شعبية</p>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {trendingProducts.length > 0 ? (
              trendingProducts.map((product) => (
                <Link key={product.id} to={`/products/${product.id}`}>
                  <ProductCard product={product} />
                </Link>
              ))
            ) : (
              <div className="col-span-4 text-center py-8">
                <p className="text-gray-500">لا توجد منتجات رائجة متاحة حالياً</p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Newsletter */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-purple-700">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            اشترك في النشرة الإخبارية
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            احصل على أحدث العروض والمنتجات الجديدة مباشرة في بريدك الإلكتروني
          </p>
          <div className="flex flex-col sm:flex-row max-w-md mx-auto">
            <input
              type="email"
              placeholder="أدخل بريدك الإلكتروني"
              className="flex-1 px-6 py-3 rounded-r-lg sm:rounded-l-none border-0 text-right focus:ring-4 focus:ring-blue-300"
            />
            <Button className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold px-8 py-3 rounded-l-lg sm:rounded-r-none mt-2 sm:mt-0">
              اشترك
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;