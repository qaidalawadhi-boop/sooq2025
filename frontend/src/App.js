import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import HomePage from "./components/HomePage";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App min-h-screen bg-gray-50" dir="rtl">
      <BrowserRouter>
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            {/* Add more routes as needed */}
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
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;