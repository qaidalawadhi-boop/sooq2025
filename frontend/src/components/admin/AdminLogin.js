import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Loader2, Shield } from 'lucide-react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { adminAuthAPI, adminApiUtils } from '../../services/adminApi';

const AdminLogin = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect if already logged in
    if (adminAuthAPI.isLoggedIn()) {
      navigate('/admin/dashboard');
    }
  }, [navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(''); // Clear error when user types
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await adminAuthAPI.login(formData);
      
      // Save authentication data
      adminAuthAPI.saveAuth(response.access_token, response.admin_info);
      
      toast({
        title: "تسجيل دخول ناجح",
        description: `مرحباً ${response.admin_info.full_name}`,
        variant: "default",
      });
      
      // Redirect to dashboard
      navigate('/admin/dashboard');
    } catch (err) {
      const errorInfo = adminApiUtils.handleError(err);
      setError(errorInfo.message);
      
      toast({
        title: "خطأ في تسجيل الدخول",
        description: errorInfo.message,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900 flex items-center justify-center p-4" dir="rtl">
      <div className="absolute inset-0 bg-black bg-opacity-30"></div>
      
      <Card className="w-full max-w-md relative z-10 shadow-2xl border-0">
        <CardHeader className="text-center pb-2">
          <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mb-4">
            <Shield className="w-8 h-8 text-white" />
          </div>
          <CardTitle className="text-2xl font-bold text-gray-800">
            لوحة التحكم الإدارية
          </CardTitle>
          <p className="text-gray-600 mt-2">تسجيل الدخول إلى منصة بازاري</p>
        </CardHeader>
        
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-red-600 text-sm text-center">{error}</p>
              </div>
            )}
            
            <div className="space-y-4">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                  اسم المستخدم
                </label>
                <Input
                  id="username"
                  name="username"
                  type="text"
                  required
                  value={formData.username}
                  onChange={handleInputChange}
                  className="text-right"
                  placeholder="أدخل اسم المستخدم"
                  disabled={loading}
                />
              </div>
              
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                  كلمة المرور
                </label>
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={formData.password}
                    onChange={handleInputChange}
                    className="text-right pr-10"
                    placeholder="أدخل كلمة المرور"
                    disabled={loading}
                  />
                  <button
                    type="button"
                    className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                    onClick={() => setShowPassword(!showPassword)}
                    disabled={loading}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>
            </div>
            
            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all duration-300 transform hover:scale-105"
              disabled={loading}
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2 space-x-reverse">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>جارٍ تسجيل الدخول...</span>
                </div>
              ) : (
                'تسجيل الدخول'
              )}
            </Button>
          </form>
          
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="font-semibold text-blue-800 text-sm mb-2">بيانات تجريبية:</h3>
              <div className="text-blue-600 text-xs space-y-1">
                <p><strong>المستخدم:</strong> admin</p>
                <p><strong>كلمة المرور:</strong> admin123</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminLogin;