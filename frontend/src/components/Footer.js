import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Facebook, 
  Twitter, 
  Instagram, 
  Youtube, 
  Mail, 
  Phone, 
  MapPin,
  Smartphone,
  CreditCard,
  Truck,
  Shield
} from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      {/* Features Section */}
      <div className="bg-gray-800 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="bg-blue-600 p-3 rounded-lg">
                <Truck className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold">شحن مجاني</h3>
                <p className="text-sm text-gray-300">للطلبات أكثر من 200 ريال</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="bg-green-600 p-3 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold">ضمان الجودة</h3>
                <p className="text-sm text-gray-300">منتجات أصلية 100%</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="bg-purple-600 p-3 rounded-lg">
                <CreditCard className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold">دفع آمن</h3>
                <p className="text-sm text-gray-300">طرق دفع متعددة</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3 space-x-reverse">
              <div className="bg-orange-600 p-3 rounded-lg">
                <Phone className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold">دعم 24/7</h3>
                <p className="text-sm text-gray-300">خدمة العملاء</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Footer */}
      <div className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Company Info */}
            <div className="col-span-1 lg:col-span-1">
              <div className="flex items-center space-x-2 space-x-reverse mb-6">
                <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white font-bold text-xl px-3 py-2 rounded-lg">
                  سوق إكسبرس
                </div>
              </div>
              <p className="text-gray-300 mb-6 leading-relaxed">
                منصة سوق إكسبرس هي وجهتك الأولى للتسوق الإلكتروني في العالم العربي. نقدم مجموعة واسعة من المنتجات عالية الجودة بأفضل الأسعار.
              </p>
              <div className="flex space-x-4 space-x-reverse">
                <a href="#" className="bg-blue-600 hover:bg-blue-700 p-2 rounded-lg transition-colors">
                  <Facebook className="h-5 w-5" />
                </a>
                <a href="#" className="bg-blue-400 hover:bg-blue-500 p-2 rounded-lg transition-colors">
                  <Twitter className="h-5 w-5" />
                </a>
                <a href="#" className="bg-pink-600 hover:bg-pink-700 p-2 rounded-lg transition-colors">
                  <Instagram className="h-5 w-5" />
                </a>
                <a href="#" className="bg-red-600 hover:bg-red-700 p-2 rounded-lg transition-colors">
                  <Youtube className="h-5 w-5" />
                </a>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="text-lg font-semibold mb-6 text-white">روابط سريعة</h3>
              <ul className="space-y-3">
                <li><Link to="/about" className="text-gray-300 hover:text-white transition-colors">من نحن</Link></li>
                <li><Link to="/contact" className="text-gray-300 hover:text-white transition-colors">اتصل بنا</Link></li>
                <li><Link to="/careers" className="text-gray-300 hover:text-white transition-colors">الوظائف</Link></li>
                <li><Link to="/press" className="text-gray-300 hover:text-white transition-colors">الصحافة</Link></li>
                <li><Link to="/blog" className="text-gray-300 hover:text-white transition-colors">المدونة</Link></li>
              </ul>
            </div>

            {/* Customer Service */}
            <div>
              <h3 className="text-lg font-semibold mb-6 text-white">خدمة العملاء</h3>
              <ul className="space-y-3">
                <li><Link to="/help" className="text-gray-300 hover:text-white transition-colors">مركز المساعدة</Link></li>
                <li><Link to="/shipping" className="text-gray-300 hover:text-white transition-colors">الشحن والتوصيل</Link></li>
                <li><Link to="/returns" className="text-gray-300 hover:text-white transition-colors">سياسة الإرجاع</Link></li>
                <li><Link to="/warranty" className="text-gray-300 hover:text-white transition-colors">الضمان</Link></li>
                <li><Link to="/faq" className="text-gray-300 hover:text-white transition-colors">الأسئلة الشائعة</Link></li>
              </ul>
            </div>

            {/* Contact Info */}
            <div>
              <h3 className="text-lg font-semibold mb-6 text-white">معلومات الاتصال</h3>
              <div className="space-y-4">
                <div className="flex items-start space-x-3 space-x-reverse">
                  <MapPin className="h-5 w-5 text-gray-400 mt-1" />
                  <div>
                    <p className="text-gray-300">الرياض، المملكة العربية السعودية</p>
                    <p className="text-gray-300">طريق الملك فهد، الحي التجاري</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3 space-x-reverse">
                  <Phone className="h-5 w-5 text-gray-400" />
                  <p className="text-gray-300" dir="ltr">+966 11 234 5678</p>
                </div>
                
                <div className="flex items-center space-x-3 space-x-reverse">
                  <Mail className="h-5 w-5 text-gray-400" />
                  <p className="text-gray-300">info@souq-express.com</p>
                </div>
              </div>

              {/* Mobile App Download */}
              <div className="mt-6">
                <h4 className="text-white font-semibold mb-3">حمل التطبيق</h4>
                <div className="flex flex-col space-y-2">
                  <a href="#" className="bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 flex items-center space-x-3 space-x-reverse transition-colors">
                    <Smartphone className="h-6 w-6 text-gray-400" />
                    <div>
                      <p className="text-xs text-gray-400">حمل من</p>
                      <p className="text-sm font-semibold">App Store</p>
                    </div>
                  </a>
                  <a href="#" className="bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 flex items-center space-x-3 space-x-reverse transition-colors">
                    <Smartphone className="h-6 w-6 text-gray-400" />
                    <div>
                      <p className="text-xs text-gray-400">حمل من</p>
                      <p className="text-sm font-semibold">Google Play</p>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Footer */}
      <div className="bg-gray-950 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="text-gray-400 text-sm mb-4 md:mb-0">
              © 2024 سوق إكسبرس. جميع الحقوق محفوظة.
            </div>
            <div className="flex space-x-6 space-x-reverse text-sm">
              <Link to="/terms" className="text-gray-400 hover:text-white transition-colors">الشروط والأحكام</Link>
              <Link to="/privacy" className="text-gray-400 hover:text-white transition-colors">سياسة الخصوصية</Link>
              <Link to="/cookies" className="text-gray-400 hover:text-white transition-colors">ملفات تعريف الارتباط</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;