from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Import existing db instance
from models import db

class Partner(db.Model):
    __tablename__ = 'partners'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    partner_type = db.Column(db.String(50), nullable=False)  # 'customer', 'vendor', 'both'
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    tax_id = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sales_orders = db.relationship('SalesOrder', back_populates='customer')
    customer_invoices = db.relationship('CustomerInvoice', back_populates='customer')
    purchase_orders = db.relationship('PurchaseOrder', back_populates='vendor')
    vendor_bills = db.relationship('VendorBill', back_populates='vendor')


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    product_code = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    product_type = db.Column(db.String(50), default='service')  # 'service', 'product', 'consumable'
    sale_price = db.Column(db.Float, default=0.0)
    cost_price = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sales_order_lines = db.relationship('SalesOrderLine', back_populates='product')
    purchase_order_lines = db.relationship('PurchaseOrderLine', back_populates='product')
    customer_invoice_lines = db.relationship('CustomerInvoiceLine', back_populates='product')
    vendor_bill_lines = db.relationship('VendorBillLine', back_populates='product')


# ==================== SALES MODELS ====================

class SalesOrder(db.Model):
    __tablename__ = 'sales_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    so_number = db.Column(db.String(50), unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='RESTRICT'))
    customer_id = db.Column(db.Integer, db.ForeignKey('partners.id', ondelete='RESTRICT'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='draft')  # draft, confirmed, done, cancelled
    currency = db.Column(db.String(10), default='USD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    from models import Project
    project = db.relationship('Project', backref='sales_orders')
    customer = db.relationship('Partner', back_populates='sales_orders')
    lines = db.relationship('SalesOrderLine', back_populates='sales_order', cascade='all, delete-orphan')


class SalesOrderLine(db.Model):
    __tablename__ = 'sales_order_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'))
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    line_total = db.Column(db.Float, default=0.0)
    milestone_flag = db.Column(db.Boolean, default=False)
    
    # Relationships
    sales_order = db.relationship('SalesOrder', back_populates='lines')
    product = db.relationship('Product', back_populates='sales_order_lines')


class CustomerInvoice(db.Model):
    __tablename__ = 'customer_invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='RESTRICT'))
    customer_id = db.Column(db.Integer, db.ForeignKey('partners.id', ondelete='RESTRICT'), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='draft')  # draft, posted, paid, cancelled
    currency = db.Column(db.String(10), default='USD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    from models import Project
    project = db.relationship('Project', backref='customer_invoices')
    customer = db.relationship('Partner', back_populates='customer_invoices')
    lines = db.relationship('CustomerInvoiceLine', back_populates='customer_invoice', cascade='all, delete-orphan')


class CustomerInvoiceLine(db.Model):
    __tablename__ = 'customer_invoice_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_invoice_id = db.Column(db.Integer, db.ForeignKey('customer_invoices.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'))
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    line_total = db.Column(db.Float, default=0.0)
    
    # Relationships
    customer_invoice = db.relationship('CustomerInvoice', back_populates='lines')
    product = db.relationship('Product', back_populates='customer_invoice_lines')


# ==================== PURCHASE MODELS ====================

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(50), unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='RESTRICT'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('partners.id', ondelete='RESTRICT'), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='draft')  # draft, confirmed, done, cancelled
    currency = db.Column(db.String(10), default='USD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    from models import Project
    project = db.relationship('Project', backref='purchase_orders')
    vendor = db.relationship('Partner', back_populates='purchase_orders')
    lines = db.relationship('PurchaseOrderLine', back_populates='purchase_order', cascade='all, delete-orphan')


class PurchaseOrderLine(db.Model):
    __tablename__ = 'purchase_order_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'))
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    unit_cost = db.Column(db.Float, nullable=False, default=0.0)
    line_total = db.Column(db.Float, default=0.0)
    
    # Relationships
    purchase_order = db.relationship('PurchaseOrder', back_populates='lines')
    product = db.relationship('Product', back_populates='purchase_order_lines')


class VendorBill(db.Model):
    __tablename__ = 'vendor_bills'
    
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='RESTRICT'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('partners.id', ondelete='RESTRICT'), nullable=False)
    bill_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='draft')  # draft, posted, paid, cancelled
    currency = db.Column(db.String(10), default='USD')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    from models import Project
    project = db.relationship('Project', backref='vendor_bills')
    vendor = db.relationship('Partner', back_populates='vendor_bills')
    lines = db.relationship('VendorBillLine', back_populates='vendor_bill', cascade='all, delete-orphan')


class VendorBillLine(db.Model):
    __tablename__ = 'vendor_bill_lines'
    
    id = db.Column(db.Integer, primary_key=True)
    vendor_bill_id = db.Column(db.Integer, db.ForeignKey('vendor_bills.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='SET NULL'))
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)
    unit_cost = db.Column(db.Float, nullable=False, default=0.0)
    line_total = db.Column(db.Float, default=0.0)
    
    # Relationships
    vendor_bill = db.relationship('VendorBill', back_populates='lines')
    product = db.relationship('Product', back_populates='vendor_bill_lines')
