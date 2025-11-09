from flask import Blueprint, request, jsonify, session
from models import db, Project
from sales_purchase_models import (
    Partner, Product, SalesOrder, SalesOrderLine, CustomerInvoice, CustomerInvoiceLine,
    PurchaseOrder, PurchaseOrderLine, VendorBill, VendorBillLine
)
from datetime import datetime

sales_purchase_bp = Blueprint('sales_purchase', __name__)

# Helper function to check authentication
def require_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    return None


# ==================== PARTNER MANAGEMENT ====================

@sales_purchase_bp.route('/partners', methods=['POST'])
def create_partner():
    """Create a new partner (customer/vendor)"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('partner_type'):
        return jsonify({'error': 'Name and partner_type are required'}), 400
    
    if data['partner_type'] not in ['customer', 'vendor', 'both']:
        return jsonify({'error': 'partner_type must be customer, vendor, or both'}), 400
    
    try:
        partner = Partner(
            name=data['name'],
            partner_type=data['partner_type'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            tax_id=data.get('tax_id')
        )
        
        db.session.add(partner)
        db.session.commit()
        
        return jsonify({
            'message': 'Partner created successfully',
            'partner': {
                'id': partner.id,
                'name': partner.name,
                'partner_type': partner.partner_type,
                'email': partner.email
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/partners', methods=['GET'])
def get_partners():
    """Get all partners with optional filtering"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    partner_type = request.args.get('partner_type')
    
    query = Partner.query
    if partner_type:
        query = query.filter((Partner.partner_type == partner_type) | (Partner.partner_type == 'both'))
    
    partners = query.all()
    
    return jsonify({
        'partners': [{
            'id': p.id,
            'name': p.name,
            'partner_type': p.partner_type,
            'email': p.email,
            'phone': p.phone,
            'address': p.address,
            'tax_id': p.tax_id,
            'is_active': p.is_active
        } for p in partners]
    }), 200


@sales_purchase_bp.route('/partners/<int:partner_id>', methods=['GET'])
def get_partner(partner_id):
    """Get a specific partner"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    partner = Partner.query.get(partner_id)
    if not partner:
        return jsonify({'error': 'Partner not found'}), 404
    
    return jsonify({
        'partner': {
            'id': partner.id,
            'name': partner.name,
            'partner_type': partner.partner_type,
            'email': partner.email,
            'phone': partner.phone,
            'address': partner.address,
            'tax_id': partner.tax_id,
            'is_active': partner.is_active,
            'created_at': partner.created_at.isoformat()
        }
    }), 200


@sales_purchase_bp.route('/partners/<int:partner_id>', methods=['PUT'])
def update_partner(partner_id):
    """Update a partner"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    partner = Partner.query.get(partner_id)
    if not partner:
        return jsonify({'error': 'Partner not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'name' in data:
            partner.name = data['name']
        if 'partner_type' in data:
            if data['partner_type'] not in ['customer', 'vendor', 'both']:
                return jsonify({'error': 'Invalid partner_type'}), 400
            partner.partner_type = data['partner_type']
        if 'email' in data:
            partner.email = data['email']
        if 'phone' in data:
            partner.phone = data['phone']
        if 'address' in data:
            partner.address = data['address']
        if 'tax_id' in data:
            partner.tax_id = data['tax_id']
        if 'is_active' in data:
            partner.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Partner updated successfully',
            'partner': {
                'id': partner.id,
                'name': partner.name,
                'partner_type': partner.partner_type
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== PRODUCT MANAGEMENT ====================

@sales_purchase_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    try:
        product = Product(
            name=data['name'],
            product_code=data.get('product_code'),
            description=data.get('description'),
            product_type=data.get('product_type', 'service'),
            sale_price=data.get('sale_price', 0.0),
            cost_price=data.get('cost_price', 0.0)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'product_code': product.product_code,
                'sale_price': product.sale_price,
                'cost_price': product.cost_price
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    products = Product.query.all()
    
    return jsonify({
        'products': [{
            'id': p.id,
            'name': p.name,
            'product_code': p.product_code,
            'description': p.description,
            'product_type': p.product_type,
            'sale_price': p.sale_price,
            'cost_price': p.cost_price,
            'is_active': p.is_active
        } for p in products]
    }), 200


@sales_purchase_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'name' in data:
            product.name = data['name']
        if 'product_code' in data:
            product.product_code = data['product_code']
        if 'description' in data:
            product.description = data['description']
        if 'product_type' in data:
            product.product_type = data['product_type']
        if 'sale_price' in data:
            product.sale_price = data['sale_price']
        if 'cost_price' in data:
            product.cost_price = data['cost_price']
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'sale_price': product.sale_price
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== SALES ORDER MANAGEMENT ====================

@sales_purchase_bp.route('/sales-orders', methods=['POST'])
def create_sales_order():
    """Create a new sales order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    
    if not data or not data.get('so_number') or not data.get('customer_id') or not data.get('order_date'):
        return jsonify({'error': 'so_number, customer_id, and order_date are required'}), 400
    
    # Check if customer exists
    customer = Partner.query.get(data['customer_id'])
    if not customer or customer.partner_type not in ['customer', 'both']:
        return jsonify({'error': 'Valid customer not found'}), 404
    
    # Check if project exists (if provided)
    if data.get('project_id'):
        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({'error': 'Project not found'}), 404
    
    try:
        sales_order = SalesOrder(
            so_number=data['so_number'],
            customer_id=data['customer_id'],
            project_id=data.get('project_id'),
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d').date(),
            status=data.get('status', 'draft'),
            currency=data.get('currency', 'USD'),
            notes=data.get('notes')
        )
        
        db.session.add(sales_order)
        db.session.flush()
        
        # Add order lines if provided
        if data.get('lines'):
            for line_data in data['lines']:
                line_total = line_data.get('quantity', 1.0) * line_data.get('unit_price', 0.0)
                line = SalesOrderLine(
                    sales_order_id=sales_order.id,
                    product_id=line_data.get('product_id'),
                    description=line_data.get('description', ''),
                    quantity=line_data.get('quantity', 1.0),
                    unit_price=line_data.get('unit_price', 0.0),
                    line_total=line_total,
                    milestone_flag=line_data.get('milestone_flag', False)
                )
                db.session.add(line)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Sales order created successfully',
            'sales_order': {
                'id': sales_order.id,
                'so_number': sales_order.so_number,
                'customer_id': sales_order.customer_id,
                'order_date': sales_order.order_date.isoformat(),
                'status': sales_order.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/sales-orders', methods=['GET'])
def get_sales_orders():
    """Get all sales orders"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    sales_orders = SalesOrder.query.all()
    
    return jsonify({
        'sales_orders': [{
            'id': so.id,
            'so_number': so.so_number,
            'customer_id': so.customer_id,
            'customer_name': so.customer.name if so.customer else None,
            'project_id': so.project_id,
            'order_date': so.order_date.isoformat(),
            'status': so.status,
            'currency': so.currency,
            'lines_count': len(so.lines),
            'total_amount': sum(line.line_total for line in so.lines)
        } for so in sales_orders]
    }), 200


@sales_purchase_bp.route('/sales-orders/<int:so_id>', methods=['GET'])
def get_sales_order(so_id):
    """Get a specific sales order with lines"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    sales_order = SalesOrder.query.get(so_id)
    if not sales_order:
        return jsonify({'error': 'Sales order not found'}), 404
    
    lines = [{
        'id': line.id,
        'product_id': line.product_id,
        'product_name': line.product.name if line.product else None,
        'description': line.description,
        'quantity': line.quantity,
        'unit_price': line.unit_price,
        'line_total': line.line_total,
        'milestone_flag': line.milestone_flag
    } for line in sales_order.lines]
    
    return jsonify({
        'sales_order': {
            'id': sales_order.id,
            'so_number': sales_order.so_number,
            'customer_id': sales_order.customer_id,
            'customer_name': sales_order.customer.name if sales_order.customer else None,
            'project_id': sales_order.project_id,
            'order_date': sales_order.order_date.isoformat(),
            'status': sales_order.status,
            'currency': sales_order.currency,
            'notes': sales_order.notes,
            'created_at': sales_order.created_at.isoformat(),
            'lines': lines,
            'total_amount': sum(line.line_total for line in sales_order.lines)
        }
    }), 200


@sales_purchase_bp.route('/sales-orders/<int:so_id>', methods=['PUT'])
def update_sales_order(so_id):
    """Update a sales order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    sales_order = SalesOrder.query.get(so_id)
    if not sales_order:
        return jsonify({'error': 'Sales order not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'status' in data:
            if data['status'] not in ['draft', 'confirmed', 'done', 'cancelled']:
                return jsonify({'error': 'Invalid status'}), 400
            sales_order.status = data['status']
        if 'currency' in data:
            sales_order.currency = data['currency']
        if 'notes' in data:
            sales_order.notes = data['notes']
        if 'order_date' in data:
            sales_order.order_date = datetime.strptime(data['order_date'], '%Y-%m-%d').date()
        
        sales_order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Sales order updated successfully',
            'sales_order': {
                'id': sales_order.id,
                'so_number': sales_order.so_number,
                'status': sales_order.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/sales-orders/<int:so_id>', methods=['DELETE'])
def delete_sales_order(so_id):
    """Delete a sales order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    sales_order = SalesOrder.query.get(so_id)
    if not sales_order:
        return jsonify({'error': 'Sales order not found'}), 404
    
    try:
        db.session.delete(sales_order)
        db.session.commit()
        return jsonify({'message': 'Sales order deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== SALES ORDER LINES ====================

@sales_purchase_bp.route('/sales-orders/<int:so_id>/lines', methods=['POST'])
def add_sales_order_line(so_id):
    """Add a line to a sales order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    sales_order = SalesOrder.query.get(so_id)
    if not sales_order:
        return jsonify({'error': 'Sales order not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('description'):
        return jsonify({'error': 'Description is required'}), 400
    
    try:
        line_total = data.get('quantity', 1.0) * data.get('unit_price', 0.0)
        
        line = SalesOrderLine(
            sales_order_id=so_id,
            product_id=data.get('product_id'),
            description=data['description'],
            quantity=data.get('quantity', 1.0),
            unit_price=data.get('unit_price', 0.0),
            line_total=line_total,
            milestone_flag=data.get('milestone_flag', False)
        )
        
        db.session.add(line)
        db.session.commit()
        
        return jsonify({
            'message': 'Sales order line added successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_price': line.unit_price,
                'line_total': line.line_total
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/sales-orders/<int:so_id>/lines/<int:line_id>', methods=['PUT'])
def update_sales_order_line(so_id, line_id):
    """Update a sales order line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = SalesOrderLine.query.filter_by(id=line_id, sales_order_id=so_id).first()
    if not line:
        return jsonify({'error': 'Sales order line not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            line.description = data['description']
        if 'quantity' in data:
            line.quantity = data['quantity']
        if 'unit_price' in data:
            line.unit_price = data['unit_price']
        if 'milestone_flag' in data:
            line.milestone_flag = data['milestone_flag']
        if 'product_id' in data:
            line.product_id = data['product_id']
        
        # Recalculate line total
        line.line_total = line.quantity * line.unit_price
        
        db.session.commit()
        
        return jsonify({
            'message': 'Sales order line updated successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_price': line.unit_price,
                'line_total': line.line_total
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/sales-orders/<int:so_id>/lines/<int:line_id>', methods=['DELETE'])
def delete_sales_order_line(so_id, line_id):
    """Delete a sales order line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = SalesOrderLine.query.filter_by(id=line_id, sales_order_id=so_id).first()
    if not line:
        return jsonify({'error': 'Sales order line not found'}), 404
    
    try:
        db.session.delete(line)
        db.session.commit()
        return jsonify({'message': 'Sales order line deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== CUSTOMER INVOICE MANAGEMENT ====================

@sales_purchase_bp.route('/customer-invoices', methods=['POST'])
def create_customer_invoice():
    """Create a new customer invoice"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    
    if not data or not data.get('invoice_number') or not data.get('customer_id') or not data.get('invoice_date'):
        return jsonify({'error': 'invoice_number, customer_id, and invoice_date are required'}), 400
    
    # Check if customer exists
    customer = Partner.query.get(data['customer_id'])
    if not customer or customer.partner_type not in ['customer', 'both']:
        return jsonify({'error': 'Valid customer not found'}), 404
    
    # Check if project exists (if provided)
    if data.get('project_id'):
        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({'error': 'Project not found'}), 404
    
    try:
        invoice = CustomerInvoice(
            invoice_number=data['invoice_number'],
            customer_id=data['customer_id'],
            project_id=data.get('project_id'),
            invoice_date=datetime.strptime(data['invoice_date'], '%Y-%m-%d').date(),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None,
            status=data.get('status', 'draft'),
            currency=data.get('currency', 'USD'),
            notes=data.get('notes')
        )
        
        db.session.add(invoice)
        db.session.flush()
        
        # Add invoice lines if provided
        if data.get('lines'):
            for line_data in data['lines']:
                line_total = line_data.get('quantity', 1.0) * line_data.get('unit_price', 0.0)
                line = CustomerInvoiceLine(
                    customer_invoice_id=invoice.id,
                    product_id=line_data.get('product_id'),
                    description=line_data.get('description', ''),
                    quantity=line_data.get('quantity', 1.0),
                    unit_price=line_data.get('unit_price', 0.0),
                    line_total=line_total
                )
                db.session.add(line)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Customer invoice created successfully',
            'invoice': {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'customer_id': invoice.customer_id,
                'invoice_date': invoice.invoice_date.isoformat(),
                'status': invoice.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/customer-invoices', methods=['GET'])
def get_customer_invoices():
    """Get all customer invoices"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    invoices = CustomerInvoice.query.all()
    
    return jsonify({
        'invoices': [{
            'id': inv.id,
            'invoice_number': inv.invoice_number,
            'customer_id': inv.customer_id,
            'customer_name': inv.customer.name if inv.customer else None,
            'project_id': inv.project_id,
            'invoice_date': inv.invoice_date.isoformat(),
            'due_date': inv.due_date.isoformat() if inv.due_date else None,
            'status': inv.status,
            'currency': inv.currency,
            'total_amount': sum(line.line_total for line in inv.lines)
        } for inv in invoices]
    }), 200


@sales_purchase_bp.route('/customer-invoices/<int:invoice_id>', methods=['GET'])
def get_customer_invoice(invoice_id):
    """Get a specific customer invoice with lines"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    invoice = CustomerInvoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Customer invoice not found'}), 404
    
    lines = [{
        'id': line.id,
        'product_id': line.product_id,
        'product_name': line.product.name if line.product else None,
        'description': line.description,
        'quantity': line.quantity,
        'unit_price': line.unit_price,
        'line_total': line.line_total
    } for line in invoice.lines]
    
    return jsonify({
        'invoice': {
            'id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'customer_id': invoice.customer_id,
            'customer_name': invoice.customer.name if invoice.customer else None,
            'project_id': invoice.project_id,
            'invoice_date': invoice.invoice_date.isoformat(),
            'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
            'status': invoice.status,
            'currency': invoice.currency,
            'notes': invoice.notes,
            'created_at': invoice.created_at.isoformat(),
            'lines': lines,
            'total_amount': sum(line.line_total for line in invoice.lines)
        }
    }), 200


@sales_purchase_bp.route('/customer-invoices/<int:invoice_id>', methods=['PUT'])
def update_customer_invoice(invoice_id):
    """Update a customer invoice"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    invoice = CustomerInvoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Customer invoice not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'status' in data:
            if data['status'] not in ['draft', 'posted', 'paid', 'cancelled']:
                return jsonify({'error': 'Invalid status'}), 400
            invoice.status = data['status']
        if 'invoice_date' in data:
            invoice.invoice_date = datetime.strptime(data['invoice_date'], '%Y-%m-%d').date()
        if 'due_date' in data:
            invoice.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data['due_date'] else None
        if 'notes' in data:
            invoice.notes = data['notes']
        if 'currency' in data:
            invoice.currency = data['currency']
        
        invoice.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Customer invoice updated successfully',
            'invoice': {
                'id': invoice.id,
                'invoice_number': invoice.invoice_number,
                'status': invoice.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/customer-invoices/<int:invoice_id>', methods=['DELETE'])
def delete_customer_invoice(invoice_id):
    """Delete a customer invoice"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    invoice = CustomerInvoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Customer invoice not found'}), 404
    
    try:
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({'message': 'Customer invoice deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== CUSTOMER INVOICE LINES ====================

@sales_purchase_bp.route('/customer-invoices/<int:invoice_id>/lines', methods=['POST'])
def add_customer_invoice_line(invoice_id):
    """Add a line to a customer invoice"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    invoice = CustomerInvoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'error': 'Customer invoice not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('description'):
        return jsonify({'error': 'Description is required'}), 400
    
    try:
        line_total = data.get('quantity', 1.0) * data.get('unit_price', 0.0)
        
        line = CustomerInvoiceLine(
            customer_invoice_id=invoice_id,
            product_id=data.get('product_id'),
            description=data['description'],
            quantity=data.get('quantity', 1.0),
            unit_price=data.get('unit_price', 0.0),
            line_total=line_total
        )
        
        db.session.add(line)
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice line added successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_price': line.unit_price,
                'line_total': line.line_total
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/customer-invoices/<int:invoice_id>/lines/<int:line_id>', methods=['PUT'])
def update_customer_invoice_line(invoice_id, line_id):
    """Update a customer invoice line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = CustomerInvoiceLine.query.filter_by(id=line_id, customer_invoice_id=invoice_id).first()
    if not line:
        return jsonify({'error': 'Invoice line not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            line.description = data['description']
        if 'quantity' in data:
            line.quantity = data['quantity']
        if 'unit_price' in data:
            line.unit_price = data['unit_price']
        if 'product_id' in data:
            line.product_id = data['product_id']
        
        # Recalculate line total
        line.line_total = line.quantity * line.unit_price
        
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice line updated successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_price': line.unit_price,
                'line_total': line.line_total
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/customer-invoices/<int:invoice_id>/lines/<int:line_id>', methods=['DELETE'])
def delete_customer_invoice_line(invoice_id, line_id):
    """Delete a customer invoice line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = CustomerInvoiceLine.query.filter_by(id=line_id, customer_invoice_id=invoice_id).first()
    if not line:
        return jsonify({'error': 'Invoice line not found'}), 404
    
    try:
        db.session.delete(line)
        db.session.commit()
        return jsonify({'message': 'Invoice line deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
