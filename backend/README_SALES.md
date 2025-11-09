# Sales and Purchase Management API Documentation

This document provides comprehensive documentation for the Sales and Purchase Management module, including Partners, Products, Sales Orders, Customer Invoices, Purchase Orders, and Vendor Bills.

## Table of Contents

1. [Partner Management](#partner-management)
2. [Product Management](#product-management)
3. [Sales Order Management](#sales-order-management)
4. [Customer Invoice Management](#customer-invoice-management)
5. [Purchase Order Management](#purchase-order-management)
6. [Vendor Bill Management](#vendor-bill-management)
7. [Complete Testing Flows](#complete-testing-flows)

---

## Partner Management

Partners represent both customers and vendors in the system.

### 1. Create Partner

**Endpoint:** `POST /partners`

**Description:** Create a new partner (customer, vendor, or both)

**Request:**
```bash
curl -X POST http://localhost:5000/partners \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Acme Corporation",
    "partner_type": "both",
    "email": "contact@acme.com",
    "phone": "+1-555-0123",
    "address": "123 Main St, City, State 12345"
  }'
```

**Response:**
```json
{
  "message": "Partner created successfully",
  "partner": {
    "id": 1,
    "name": "Acme Corporation",
    "partner_type": "both",
    "email": "contact@acme.com"
  }
}
```

### 2. Get All Partners

**Endpoint:** `GET /partners`

**Description:** Retrieve all partners with optional filtering by partner_type

**Request:**
```bash
# Get all partners
curl -X GET http://localhost:5000/partners \
  -b cookies.txt

# Get only customers
curl -X GET "http://localhost:5000/partners?partner_type=customer" \
  -b cookies.txt

# Get only vendors
curl -X GET "http://localhost:5000/partners?partner_type=vendor" \
  -b cookies.txt
```

**Response:**
```json
{
  "partners": [
    {
      "id": 1,
      "name": "Acme Corporation",
      "partner_type": "both",
      "email": "contact@acme.com",
      "phone": "+1-555-0123",
      "address": "123 Main St, City, State 12345",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### 3. Get Specific Partner

**Endpoint:** `GET /partners/<partner_id>`

**Description:** Retrieve details of a specific partner

**Request:**
```bash
curl -X GET http://localhost:5000/partners/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "partner": {
    "id": 1,
    "name": "Acme Corporation",
    "partner_type": "both",
    "email": "contact@acme.com",
    "phone": "+1-555-0123",
    "address": "123 Main St, City, State 12345",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

### 4. Update Partner

**Endpoint:** `PUT /partners/<partner_id>`

**Description:** Update partner information

**Request:**
```bash
curl -X PUT http://localhost:5000/partners/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "phone": "+1-555-9999",
    "address": "456 New St, City, State 54321"
  }'
```

**Response:**
```json
{
  "message": "Partner updated successfully",
  "partner": {
    "id": 1,
    "name": "Acme Corporation",
    "email": "contact@acme.com"
  }
}
```

---

## Product Management

Products can be physical products, services, or consumables.

### 1. Create Product

**Endpoint:** `POST /products`

**Description:** Create a new product

**Request:**
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Professional Consulting",
    "product_type": "service",
    "description": "Expert business consulting services",
    "sale_price": 150.00,
    "cost_price": 80.00
  }'
```

**Response:**
```json
{
  "message": "Product created successfully",
  "product": {
    "id": 1,
    "name": "Professional Consulting",
    "product_type": "service",
    "sale_price": 150.0,
    "cost_price": 80.0
  }
}
```

### 2. Get All Products

**Endpoint:** `GET /products`

**Description:** Retrieve all products

**Request:**
```bash
curl -X GET http://localhost:5000/products \
  -b cookies.txt
```

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Professional Consulting",
      "product_type": "service",
      "description": "Expert business consulting services",
      "sale_price": 150.0,
      "cost_price": 80.0,
      "created_at": "2024-01-15T11:00:00"
    }
  ]
}
```

### 3. Update Product

**Endpoint:** `PUT /products/<product_id>`

**Description:** Update product information

**Request:**
```bash
curl -X PUT http://localhost:5000/products/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "sale_price": 175.00,
    "description": "Premium business consulting services"
  }'
```

**Response:**
```json
{
  "message": "Product updated successfully",
  "product": {
    "id": 1,
    "name": "Professional Consulting",
    "sale_price": 175.0
  }
}
```

---

## Sales Order Management

Sales orders track customer orders with multiple line items.

### 1. Create Sales Order

**Endpoint:** `POST /sales-orders`

**Description:** Create a new sales order with optional line items

**Request:**
```bash
curl -X POST http://localhost:5000/sales-orders \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "so_number": "SO-2024-001",
    "customer_id": 1,
    "project_id": 1,
    "order_date": "2024-01-15",
    "status": "draft",
    "currency": "USD",
    "notes": "Initial consulting engagement",
    "lines": [
      {
        "product_id": 1,
        "description": "20 hours consulting",
        "quantity": 20.0,
        "unit_price": 150.00,
        "milestone_flag": false
      }
    ]
  }'
```

**Response:**
```json
{
  "message": "Sales order created successfully",
  "sales_order": {
    "id": 1,
    "so_number": "SO-2024-001",
    "customer_id": 1,
    "order_date": "2024-01-15",
    "status": "draft"
  }
}
```

**Note:** `line_total` is automatically calculated as `quantity * unit_price = 20 * 150 = 3000.00`

### 2. Get All Sales Orders

**Endpoint:** `GET /sales-orders`

**Description:** Retrieve all sales orders with totals

**Request:**
```bash
curl -X GET http://localhost:5000/sales-orders \
  -b cookies.txt
```

**Response:**
```json
{
  "sales_orders": [
    {
      "id": 1,
      "so_number": "SO-2024-001",
      "customer_id": 1,
      "customer_name": "Acme Corporation",
      "project_id": 1,
      "order_date": "2024-01-15",
      "status": "draft",
      "currency": "USD",
      "lines_count": 1,
      "total_amount": 3000.0
    }
  ]
}
```

### 3. Get Specific Sales Order

**Endpoint:** `GET /sales-orders/<so_id>`

**Description:** Retrieve a specific sales order with all line items

**Request:**
```bash
curl -X GET http://localhost:5000/sales-orders/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "sales_order": {
    "id": 1,
    "so_number": "SO-2024-001",
    "customer_id": 1,
    "customer_name": "Acme Corporation",
    "project_id": 1,
    "order_date": "2024-01-15",
    "status": "draft",
    "currency": "USD",
    "notes": "Initial consulting engagement",
    "created_at": "2024-01-15T12:00:00",
    "lines": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "Professional Consulting",
        "description": "20 hours consulting",
        "quantity": 20.0,
        "unit_price": 150.0,
        "line_total": 3000.0,
        "milestone_flag": false
      }
    ],
    "total_amount": 3000.0
  }
}
```

### 4. Update Sales Order

**Endpoint:** `PUT /sales-orders/<so_id>`

**Description:** Update sales order status, currency, or notes

**Request:**
```bash
curl -X PUT http://localhost:5000/sales-orders/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "status": "confirmed"
  }'
```

**Response:**
```json
{
  "message": "Sales order updated successfully",
  "sales_order": {
    "id": 1,
    "so_number": "SO-2024-001",
    "status": "confirmed"
  }
}
```

**Valid Status Values:** `draft`, `confirmed`, `done`, `cancelled`

### 5. Delete Sales Order

**Endpoint:** `DELETE /sales-orders/<so_id>`

**Description:** Delete a sales order (cascades to all lines)

**Request:**
```bash
curl -X DELETE http://localhost:5000/sales-orders/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Sales order deleted successfully"
}
```

### 6. Add Sales Order Line

**Endpoint:** `POST /sales-orders/<so_id>/lines`

**Description:** Add a new line item to a sales order

**Request:**
```bash
curl -X POST http://localhost:5000/sales-orders/1/lines \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "product_id": 2,
    "description": "Additional services",
    "quantity": 10.0,
    "unit_price": 200.00,
    "milestone_flag": true
  }'
```

**Response:**
```json
{
  "message": "Sales order line added successfully",
  "line": {
    "id": 2,
    "description": "Additional services",
    "quantity": 10.0,
    "unit_price": 200.0,
    "line_total": 2000.0,
    "milestone_flag": true
  }
}
```

### 7. Update Sales Order Line

**Endpoint:** `PUT /sales-orders/<so_id>/lines/<line_id>`

**Description:** Update a sales order line (auto-recalculates line_total)

**Request:**
```bash
curl -X PUT http://localhost:5000/sales-orders/1/lines/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "quantity": 15.0,
    "unit_price": 180.00
  }'
```

**Response:**
```json
{
  "message": "Sales order line updated successfully",
  "line": {
    "id": 2,
    "description": "Additional services",
    "quantity": 15.0,
    "unit_price": 180.0,
    "line_total": 2700.0,
    "milestone_flag": true
  }
}
```

**Note:** `line_total` is automatically recalculated as `15 * 180 = 2700.00`

### 8. Delete Sales Order Line

**Endpoint:** `DELETE /sales-orders/<so_id>/lines/<line_id>`

**Description:** Delete a sales order line

**Request:**
```bash
curl -X DELETE http://localhost:5000/sales-orders/1/lines/2 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Sales order line deleted successfully"
}
```

---

## Customer Invoice Management

Customer invoices bill customers based on sales orders or directly.

### 1. Create Customer Invoice

**Endpoint:** `POST /customer-invoices`

**Description:** Create a new customer invoice with optional line items

**Request:**
```bash
curl -X POST http://localhost:5000/customer-invoices \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "invoice_number": "INV-2024-001",
    "customer_id": 1,
    "project_id": 1,
    "invoice_date": "2024-01-20",
    "due_date": "2024-02-20",
    "status": "draft",
    "currency": "USD",
    "notes": "Payment terms: Net 30",
    "lines": [
      {
        "product_id": 1,
        "description": "Consulting services - January 2024",
        "quantity": 20.0,
        "unit_price": 150.00
      }
    ]
  }'
```

**Response:**
```json
{
  "message": "Customer invoice created successfully",
  "invoice": {
    "id": 1,
    "invoice_number": "INV-2024-001",
    "customer_id": 1,
    "invoice_date": "2024-01-20",
    "status": "draft"
  }
}
```

### 2. Get All Customer Invoices

**Endpoint:** `GET /customer-invoices`

**Description:** Retrieve all customer invoices with totals

**Request:**
```bash
curl -X GET http://localhost:5000/customer-invoices \
  -b cookies.txt
```

**Response:**
```json
{
  "invoices": [
    {
      "id": 1,
      "invoice_number": "INV-2024-001",
      "customer_id": 1,
      "customer_name": "Acme Corporation",
      "project_id": 1,
      "invoice_date": "2024-01-20",
      "due_date": "2024-02-20",
      "status": "draft",
      "currency": "USD",
      "total_amount": 3000.0
    }
  ]
}
```

### 3. Get Specific Customer Invoice

**Endpoint:** `GET /customer-invoices/<invoice_id>`

**Description:** Retrieve a specific customer invoice with all line items

**Request:**
```bash
curl -X GET http://localhost:5000/customer-invoices/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "invoice": {
    "id": 1,
    "invoice_number": "INV-2024-001",
    "customer_id": 1,
    "customer_name": "Acme Corporation",
    "project_id": 1,
    "invoice_date": "2024-01-20",
    "due_date": "2024-02-20",
    "status": "draft",
    "currency": "USD",
    "notes": "Payment terms: Net 30",
    "created_at": "2024-01-20T10:00:00",
    "lines": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "Professional Consulting",
        "description": "Consulting services - January 2024",
        "quantity": 20.0,
        "unit_price": 150.0,
        "line_total": 3000.0
      }
    ],
    "total_amount": 3000.0
  }
}
```

### 4. Update Customer Invoice

**Endpoint:** `PUT /customer-invoices/<invoice_id>`

**Description:** Update invoice status, dates, or notes

**Request:**
```bash
curl -X PUT http://localhost:5000/customer-invoices/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "status": "posted"
  }'
```

**Response:**
```json
{
  "message": "Customer invoice updated successfully",
  "invoice": {
    "id": 1,
    "invoice_number": "INV-2024-001",
    "status": "posted"
  }
}
```

**Valid Status Values:** `draft`, `posted`, `paid`, `cancelled`

### 5. Delete Customer Invoice

**Endpoint:** `DELETE /customer-invoices/<invoice_id>`

**Description:** Delete a customer invoice (cascades to all lines)

**Request:**
```bash
curl -X DELETE http://localhost:5000/customer-invoices/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Customer invoice deleted successfully"
}
```

### 6. Add Customer Invoice Line

**Endpoint:** `POST /customer-invoices/<invoice_id>/lines`

**Description:** Add a new line item to a customer invoice

**Request:**
```bash
curl -X POST http://localhost:5000/customer-invoices/1/lines \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "product_id": 2,
    "description": "Additional consulting hours",
    "quantity": 5.0,
    "unit_price": 175.00
  }'
```

**Response:**
```json
{
  "message": "Invoice line added successfully",
  "line": {
    "id": 2,
    "description": "Additional consulting hours",
    "quantity": 5.0,
    "unit_price": 175.0,
    "line_total": 875.0
  }
}
```

### 7. Update Customer Invoice Line

**Endpoint:** `PUT /customer-invoices/<invoice_id>/lines/<line_id>`

**Description:** Update a customer invoice line (auto-recalculates line_total)

**Request:**
```bash
curl -X PUT http://localhost:5000/customer-invoices/1/lines/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "quantity": 10.0
  }'
```

**Response:**
```json
{
  "message": "Invoice line updated successfully",
  "line": {
    "id": 2,
    "description": "Additional consulting hours",
    "quantity": 10.0,
    "unit_price": 175.0,
    "line_total": 1750.0
  }
}
```

### 8. Delete Customer Invoice Line

**Endpoint:** `DELETE /customer-invoices/<invoice_id>/lines/<line_id>`

**Description:** Delete a customer invoice line

**Request:**
```bash
curl -X DELETE http://localhost:5000/customer-invoices/1/lines/2 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Invoice line deleted successfully"
}
```

---

## Purchase Order Management

Purchase orders track vendor orders with multiple line items.

### 1. Create Purchase Order

**Endpoint:** `POST /purchase-orders`

**Description:** Create a new purchase order with optional line items

**Request:**
```bash
curl -X POST http://localhost:5000/purchase-orders \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "po_number": "PO-2024-001",
    "vendor_id": 1,
    "project_id": 1,
    "order_date": "2024-01-15",
    "status": "draft",
    "currency": "USD",
    "notes": "Hardware procurement",
    "lines": [
      {
        "product_id": 3,
        "description": "10 laptops",
        "quantity": 10.0,
        "unit_cost": 1200.00
      }
    ]
  }'
```

**Response:**
```json
{
  "message": "Purchase order created successfully",
  "purchase_order": {
    "id": 1,
    "po_number": "PO-2024-001",
    "vendor_id": 1,
    "order_date": "2024-01-15",
    "status": "draft"
  }
}
```

**Note:** `line_total` is automatically calculated as `quantity * unit_cost = 10 * 1200 = 12000.00`

### 2. Get All Purchase Orders

**Endpoint:** `GET /purchase-orders`

**Description:** Retrieve all purchase orders with totals

**Request:**
```bash
curl -X GET http://localhost:5000/purchase-orders \
  -b cookies.txt
```

**Response:**
```json
{
  "purchase_orders": [
    {
      "id": 1,
      "po_number": "PO-2024-001",
      "vendor_id": 1,
      "vendor_name": "Acme Corporation",
      "project_id": 1,
      "order_date": "2024-01-15",
      "status": "draft",
      "currency": "USD",
      "lines_count": 1,
      "total_amount": 12000.0
    }
  ]
}
```

### 3. Get Specific Purchase Order

**Endpoint:** `GET /purchase-orders/<po_id>`

**Description:** Retrieve a specific purchase order with all line items

**Request:**
```bash
curl -X GET http://localhost:5000/purchase-orders/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "purchase_order": {
    "id": 1,
    "po_number": "PO-2024-001",
    "vendor_id": 1,
    "vendor_name": "Acme Corporation",
    "project_id": 1,
    "order_date": "2024-01-15",
    "status": "draft",
    "currency": "USD",
    "notes": "Hardware procurement",
    "created_at": "2024-01-15T14:00:00",
    "lines": [
      {
        "id": 1,
        "product_id": 3,
        "product_name": "Business Laptop",
        "description": "10 laptops",
        "quantity": 10.0,
        "unit_cost": 1200.0,
        "line_total": 12000.0
      }
    ],
    "total_amount": 12000.0
  }
}
```

### 4. Update Purchase Order

**Endpoint:** `PUT /purchase-orders/<po_id>`

**Description:** Update purchase order status, currency, or notes

**Request:**
```bash
curl -X PUT http://localhost:5000/purchase-orders/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "status": "confirmed"
  }'
```

**Response:**
```json
{
  "message": "Purchase order updated successfully",
  "purchase_order": {
    "id": 1,
    "po_number": "PO-2024-001",
    "status": "confirmed"
  }
}
```

**Valid Status Values:** `draft`, `confirmed`, `done`, `cancelled`

### 5. Delete Purchase Order

**Endpoint:** `DELETE /purchase-orders/<po_id>`

**Description:** Delete a purchase order (cascades to all lines)

**Request:**
```bash
curl -X DELETE http://localhost:5000/purchase-orders/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Purchase order deleted successfully"
}
```

### 6. Add Purchase Order Line

**Endpoint:** `POST /purchase-orders/<po_id>/lines`

**Description:** Add a new line item to a purchase order

**Request:**
```bash
curl -X POST http://localhost:5000/purchase-orders/1/lines \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "product_id": 4,
    "description": "Software licenses",
    "quantity": 20.0,
    "unit_cost": 50.00
  }'
```

**Response:**
```json
{
  "message": "Purchase order line added successfully",
  "line": {
    "id": 2,
    "description": "Software licenses",
    "quantity": 20.0,
    "unit_cost": 50.0,
    "line_total": 1000.0
  }
}
```

### 7. Update Purchase Order Line

**Endpoint:** `PUT /purchase-orders/<po_id>/lines/<line_id>`

**Description:** Update a purchase order line (auto-recalculates line_total)

**Request:**
```bash
curl -X PUT http://localhost:5000/purchase-orders/1/lines/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "quantity": 30.0,
    "unit_cost": 45.00
  }'
```

**Response:**
```json
{
  "message": "Purchase order line updated successfully",
  "line": {
    "id": 2,
    "description": "Software licenses",
    "quantity": 30.0,
    "unit_cost": 45.0,
    "line_total": 1350.0
  }
}
```

**Note:** `line_total` is automatically recalculated as `30 * 45 = 1350.00`

### 8. Delete Purchase Order Line

**Endpoint:** `DELETE /purchase-orders/<po_id>/lines/<line_id>`

**Description:** Delete a purchase order line

**Request:**
```bash
curl -X DELETE http://localhost:5000/purchase-orders/1/lines/2 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Purchase order line deleted successfully"
}
```

---

## Vendor Bill Management

Vendor bills record payments owed to vendors based on purchase orders or directly.

### 1. Create Vendor Bill

**Endpoint:** `POST /vendor-bills`

**Description:** Create a new vendor bill with optional line items

**Request:**
```bash
curl -X POST http://localhost:5000/vendor-bills \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "bill_number": "BILL-2024-001",
    "vendor_id": 1,
    "project_id": 1,
    "bill_date": "2024-01-25",
    "due_date": "2024-02-25",
    "status": "draft",
    "currency": "USD",
    "notes": "Payment terms: Net 30",
    "lines": [
      {
        "product_id": 3,
        "description": "10 laptops delivered",
        "quantity": 10.0,
        "unit_cost": 1200.00
      }
    ]
  }'
```

**Response:**
```json
{
  "message": "Vendor bill created successfully",
  "bill": {
    "id": 1,
    "bill_number": "BILL-2024-001",
    "vendor_id": 1,
    "bill_date": "2024-01-25",
    "status": "draft"
  }
}
```

### 2. Get All Vendor Bills

**Endpoint:** `GET /vendor-bills`

**Description:** Retrieve all vendor bills with totals

**Request:**
```bash
curl -X GET http://localhost:5000/vendor-bills \
  -b cookies.txt
```

**Response:**
```json
{
  "bills": [
    {
      "id": 1,
      "bill_number": "BILL-2024-001",
      "vendor_id": 1,
      "vendor_name": "Acme Corporation",
      "project_id": 1,
      "bill_date": "2024-01-25",
      "due_date": "2024-02-25",
      "status": "draft",
      "currency": "USD",
      "total_amount": 12000.0
    }
  ]
}
```

### 3. Get Specific Vendor Bill

**Endpoint:** `GET /vendor-bills/<bill_id>`

**Description:** Retrieve a specific vendor bill with all line items

**Request:**
```bash
curl -X GET http://localhost:5000/vendor-bills/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "bill": {
    "id": 1,
    "bill_number": "BILL-2024-001",
    "vendor_id": 1,
    "vendor_name": "Acme Corporation",
    "project_id": 1,
    "bill_date": "2024-01-25",
    "due_date": "2024-02-25",
    "status": "draft",
    "currency": "USD",
    "notes": "Payment terms: Net 30",
    "created_at": "2024-01-25T09:00:00",
    "lines": [
      {
        "id": 1,
        "product_id": 3,
        "product_name": "Business Laptop",
        "description": "10 laptops delivered",
        "quantity": 10.0,
        "unit_cost": 1200.0,
        "line_total": 12000.0
      }
    ],
    "total_amount": 12000.0
  }
}
```

### 4. Update Vendor Bill

**Endpoint:** `PUT /vendor-bills/<bill_id>`

**Description:** Update vendor bill status, dates, or notes

**Request:**
```bash
curl -X PUT http://localhost:5000/vendor-bills/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "status": "posted"
  }'
```

**Response:**
```json
{
  "message": "Vendor bill updated successfully",
  "bill": {
    "id": 1,
    "bill_number": "BILL-2024-001",
    "status": "posted"
  }
}
```

**Valid Status Values:** `draft`, `posted`, `paid`, `cancelled`

### 5. Delete Vendor Bill

**Endpoint:** `DELETE /vendor-bills/<bill_id>`

**Description:** Delete a vendor bill (cascades to all lines)

**Request:**
```bash
curl -X DELETE http://localhost:5000/vendor-bills/1 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Vendor bill deleted successfully"
}
```

### 6. Add Vendor Bill Line

**Endpoint:** `POST /vendor-bills/<bill_id>/lines`

**Description:** Add a new line item to a vendor bill

**Request:**
```bash
curl -X POST http://localhost:5000/vendor-bills/1/lines \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "product_id": 5,
    "description": "Extended warranty",
    "quantity": 10.0,
    "unit_cost": 100.00
  }'
```

**Response:**
```json
{
  "message": "Bill line added successfully",
  "line": {
    "id": 2,
    "description": "Extended warranty",
    "quantity": 10.0,
    "unit_cost": 100.0,
    "line_total": 1000.0
  }
}
```

### 7. Update Vendor Bill Line

**Endpoint:** `PUT /vendor-bills/<bill_id>/lines/<line_id>`

**Description:** Update a vendor bill line (auto-recalculates line_total)

**Request:**
```bash
curl -X PUT http://localhost:5000/vendor-bills/1/lines/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "quantity": 12.0,
    "unit_cost": 95.00
  }'
```

**Response:**
```json
{
  "message": "Bill line updated successfully",
  "line": {
    "id": 2,
    "description": "Extended warranty",
    "quantity": 12.0,
    "unit_cost": 95.0,
    "line_total": 1140.0
  }
}
```

### 8. Delete Vendor Bill Line

**Endpoint:** `DELETE /vendor-bills/<bill_id>/lines/<line_id>`

**Description:** Delete a vendor bill line

**Request:**
```bash
curl -X DELETE http://localhost:5000/vendor-bills/1/lines/2 \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Bill line deleted successfully"
}
```

---

## Complete Testing Flows

### Sales Flow: From Order to Invoice

```bash
# Step 1: Register and login
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "password123"}' \
  -c cookies.txt

curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "password123"}' \
  -c cookies.txt

# Step 2: Create a customer partner
curl -X POST http://localhost:5000/partners \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "TechCorp Inc",
    "partner_type": "customer",
    "email": "contact@techcorp.com",
    "phone": "+1-555-1234"
  }'
# Response: customer_id = 1

# Step 3: Create a product
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Cloud Hosting Service",
    "product_type": "service",
    "sale_price": 500.00,
    "cost_price": 200.00
  }'
# Response: product_id = 1

# Step 4: Create a project (if needed)
curl -X POST http://localhost:5000/projects \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "TechCorp Cloud Migration",
    "description": "Migrating infrastructure to cloud",
    "start_date": "2024-01-01",
    "end_date": "2024-06-30",
    "status": "in_progress"
  }'
# Response: project_id = 1

# Step 5: Create a sales order
curl -X POST http://localhost:5000/sales-orders \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "so_number": "SO-2024-001",
    "customer_id": 1,
    "project_id": 1,
    "order_date": "2024-01-15",
    "status": "draft",
    "lines": [
      {
        "product_id": 1,
        "description": "3 months cloud hosting",
        "quantity": 3.0,
        "unit_price": 500.00,
        "milestone_flag": false
      }
    ]
  }'
# Response: sales_order_id = 1, total = 1500.00

# Step 6: Confirm the sales order
curl -X PUT http://localhost:5000/sales-orders/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "confirmed"}'

# Step 7: Create a customer invoice based on the sales order
curl -X POST http://localhost:5000/customer-invoices \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "invoice_number": "INV-2024-001",
    "customer_id": 1,
    "project_id": 1,
    "invoice_date": "2024-01-20",
    "due_date": "2024-02-20",
    "status": "draft",
    "lines": [
      {
        "product_id": 1,
        "description": "3 months cloud hosting - January to March 2024",
        "quantity": 3.0,
        "unit_price": 500.00
      }
    ]
  }'
# Response: invoice_id = 1, total = 1500.00

# Step 8: Post the invoice
curl -X PUT http://localhost:5000/customer-invoices/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "posted"}'

# Step 9: Mark invoice as paid
curl -X PUT http://localhost:5000/customer-invoices/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "paid"}'

# Step 10: Complete the sales order
curl -X PUT http://localhost:5000/sales-orders/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "done"}'
```

### Purchase Flow: From Order to Bill

```bash
# Step 1: Create a vendor partner
curl -X POST http://localhost:5000/partners \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Hardware Supplier Co",
    "partner_type": "vendor",
    "email": "sales@hardwaresupplier.com",
    "phone": "+1-555-5678"
  }'
# Response: vendor_id = 2

# Step 2: Create a product for purchase
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "Server Hardware",
    "product_type": "product",
    "sale_price": 5000.00,
    "cost_price": 3500.00
  }'
# Response: product_id = 2

# Step 3: Create a purchase order
curl -X POST http://localhost:5000/purchase-orders \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "po_number": "PO-2024-001",
    "vendor_id": 2,
    "project_id": 1,
    "order_date": "2024-01-10",
    "status": "draft",
    "lines": [
      {
        "product_id": 2,
        "description": "2 rack servers",
        "quantity": 2.0,
        "unit_cost": 3500.00
      }
    ]
  }'
# Response: purchase_order_id = 1, total = 7000.00

# Step 4: Confirm the purchase order
curl -X PUT http://localhost:5000/purchase-orders/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "confirmed"}'

# Step 5: Receive goods and create vendor bill
curl -X POST http://localhost:5000/vendor-bills \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "bill_number": "BILL-2024-001",
    "vendor_id": 2,
    "project_id": 1,
    "bill_date": "2024-01-25",
    "due_date": "2024-02-25",
    "status": "draft",
    "lines": [
      {
        "product_id": 2,
        "description": "2 rack servers - delivered",
        "quantity": 2.0,
        "unit_cost": 3500.00
      }
    ]
  }'
# Response: bill_id = 1, total = 7000.00

# Step 6: Post the vendor bill
curl -X PUT http://localhost:5000/vendor-bills/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "posted"}'

# Step 7: Pay the vendor bill
curl -X PUT http://localhost:5000/vendor-bills/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "paid"}'

# Step 8: Complete the purchase order
curl -X PUT http://localhost:5000/purchase-orders/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "done"}'
```

### Line Total Auto-Calculation Examples

```bash
# Example 1: Creating a line automatically calculates total
curl -X POST http://localhost:5000/sales-orders/1/lines \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "description": "Additional service",
    "quantity": 5.0,
    "unit_price": 100.00
  }'
# line_total is automatically set to: 5.0 * 100.00 = 500.00

# Example 2: Updating quantity recalculates total
curl -X PUT http://localhost:5000/sales-orders/1/lines/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"quantity": 10.0}'
# line_total is automatically recalculated to: 10.0 * 100.00 = 1000.00

# Example 3: Updating unit_price recalculates total
curl -X PUT http://localhost:5000/sales-orders/1/lines/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"unit_price": 150.00}'
# line_total is automatically recalculated to: 10.0 * 150.00 = 1500.00

# Example 4: Updating both recalculates total
curl -X PUT http://localhost:5000/sales-orders/1/lines/2 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"quantity": 8.0, "unit_price": 200.00}'
# line_total is automatically recalculated to: 8.0 * 200.00 = 1600.00
```

---

## Important Notes

### Automatic Calculations

- **Line Totals**: All `line_total` values are automatically calculated as `quantity * unit_price` (sales) or `quantity * unit_cost` (purchase)
- **Never** manually set `line_total` - it will be overwritten
- Updates to `quantity`, `unit_price`, or `unit_cost` trigger automatic recalculation

### Status Workflows

**Sales Orders & Purchase Orders:**
- `draft` → `confirmed` → `done` or `cancelled`

**Customer Invoices & Vendor Bills:**
- `draft` → `posted` → `paid` or `cancelled`

### Partner Types

- **customer**: Can only be used in sales orders and customer invoices
- **vendor**: Can only be used in purchase orders and vendor bills
- **both**: Can be used in any transaction

### Cascade Behavior

- Deleting a sales order/purchase order cascades to all line items
- Deleting a customer invoice/vendor bill cascades to all line items
- Deleting a partner sets foreign keys to NULL (doesn't cascade)

### Authentication

All endpoints require authentication. Make sure to:
1. Register a user with `/register`
2. Login with `/login` and save cookies (`-c cookies.txt`)
3. Include cookies in all subsequent requests (`-b cookies.txt`)

---

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py

# The API will be available at http://localhost:5000
```

---

This completes the Sales and Purchase Management API documentation with comprehensive examples and testing flows!
