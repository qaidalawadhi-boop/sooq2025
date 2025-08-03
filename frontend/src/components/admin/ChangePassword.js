import React, { useState } from 'react';
import { Eye, EyeOff, Loader2, Lock, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { adminAuthAPI, adminApiUtils } from '../../services/adminApi';
import AdminLayout from './AdminLayout';

const ChangePassword = () => {
  const [formData, setFormData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setMessage({ type: '', text: '' }); // Clear message when user types
  };

  const togglePasswordVisibility = (field) => {
    setShowPasswords(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  const validateForm = () => {
    if (!formData.current_password) {
      setMessage({ type: 'error', text: 'يرجى إدخال كلمة المرور الحالية' });
      return false;
    }
    if (!formData.new_password) {
      setMessage({ type: 'error', text: 'يرجى إدخال كلمة المرور الجديدة' });
      return false;
    }
    if (formData.new_password.length < 6) {
      setMessage({ type: 'error', text: 'كلمة المرور الجديدة يجب أن تكون 6 أحرف على الأقل' });
      return false;
    }
    if (formData.new_password !== formData.confirm_password) {
      setMessage({ type: 'error', text: 'كلمة المرور الجديدة وتأكيدها غير متطابقان' });
      return false;
    }
    if (formData.current_password === formData.new_password) {
      setMessage({ type: 'error', text: 'كلمة المرور الجديدة يجب أن تكون مختلفة عن الحالية' });
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setMessage({ type: '', text: '' });

    try {
      await adminAuthAPI.changePassword(formData);
      
      setMessage({ 
        type: 'success', 
        text: 'تم تحديث كلمة المرور بنجاح! يرجى تسجيل الدخول مرة أخرى' 
      });
      
      // Clear form
      setFormData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
      
      // Logout user after successful password change
      setTimeout(() => {
        adminAuthAPI.clearAuth();
        window.location.href = '/admin/login';
      }, 2000);
      
    } catch (err) {
      const errorInfo = adminApiUtils.handleError(err);
      setMessage({ type: 'error', text: errorInfo.message });
    } finally {
      setLoading(false);
    }
  };

  const getPasswordStrength = (password) => {
    if (!password) return { strength: 0, text: '', color: '' };
    
    let strength = 0;
    let requirements = [];
    
    if (password.length >= 6) {
      strength += 25;
      requirements.push('✓ 6 أحرف على الأقل');
    } else {
      requirements.push('✗ 6 أحرف على الأقل');
    }
    
    if (/[A-Z]/.test(password)) {
      strength += 25;
      requirements.push('✓ حرف كبير');
    } else {
      requirements.push('✗ حرف كبير');
    }
    
    if (/[a-z]/.test(password)) {
      strength += 25;
      requirements.push('✓ حرف صغير');
    } else {
      requirements.push('✗ حرف صغير');
    }
    
    if (/[0-9]/.test(password)) {
      strength += 25;
      requirements.push('✓ رقم');
    } else {
      requirements.push('✗ رقم');
    }
    
    let strengthText = '';
    let color = '';
    
    if (strength < 50) {
      strengthText = 'ضعيفة';
      color = 'text-red-600';
    } else if (strength < 75) {
      strengthText = 'متوسطة';
      color = 'text-yellow-600';
    } else {
      strengthText = 'قوية';
      color = 'text-green-600';
    }
    
    return { strength, text: strengthText, color, requirements };
  };

  const passwordStrength = getPasswordStrength(formData.new_password);

  return (
    <AdminLayout>
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">تغيير كلمة المرور</h1>
          <p className="text-gray-600">قم بتحديث كلمة المرور الخاصة بك للحفاظ على أمان حسابك</p>
        </div>

        <Card className="shadow-lg">
          <CardHeader className="text-center pb-2">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mb-4">
              <Lock className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-xl font-bold text-gray-800">
              تحديث كلمة المرور
            </CardTitle>
          </CardHeader>
          
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {message.text && (
                <div className={`rounded-lg p-4 flex items-start space-x-3 space-x-reverse ${
                  message.type === 'success' 
                    ? 'bg-green-50 border border-green-200' 
                    : 'bg-red-50 border border-red-200'
                }`}>
                  {message.type === 'success' ? (
                    <CheckCircle className="h-5 w-5 text-green-600 mt-0.5" />
                  ) : (
                    <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                  )}
                  <p className={`text-sm ${
                    message.type === 'success' ? 'text-green-700' : 'text-red-700'
                  }`}>
                    {message.text}
                  </p>
                </div>
              )}
              
              <div className="space-y-4">
                {/* Current Password */}
                <div>
                  <label htmlFor="current_password" className="block text-sm font-medium text-gray-700 mb-2">
                    كلمة المرور الحالية *
                  </label>
                  <div className="relative">
                    <Input
                      id="current_password"
                      name="current_password"
                      type={showPasswords.current ? 'text' : 'password'}
                      required
                      value={formData.current_password}
                      onChange={handleInputChange}
                      className="text-right pr-10"
                      placeholder="أدخل كلمة المرور الحالية"
                      disabled={loading}
                    />
                    <button
                      type="button"
                      className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      onClick={() => togglePasswordVisibility('current')}
                      disabled={loading}
                    >
                      {showPasswords.current ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                </div>
                
                {/* New Password */}
                <div>
                  <label htmlFor="new_password" className="block text-sm font-medium text-gray-700 mb-2">
                    كلمة المرور الجديدة *
                  </label>
                  <div className="relative">
                    <Input
                      id="new_password"
                      name="new_password"
                      type={showPasswords.new ? 'text' : 'password'}
                      required
                      value={formData.new_password}
                      onChange={handleInputChange}
                      className="text-right pr-10"
                      placeholder="أدخل كلمة المرور الجديدة"
                      disabled={loading}
                    />
                    <button
                      type="button"
                      className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      onClick={() => togglePasswordVisibility('new')}
                      disabled={loading}
                    >
                      {showPasswords.new ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                  
                  {/* Password Strength Indicator */}
                  {formData.new_password && (
                    <div className="mt-2">
                      <div className="flex items-center justify-between text-xs mb-1">
                        <span className="text-gray-600">قوة كلمة المرور:</span>
                        <span className={passwordStrength.color}>
                          {passwordStrength.text}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full transition-all duration-300 ${
                            passwordStrength.strength < 50 ? 'bg-red-500' :
                            passwordStrength.strength < 75 ? 'bg-yellow-500' : 'bg-green-500'
                          }`}
                          style={{ width: `${passwordStrength.strength}%` }}
                        ></div>
                      </div>
                      <div className="mt-2 text-xs text-gray-600">
                        <p className="mb-1">متطلبات كلمة المرور:</p>
                        <ul className="space-y-1">
                          {passwordStrength.requirements.map((req, index) => (
                            <li key={index} className={req.startsWith('✓') ? 'text-green-600' : 'text-red-600'}>
                              {req}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
                
                {/* Confirm Password */}
                <div>
                  <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700 mb-2">
                    تأكيد كلمة المرور الجديدة *
                  </label>
                  <div className="relative">
                    <Input
                      id="confirm_password"
                      name="confirm_password"
                      type={showPasswords.confirm ? 'text' : 'password'}
                      required
                      value={formData.confirm_password}
                      onChange={handleInputChange}
                      className="text-right pr-10"
                      placeholder="أعد إدخال كلمة المرور الجديدة"
                      disabled={loading}
                    />
                    <button
                      type="button"
                      className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      onClick={() => togglePasswordVisibility('confirm')}
                      disabled={loading}
                    >
                      {showPasswords.confirm ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                  {formData.confirm_password && formData.new_password !== formData.confirm_password && (
                    <p className="text-red-600 text-xs mt-1">كلمتا المرور غير متطابقتان</p>
                  )}
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
                    <span>جارٍ تحديث كلمة المرور...</span>
                  </div>
                ) : (
                  'تحديث كلمة المرور'
                )}
              </Button>
            </form>
            
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="bg-blue-50 rounded-lg p-4">
                <h3 className="font-semibold text-blue-800 text-sm mb-2">نصائح لكلمة مرور قوية:</h3>
                <ul className="text-blue-600 text-xs space-y-1">
                  <li>• استخدم 6 أحرف على الأقل</li>
                  <li>• اجمع بين الأحرف الكبيرة والصغيرة</li>
                  <li>• أضف أرقاماً ورموزاً خاصة</li>
                  <li>• تجنب استخدام معلومات شخصية</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </AdminLayout>
  );
};

export default ChangePassword;