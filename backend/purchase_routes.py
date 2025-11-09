from flask import request, jsonify, session
from models import db, Project
from sales_purchase_models import (
    Partner, Product, PurchaseOrder, PurchaseOrderLine, VendorBill, VendorBillLine
)
from datetime import datetime
from sales_routes import sales_purchase_bp


# Helper function to check authentication
def require_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    return None


# ==================== PURCHASE ORDER MANAGEMENT ====================

@sales_purchase_bp.route('/purchase-orders', methods=['POST'])
def create_purchase_order():
    """Create a new purchase order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    
    if not data or not data.get('po_number') or not data.get('vendor_id') or not data.get('order_date'):
        return jsonify({'error': 'po_number, vendor_id, and order_date are required'}), 400
    
    # Check if vendor exists
    vendor = Partner.query.get(data['vendor_id'])
    if not vendor or vendor.partner_type not in ['vendor', 'both']:
        return jsonify({'error': 'Valid vendor not found'}), 404
    
    # Check if project exists (if provided)
    if data.get('project_id'):
        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({'error': 'Project not found'}), 404
    
    try:
        purchase_order = PurchaseOrder(
            po_number=data['po_number'],
            vendor_id=data['vendor_id'],
            project_id=data.get('project_id'),
            order_date=datetime.strptime(data['order_date'], '%Y-%m-%d').date(),
            status=data.get('status', 'draft'),
            currency=data.get('currency', 'USD'),
            notes=data.get('notes')
        )
        
        db.session.add(purchase_order)
        db.session.flush()
        
        # Add order lines if provided
        if data.get('lines'):
            for line_data in data['lines']:
                line_total = line_data.get('quantity', 1.0) * line_data.get('unit_cost', 0.0)
                line = PurchaseOrderLine(
                    purchase_order_id=purchase_order.id,
                    product_id=line_data.get('product_id'),
                    description=line_data.get('description', ''),
                    quantity=line_data.get('quantity', 1.0),
                    unit_cost=line_data.get('unit_cost', 0.0),
                    line_total=line_total
                )
                db.session.add(line)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Purchase order created successfully',
            'purchase_order': {
                'id': purchase_order.id,
                'po_number': purchase_order.po_number,
                'vendor_id': purchase_order.vendor_id,
                'order_date': purchase_order.order_date.isoformat(),
                'status': purchase_order.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/purchase-orders', methods=['GET'])
def get_purchase_orders():
    """Get all purchase orders"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    purchase_orders = PurchaseOrder.query.all()
    
    return jsonify({
        'purchase_orders': [{
            'id': po.id,
            'po_number': po.po_number,
            'vendor_id': po.vendor_id,
            'vendor_name': po.vendor.name if po.vendor else None,
            'project_id': po.project_id,
            'order_date': po.order_date.isoformat(),
            'status': po.status,
            'currency': po.currency,
            'lines_count': len(po.lines),
            'total_amount': sum(line.line_total for line in po.lines)
        } for po in purchase_orders]
    }), 200


@sales_purchase_bp.route('/purchase-orders/<int:po_id>', methods=['GET'])
def get_purchase_order(po_id):
    """Get a specific purchase order with lines"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    purchase_order = PurchaseOrder.query.get(po_id)
    if not purchase_order:
        return jsonify({'error': 'Purchase order not found'}), 404
    
    lines = [{
        'id': line.id,
        'product_id': line.product_id,
        'product_name': line.product.name if line.product else None,
        'description': line.description,
        'quantity': line.quantity,
        'unit_cost': line.unit_cost,
        'line_total': line.line_total
    } for line in purchase_order.lines]
    
    return jsonify({
        'purchase_order': {
            'id': purchase_order.id,
            'po_number': purchase_order.po_number,
            'vendor_id': purchase_order.vendor_id,
            'vendor_name': purchase_order.vendor.name if purchase_order.vendor else None,
            'project_id': purchase_order.project_id,
            'order_date': purchase_order.order_date.isoformat(),
            'status': purchase_order.status,
            'currency': purchase_order.currency,
            'notes': purchase_order.notes,
            'created_at': purchase_order.created_at.isoformat(),
            'lines': lines,
            'total_amount': sum(line.line_total for line in purchase_order.lines)
        }
    }), 200


@sales_purchase_bp.route('/purchase-orders/<int:po_id>', methods=['PUT'])
def update_purchase_order(po_id):
    """Update a purchase order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    purchase_order = PurchaseOrder.query.get(po_id)
    if not purchase_order:
        return jsonify({'error': 'Purchase order not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'status' in data:
            if data['status'] not in ['draft', 'confirmed', 'done', 'cancelled']:
                return jsonify({'error': 'Invalid status'}), 400
            purchase_order.status = data['status']
        if 'currency' in data:
            purchase_order.currency = data['currency']
        if 'notes' in data:
            purchase_order.notes = data['notes']
        if 'order_date' in data:
            purchase_order.order_date = datetime.strptime(data['order_date'], '%Y-%m-%d').date()
        
        purchase_order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Purchase order updated successfully',
            'purchase_order': {
                'id': purchase_order.id,
                'po_number': purchase_order.po_number,
                'status': purchase_order.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/purchase-orders/<int:po_id>', methods=['DELETE'])
def delete_purchase_order(po_id):
    """Delete a purchase order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    purchase_order = PurchaseOrder.query.get(po_id)
    if not purchase_order:
        return jsonify({'error': 'Purchase order not found'}), 404
    
    try:
        db.session.delete(purchase_order)
        db.session.commit()
        return jsonify({'message': 'Purchase order deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== PURCHASE ORDER LINES ====================

@sales_purchase_bp.route('/purchase-orders/<int:po_id>/lines', methods=['POST'])
def add_purchase_order_line(po_id):
    """Add a line to a purchase order"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    purchase_order = PurchaseOrder.query.get(po_id)
    if not purchase_order:
        return jsonify({'error': 'Purchase order not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('description'):
        return jsonify({'error': 'Description is required'}), 400
    
    try:
        line_total = data.get('quantity', 1.0) * data.get('unit_cost', 0.0)
        
        line = PurchaseOrderLine(
            purchase_order_id=po_id,
            product_id=data.get('product_id'),
            description=data['description'],
            quantity=data.get('quantity', 1.0),
            unit_cost=data.get('unit_cost', 0.0),
            line_total=line_total
        )
        
        db.session.add(line)
        db.session.commit()
        
        return jsonify({
            'message': 'Purchase order line added successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_cost': line.unit_cost,
                'line_total': line.line_total
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/purchase-orders/<int:po_id>/lines/<int:line_id>', methods=['PUT'])
def update_purchase_order_line(po_id, line_id):
    """Update a purchase order line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = PurchaseOrderLine.query.filter_by(id=line_id, purchase_order_id=po_id).first()
    if not line:
        return jsonify({'error': 'Purchase order line not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            line.description = data['description']
        if 'quantity' in data:
            line.quantity = data['quantity']
        if 'unit_cost' in data:
            line.unit_cost = data['unit_cost']
        if 'product_id' in data:
            line.product_id = data['product_id']
        
        # Recalculate line total
        line.line_total = line.quantity * line.unit_cost
        
        db.session.commit()
        
        return jsonify({
            'message': 'Purchase order line updated successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_cost': line.unit_cost,
                'line_total': line.line_total
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/purchase-orders/<int:po_id>/lines/<int:line_id>', methods=['DELETE'])
def delete_purchase_order_line(po_id, line_id):
    """Delete a purchase order line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = PurchaseOrderLine.query.filter_by(id=line_id, purchase_order_id=po_id).first()
    if not line:
        return jsonify({'error': 'Purchase order line not found'}), 404
    
    try:
        db.session.delete(line)
        db.session.commit()
        return jsonify({'message': 'Purchase order line deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== VENDOR BILL MANAGEMENT ====================

@sales_purchase_bp.route('/vendor-bills', methods=['POST'])
def create_vendor_bill():
    """Create a new vendor bill"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    data = request.get_json()
    
    if not data or not data.get('bill_number') or not data.get('vendor_id') or not data.get('bill_date'):
        return jsonify({'error': 'bill_number, vendor_id, and bill_date are required'}), 400
    
    # Check if vendor exists
    vendor = Partner.query.get(data['vendor_id'])
    if not vendor or vendor.partner_type not in ['vendor', 'both']:
        return jsonify({'error': 'Valid vendor not found'}), 404
    
    # Check if project exists (if provided)
    if data.get('project_id'):
        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({'error': 'Project not found'}), 404
    
    try:
        bill = VendorBill(
            bill_number=data['bill_number'],
            vendor_id=data['vendor_id'],
            project_id=data.get('project_id'),
            bill_date=datetime.strptime(data['bill_date'], '%Y-%m-%d').date(),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None,
            status=data.get('status', 'draft'),
            currency=data.get('currency', 'USD'),
            notes=data.get('notes')
        )
        
        db.session.add(bill)
        db.session.flush()
        
        # Add bill lines if provided
        if data.get('lines'):
            for line_data in data['lines']:
                line_total = line_data.get('quantity', 1.0) * line_data.get('unit_cost', 0.0)
                line = VendorBillLine(
                    vendor_bill_id=bill.id,
                    product_id=line_data.get('product_id'),
                    description=line_data.get('description', ''),
                    quantity=line_data.get('quantity', 1.0),
                    unit_cost=line_data.get('unit_cost', 0.0),
                    line_total=line_total
                )
                db.session.add(line)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Vendor bill created successfully',
            'bill': {
                'id': bill.id,
                'bill_number': bill.bill_number,
                'vendor_id': bill.vendor_id,
                'bill_date': bill.bill_date.isoformat(),
                'status': bill.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/vendor-bills', methods=['GET'])
def get_vendor_bills():
    """Get all vendor bills"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    bills = VendorBill.query.all()
    
    return jsonify({
        'bills': [{
            'id': bill.id,
            'bill_number': bill.bill_number,
            'vendor_id': bill.vendor_id,
            'vendor_name': bill.vendor.name if bill.vendor else None,
            'project_id': bill.project_id,
            'bill_date': bill.bill_date.isoformat(),
            'due_date': bill.due_date.isoformat() if bill.due_date else None,
            'status': bill.status,
            'currency': bill.currency,
            'total_amount': sum(line.line_total for line in bill.lines)
        } for bill in bills]
    }), 200


@sales_purchase_bp.route('/vendor-bills/<int:bill_id>', methods=['GET'])
def get_vendor_bill(bill_id):
    """Get a specific vendor bill with lines"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    bill = VendorBill.query.get(bill_id)
    if not bill:
        return jsonify({'error': 'Vendor bill not found'}), 404
    
    lines = [{
        'id': line.id,
        'product_id': line.product_id,
        'product_name': line.product.name if line.product else None,
        'description': line.description,
        'quantity': line.quantity,
        'unit_cost': line.unit_cost,
        'line_total': line.line_total
    } for line in bill.lines]
    
    return jsonify({
        'bill': {
            'id': bill.id,
            'bill_number': bill.bill_number,
            'vendor_id': bill.vendor_id,
            'vendor_name': bill.vendor.name if bill.vendor else None,
            'project_id': bill.project_id,
            'bill_date': bill.bill_date.isoformat(),
            'due_date': bill.due_date.isoformat() if bill.due_date else None,
            'status': bill.status,
            'currency': bill.currency,
            'notes': bill.notes,
            'created_at': bill.created_at.isoformat(),
            'lines': lines,
            'total_amount': sum(line.line_total for line in bill.lines)
        }
    }), 200


@sales_purchase_bp.route('/vendor-bills/<int:bill_id>', methods=['PUT'])
def update_vendor_bill(bill_id):
    """Update a vendor bill"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    bill = VendorBill.query.get(bill_id)
    if not bill:
        return jsonify({'error': 'Vendor bill not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'status' in data:
            if data['status'] not in ['draft', 'posted', 'paid', 'cancelled']:
                return jsonify({'error': 'Invalid status'}), 400
            bill.status = data['status']
        if 'bill_date' in data:
            bill.bill_date = datetime.strptime(data['bill_date'], '%Y-%m-%d').date()
        if 'due_date' in data:
            bill.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data['due_date'] else None
        if 'notes' in data:
            bill.notes = data['notes']
        if 'currency' in data:
            bill.currency = data['currency']
        
        bill.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Vendor bill updated successfully',
            'bill': {
                'id': bill.id,
                'bill_number': bill.bill_number,
                'status': bill.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/vendor-bills/<int:bill_id>', methods=['DELETE'])
def delete_vendor_bill(bill_id):
    """Delete a vendor bill"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    bill = VendorBill.query.get(bill_id)
    if not bill:
        return jsonify({'error': 'Vendor bill not found'}), 404
    
    try:
        db.session.delete(bill)
        db.session.commit()
        return jsonify({'message': 'Vendor bill deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== VENDOR BILL LINES ====================

@sales_purchase_bp.route('/vendor-bills/<int:bill_id>/lines', methods=['POST'])
def add_vendor_bill_line(bill_id):
    """Add a line to a vendor bill"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    bill = VendorBill.query.get(bill_id)
    if not bill:
        return jsonify({'error': 'Vendor bill not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('description'):
        return jsonify({'error': 'Description is required'}), 400
    
    try:
        line_total = data.get('quantity', 1.0) * data.get('unit_cost', 0.0)
        
        line = VendorBillLine(
            vendor_bill_id=bill_id,
            product_id=data.get('product_id'),
            description=data['description'],
            quantity=data.get('quantity', 1.0),
            unit_cost=data.get('unit_cost', 0.0),
            line_total=line_total
        )
        
        db.session.add(line)
        db.session.commit()
        
        return jsonify({
            'message': 'Bill line added successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_cost': line.unit_cost,
                'line_total': line.line_total
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/vendor-bills/<int:bill_id>/lines/<int:line_id>', methods=['PUT'])
def update_vendor_bill_line(bill_id, line_id):
    """Update a vendor bill line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = VendorBillLine.query.filter_by(id=line_id, vendor_bill_id=bill_id).first()
    if not line:
        return jsonify({'error': 'Bill line not found'}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            line.description = data['description']
        if 'quantity' in data:
            line.quantity = data['quantity']
        if 'unit_cost' in data:
            line.unit_cost = data['unit_cost']
        if 'product_id' in data:
            line.product_id = data['product_id']
        
        # Recalculate line total
        line.line_total = line.quantity * line.unit_cost
        
        db.session.commit()
        
        return jsonify({
            'message': 'Bill line updated successfully',
            'line': {
                'id': line.id,
                'description': line.description,
                'quantity': line.quantity,
                'unit_cost': line.unit_cost,
                'line_total': line.line_total
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@sales_purchase_bp.route('/vendor-bills/<int:bill_id>/lines/<int:line_id>', methods=['DELETE'])
def delete_vendor_bill_line(bill_id, line_id):
    """Delete a vendor bill line"""
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    line = VendorBillLine.query.filter_by(id=line_id, vendor_bill_id=bill_id).first()
    if not line:
        return jsonify({'error': 'Bill line not found'}), 404
    
    try:
        db.session.delete(line)
        db.session.commit()
        return jsonify({'message': 'Bill line deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
