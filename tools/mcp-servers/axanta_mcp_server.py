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

ODOO_URL = os.environ.get("AXANTA_URL", "")
ODOO_DB = os.environ.get("AXANTA_DB", "")
ODOO_USER = os.environ.get("AXANTA_USER", "")
ODOO_KEY = os.environ.get("AXANTA_KEY", "")

_uid = None
_common = None
_models = None


def _connect():
    global _uid, _common, _models
    if _uid is not None:
        return
    if not all([ODOO_URL, ODOO_DB, ODOO_USER, ODOO_KEY]):
        raise RuntimeError(
            "Missing env vars. Set AXANTA_URL, AXANTA_DB, AXANTA_USER, AXANTA_KEY"
        )
    _common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    _models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    _uid = _common.authenticate(ODOO_DB, ODOO_USER, ODOO_KEY, {})
    if not _uid:
        raise RuntimeError("Authentication failed — check credentials")


def q(model, method, args=None, kw=None):
    _connect()
    return _models.execute_kw(
        ODOO_DB, _uid, ODOO_KEY, model, method, args or [], kw or {}
    )


app = Server("axanta-erp")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_models",
            description="List available Odoo models (database tables). Use to discover what data is available.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Filter model names (e.g. 'sale', 'stock', 'account')",
                        "default": "",
                    },
                },
            },
        ),
        types.Tool(
            name="get_model_fields",
            description="Get field definitions for an Odoo model. Use to understand what data a model contains before querying.",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string", "description": "Model name (e.g. sale.order)"},
                },
                "required": ["model"],
            },
        ),
        types.Tool(
            name="search_records",
            description="Search any Odoo model with filters. Common models: sale.order, purchase.order, account.move, stock.picking, res.partner, product.product, product.template, stock.quant, hr.employee, account.payment, pos.order",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string"},
                    "domain": {
                        "type": "array",
                        "description": "Odoo domain filter, e.g. [['state','=','sale']]",
                        "default": [],
                    },
                    "fields": {"type": "array", "default": ["id", "name"]},
                    "limit": {"type": "integer", "default": 20},
                    "offset": {"type": "integer", "default": 0},
                    "order": {"type": "string", "default": "id desc"},
                },
                "required": ["model"],
            },
        ),
        types.Tool(
            name="count_records",
            description="Count records matching a domain filter",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string"},
                    "domain": {"type": "array", "default": []},
                },
                "required": ["model"],
            },
        ),
        types.Tool(
            name="get_record",
            description="Get full details of one or more records by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string"},
                    "ids": {
                        "oneOf": [
                            {"type": "integer"},
                            {"type": "array", "items": {"type": "integer"}},
                        ],
                        "description": "Single ID or list of IDs",
                    },
                    "fields": {"type": "array", "default": []},
                },
                "required": ["model", "ids"],
            },
        ),
        types.Tool(
            name="get_sales_summary",
            description="Get sales orders summary — totals, statuses, top customers",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "draft/sent/sale/done/cancel or 'all'",
                        "default": "sale",
                    },
                    "limit": {"type": "integer", "default": 50},
                },
            },
        ),
        types.Tool(
            name="get_inventory",
            description="Get product stock levels and availability",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "default": ""},
                    "low_stock_only": {"type": "boolean", "default": False},
                    "limit": {"type": "integer", "default": 50},
                },
            },
        ),
        types.Tool(
            name="get_customers",
            description="Search and list customers with contact info",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "default": ""},
                    "limit": {"type": "integer", "default": 20},
                },
            },
        ),
        types.Tool(
            name="get_invoices",
            description="Get customer invoices with amounts and status",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "draft/posted/cancel",
                        "default": "posted",
                    },
                    "limit": {"type": "integer", "default": 20},
                },
            },
        ),
        types.Tool(
            name="get_purchase_orders",
            description="Get purchase orders from vendors",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "draft/purchase/done/cancel",
                        "default": "purchase",
                    },
                    "limit": {"type": "integer", "default": 20},
                },
            },
        ),
        types.Tool(
            name="get_employees",
            description="List employees and their details",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "default": ""},
                    "limit": {"type": "integer", "default": 30},
                },
            },
        ),
        types.Tool(
            name="get_stock_movements",
            description="Get inventory transfers/movements (deliveries, receipts)",
            inputSchema={
                "type": "object",
                "properties": {
                    "picking_type": {
                        "type": "string",
                        "description": "outgoing/incoming/internal",
                        "default": "outgoing",
                    },
                    "limit": {"type": "integer", "default": 20},
                },
            },
        ),
        types.Tool(
            name="get_pos_orders",
            description="Get POS (point of sale) orders and session data",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "draft/paid/done/invoiced/cancel or 'all'",
                        "default": "all",
                    },
                    "limit": {"type": "integer", "default": 30},
                },
            },
        ),
        types.Tool(
            name="get_accounting_summary",
            description="Get journal entries, account balances, or payment summary",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "payments/journal_entries/vendor_bills",
                        "default": "payments",
                    },
                    "state": {"type": "string", "default": "posted"},
                    "limit": {"type": "integer", "default": 20},
                },
            },
        ),
        types.Tool(
            name="create_record",
            description="Create a new record (e.g. customer, product, sale order)",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string"},
                    "values": {"type": "object"},
                },
                "required": ["model", "values"],
            },
        ),
        types.Tool(
            name="update_record",
            description="Update fields of an existing record",
            inputSchema={
                "type": "object",
                "properties": {
                    "model": {"type": "string"},
                    "id": {"type": "integer"},
                    "values": {"type": "object"},
                },
                "required": ["model", "id", "values"],
            },
        ),
        types.Tool(
            name="get_report_data",
            description="Get aggregated report data — sales by branch, product, period",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_type": {
                        "type": "string",
                        "description": "sales_by_branch/sales_by_product/top_customers",
                    },
                    "limit": {"type": "integer", "default": 20},
                },
                "required": ["report_type"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        result = _dispatch(name, arguments)
        return [
            types.TextContent(
                type="text", text=json.dumps(result, indent=2, default=str)
            )
        ]
    except Exception as e:
        return [
            types.TextContent(
                type="text", text=json.dumps({"error": str(e), "tool": name})
            )
        ]


def _dispatch(name: str, arguments: dict):
    if name == "list_models":
        search = arguments.get("search", "")
        domain = [["model", "ilike", search]] if search else []
        models_list = q(
            "ir.model",
            "search_read",
            [domain],
            {
                "fields": ["model", "name"],
                "limit": 100,
                "order": "model asc",
            },
        )
        return [{"model": m["model"], "label": m["name"]} for m in models_list]

    if name == "get_model_fields":
        fields = q(arguments["model"], "fields_get", [], {"attributes": ["string", "type", "required", "relation"]})
        return {
            k: {
                "label": v.get("string", ""),
                "type": v.get("type", ""),
                "required": v.get("required", False),
                "relation": v.get("relation", ""),
            }
            for k, v in fields.items()
        }

    if name == "search_records":
        return q(
            arguments["model"],
            "search_read",
            [arguments.get("domain", [])],
            {
                "fields": arguments.get("fields", ["id", "name"]),
                "limit": arguments.get("limit", 20),
                "offset": arguments.get("offset", 0),
                "order": arguments.get("order", "id desc"),
            },
        )

    if name == "count_records":
        return {"model": arguments["model"], "count": q(arguments["model"], "search_count", [arguments.get("domain", [])])}

    if name == "get_record":
        ids = arguments["ids"]
        if isinstance(ids, int):
            ids = [ids]
        return q(
            arguments["model"],
            "read",
            [ids],
            {"fields": arguments.get("fields", [])},
        )

    if name == "get_sales_summary":
        state = arguments.get("state", "sale")
        domain = [] if state == "all" else [["state", "=", state]]
        orders = q(
            "sale.order",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "partner_id", "amount_total", "state",
                    "date_order", "user_id", "team_id",
                ],
                "limit": arguments.get("limit", 50),
                "order": "date_order desc",
            },
        )
        total = sum(o["amount_total"] for o in orders)
        return {
            "orders": orders,
            "count": len(orders),
            "total_amount": round(total, 2),
        }

    if name == "get_inventory":
        domain = [["type", "in", ["product", "consu"]]]
        if arguments.get("product_name"):
            domain.append(["name", "ilike", arguments["product_name"]])
        if arguments.get("low_stock_only"):
            domain.append(["qty_available", "<", 10])
        return q(
            "product.product",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "default_code", "qty_available",
                    "virtual_available", "list_price", "categ_id",
                ],
                "limit": arguments.get("limit", 50),
                "order": "qty_available asc",
            },
        )

    if name == "get_customers":
        domain = [["customer_rank", ">", 0]]
        if arguments.get("name"):
            domain.append(["name", "ilike", arguments["name"]])
        return q(
            "res.partner",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "email", "phone", "city",
                    "customer_rank", "total_invoiced",
                ],
                "limit": arguments.get("limit", 20),
            },
        )

    if name == "get_invoices":
        domain = [
            ["move_type", "=", "out_invoice"],
            ["state", "=", arguments.get("state", "posted")],
        ]
        return q(
            "account.move",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "partner_id", "amount_total",
                    "amount_residual", "state", "invoice_date",
                    "invoice_date_due",
                ],
                "limit": arguments.get("limit", 20),
                "order": "invoice_date desc",
            },
        )

    if name == "get_purchase_orders":
        domain = [["state", "=", arguments.get("state", "purchase")]]
        return q(
            "purchase.order",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "partner_id", "amount_total", "state",
                    "date_order", "date_planned",
                ],
                "limit": arguments.get("limit", 20),
                "order": "date_order desc",
            },
        )

    if name == "get_employees":
        domain = [["active", "=", True]]
        if arguments.get("name"):
            domain.append(["name", "ilike", arguments["name"]])
        return q(
            "hr.employee",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "job_title", "department_id",
                    "work_email", "work_phone",
                ],
                "limit": arguments.get("limit", 30),
            },
        )

    if name == "get_stock_movements":
        ptype = arguments.get("picking_type", "outgoing")
        domain = [
            ["picking_type_code", "=", ptype],
            ["state", "in", ["done", "assigned"]],
        ]
        return q(
            "stock.picking",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "partner_id", "state",
                    "scheduled_date", "date_done",
                    "picking_type_id", "origin",
                ],
                "limit": arguments.get("limit", 20),
                "order": "date_done desc",
            },
        )

    if name == "get_pos_orders":
        state = arguments.get("state", "all")
        domain = [] if state == "all" else [["state", "=", state]]
        orders = q(
            "pos.order",
            "search_read",
            [domain],
            {
                "fields": [
                    "name", "partner_id", "amount_total", "amount_paid",
                    "state", "date_order", "pos_reference",
                    "session_id", "employee_id",
                ],
                "limit": arguments.get("limit", 30),
                "order": "date_order desc",
            },
        )
        total = sum(o["amount_total"] for o in orders)
        return {
            "orders": orders,
            "count": len(orders),
            "total_amount": round(total, 2),
        }

    if name == "get_accounting_summary":
        atype = arguments.get("type", "payments")
        state = arguments.get("state", "posted")
        limit = arguments.get("limit", 20)

        if atype == "payments":
            return q(
                "account.payment",
                "search_read",
                [[["state", "=", state]]],
                {
                    "fields": [
                        "name", "partner_id", "amount", "payment_type",
                        "date", "journal_id", "state",
                    ],
                    "limit": limit,
                    "order": "date desc",
                },
            )
        elif atype == "journal_entries":
            return q(
                "account.move",
                "search_read",
                [[["state", "=", state]]],
                {
                    "fields": [
                        "name", "date", "journal_id", "amount_total",
                        "state", "move_type", "ref",
                    ],
                    "limit": limit,
                    "order": "date desc",
                },
            )
        elif atype == "vendor_bills":
            return q(
                "account.move",
                "search_read",
                [[["move_type", "=", "in_invoice"], ["state", "=", state]]],
                {
                    "fields": [
                        "name", "partner_id", "amount_total",
                        "amount_residual", "state", "invoice_date",
                        "invoice_date_due",
                    ],
                    "limit": limit,
                    "order": "invoice_date desc",
                },
            )
        return {"error": f"Unknown accounting type: {atype}"}

    if name == "create_record":
        new_id = q(arguments["model"], "create", [arguments["values"]])
        return {
            "success": True,
            "id": new_id,
            "message": f"Created {arguments['model']} with ID {new_id}",
        }

    if name == "update_record":
        q(arguments["model"], "write", [[arguments["id"]], arguments["values"]])
        return {
            "success": True,
            "message": f"Updated {arguments['model']} ID {arguments['id']}",
        }

    if name == "get_report_data":
        return _report(arguments)

    return {"error": f"Unknown tool: {name}"}


def _report(arguments: dict):
    rtype = arguments["report_type"]
    limit = arguments.get("limit", 20)

    if rtype == "sales_by_branch":
        orders = q(
            "sale.order",
            "search_read",
            [[["state", "in", ["sale", "done"]]]],
            {"fields": ["name", "team_id", "amount_total"], "limit": 500},
        )
        branches: dict[str, float] = {}
        for o in orders:
            b = o["team_id"][1] if o["team_id"] else "Unknown"
            branches[b] = branches.get(b, 0) + o["amount_total"]
        return {
            "by_branch": sorted(
                branches.items(), key=lambda x: x[1], reverse=True
            )[:limit]
        }

    if rtype == "top_customers":
        return {
            "top_customers": q(
                "res.partner",
                "search_read",
                [[["customer_rank", ">", 0]]],
                {
                    "fields": ["name", "total_invoiced"],
                    "limit": limit,
                    "order": "total_invoiced desc",
                },
            )
        }

    if rtype == "sales_by_product":
        lines = q(
            "sale.order.line",
            "search_read",
            [[["order_id.state", "in", ["sale", "done"]]]],
            {
                "fields": ["product_id", "product_uom_qty", "price_subtotal"],
                "limit": 1000,
            },
        )
        products: dict[str, dict] = {}
        for ln in lines:
            p = ln["product_id"][1] if ln["product_id"] else "Unknown"
            if p not in products:
                products[p] = {"qty": 0, "revenue": 0}
            products[p]["qty"] += ln["product_uom_qty"]
            products[p]["revenue"] += ln["price_subtotal"]
        return {
            "by_product": sorted(
                products.items(), key=lambda x: x[1]["revenue"], reverse=True
            )[:limit]
        }

    return {"error": f"Unknown report type: {rtype}"}


async def main():
    async with mcp.server.stdio.stdio_server() as (r, w):
        await app.run(r, w, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
