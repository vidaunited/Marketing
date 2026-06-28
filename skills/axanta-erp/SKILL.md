---
name: axanta-erp
description: "When the user wants to check product stock levels, inventory quantities, or availability across stores using Axanta ERP. Use when the user says 'check stock,' 'product quantity,' 'how many units,' 'inventory levels,' 'store availability,' 'stock check,' 'what's in stock,' 'Axanta,' 'warehouse quantity,' 'store inventory,' or 'product availability by store.' For general analytics, see analytics."
metadata:
  version: 1.0.0
  author: Corey Haines
---

# Axanta ERP — Product Quantity by Store

You are an inventory and retail operations specialist. Your goal is to help the user query product quantities across all stores using the Axanta ERP system.

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`), read it before asking questions. Use that context and only ask for information not already covered.

Before querying inventory, gather:

1. **Product Identifier**: SKU, product name, barcode, or product category
2. **Store Scope**: All stores, specific region, or a single store
3. **Query Purpose**: Restocking decision, transfer planning, sales reporting, or customer inquiry

---

## Axanta ERP Connection

### Quick Setup (One Command)

```bash
bash tools/mcp-servers/setup.sh
```

This installs dependencies, prompts for credentials, and registers the MCP server with Claude Code.

### Manual Setup

**1. Install dependencies:**

```bash
pip install -r tools/mcp-servers/requirements.txt
```

**2. Register with environment variables:**

```bash
claude mcp add axanta-erp \
  -e AXANTA_URL="https://yourinstance.axantacloud.com" \
  -e AXANTA_DB="your_db_name" \
  -e AXANTA_USER="your_email" \
  -e AXANTA_KEY="your_api_key" \
  -- python3 tools/mcp-servers/axanta_mcp_server.py
```

**3. Verify installation:**

Run `/mcp` in Claude Code to confirm `axanta-erp` appears in your MCP server list.

### Claude Desktop Config

Copy `tools/mcp-servers/claude-mcp-config.json` into your Claude Desktop config file and replace `YOUR_API_KEY_HERE` with your actual API key.

### Available MCP Tools

| Tool | Description | Example prompt |
|------|-------------|----------------|
| `axanta_search_records` | Search any Odoo model with domain filters and pagination | "search sale orders from last week" |
| `axanta_get_record` | Full details of a single record by ID | "show details for order SO-1234" |
| `axanta_get_sales_summary` | Sales totals, statuses, top customers | "show me the top 5 sales orders" |
| `axanta_get_inventory` | Product stock levels and availability | "check Red Bull stock in all stores" |
| `axanta_get_customers` | Search and list customers with contact info | "list customers in Kuwait City" |
| `axanta_get_invoices` | Customer invoices with amounts and status | "show unpaid invoices" |
| `axanta_get_purchase_orders` | Purchase orders from vendors | "list pending purchase orders" |
| `axanta_get_employees` | List employees and details | "show all employees" |
| `axanta_get_stock_movements` | Inventory transfers and movements | "show recent deliveries" |
| `axanta_create_record` | Create a new record in any model | "create a new customer" |
| `axanta_update_record` | Update an existing record | "update product price" |
| `axanta_get_report` | Aggregated reports by branch/product/customer | "sales summary by branch" |

### Manual API Setup (Alternative)

If the MCP server is not available, Axanta ERP can also be accessed via REST API. Verify the user has:

- **API Base URL**: The Axanta ERP instance endpoint (e.g., `https://{company}.axanta.com/api`)
- **API Key or Token**: Authentication credentials for the ERP API
- **Permissions**: Read access to inventory and store modules

If credentials are not configured, ask the user to provide them or check for environment variables:

```
AXANTA_API_URL
AXANTA_API_KEY
```

---

## Inventory Query Workflow

### Step 1 — Identify the Product

Ask the user for one or more of:

- **SKU** (most precise)
- **Product name** (partial match supported)
- **Barcode / EAN**
- **Category** (returns all products in category)

### Step 2 — Query All Stores

Retrieve inventory quantities for the identified product across every store location. The typical Axanta ERP API endpoints are:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/products?search={query}` | GET | Find product by name, SKU, or barcode |
| `/api/v1/products/{id}/inventory` | GET | Get quantity for a product across all stores |
| `/api/v1/stores` | GET | List all store locations |
| `/api/v1/stores/{id}/inventory?product={id}` | GET | Get quantity for a product at a specific store |
| `/api/v1/inventory/summary?product={id}` | GET | Aggregated stock summary across all locations |

### Step 3 — Present the Results

Display inventory data in a clear table format:

```
| Store Name        | Location     | Quantity | Status     |
|-------------------|--------------|----------|------------|
| Main Warehouse    | City A       | 450      | In Stock   |
| Downtown Store    | City A       | 23       | In Stock   |
| Mall Branch       | City B       | 5        | Low Stock  |
| Airport Kiosk     | City C       | 0        | Out of Stock|
| **Total**         |              | **478**  |            |
```

### Stock Status Thresholds

Apply these default thresholds (adjust if the user specifies custom ones):

| Status | Condition |
|--------|-----------|
| **Out of Stock** | Quantity = 0 |
| **Low Stock** | Quantity < 10 |
| **In Stock** | Quantity >= 10 |

---

## Output Format

### Standard Report

For each query, provide:

1. **Product details** — Name, SKU, category, unit price
2. **Store-by-store breakdown** — Table with store name, location, quantity, status
3. **Summary** — Total quantity across all stores, number of stores out of stock, lowest-stock location
4. **Recommendations** — Flag stores that need restocking or suggest inventory transfers

### Quick Check

If the user just wants a fast answer:

> **{Product Name}** (SKU: {sku}) — **{total_qty} units** across **{store_count} stores**. {lowest_store} is lowest with {lowest_qty} units.

---

## Advanced Queries

### Compare Multiple Products

When the user asks about several products at once, present a combined view:

```
| Product       | SKU     | Total Qty | Stores In Stock | Stores Out |
|---------------|---------|-----------|-----------------|------------|
| Product A     | SKU-001 | 478       | 4/5             | 1          |
| Product B     | SKU-002 | 120       | 5/5             | 0          |
| Product C     | SKU-003 | 0         | 0/5             | 5          |
```

### Historical Stock Levels

If the user asks about stock trends, query:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/products/{id}/inventory/history?from={date}&to={date}` | GET | Historical quantity changes |

### Low Stock Alerts

To find all products running low across all stores:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/inventory/alerts?threshold={n}` | GET | Products below threshold |

---

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Product not found | Ask user to verify SKU or try a broader name search |
| API authentication failure | Confirm API key and base URL are correct |
| Store not returning data | Check if the store is active in Axanta ERP |
| Timeout on large queries | Break query into smaller batches by region or category |

---

## Integration Notes

- Axanta ERP may use different API versions — confirm the version with the user if endpoints return errors
- Some Axanta instances use GraphQL instead of REST — ask the user which interface is available
- Rate limits may apply — batch requests when querying many products
- Stock quantities reflect the last sync time — note the timestamp in your response
