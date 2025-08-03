import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, ShoppingCart, User, Heart, Menu, X } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { categoriesAPI } from '../services/api';

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [categories, setCategories] = useState([]);
  const [cartItems] = useState(3); // Mock cart count
  const navigate = useNavigate();

  useEffect(() => {
    const loadCategories = async () => {
      try {
        const categoriesData = await categoriesAPI.getAll();
        setCategories(categoriesData || []);
      } catch (error) {
        console.error('Error loading categories:', error);
      }
    };

    loadCategories();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-blue-900 to-blue-800 text-white py-2 px-4 text-center text-sm">
        <span>شحن مجاني للطلبات أكثر من 200 ريال 🚚</span>
      </div>

      {/* Main Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2"
            >
              {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>

          {/* Logo */}
          <div className="flex-shrink-0">
            <Link to="/" className="flex items-center space-x-2 space-x-reverse">
              <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold text-xl px-3 py-2 rounded-lg shadow-lg">
                بازاري
              </div>
            </Link>
          </div>

          {/* Search Bar - Desktop */}
          <div className="hidden md:flex flex-1 max-w-lg mx-8">
            <form onSubmit={handleSearch} className="w-full relative">
              <div className="relative">
                <Input
                  type="text"
                  placeholder="ابحث عن المنتجات..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-2 text-right border-2 border-gray-200 rounded-full focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
                />
                <Button
                  type="submit"
                  variant="ghost"
                  size="sm"
                  className="absolute left-2 top-1/2 transform -translate-y-1/2 p-2 text-gray-500 hover:text-blue-600"
                >
                  <Search className="h-5 w-5" />
                </Button>
              </div>
            </form>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-4 space-x-reverse">
            {/* User Account */}
            <Link to="/login">
              <Button variant="ghost" size="sm" className="hidden sm:flex items-center space-x-2 space-x-reverse text-gray-700 hover:text-blue-600">
                <User className="h-5 w-5" />
                <span className="hidden lg:block">حسابي</span>
              </Button>
            </Link>

            {/* Wishlist */}
            <Link to="/wishlist">
              <Button variant="ghost" size="sm" className="relative p-2 text-gray-700 hover:text-red-500">
                <Heart className="h-5 w-5" />
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                  2
                </span>
              </Button>
            </Link>

            {/* Shopping Cart */}
            <Link to="/cart">
              <Button variant="ghost" size="sm" className="relative p-2 text-gray-700 hover:text-blue-600">
                <ShoppingCart className="h-5 w-5" />
                {cartItems > 0 && (
                  <span className="absolute -top-1 -right-1 bg-blue-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                    {cartItems}
                  </span>
                )}
              </Button>
            </Link>
          </div>
        </div>

        {/* Mobile Search */}
        <div className="md:hidden pb-3">
          <form onSubmit={handleSearch} className="w-full relative">
            <Input
              type="text"
              placeholder="ابحث عن المنتجات..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-2 text-right border-2 border-gray-200 rounded-full focus:border-blue-500"
            />
            <Button
              type="submit"
              variant="ghost"
              size="sm"
              className="absolute left-2 top-1/2 transform -translate-y-1/2 p-2 text-gray-500"
            >
              <Search className="h-5 w-5" />
            </Button>
          </form>
        </div>
      </div>

      {/* Navigation Menu - Desktop */}
      <nav className="hidden md:block bg-gray-50 border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center space-x-8 space-x-reverse py-3">
            <Link
              to="/categories"
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-200"
            >
              جميع الأقسام
            </Link>
            {categories.slice(0, 5).map((category) => (
              <Link
                key={category.id}
                to={`/categories/${category.id}`}
                className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-200 whitespace-nowrap"
              >
                {category.name}
              </Link>
            ))}
            <Link
              to="/sellers"
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors duration-200"
            >
              المتاجر
            </Link>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-200 shadow-lg">
          <div className="px-4 py-3 space-y-3">
            <Link
              to="/categories"
              className="block text-gray-700 hover:text-blue-600 font-medium py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              جميع الأقسام
            </Link>
            {mockCategories.map((category) => (
              <Link
                key={category.id}
                to={`/categories/${category.id}`}
                className="block text-gray-700 hover:text-blue-600 font-medium py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {category.name}
              </Link>
            ))}
            <Link
              to="/sellers"
              className="block text-gray-700 hover:text-blue-600 font-medium py-2"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              المتاجر
            </Link>
            <div className="border-t border-gray-200 pt-3 mt-3">
              <Link
                to="/login"
                className="block text-gray-700 hover:text-blue-600 font-medium py-2"
                onClick={() => setIsMobileMenuOpen(false)}
              >
                تسجيل الدخول
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;