from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid
from enum import Enum

# Enums for accounting system
class AccountType(str, Enum):
    ASSET = "asset"              # أصول
    LIABILITY = "liability"       # التزامات
    EQUITY = "equity"            # حقوق الملكية
    REVENUE = "revenue"          # إيرادات
    EXPENSE = "expense"          # مصروفات

class TransactionType(str, Enum):
    DEBIT = "debit"              # مدين
    CREDIT = "credit"            # دائن

class PaymentMethod(str, Enum):
    CASH = "cash"                # نقدي
    BANK_TRANSFER = "bank_transfer"  # تحويل بنكي
    CHECK = "check"              # شيك
    CREDIT_CARD = "credit_card"  # بطاقة ائتمان

class JournalEntryStatus(str, Enum):
    DRAFT = "draft"              # مسودة
    POSTED = "posted"            # مرحل
    CANCELLED = "cancelled"      # ملغي

# Chart of Accounts (دليل الحسابات)
class ChartOfAccount(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_code: str            # رقم الحساب
    account_name: str            # اسم الحساب
    account_name_en: Optional[str] = None
    account_type: AccountType    # نوع الحساب
    parent_account_id: Optional[str] = None  # الحساب الأب
    level: int = 1               # مستوى الحساب في الشجرة
    is_active: bool = True       # نشط/غير نشط
    opening_balance: float = 0.0  # الرصيد الافتتاحي
    current_balance: float = 0.0  # الرصيد الحالي
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class ChartOfAccountCreate(BaseModel):
    account_code: str
    account_name: str
    account_name_en: Optional[str] = None
    account_type: AccountType
    parent_account_id: Optional[str] = None
    opening_balance: float = 0.0

# Journal Entry (قيود اليومية)
class JournalEntry(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    entry_number: str            # رقم القيد
    entry_date: date            # تاريخ القيد
    reference: Optional[str] = None  # المرجع
    description: str            # البيان
    total_debit: float = 0.0    # إجمالي المدين
    total_credit: float = 0.0   # إجمالي الدائن
    status: JournalEntryStatus = JournalEntryStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    posted_at: Optional[datetime] = None
    posted_by: Optional[str] = None

class JournalEntryDetail(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    journal_entry_id: str       # معرف قيد اليومية
    account_id: str             # معرف الحساب
    account_name: str           # اسم الحساب (للعرض)
    description: str            # البيان
    debit_amount: float = 0.0   # المبلغ المدين
    credit_amount: float = 0.0  # المبلغ الدائن
    line_number: int            # رقم السطر

class JournalEntryCreate(BaseModel):
    entry_date: date
    reference: Optional[str] = None
    description: str
    details: List[Dict[str, Any]]  # تفاصيل القيد

# Customer (العملاء)
class Customer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_code: str           # كود العميل
    customer_name: str          # اسم العميل
    customer_name_en: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None  # الرقم الضريبي
    credit_limit: float = 0.0   # حد الائتمان
    current_balance: float = 0.0  # الرصيد الحالي
    is_active: bool = True
    account_id: Optional[str] = None  # ربط بحساب العميل في دليل الحسابات
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CustomerCreate(BaseModel):
    customer_code: str
    customer_name: str
    customer_name_en: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None
    credit_limit: float = 0.0

# Supplier (الموردين)
class Supplier(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    supplier_code: str           # كود المورد
    supplier_name: str          # اسم المورد
    supplier_name_en: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None
    current_balance: float = 0.0  # الرصيد الحالي
    is_active: bool = True
    account_id: Optional[str] = None  # ربط بحساب المورد
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SupplierCreate(BaseModel):
    supplier_code: str
    supplier_name: str
    supplier_name_en: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    tax_number: Optional[str] = None

# Product/Item (المنتجات/الأصناف)
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    product_code: str            # كود المنتج
    product_name: str           # اسم المنتج
    product_name_en: Optional[str] = None
    category_id: Optional[str] = None  # فئة المنتج
    unit_of_measure: str = "قطعة"  # وحدة القياس
    cost_price: float = 0.0     # سعر التكلفة
    selling_price: float = 0.0  # سعر البيع
    current_stock: float = 0.0  # المخزون الحالي
    reorder_level: float = 0.0  # حد إعادة الطلب
    is_active: bool = True
    inventory_account_id: Optional[str] = None  # حساب المخزون
    sales_account_id: Optional[str] = None      # حساب المبيعات
    cost_account_id: Optional[str] = None       # حساب تكلفة البضاعة
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    product_code: str
    product_name: str
    product_name_en: Optional[str] = None
    category_id: Optional[str] = None
    unit_of_measure: str = "قطعة"
    cost_price: float = 0.0
    selling_price: float = 0.0
    reorder_level: float = 0.0

# Sales Invoice (فاتورة المبيعات)
class SalesInvoice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_number: str          # رقم الفاتورة
    invoice_date: date          # تاريخ الفاتورة
    customer_id: str            # معرف العميل
    customer_name: str          # اسم العميل (للعرض)
    subtotal: float = 0.0       # المجموع الفرعي
    discount_amount: float = 0.0  # مبلغ الخصم
    tax_amount: float = 0.0     # مبلغ الضريبة
    total_amount: float = 0.0   # المجموع الكلي
    paid_amount: float = 0.0    # المبلغ المدفوع
    remaining_amount: float = 0.0  # المبلغ المتبقي
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    is_posted: bool = False     # مرحل أم لا
    journal_entry_id: Optional[str] = None  # معرف القيد المحاسبي
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class SalesInvoiceDetail(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_id: str             # معرف الفاتورة
    product_id: str             # معرف المنتج
    product_name: str           # اسم المنتج (للعرض)
    quantity: float             # الكمية
    unit_price: float           # سعر الوحدة
    discount_percent: float = 0.0  # نسبة الخصم
    discount_amount: float = 0.0   # مبلغ الخصم
    line_total: float           # إجمالي السطر

class SalesInvoiceCreate(BaseModel):
    invoice_date: date
    customer_id: str
    subtotal: float = 0.0
    discount_amount: float = 0.0
    tax_amount: float = 0.0
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    details: List[Dict[str, Any]]

# Purchase Invoice (فاتورة المشتريات)
class PurchaseInvoice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_number: str
    invoice_date: date
    supplier_id: str
    supplier_name: str
    subtotal: float = 0.0
    discount_amount: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    paid_amount: float = 0.0
    remaining_amount: float = 0.0
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    is_posted: bool = False
    journal_entry_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class PurchaseInvoiceDetail(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_id: str
    product_id: str
    product_name: str
    quantity: float
    unit_price: float
    discount_percent: float = 0.0
    discount_amount: float = 0.0
    line_total: float

class PurchaseInvoiceCreate(BaseModel):
    invoice_date: date
    supplier_id: str
    subtotal: float = 0.0
    discount_amount: float = 0.0
    tax_amount: float = 0.0
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    details: List[Dict[str, Any]]

# Payment Voucher (سند دفع)
class PaymentVoucher(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    voucher_number: str
    voucher_date: date
    payee_name: str             # المدفوع إليه
    amount: float               # المبلغ
    payment_method: PaymentMethod
    bank_account_id: Optional[str] = None  # الحساب البنكي
    check_number: Optional[str] = None     # رقم الشيك
    reference: Optional[str] = None
    description: str
    is_posted: bool = False
    journal_entry_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class PaymentVoucherCreate(BaseModel):
    voucher_date: date
    payee_name: str
    amount: float
    payment_method: PaymentMethod
    bank_account_id: Optional[str] = None
    check_number: Optional[str] = None
    reference: Optional[str] = None
    description: str

# Receipt Voucher (سند قبض)
class ReceiptVoucher(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    voucher_number: str
    voucher_date: date
    payer_name: str             # المدفوع من
    amount: float
    payment_method: PaymentMethod
    bank_account_id: Optional[str] = None
    check_number: Optional[str] = None
    reference: Optional[str] = None
    description: str
    is_posted: bool = False
    journal_entry_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class ReceiptVoucherCreate(BaseModel):
    voucher_date: date
    payer_name: str
    amount: float
    payment_method: PaymentMethod
    bank_account_id: Optional[str] = None
    check_number: Optional[str] = None
    reference: Optional[str] = None
    description: str

# Trial Balance (ميزان المراجعة)
class TrialBalanceItem(BaseModel):
    account_code: str
    account_name: str
    opening_balance: float
    total_debit: float
    total_credit: float
    closing_balance: float

class TrialBalance(BaseModel):
    from_date: date
    to_date: date
    items: List[TrialBalanceItem]
    total_debits: float
    total_credits: float

# Financial Reports
class BalanceSheetItem(BaseModel):
    account_name: str
    amount: float

class BalanceSheet(BaseModel):
    as_of_date: date
    assets: List[BalanceSheetItem]
    liabilities: List[BalanceSheetItem]
    equity: List[BalanceSheetItem]
    total_assets: float
    total_liabilities: float
    total_equity: float

class IncomeStatementItem(BaseModel):
    account_name: str
    amount: float

class IncomeStatement(BaseModel):
    from_date: date
    to_date: date
    revenues: List[IncomeStatementItem]
    expenses: List[IncomeStatementItem]
    total_revenues: float
    total_expenses: float
    net_income: float