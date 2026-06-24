#!/usr/bin/env python3
"""Axanta ERP MCP Server for Claude Code.

Connects to Axanta (Odoo) via XML-RPC. Exposes sales, inventory, customers,
invoices, purchases, employees, stock movements, and reports.

Setup:
    pip install mcp
    export AXANTA_URL="https://yourinstance.axantacloud.com"
    export AXANTA_DB="your_db_name"
    export AXANTA_USER="your_email"
    export AXANTA_KEY="your_api_key"
    claude mcp add axanta-erp -- python3 tools/mcp-servers/axanta_mcp_server.py
"""

import asyncio
import json
import os
import xmlrpc.client

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

ODOO_URL  = os.environ.get("AXANTA_URL", "")
ODOO_DB   = os.environ.get("AXANTA_DB", "")
ODOO_USER = os.environ.get("AXANTA_USER", "")
ODOO_KEY  = os.environ.get("AXANTA_KEY", "")

common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
uid    = common.authenticate(ODOO_DB, ODOO_USER, ODOO_KEY, {})


def q(model, method, args=None, kw=None):
    return models.execute_kw(ODOO_DB, uid, ODOO_KEY, model, method, args or [], kw or {})


app = Server("axanta-erp")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_records",
            description="Search any Odoo model with filters. Models: sale.order, purchase.order, account.move, stock.picking, res.partner, product.product, product.template, stock.quant, hr.employee, account.payment",
            inputSchema={"type": "object", "properties": {
                "model":  {"type": "string"},
                "domain": {"type": "array", "default": []},
                "fields": {"type": "array", "default": ["id", "name"]},
                "limit":  {"type": "integer", "default": 20},
                "order":  {"type": "string", "default": "id desc"},
            }, "required": ["model"]}),
        types.Tool(
            name="get_record",
            description="Get full details of a single record by ID",
            inputSchema={"type": "object", "properties": {
                "model":  {"type": "string"},
                "id":     {"type": "integer"},
                "fields": {"type": "array", "default": []},
            }, "required": ["model", "id"]}),
        types.Tool(
            name="get_sales_summary",
            description="Get sales orders summary — totals, statuses, top customers",
            inputSchema={"type": "object", "properties": {
                "state": {"type": "string", "description": "draft/sent/sale/done/cancel or 'all'", "default": "sale"},
                "limit": {"type": "integer", "default": 50},
            }}),
        types.Tool(
            name="get_inventory",
            description="Get product stock levels and availability",
            inputSchema={"type": "object", "properties": {
                "product_name":  {"type": "string", "default": ""},
                "low_stock_only": {"type": "boolean", "default": False},
                "limit":         {"type": "integer", "default": 50},
            }}),
        types.Tool(
            name="get_customers",
            description="Search and list customers with contact info",
            inputSchema={"type": "object", "properties": {
                "name":  {"type": "string", "default": ""},
                "limit": {"type": "integer", "default": 20},
            }}),
        types.Tool(
            name="get_invoices",
            description="Get customer invoices with amounts and status",
            inputSchema={"type": "object", "properties": {
                "state": {"type": "string", "description": "draft/posted/cancel", "default": "posted"},
                "limit": {"type": "integer", "default": 20},
            }}),
        types.Tool(
            name="get_purchase_orders",
            description="Get purchase orders from vendors",
            inputSchema={"type": "object", "properties": {
                "state": {"type": "string", "description": "draft/purchase/done/cancel", "default": "purchase"},
                "limit": {"type": "integer", "default": 20},
            }}),
        types.Tool(
            name="get_employees",
            description="List employees and their details",
            inputSchema={"type": "object", "properties": {
                "name":  {"type": "string", "default": ""},
                "limit": {"type": "integer", "default": 30},
            }}),
        types.Tool(
            name="get_stock_movements",
            description="Get inventory transfers/movements (deliveries, receipts)",
            inputSchema={"type": "object", "properties": {
                "picking_type": {"type": "string", "description": "outgoing/incoming/internal", "default": "outgoing"},
                "limit":        {"type": "integer", "default": 20},
            }}),
        types.Tool(
            name="create_record",
            description="Create a new record (e.g. customer, product, sale order)",
            inputSchema={"type": "object", "properties": {
                "model":  {"type": "string"},
                "values": {"type": "object"},
            }, "required": ["model", "values"]}),
        types.Tool(
            name="update_record",
            description="Update fields of an existing record",
            inputSchema={"type": "object", "properties": {
                "model":  {"type": "string"},
                "id":     {"type": "integer"},
                "values": {"type": "object"},
            }, "required": ["model", "id", "values"]}),
        types.Tool(
            name="get_report_data",
            description="Get aggregated report data — sales by branch, product, period",
            inputSchema={"type": "object", "properties": {
                "report_type": {"type": "string", "description": "sales_by_branch/sales_by_product/top_customers"},
                "limit":       {"type": "integer", "default": 20},
            }, "required": ["report_type"]}),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        result = {}

        if name == "search_records":
            result = q(arguments["model"], "search_read",
                       [arguments.get("domain", [])],
                       {"fields": arguments.get("fields", ["id", "name"]),
                        "limit":  arguments.get("limit", 20),
                        "order":  arguments.get("order", "id desc")})

        elif name == "get_record":
            result = q(arguments["model"], "read",
                       [[arguments["id"]]],
                       {"fields": arguments.get("fields", [])})

        elif name == "get_sales_summary":
            state = arguments.get("state", "sale")
            domain = [] if state == "all" else [["state", "=", state]]
            orders = q("sale.order", "search_read", [domain],
                       {"fields": ["name", "partner_id", "amount_total", "state",
                                   "date_order", "user_id", "team_id"],
                        "limit": arguments.get("limit", 50),
                        "order": "date_order desc"})
            total = sum(o["amount_total"] for o in orders)
            result = {"orders": orders, "count": len(orders),
                      "total_amount": round(total, 2), "currency": "KWD"}

        elif name == "get_inventory":
            domain = [["type", "in", ["product", "consu"]]]
            if arguments.get("product_name"):
                domain.append(["name", "ilike", arguments["product_name"]])
            if arguments.get("low_stock_only"):
                domain.append(["qty_available", "<", 10])
            result = q("product.product", "search_read", [domain],
                       {"fields": ["name", "default_code", "qty_available",
                                   "virtual_available", "list_price", "categ_id"],
                        "limit": arguments.get("limit", 50),
                        "order": "qty_available asc"})

        elif name == "get_customers":
            domain = [["customer_rank", ">", 0]]
            if arguments.get("name"):
                domain.append(["name", "ilike", arguments["name"]])
            result = q("res.partner", "search_read", [domain],
                       {"fields": ["name", "email", "phone", "city",
                                   "customer_rank", "total_invoiced"],
                        "limit": arguments.get("limit", 20)})

        elif name == "get_invoices":
            domain = [["move_type", "=", "out_invoice"],
                      ["state", "=", arguments.get("state", "posted")]]
            result = q("account.move", "search_read", [domain],
                       {"fields": ["name", "partner_id", "amount_total",
                                   "amount_residual", "state", "invoice_date",
                                   "invoice_date_due"],
                        "limit": arguments.get("limit", 20),
                        "order": "invoice_date desc"})

        elif name == "get_purchase_orders":
            domain = [["state", "=", arguments.get("state", "purchase")]]
            result = q("purchase.order", "search_read", [domain],
                       {"fields": ["name", "partner_id", "amount_total", "state",
                                   "date_order", "date_planned"],
                        "limit": arguments.get("limit", 20),
                        "order": "date_order desc"})

        elif name == "get_employees":
            domain = [["active", "=", True]]
            if arguments.get("name"):
                domain.append(["name", "ilike", arguments["name"]])
            result = q("hr.employee", "search_read", [domain],
                       {"fields": ["name", "job_title", "department_id",
                                   "work_email", "work_phone"],
                        "limit": arguments.get("limit", 30)})

        elif name == "get_stock_movements":
            ptype = arguments.get("picking_type", "outgoing")
            domain = [["picking_type_code", "=", ptype],
                      ["state", "in", ["done", "assigned"]]]
            result = q("stock.picking", "search_read", [domain],
                       {"fields": ["name", "partner_id", "state",
                                   "scheduled_date", "date_done",
                                   "picking_type_id", "origin"],
                        "limit": arguments.get("limit", 20),
                        "order": "date_done desc"})

        elif name == "create_record":
            new_id = q(arguments["model"], "create", [arguments["values"]])
            result = {"success": True, "id": new_id,
                      "message": f"Created {arguments['model']} with ID {new_id}"}

        elif name == "update_record":
            q(arguments["model"], "write",
              [[arguments["id"]], arguments["values"]])
            result = {"success": True,
                      "message": f"Updated {arguments['model']} ID {arguments['id']}"}

        elif name == "get_report_data":
            rtype = arguments["report_type"]
            limit = arguments.get("limit", 20)
            if rtype == "sales_by_branch":
                orders = q("sale.order", "search_read",
                           [[["state", "in", ["sale", "done"]]]],
                           {"fields": ["name", "team_id", "amount_total"],
                            "limit": 500})
                branches: dict[str, float] = {}
                for o in orders:
                    b = o["team_id"][1] if o["team_id"] else "Unknown"
                    branches[b] = branches.get(b, 0) + o["amount_total"]
                result = {"by_branch": sorted(branches.items(),
                          key=lambda x: x[1], reverse=True)[:limit]}
            elif rtype == "top_customers":
                result = {"top_customers": q("res.partner", "search_read",
                          [[["customer_rank", ">", 0]]],
                          {"fields": ["name", "total_invoiced"],
                           "limit": limit, "order": "total_invoiced desc"})}
            elif rtype == "sales_by_product":
                lines = q("sale.order.line", "search_read",
                          [[["order_id.state", "in", ["sale", "done"]]]],
                          {"fields": ["product_id", "product_uom_qty",
                                      "price_subtotal"], "limit": 1000})
                products: dict[str, dict] = {}
                for ln in lines:
                    p = ln["product_id"][1] if ln["product_id"] else "Unknown"
                    if p not in products:
                        products[p] = {"qty": 0, "revenue": 0}
                    products[p]["qty"] += ln["product_uom_qty"]
                    products[p]["revenue"] += ln["price_subtotal"]
                result = {"by_product": sorted(products.items(),
                          key=lambda x: x[1]["revenue"], reverse=True)[:limit]}

        return [types.TextContent(type="text",
                text=json.dumps(result, indent=2, default=str))]

    except Exception as e:
        return [types.TextContent(type="text",
                text=json.dumps({"error": str(e), "tool": name}))]


async def main():
    async with mcp.server.stdio.stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
