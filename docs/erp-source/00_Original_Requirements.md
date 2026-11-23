# Project: Complete Business Management, Inventory, Accounting & Manufacturing ERP System

## 1. Project Overview

I want to develop a comprehensive, professional, scalable, and modular ERP (Enterprise Resource Planning) system for a trading, wholesale, retail, spare parts, and manufacturing business.

The business deals with:

- Motorcycle spare parts and accessories.
- Electrical meters and related products.
- General trading products.
- Multiple suppliers and vendors.
- Wholesale and retail customers.
- Cash, credit, and debit transactions.
- Daily manufacturing and batch-based production.
- Inventory purchasing, selling, receiving, and dispatching.

The objective is to digitize and centralize every important business operation, including accounting, inventory, manufacturing, purchasing, sales, financial transactions, and reporting.

This must be a complete business management solution, not just a basic inventory management application.

---

# 2. Technology Stack

Use the following technologies strictly.

### Frontend
- React.js
- Vite
- Tailwind CSS v4
- JavaScript (ES6+)
- React Router DOM
- Axios
- React Hook Form
- Zod for validation
- Recharts for dashboards and analytics
- Lucide React for icons

### Backend
- Python
- FastAPI
- SQLAlchemy 2.0
- Pydantic v2
- Alembic for database migrations
- JWT Authentication
- Python-based business logic and service layers

### Database
- PostgreSQL

### Additional Technologies
- Redis for caching and background jobs where required.
- Celery or an equivalent background task system.
- Docker and Docker Compose.
- Environment-based configuration.
- Structured application logging.

Use stable, compatible versions of all dependencies.

---

# 3. Initial Project Setup Commands

Before writing application code, initialize the complete project structure.

The root directory should be:

business-erp/

## Frontend Setup

Execute the following commands:

```bash
mkdir business-erp
cd business-erp

npm create vite@latest frontend -- --template react
cd frontend

npm install

npm install react-router-dom axios
npm install react-hook-form zod @hookform/resolvers
npm install recharts lucide-react
npm install date-fns

npm install -D tailwindcss @tailwindcss/vite

cd ..
```

Configure Tailwind CSS v4 using the official Vite plugin.

## Backend Setup

```bash
mkdir backend
cd backend

python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
# venv\Scripts\activate

pip install fastapi "uvicorn[standard]"
pip install sqlalchemy psycopg[binary]
pip install alembic
pip install pydantic pydantic-settings
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
pip install redis celery
pip install email-validator

pip freeze > requirements.txt

cd ..
```

Create the PostgreSQL database and configure the connection through environment variables.

Do not hardcode credentials.

---

# 4. Professional Project Architecture

Follow a clean, modular, layered architecture.

## Frontend Structure

```text
frontend/
│
├── public/
│
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │   ├── common/
│   │   ├── forms/
│   │   ├── tables/
│   │   ├── charts/
│   │   ├── modals/
│   │   └── layout/
│   │
│   ├── pages/
│   │   ├── Dashboard/
│   │   ├── Inventory/
│   │   ├── Products/
│   │   ├── Categories/
│   │   ├── Warehouses/
│   │   ├── Purchases/
│   │   ├── Sales/
│   │   ├── Customers/
│   │   ├── Suppliers/
│   │   ├── Vendors/
│   │   ├── Manufacturing/
│   │   ├── Batches/
│   │   ├── Accounting/
│   │   ├── Expenses/
│   │   ├── Payments/
│   │   ├── Reports/
│   │   ├── Employees/
│   │   └── Settings/
│   │
│   ├── layouts/
│   │   ├── DashboardLayout.jsx
│   │   └── AuthLayout.jsx
│   │
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── inventoryService.js
│   │   ├── salesService.js
│   │   ├── purchaseService.js
│   │   ├── accountingService.js
│   │   └── manufacturingService.js
│   │
│   ├── hooks/
│   ├── context/
│   ├── utils/
│   ├── constants/
│   ├── validations/
│   ├── routes/
│   ├── App.jsx
│   └── main.jsx
│
├── index.html
├── vite.config.js
└── package.json
```

## Backend Structure

```text
backend/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── dashboard.py
│   │   │   │   ├── products.py
│   │   │   │   ├── inventory.py
│   │   │   │   ├── warehouses.py
│   │   │   │   ├── purchases.py
│   │   │   │   ├── sales.py
│   │   │   │   ├── customers.py
│   │   │   │   ├── suppliers.py
│   │   │   │   ├── manufacturing.py
│   │   │   │   ├── batches.py
│   │   │   │   ├── accounting.py
│   │   │   │   ├── payments.py
│   │   │   │   ├── expenses.py
│   │   │   │   └── reports.py
│   │   │   └── router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── permissions.py
│   │   └── logging.py
│   │
│   ├── database/
│   │   ├── session.py
│   │   ├── base.py
│   │   └── init_db.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── dependencies/
│   ├── utils/
│   └── main.py
│
├── alembic/
├── tests/
├── requirements.txt
├── .env.example
└── run.py
```

Use separate model, schema, repository, service, and API layers. Do not put all business logic inside API routes.

---

# 5. Main Business Modules

## A. Dashboard

Develop a comprehensive business dashboard showing:

- Total inventory value.
- Total products.
- Total stock quantity.
- Today's sales.
- Today's purchases.
- Today's cash received.
- Today's credit sales.
- Outstanding customer balances.
- Outstanding supplier balances.
- Total expenses.
- Gross profit and net profit.
- Manufacturing production summary.
- Low-stock products.
- Out-of-stock products.
- Recent transactions.
- Daily, weekly, monthly, and yearly financial statistics.

Include interactive charts and date filters.

## B. Product Management

Create a complete product management module.

Features:

- Product name and unique SKU.
- Barcode and QR code support.
- Product category and subcategory.
- Brand and manufacturer.
- Product description.
- Purchase price.
- Wholesale price.
- Retail price.
- Minimum selling price.
- Current stock.
- Minimum stock level.
- Unit of measurement.
- Product image.
- Supplier association.
- Product status.
- Product history.

Support different product types, including motorcycle spare parts, meters, accessories, and general trading items.

## C. Inventory Management

Implement a complete inventory tracking system.

Features:

- Stock in.
- Stock out.
- Stock adjustments.
- Opening stock.
- Closing stock.
- Stock transfers between warehouses.
- Damaged stock.
- Returned stock.
- Reserved stock.
- Available stock.
- Stock valuation.
- Inventory movement history.
- Reorder level notifications.
- Low-stock alerts.
- Physical stock reconciliation.

Every inventory movement must have a transaction reference and an audit trail.

Never allow stock to change without recording the corresponding inventory transaction.

## D. Purchase Management

Manage all purchasing activities.

Features:

- Purchase orders.
- Supplier invoices.
- Purchase receiving.
- Partial receiving.
- Full receiving.
- Purchase returns.
- Purchase discounts.
- Additional purchase expenses.
- Purchase tax.
- Purchase payment status.
- Cash purchases.
- Credit purchases.
- Supplier-wise purchase history.

When a purchase is finalized, update inventory and the relevant accounting records automatically.

## E. Sales Management

Create a complete sales and billing module.

Features:

- Sales invoices.
- POS interface.
- Wholesale sales.
- Retail sales.
- Cash sales.
- Credit sales.
- Partial payments.
- Full payments.
- Customer discounts.
- Sales returns.
- Invoice cancellation.
- Customer-wise sales history.
- Product-wise sales history.
- Daily sales reports.
- Profit per invoice and product.

Support multiple payment methods, including cash, bank transfer, and other configurable payment channels.

## F. Customer Management

Maintain complete customer records.

Features:

- Customer profile.
- Contact information.
- Address.
- Opening balance.
- Credit limit.
- Total purchases.
- Total outstanding balance.
- Payment history.
- Customer ledger.
- Credit and debit transactions.
- Due dates.
- Payment reminders.
- Customer statements.

Each customer should have an automatically maintained account ledger.

## G. Supplier and Vendor Management

Maintain separate supplier and vendor records where required.

Features:

- Supplier profiles.
- Vendor profiles.
- Contact information.
- Opening balances.
- Purchase history.
- Payment history.
- Outstanding payable amounts.
- Supplier ledger.
- Credit purchases.
- Debit payments.
- Supplier returns.
- Due dates.
- Supplier statements.

## H. Accounting and Financial Management

This is one of the most important modules.

Implement a proper double-entry accounting system.

Required modules:

- Chart of Accounts.
- General Ledger.
- Cash Book.
- Bank Book.
- Journal Entries.
- Cash Receipts.
- Cash Payments.
- Customer Receivables.
- Supplier Payables.
- Accounts Receivable (AR).
- Accounts Payable (AP).
- Income and Expenses.
- Trial Balance.
- Profit and Loss Statement.
- Balance Sheet.
- Cash Flow Statement.
- Day Book.
- Opening Balances.
- Closing Balances.

Support:

1. Cash transactions.
2. Credit transactions.
3. Debit transactions.
4. Partial settlements.
5. Advance payments.
6. Outstanding balances.
7. Customer and supplier adjustments.

Every finalized financial transaction must generate balanced journal entries.

Do not treat credit sales as cash received. Do not treat unpaid purchases as cash payments.

## I. Manufacturing Management

Develop a dedicated manufacturing and production management module.

The business manufactures products in daily batches.

Features:

- Manufacturing orders.
- Production planning.
- Production schedules.
- Daily production entries.
- Batch creation.
- Batch numbers.
- Manufacturing date.
- Production quantity.
- Raw material consumption.
- Finished goods production.
- Production cost calculation.
- Labor costs.
- Manufacturing expenses.
- Production wastage.
- Rejected products.
- Quality control.
- Batch-wise inventory.
- Batch-wise profitability.

Every manufactured batch must have its own unique identification number.

Track:

- Product name.
- Batch number.
- Manufacturing date.
- Production date.
- Quantity manufactured.
- Raw materials consumed.
- Production cost.
- Remaining quantity.
- Quantity sold.
- Quantity returned.
- Quantity damaged.
- Batch status.

The system must allow production planning by date, including specific weekdays such as Friday and other scheduled production days.

Support configurable weekly and daily production schedules.

## J. Batch and Expiry Tracking

Implement batch-level inventory tracking.

Features:

- Batch-wise stock.
- Manufacturing date.
- Expiry date, where applicable.
- Batch purchase cost.
- Batch manufacturing cost.
- Batch selling price.
- Batch-wise sales history.
- Batch returns.
- Batch transfers.
- Batch availability.

Support FIFO and FEFO stock allocation where applicable.

Allow the business to select the appropriate batch when selling products.

The system must maintain complete traceability from manufacturing or purchasing through final sale.

## K. Expense Management

Create an expense tracking module.

Categories may include:

- Rent.
- Electricity.
- Salaries.
- Transportation.
- Fuel.
- Maintenance.
- Manufacturing expenses.
- Packaging.
- Miscellaneous expenses.

Support expense receipts, dates, payment methods, categories, and accounting entries.

## L. Cash and Bank Management

Implement:

- Multiple cash accounts.
- Multiple bank accounts.
- Cash deposits.
- Cash withdrawals.
- Bank transfers.
- Cash opening balances.
- Daily cash closing.
- Cash reconciliation.
- Bank reconciliation.
- Cash transaction history.
- Cash-in-hand reporting.

## M. Returns and Adjustments

Support:

- Customer sales returns.
- Supplier purchase returns.
- Damaged goods.
- Stock corrections.
- Credit notes.
- Debit notes.
- Refunds.
- Account adjustments.

Every return must correctly update inventory and accounting records.

---

# 6. Reports and Analytics

Create a dedicated reporting center.

Required reports:

### Inventory Reports
- Current stock report.
- Stock movement report.
- Stock valuation.
- Low-stock report.
- Out-of-stock report.
- Batch-wise stock.
- Warehouse-wise stock.
- Damaged stock report.

### Sales Reports
- Daily sales.
- Weekly sales.
- Monthly sales.
- Annual sales.
- Customer-wise sales.
- Product-wise sales.
- Profit margin report.
- Credit sales report.
- Cash sales report.

### Purchase Reports
- Supplier-wise purchases.
- Product-wise purchases.
- Purchase returns.
- Outstanding purchases.
- Purchase history.

### Accounting Reports
- Customer ledger.
- Supplier ledger.
- General ledger.
- Cash book.
- Bank book.
- Trial balance.
- Profit and loss.
- Balance sheet.
- Cash flow.
- Receivables aging.
- Payables aging.

### Manufacturing Reports
- Daily production.
- Batch-wise production.
- Manufacturing cost.
- Raw material consumption.
- Production wastage.
- Finished goods.
- Batch profitability.

Allow filtering by date range, product, customer, supplier, category, and warehouse.

Provide PDF and Excel export functionality.

---

# 7. User Authentication and Permissions

Implement secure authentication and role-based access control.

Suggested roles:

- Super Admin.
- Business Owner.
- Manager.
- Accountant.
- Inventory Manager.
- Sales Operator.
- Purchase Operator.
- Production Manager.
- Read-only User.

Permissions should be configurable by module and action.

For example:

- View.
- Create.
- Edit.
- Delete.
- Approve.
- Export.
- Manage Financial Records.

Implement an audit log for sensitive operations.

---

# 8. UI/UX Requirements

The frontend must look like a modern, professional commercial ERP dashboard.

Design requirements:

- Clean and professional interface.
- Responsive layout.
- Sidebar navigation.
- Top navigation bar.
- Dashboard cards.
- Interactive charts.
- Advanced searchable tables.
- Pagination.
- Date range filters.
- Dropdown filters.
- Professional forms.
- Confirmation dialogs.
- Loading states.
- Error handling.
- Toast notifications.
- Dark and light mode.

Use a consistent design system with reusable components.

Prioritize usability and data visibility. The application must be easy for accountants, shop operators, inventory managers, and business owners to operate.

---

# 9. Database Architecture and Integrity

Use PostgreSQL with properly normalized relational database tables.

Create appropriate relationships, indexes, foreign keys, constraints, and transaction boundaries.

Important entities should include:

- Users
- Roles
- Permissions
- Products
- Categories
- Brands
- Warehouses
- Inventory Transactions
- Stock Balances
- Batches
- Manufacturing Orders
- Production Records
- Raw Materials
- Bills of Materials
- Customers
- Suppliers
- Vendors
- Purchase Orders
- Purchase Items
- Sales Invoices
- Sales Items
- Payments
- Expenses
- Accounts
- Journal Entries
- Journal Entry Lines
- Customer Ledgers
- Supplier Ledgers
- Returns
- Audit Logs

Use database transactions for operations that update multiple related records.

Prevent duplicate invoices, invalid stock movements, unbalanced journal entries, and inconsistent account balances.

Maintain historical transaction records rather than permanently deleting finalized financial or inventory transactions.

---

# 10. Critical Business Rules

The following rules must be followed:

1. Every purchase and sale must be traceable.
2. Every finalized stock movement must update inventory.
3. Every credit transaction must update the relevant outstanding balance.
4. Every cash transaction must update the relevant cash account.
5. Partial payments must be supported.
6. Every financial transaction must maintain double-entry accounting integrity.
7. Manufacturing must create batch-wise finished goods.
8. Raw material consumption must reduce raw material inventory.
9. Finished goods production must increase finished goods inventory.
10. Sales must reduce the correct product and batch stock.
11. Returns must reverse the appropriate inventory and financial effects.
12. Every important operation must have an audit trail.
13. Use decimal-based financial calculations, never floating-point arithmetic for money.
14. Prevent negative stock unless explicitly enabled by an authorized administrator.
15. Historical reports must remain accurate even when product prices change.

---

# 11. Development Workflow

Do not attempt to build the entire system in one step.

Follow a phased development approach.

### Phase 1: Foundation
- Project initialization.
- Frontend and backend setup.
- PostgreSQL connection.
- Database configuration.
- Authentication.
- Dashboard layout.
- Initial database migrations.

### Phase 2: Master Data
- Products.
- Categories.
- Units.
- Brands.
- Customers.
- Suppliers.
- Vendors.
- Warehouses.

### Phase 3: Inventory
- Stock opening.
- Stock in/out.
- Inventory movements.
- Stock transfers.
- Stock valuation.
- Low-stock alerts.

### Phase 4: Purchases and Sales
- Purchase orders.
- Receiving.
- Sales invoices.
- POS.
- Cash and credit transactions.
- Returns.

### Phase 5: Accounting
- Chart of accounts.
- Double-entry accounting.
- Customer and supplier ledgers.
- Payments.
- Expenses.
- Financial statements.

### Phase 6: Manufacturing
- Production planning.
- Raw materials.
- BOM.
- Manufacturing orders.
- Batch management.
- Production costing.
- Quality control.

### Phase 7: Reports and Analytics
- Business dashboard.
- Inventory reports.
- Financial reports.
- Manufacturing reports.
- PDF and Excel exports.

### Phase 8: Testing and Optimization
- Unit testing.
- API testing.
- Integration testing.
- Database integrity testing.
- Performance optimization.
- Security checks.
- Deployment preparation.

---

# 12. Instructions for the AI Development Agent

Follow these instructions strictly:

1. First, inspect the requirements and propose the complete system architecture.
2. Execute the frontend and backend setup commands.
3. Create the professional folder structure.
4. Explain the purpose of each major folder and layer.
5. Design the database schema before implementing business modules.
6. Establish relationships between inventory, accounting, sales, purchases, and manufacturing.
7. Implement reusable services and components.
8. Use proper validation and error handling.
9. Document every API endpoint.
10. Use Swagger/OpenAPI through FastAPI.
11. Write tests for critical business operations.
12. Do not create fake or disconnected functionality.
13. Do not hardcode business data.
14. Do not put all logic into a single file.
15. Do not skip database migrations.
16. Maintain clean, readable, maintainable, production-oriented code.

For every phase:

- Explain what will be developed.
- Identify the database tables involved.
- Identify the APIs required.
- Implement the backend.
- Implement the frontend.
- Connect both sides.
- Test the functionality.
- Document the completed work.

Do not move to the next phase until the current phase is implemented and tested.

## Final Objective

Build a complete, reliable, professional, and scalable ERP system that can manage the entire business from one centralized platform.

The system should provide complete visibility into:

- What products are available?
- How much stock is available?
- What was purchased?
- What was sold?
- How much cash was received?
- How much money is outstanding?
- How much is owed to suppliers?
- What was manufactured today?
- Which batches were produced?
- What is the manufacturing cost?
- What is the actual profit?
- What are the total assets, liabilities, income, and expenses?

The final product should be suitable for real-world business operations, with accurate accounting, inventory tracking, manufacturing traceability, and comprehensive reporting.