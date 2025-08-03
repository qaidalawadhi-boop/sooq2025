import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Package, 
  FolderOpen,
  Store,
  ShoppingCart,
  Users,
  Settings,
  Bell,
  LogOut,
  Menu,
  X,
  ChevronDown,
  Lock
} from 'lucide-react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { adminAuthAPI, adminNotificationsAPI } from '../../services/adminApi';

const AdminLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [adminInfo, setAdminInfo] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Get admin info from localStorage
    const { adminInfo: storedAdminInfo } = adminAuthAPI.getAuth();
    if (storedAdminInfo) {
      setAdminInfo(storedAdminInfo);
    }

    // Load notifications
    loadNotifications();
  }, []);

  const loadNotifications = async () => {
    try {
      const response = await adminNotificationsAPI.getAll({ unread_only: true });
      setNotifications(response.items || []);
      setUnreadCount(response.items?.filter(n => !n.is_read).length || 0);
    } catch (error) {
      console.error('Error loading notifications:', error);
    }
  };

  const handleLogout = () => {
    adminAuthAPI.clearAuth();
    navigate('/admin/login');
  };

  const menuItems = [
    {
      title: 'لوحة القيادة',
      icon: LayoutDashboard,
      path: '/admin/dashboard',
      exact: true
    },
    {
      title: 'الطلبات',
      icon: ShoppingCart,
      path: '/admin/orders',
      badge: '12'
    },
    {
      title: 'المنتجات',
      icon: Package,
      path: '/admin/products'
    },
    {
      title: 'الأقسام',
      icon: FolderOpen,
      path: '/admin/categories'
    },
    {
      title: 'البائعون',
      icon: Store,
      path: '/admin/sellers'
    },
    {
      title: 'العملاء',
      icon: Users,
      path: '/admin/customers'
    },
    {
      title: 'التقارير',
      icon: LayoutDashboard,
      path: '/admin/reports'
    },
    {
      title: 'تغيير كلمة المرور',
      icon: Lock,
      path: '/admin/change-password'
    },
    {
      title: 'الإعدادات',
      icon: Settings,
      path: '/admin/settings'
    }
  ];

  const isActiveLink = (path, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex" dir="rtl">
      {/* Sidebar */}
      <div className={`bg-white shadow-lg transition-all duration-300 ${sidebarOpen ? 'w-64' : 'w-20'}`}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-lg px-3 py-2 rounded-lg">
                ب
              </div>
              {sidebarOpen && (
                <div>
                  <h1 className="text-xl font-bold text-gray-800">لوحة التحكم</h1>
                  <p className="text-sm text-gray-500">منصة سوق إكسبرس</p>
                </div>
              )}
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = isActiveLink(item.path, item.exact);
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-3 space-x-reverse px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                    isActive
                      ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-600'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  {sidebarOpen && (
                    <>
                      <span className="flex-1">{item.title}</span>
                      {item.badge && (
                        <Badge variant="destructive" className="text-xs">
                          {item.badge}
                        </Badge>
                      )}
                    </>
                  )}
                </Link>
              );
            })}
          </nav>

          {/* Admin Info */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-bold">
                  {adminInfo?.full_name?.charAt(0) || 'أ'}
                </span>
              </div>
              {sidebarOpen && (
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {adminInfo?.full_name || 'المدير'}
                  </p>
                  <p className="text-xs text-gray-500 truncate">
                    {adminInfo?.role === 'super_admin' ? 'مدير رئيسي' : 'مدير'}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center space-x-4 space-x-reverse">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2"
              >
                <Menu className="h-5 w-5" />
              </Button>
              
              <div>
                <h2 className="text-xl font-semibold text-gray-800">
                  {menuItems.find(item => isActiveLink(item.path, item.exact))?.title || 'لوحة التحكم'}
                </h2>
              </div>
            </div>

            <div className="flex items-center space-x-4 space-x-reverse">
              {/* Notifications */}
              <div className="relative">
                <Button variant="ghost" size="sm" className="relative p-2">
                  <Bell className="h-5 w-5 text-gray-500" />
                  {unreadCount > 0 && (
                    <Badge className="absolute -top-1 -right-1 h-4 w-4 p-0 text-xs bg-red-500 text-white rounded-full flex items-center justify-center">
                      {unreadCount > 9 ? '9+' : unreadCount}
                    </Badge>
                  )}
                </Button>
              </div>

              {/* Logout */}
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                className="p-2 text-gray-500 hover:text-red-600"
              >
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
          <div className="container mx-auto px-6 py-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;