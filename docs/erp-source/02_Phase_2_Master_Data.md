# Phase 2 — Master Data

## Goal

Create the reliable shared records required by inventory, purchasing, sales, manufacturing and accounting.

## Prerequisites

Phase 1 passes its exit criteria. Shared forms, tables, authorization and migrations are available. Decide the base unit and quantity precision rules before stock is introduced.

## Functional scope

### Product catalog

Support unique SKU, name, barcode/QR identifiers, category and subcategory, brand/manufacturer, description, purchase reference price, wholesale/retail price, minimum selling price, minimum stock, image, supplier associations and active/inactive status.

Products may represent motorcycle spare parts, electrical meters, accessories, general trading goods, raw materials and finished goods. Model commercial classification separately from inventory/manufacturing behavior where useful.

Current stock is calculated from inventory records in Phase 3. Product editing must never directly overwrite it. Product history includes material master-data changes and links to later business transactions.

### Units and locations

Support units, product-specific conversions, categories with parent-child relationships, brands/manufacturers and warehouses. Document whether fractional quantities are allowed for each unit.

### Customers, suppliers and vendors

Support profiles, contacts, addresses, credit limits where relevant, due-date/payment-term configuration and opening-balance input staged for controlled accounting posting. One party may have both customer and supplier roles without duplicating its identity unnecessarily.

Opening receivable/payable balances must remain drafts until the accounting posting service validates and posts them. Final historical totals are derived from transactions.

## Database tables

| Tables | Responsibility |
| --- | --- |
| units, product_unit_conversions | Base units, allowed quantities and conversions |
| categories, brands, manufacturers | Classification |
| products, product_images, product_suppliers | Catalog and vendor associations |
| parties, party_roles, party_contacts, party_addresses | Shared customer/supplier/vendor identity |
| customer_profiles, supplier_profiles, vendor_profiles | Role-specific terms and limits |
| warehouses | Stock locations |
| opening_balance_drafts | Controlled party opening balance preparation |

A normalized shared party model is a proposed implementation choice. Separate customer/supplier tables are also acceptable if shared identities and reconciliation remain explicit.

Enforce business-scoped SKU uniqueness, valid prices, positive conversion factors and unique configured identifiers. Block category cycles. Archive referenced master records rather than deleting transaction history.

## Proposed APIs

| Method | Route | Behavior |
| --- | --- | --- |
| GET/POST | /products | Search/filter products or create |
| GET/PATCH | /products/{id} | Product details and authorized edits |
| POST | /products/{id}/archive | Deactivate with audit |
| GET | /products/{id}/history | Product change and transaction history |
| POST/DELETE | /products/{id}/images and /products/{id}/images/{image_id} | Manage images |
| GET/POST/PATCH | /categories, /brands, /units, /manufacturers | Maintain catalog lookups |
| GET/POST/PATCH | /warehouses and /warehouses/{id} | Maintain warehouses |
| GET/POST/PATCH | /customers, /suppliers, /vendors | Maintain party roles and profiles |
| GET | /parties/{id}/summary | Available activity totals with clear initial state |
| POST | /parties/{id}/opening-balance-drafts | Prepare opening balance for controlled posting |
| GET | /products/{id}/barcode | Produce printable barcode/QR representation |

Define item routes for updates consistently rather than updating an entire collection.

## Backend work

Implement validated models, schemas, repositories and services. Restrict image types and size, store images through a configurable storage abstraction, and prevent user-supplied file paths from controlling storage locations.

Prevent deletion of referenced units, warehouses and parties. Do not allow base-unit conversion changes to reinterpret historical quantities. Return paginated search results and server-derived totals.

## Frontend work

Build searchable product and party tables, detail pages, create/edit forms, image previews, archive confirmation and status filters. Include product unit conversions and supplier associations.

Show customer credit limits and configured terms clearly. Mark opening balances as pending until posted. Display barcode/QR previews and print support. Use consistent server and client validation with useful field-level errors.

## Acceptance checks

- Duplicate SKU or configured unique barcode is rejected, including concurrent requests.
- Invalid prices, zero/negative conversion factors and circular categories fail.
- A party can hold customer and supplier roles while balances stay separate.
- Referenced records are archived or blocked from deletion safely.
- Image validation and permission checks work.
- Searching, filtering and pagination use real backend data.
- Product stock cannot be changed through a catalog update.
- Opening-balance drafts do not silently change financial statements.
- Permission-denied actions fail through direct API requests.

## Deliverables and exit criteria

Deliver connected master-data screens, migrations, documented APIs and a documented unit/party model. Exit when validated catalog, party and warehouse records are available to downstream modules without manual database editing.
