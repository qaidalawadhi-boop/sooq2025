import React, { useState, useEffect } from 'react';
import { 
  DollarSign, 
  ShoppingCart, 
  Users, 
  Package,
  TrendingUp,
  TrendingDown,
  Clock,
  AlertTriangle,
  Eye
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { adminDashboardAPI, adminApiUtils } from '../../services/adminApi';
import AdminLayout from './AdminLayout';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [statsData, analyticsData] = await Promise.all([
        adminDashboardAPI.getStats(),
        adminDashboardAPI.getAnalytics()
      ]);
      
      setStats(statsData);
      setAnalytics(analyticsData);
    } catch (err) {
      const errorInfo = adminApiUtils.handleError(err);
      setError(errorInfo.message);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return `${amount.toLocaleString()} ر.س`;
  };

  const StatCard = ({ title, value, icon: Icon, change, changeType, color = "blue" }) => (
    <Card className="hover:shadow-lg transition-shadow duration-200">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
            {change && (
              <div className={`flex items-center mt-2 text-sm ${
                changeType === 'increase' ? 'text-green-600' : 'text-red-600'
              }`}>
                {changeType === 'increase' ? (
                  <TrendingUp className="h-4 w-4 ml-1" />
                ) : (
                  <TrendingDown className="h-4 w-4 ml-1" />
                )}
                <span>{change}</span>
              </div>
            )}
          </div>
          <div className={`p-3 rounded-full bg-${color}-100`}>
            <Icon className={`h-6 w-6 text-${color}-600`} />
          </div>
        </div>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">جارٍ تحميل البيانات...</p>
          </div>
        </div>
      </AdminLayout>
    );
  }

  if (error) {
    return (
      <AdminLayout>
        <div className="text-center py-12">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
            <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-red-800 mb-2">خطأ في تحميل البيانات</h3>
            <p className="text-red-600 mb-4">{error}</p>
            <Button onClick={loadDashboardData} variant="outline" className="text-red-600 border-red-300">
              إعادة المحاولة
            </Button>
          </div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="space-y-8">
        {/* Welcome Section */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">مرحباً في لوحة التحكم</h1>
          <p className="text-gray-600 mt-2">إليك نظرة عامة على أداء منصة سوق إكسبرس</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="إجمالي المبيعات"
            value={formatCurrency(stats?.total_revenue || 0)}
            icon={DollarSign}
            change="+12.5% من الأسبوع الماضي"
            changeType="increase"
            color="green"
          />
          <StatCard
            title="إجمالي الطلبات"
            value={stats?.total_orders || 0}
            icon={ShoppingCart}
            change="+8.2% من الأسبوع الماضي"
            changeType="increase"
            color="blue"
          />
          <StatCard
            title="العملاء"
            value={stats?.total_customers || 0}
            icon={Users}
            change="+15.3% من الأسبوع الماضي"
            changeType="increase"
            color="purple"
          />
          <StatCard
            title="المنتجات"
            value={stats?.total_products || 0}
            icon={Package}
            change="+3.1% من الأسبوع الماضي"
            changeType="increase"
            color="orange"
          />
        </div>

        {/* Today's Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-lg">
                <Clock className="h-5 w-5 ml-2 text-blue-600" />
                إحصائيات اليوم
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">طلبات اليوم</span>
                  <span className="font-bold text-blue-600">{stats?.orders_today || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">مبيعات اليوم</span>
                  <span className="font-bold text-green-600">
                    {formatCurrency(stats?.revenue_today || 0)}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-lg">
                <AlertTriangle className="h-5 w-5 ml-2 text-orange-600" />
                تنبيهات
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">طلبات معلقة</span>
                  <Badge variant="destructive">{stats?.pending_orders || 0}</Badge>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">مخزون منخفض</span>
                  <Badge variant="secondary">{stats?.low_stock_products || 0}</Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-lg">
                <TrendingUp className="h-5 w-5 ml-2 text-green-600" />
                النمو
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">معدل النمو الشهري</span>
                  <span className="font-bold text-green-600">+18.5%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">عملاء جدد</span>
                  <span className="font-bold text-blue-600">+24</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Orders */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>أحدث الطلبات</span>
              <Button variant="outline" size="sm">
                <Eye className="h-4 w-4 ml-2" />
                عرض الكل
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-right py-3 px-4 font-semibold text-gray-700">رقم الطلب</th>
                    <th className="text-right py-3 px-4 font-semibold text-gray-700">العميل</th>
                    <th className="text-right py-3 px-4 font-semibold text-gray-700">المبلغ</th>
                    <th className="text-right py-3 px-4 font-semibold text-gray-700">الحالة</th>
                    <th className="text-right py-3 px-4 font-semibold text-gray-700">التاريخ</th>
                  </tr>
                </thead>
                <tbody>
                  {analytics?.recent_orders?.slice(0, 5).map((order) => (
                    <tr key={order.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm">{order.order_number}</td>
                      <td className="py-3 px-4 text-sm">{order.customer_name}</td>
                      <td className="py-3 px-4 text-sm font-medium">
                        {formatCurrency(order.total)}
                      </td>
                      <td className="py-3 px-4 text-sm">
                        <Badge 
                          variant={order.status === 'confirmed' ? 'default' : 'secondary'}
                          className={order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : ''}
                        >
                          {order.status === 'pending' ? 'معلق' : 
                           order.status === 'confirmed' ? 'مؤكد' : 
                           order.status}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-500">
                        {new Date(order.created_at).toLocaleDateString('ar')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Top Products */}
        <Card>
          <CardHeader>
            <CardTitle>أفضل المنتجات مبيعاً</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {analytics?.top_products?.slice(0, 6).map((product) => (
                <div key={product.id} className="flex items-center space-x-3 space-x-reverse p-3 bg-gray-50 rounded-lg">
                  <img
                    src={product.image}
                    alt={product.title}
                    className="w-12 h-12 rounded-lg object-cover"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-sm text-gray-900 truncate">
                      {product.title}
                    </p>
                    <div className="flex items-center justify-between mt-1">
                      <span className="text-xs text-gray-500">
                        {product.sales_count} مبيعة
                      </span>
                      <span className="text-xs font-medium text-green-600">
                        {formatCurrency(product.revenue)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
};

export default AdminDashboard;