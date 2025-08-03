from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, date
from models_accounting import (
    ChartOfAccount, ChartOfAccountCreate,
    Customer, CustomerCreate,
    Supplier, SupplierCreate,
    Product, ProductCreate,
    JournalEntry, JournalEntryCreate, JournalEntryDetail,
    SalesInvoice, SalesInvoiceCreate, SalesInvoiceDetail,
    PurchaseInvoice, PurchaseInvoiceCreate, PurchaseInvoiceDetail,
    PaymentVoucher, PaymentVoucherCreate,
    ReceiptVoucher, ReceiptVoucherCreate,
    TrialBalance, BalanceSheet, IncomeStatement,
    JournalEntryStatus
)
from models_admin import AdminUser  # للمصادقة
from database import get_paginated_results
from routes.admin import verify_admin_token
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Database connection
client = AsyncIOMotorClient(os.environ.get('MONGO_URL', 'mongodb://localhost:27017'))
db = client[os.environ.get('DB_NAME', 'souq_express_db')]

# Collections
chart_of_accounts_collection = db.chart_of_accounts
customers_collection = db.customers
suppliers_collection = db.suppliers
products_collection = db.accounting_products  # منفصل عن منتجات المتجر
journal_entries_collection = db.journal_entries
journal_entry_details_collection = db.journal_entry_details
sales_invoices_collection = db.sales_invoices
sales_invoice_details_collection = db.sales_invoice_details
purchase_invoices_collection = db.purchase_invoices
purchase_invoice_details_collection = db.purchase_invoice_details
payment_vouchers_collection = db.payment_vouchers
receipt_vouchers_collection = db.receipt_vouchers

router = APIRouter(prefix="/accounting", tags=["accounting"])

def convert_objectid(data):
    """Convert MongoDB ObjectId to string recursively"""
    if isinstance(data, dict):
        if "_id" in data:
            data.pop("_id", None)
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid(item) for item in data]
    else:
        return data

# Chart of Accounts Routes
@router.get("/chart-of-accounts", response_model=List[ChartOfAccount])
async def get_chart_of_accounts(current_admin = Depends(verify_admin_token)):
    """Get all chart of accounts"""
    accounts = await chart_of_accounts_collection.find({"is_active": True}).sort("account_code", 1).to_list(1000)
    cleaned_accounts = convert_objectid(accounts)
    return [ChartOfAccount(**account) for account in cleaned_accounts]

@router.post("/chart-of-accounts", response_model=ChartOfAccount)
async def create_chart_of_account(account: ChartOfAccountCreate, current_admin = Depends(verify_admin_token)):
    """Create new chart of account"""
    
    # Check if account code already exists
    existing = await chart_of_accounts_collection.find_one({"account_code": account.account_code})
    if existing:
        raise HTTPException(status_code=400, detail="رقم الحساب موجود مسبقاً")
    
    account_dict = account.dict()
    account_dict["created_by"] = current_admin["username"]
    account_dict["current_balance"] = account.opening_balance
    
    account_obj = ChartOfAccount(**account_dict)
    await chart_of_accounts_collection.insert_one(account_obj.dict())
    
    return account_obj

@router.get("/chart-of-accounts/{account_id}", response_model=ChartOfAccount)
async def get_chart_of_account(account_id: str, current_admin = Depends(verify_admin_token)):
    """Get specific chart of account"""
    account = await chart_of_accounts_collection.find_one({"id": account_id})
    if not account:
        raise HTTPException(status_code=404, detail="الحساب غير موجود")
    
    cleaned_account = convert_objectid(account)
    return ChartOfAccount(**cleaned_account)

# Customer Routes
@router.get("/customers")
async def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_admin = Depends(verify_admin_token)
):
    """Get all customers"""
    result = await get_paginated_results(customers_collection, {"is_active": True}, page, limit, "customer_name", 1)
    result["items"] = convert_objectid(result["items"])
    return result

@router.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate, current_admin = Depends(verify_admin_token)):
    """Create new customer"""
    
    # Check if customer code already exists
    existing = await customers_collection.find_one({"customer_code": customer.customer_code})
    if existing:
        raise HTTPException(status_code=400, detail="كود العميل موجود مسبقاً")
    
    customer_dict = customer.dict()
    customer_obj = Customer(**customer_dict)
    await customers_collection.insert_one(customer_obj.dict())
    
    return customer_obj

@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str, current_admin = Depends(verify_admin_token)):
    """Get specific customer"""
    customer = await customers_collection.find_one({"id": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    
    cleaned_customer = convert_objectid(customer)
    return Customer(**cleaned_customer)

# Supplier Routes
@router.get("/suppliers")
async def get_suppliers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_admin = Depends(verify_admin_token)
):
    """Get all suppliers"""
    result = await get_paginated_results(suppliers_collection, {"is_active": True}, page, limit, "supplier_name", 1)
    result["items"] = convert_objectid(result["items"])
    return result

@router.post("/suppliers", response_model=Supplier)
async def create_supplier(supplier: SupplierCreate, current_admin = Depends(verify_admin_token)):
    """Create new supplier"""
    
    # Check if supplier code already exists
    existing = await suppliers_collection.find_one({"supplier_code": supplier.supplier_code})
    if existing:
        raise HTTPException(status_code=400, detail="كود المورد موجود مسبقاً")
    
    supplier_dict = supplier.dict()
    supplier_obj = Supplier(**supplier_dict)
    await suppliers_collection.insert_one(supplier_obj.dict())
    
    return supplier_obj

# Product Routes (for accounting)
@router.get("/products")
async def get_accounting_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_admin = Depends(verify_admin_token)
):
    """Get all accounting products"""
    result = await get_paginated_results(products_collection, {"is_active": True}, page, limit, "product_name", 1)
    result["items"] = convert_objectid(result["items"])
    return result

@router.post("/products", response_model=Product)
async def create_accounting_product(product: ProductCreate, current_admin = Depends(verify_admin_token)):
    """Create new accounting product"""
    
    # Check if product code already exists
    existing = await products_collection.find_one({"product_code": product.product_code})
    if existing:
        raise HTTPException(status_code=400, detail="كود المنتج موجود مسبقاً")
    
    product_dict = product.dict()
    product_obj = Product(**product_dict)
    await products_collection.insert_one(product_obj.dict())
    
    return product_obj

# Journal Entry Routes
@router.get("/journal-entries")
async def get_journal_entries(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_admin = Depends(verify_admin_token)
):
    """Get all journal entries"""
    filter_dict = {}
    if status:
        filter_dict["status"] = status
    
    result = await get_paginated_results(journal_entries_collection, filter_dict, page, limit, "entry_date", -1)
    result["items"] = convert_objectid(result["items"])
    return result

@router.post("/journal-entries", response_model=JournalEntry)
async def create_journal_entry(entry: JournalEntryCreate, current_admin = Depends(verify_admin_token)):
    """Create new journal entry"""
    
    # Generate entry number
    count = await journal_entries_collection.count_documents({}) + 1
    entry_number = f"JE-{count:06d}"
    
    # Calculate totals
    total_debit = sum(detail.get("debit_amount", 0) for detail in entry.details)
    total_credit = sum(detail.get("credit_amount", 0) for detail in entry.details)
    
    # Validate balanced entry
    if abs(total_debit - total_credit) > 0.01:  # Allow small rounding differences
        raise HTTPException(status_code=400, detail="القيد غير متوازن - إجمالي المدين يجب أن يساوي إجمالي الدائن")
    
    # Create journal entry
    entry_dict = entry.dict()
    entry_dict["entry_number"] = entry_number
    entry_dict["total_debit"] = total_debit
    entry_dict["total_credit"] = total_credit
    entry_dict["created_by"] = current_admin["username"]
    
    entry_obj = JournalEntry(**entry_dict)
    await journal_entries_collection.insert_one(entry_obj.dict())
    
    # Create journal entry details
    for i, detail in enumerate(entry.details, 1):
        detail_dict = detail.copy()
        detail_dict["journal_entry_id"] = entry_obj.id
        detail_dict["line_number"] = i
        
        # Get account name
        account = await chart_of_accounts_collection.find_one({"id": detail["account_id"]})
        if account:
            detail_dict["account_name"] = account["account_name"]
        
        detail_obj = JournalEntryDetail(**detail_dict)
        await journal_entry_details_collection.insert_one(detail_obj.dict())
    
    return entry_obj

@router.get("/journal-entries/{entry_id}")
async def get_journal_entry_with_details(entry_id: str, current_admin = Depends(verify_admin_token)):
    """Get journal entry with details"""
    
    # Get journal entry
    entry = await journal_entries_collection.find_one({"id": entry_id})
    if not entry:
        raise HTTPException(status_code=404, detail="القيد غير موجود")
    
    # Get details
    details = await journal_entry_details_collection.find({"journal_entry_id": entry_id}).sort("line_number", 1).to_list(100)
    
    cleaned_entry = convert_objectid(entry)
    cleaned_details = convert_objectid(details)
    
    return {
        "entry": JournalEntry(**cleaned_entry),
        "details": [JournalEntryDetail(**detail) for detail in cleaned_details]
    }

@router.put("/journal-entries/{entry_id}/post")
async def post_journal_entry(entry_id: str, current_admin = Depends(verify_admin_token)):
    """Post journal entry and update account balances"""
    
    # Get journal entry
    entry = await journal_entries_collection.find_one({"id": entry_id})
    if not entry:
        raise HTTPException(status_code=404, detail="القيد غير موجود")
    
    if entry["status"] == JournalEntryStatus.POSTED:
        raise HTTPException(status_code=400, detail="القيد مرحل مسبقاً")
    
    # Get entry details
    details = await journal_entry_details_collection.find({"journal_entry_id": entry_id}).to_list(100)
    
    # Update account balances
    for detail in details:
        account_id = detail["account_id"]
        debit_amount = detail["debit_amount"]
        credit_amount = detail["credit_amount"]
        
        # Get account
        account = await chart_of_accounts_collection.find_one({"id": account_id})
        if account:
            account_type = account["account_type"]
            current_balance = account["current_balance"]
            
            # Update balance based on account type and normal balance
            if account_type in ["asset", "expense"]:
                # Debit increases, credit decreases
                new_balance = current_balance + debit_amount - credit_amount
            else:  # liability, equity, revenue
                # Credit increases, debit decreases
                new_balance = current_balance + credit_amount - debit_amount
            
            await chart_of_accounts_collection.update_one(
                {"id": account_id},
                {"$set": {"current_balance": new_balance}}
            )
    
    # Mark entry as posted
    await journal_entries_collection.update_one(
        {"id": entry_id},
        {
            "$set": {
                "status": JournalEntryStatus.POSTED,
                "posted_at": datetime.utcnow(),
                "posted_by": current_admin["username"]
            }
        }
    )
    
    return {"message": "تم ترحيل القيد بنجاح"}

# Sales Invoice Routes
@router.get("/sales-invoices")
async def get_sales_invoices(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_admin = Depends(verify_admin_token)
):
    """Get all sales invoices"""
    result = await get_paginated_results(sales_invoices_collection, {}, page, limit, "invoice_date", -1)
    result["items"] = convert_objectid(result["items"])
    return result

@router.post("/sales-invoices", response_model=SalesInvoice)
async def create_sales_invoice(invoice: SalesInvoiceCreate, current_admin = Depends(verify_admin_token)):
    """Create new sales invoice"""
    
    # Generate invoice number
    count = await sales_invoices_collection.count_documents({}) + 1
    invoice_number = f"SI-{count:06d}"
    
    # Get customer info
    customer = await customers_collection.find_one({"id": invoice.customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    
    # Calculate totals
    subtotal = sum(detail.get("line_total", 0) for detail in invoice.details)
    total_amount = subtotal - invoice.discount_amount + invoice.tax_amount
    remaining_amount = total_amount - invoice.paid_amount if hasattr(invoice, 'paid_amount') else total_amount
    
    # Create sales invoice
    invoice_dict = invoice.dict()
    invoice_dict["invoice_number"] = invoice_number
    invoice_dict["customer_name"] = customer["customer_name"]
    invoice_dict["subtotal"] = subtotal
    invoice_dict["total_amount"] = total_amount
    invoice_dict["remaining_amount"] = remaining_amount
    invoice_dict["created_by"] = current_admin["username"]
    
    invoice_obj = SalesInvoice(**invoice_dict)
    await sales_invoices_collection.insert_one(invoice_obj.dict())
    
    # Create invoice details
    for detail in invoice.details:
        detail_dict = detail.copy()
        detail_dict["invoice_id"] = invoice_obj.id
        
        # Get product name
        product = await products_collection.find_one({"id": detail["product_id"]})
        if product:
            detail_dict["product_name"] = product["product_name"]
        
        detail_obj = SalesInvoiceDetail(**detail_dict)
        await sales_invoice_details_collection.insert_one(detail_obj.dict())
    
    return invoice_obj

# Reports Routes
@router.get("/reports/trial-balance")
async def get_trial_balance(
    from_date: date = Query(...),
    to_date: date = Query(...),
    current_admin = Depends(verify_admin_token)
):
    """Get trial balance report"""
    
    accounts = await chart_of_accounts_collection.find({"is_active": True}).sort("account_code", 1).to_list(1000)
    trial_balance_items = []
    
    total_debits = 0.0
    total_credits = 0.0
    
    for account in accounts:
        account_id = account["id"]
        
        # Get total debits and credits for the period
        pipeline = [
            {
                "$lookup": {
                    "from": "journal_entries",
                    "localField": "journal_entry_id",
                    "foreignField": "id",
                    "as": "journal_entry"
                }
            },
            {"$unwind": "$journal_entry"},
            {
                "$match": {
                    "account_id": account_id,
                    "journal_entry.status": "posted",
                    "journal_entry.entry_date": {
                        "$gte": from_date,
                        "$lte": to_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_debit": {"$sum": "$debit_amount"},
                    "total_credit": {"$sum": "$credit_amount"}
                }
            }
        ]
        
        result = await journal_entry_details_collection.aggregate(pipeline).to_list(1)
        
        if result:
            account_debit = result[0]["total_debit"]
            account_credit = result[0]["total_credit"]
        else:
            account_debit = 0.0
            account_credit = 0.0
        
        # Calculate closing balance
        opening_balance = account.get("opening_balance", 0.0)
        if account["account_type"] in ["asset", "expense"]:
            closing_balance = opening_balance + account_debit - account_credit
        else:
            closing_balance = opening_balance + account_credit - account_debit
        
        trial_balance_items.append({
            "account_code": account["account_code"],
            "account_name": account["account_name"],
            "opening_balance": opening_balance,
            "total_debit": account_debit,
            "total_credit": account_credit,
            "closing_balance": closing_balance
        })
        
        total_debits += account_debit
        total_credits += account_credit
    
    return {
        "from_date": from_date,
        "to_date": to_date,
        "items": trial_balance_items,
        "total_debits": total_debits,
        "total_credits": total_credits
    }

@router.get("/reports/income-statement")
async def get_income_statement(
    from_date: date = Query(...),
    to_date: date = Query(...),
    current_admin = Depends(verify_admin_token)
):
    """Get income statement (profit & loss) report"""
    
    # Get revenue accounts
    revenue_accounts = await chart_of_accounts_collection.find({
        "account_type": "revenue",
        "is_active": True
    }).to_list(1000)
    
    # Get expense accounts
    expense_accounts = await chart_of_accounts_collection.find({
        "account_type": "expense", 
        "is_active": True
    }).to_list(1000)
    
    revenues = []
    expenses = []
    total_revenues = 0.0
    total_expenses = 0.0
    
    # Calculate revenues
    for account in revenue_accounts:
        # Get net amount for the period (credits - debits for revenue)
        pipeline = [
            {
                "$lookup": {
                    "from": "journal_entries",
                    "localField": "journal_entry_id", 
                    "foreignField": "id",
                    "as": "journal_entry"
                }
            },
            {"$unwind": "$journal_entry"},
            {
                "$match": {
                    "account_id": account["id"],
                    "journal_entry.status": "posted",
                    "journal_entry.entry_date": {
                        "$gte": from_date,
                        "$lte": to_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_credit": {"$sum": "$credit_amount"},
                    "total_debit": {"$sum": "$debit_amount"}
                }
            }
        ]
        
        result = await journal_entry_details_collection.aggregate(pipeline).to_list(1)
        net_amount = result[0]["total_credit"] - result[0]["total_debit"] if result else 0.0
        
        if net_amount != 0:
            revenues.append({
                "account_name": account["account_name"],
                "amount": net_amount
            })
            total_revenues += net_amount
    
    # Calculate expenses
    for account in expense_accounts:
        # Get net amount for the period (debits - credits for expenses)
        pipeline = [
            {
                "$lookup": {
                    "from": "journal_entries",
                    "localField": "journal_entry_id",
                    "foreignField": "id", 
                    "as": "journal_entry"
                }
            },
            {"$unwind": "$journal_entry"},
            {
                "$match": {
                    "account_id": account["id"],
                    "journal_entry.status": "posted",
                    "journal_entry.entry_date": {
                        "$gte": from_date,
                        "$lte": to_date
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_debit": {"$sum": "$debit_amount"},
                    "total_credit": {"$sum": "$credit_amount"}
                }
            }
        ]
        
        result = await journal_entry_details_collection.aggregate(pipeline).to_list(1)
        net_amount = result[0]["total_debit"] - result[0]["total_credit"] if result else 0.0
        
        if net_amount != 0:
            expenses.append({
                "account_name": account["account_name"],
                "amount": net_amount
            })
            total_expenses += net_amount
    
    net_income = total_revenues - total_expenses
    
    return {
        "from_date": from_date,
        "to_date": to_date,
        "revenues": revenues,
        "expenses": expenses,
        "total_revenues": total_revenues,
        "total_expenses": total_expenses,
        "net_income": net_income
    }