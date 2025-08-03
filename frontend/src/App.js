import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import HomePage from "./components/HomePage";
import AdminLogin from "./components/admin/AdminLogin";
import AdminDashboard from "./components/admin/AdminDashboard";
import ChangePassword from "./components/admin/ChangePassword";
import { Toaster } from "./components/ui/toaster";

// Admin routes wrapper
const AdminRoutes = () => (
  <Routes>
    <Route path="/login" element={<AdminLogin />} />
    <Route path="/dashboard" element={<AdminDashboard />} />
    <Route path="/change-password" element={<ChangePassword />} />
    <Route path="/" element={<AdminDashboard />} />
  </Routes>
);

// Public routes wrapper
const PublicRoutes = () => (
  <>
    <Header />
    <main>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/categories" element={<div className="p-8 text-center">صفحة الأقسام قيد التطوير</div>} />
        <Route path="/categories/:id" element={<div className="p-8 text-center">صفحة القسم قيد التطوير</div>} />
        <Route path="/products/:id" element={<div className="p-8 text-center">صفحة المنتج قيد التطوير</div>} />
        <Route path="/sellers" element={<div className="p-8 text-center">صفحة المتاجر قيد التطوير</div>} />
        <Route path="/cart" element={<div className="p-8 text-center">سلة التسوق قيد التطوير</div>} />
        <Route path="/wishlist" element={<div className="p-8 text-center">قائمة الرغبات قيد التطوير</div>} />
        <Route path="/login" element={<div className="p-8 text-center">تسجيل الدخول قيد التطوير</div>} />
        <Route path="/search" element={<div className="p-8 text-center">صفحة البحث قيد التطوير</div>} />
      </Routes>
    </main>
    <Footer />
  </>
);

function App() {
  return (
    <div className="App min-h-screen bg-gray-50" dir="rtl">
      <BrowserRouter>
        <Routes>
          {/* Admin Routes */}
          <Route path="/admin/*" element={<AdminRoutes />} />
          
          {/* Public Routes */}
          <Route path="/*" element={<PublicRoutes />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;