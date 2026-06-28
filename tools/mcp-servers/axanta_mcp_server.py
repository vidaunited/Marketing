#!/usr/bin/env python3
"""Axanta ERP MCP Server for Claude Code.

Connects to Axanta (Odoo) via XML-RPC using FastMCP. Exposes sales, inventory,
customers, invoices, purchases, employees, stock movements, and reports.

Setup:
    pip install "mcp[cli]" pydantic
    export AXANTA_URL="https://yourinstance.axantacloud.com"
    export AXANTA_DB="your_db_name"
    export AXANTA_USER="your_email"
    export AXANTA_KEY="your_api_key"
    claude mcp add axanta-erp -- python3 tools/mcp-servers/axanta_mcp_server.py
"""

import json
import os
import xmlrpc.client
from contextlib import asynccontextmanager
from enum import Enum
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Lifespan: lazy connection & authentication
# ---------------------------------------------------------------------------

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    url = os.environ.get("AXANTA_URL", "")
    db = os.environ.get("AXANTA_DB", "")
    user = os.environ.get("AXANTA_USER", "")
    key = os.environ.get("AXANTA_KEY", "")

    missing = [v for v, n in [(url, "AXANTA_URL"), (db, "AXANTA_DB"),
               (user, "AXANTA_USER"), (key, "AXANTA_KEY")] if not n]
    if not all([url, db, user, key]):
        missing = [n for v, n in [(url, "AXANTA_URL"), (db, "AXANTA_DB"),
                   (user, "AXANTA_USER"), (key, "AXANTA_KEY")] if not v]
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Set them before starting the server."
        )

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    uid = common.authenticate(db, user, key, {})

    if not uid:
        raise EnvironmentError(
            "Axanta authentication failed. Check AXANTA_URL, AXANTA_DB, "
            "AXANTA_USER, and AXANTA_KEY are correct."
        )

    yield {"odoo_models": models, "odoo_db": db, "odoo_uid": uid, "odoo_key": key}


mcp = FastMCP("axanta_mcp", lifespan=app_lifespan)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _odoo(ctx, model: str, method: str, args: list | None = None,
          kw: dict | None = None) -> Any:
    state = ctx.request_context.lifespan_state
    return state["odoo_models"].execute_kw(
        state["odoo_db"], state["odoo_uid"], state["odoo_key"],
        model, method, args or [], kw or {},
    )


def _handle_error(e: Exception, tool: str) -> str:
    if isinstance(e, xmlrpc.client.Fault):
        msg = str(e.faultString)
        if "AccessError" in msg or "AccessDenied" in msg:
            return (f"Error in {tool}: Permission denied. Your Axanta user "
                    "may lack access to this module. Ask your admin to grant "
                    "the necessary access rights.")
        if "MissingError" in msg:
            return (f"Error in {tool}: Record not found. The ID may have been "
                    "deleted or archived. Try searching by name instead.")
        return f"Error in {tool}: Odoo fault — {msg}"
    if isinstance(e, ConnectionRefusedError):
        return (f"Error in {tool}: Cannot reach Axanta server. "
                "Check that AXANTA_URL is correct and the server is running.")
    if isinstance(e, xmlrpc.client.ProtocolError):
        return (f"Error in {tool}: Protocol error ({e.errcode}). "
                "Verify AXANTA_URL uses the correct protocol (https://).")
    return f"Error in {tool}: {type(e).__name__} — {e}"


def _fmt(data: Any, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(data, indent=2, default=str)
    return json.dumps(data, indent=2, default=str)


def _pagination_meta(total: int, offset: int, count: int) -> dict:
    return {
        "total": total,
        "count": count,
        "offset": offset,
        "has_more": total > offset + count,
        "next_offset": offset + count if total > offset + count else None,
    }


# ---------------------------------------------------------------------------
# Enums & Pydantic models
# ---------------------------------------------------------------------------

class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


class SearchRecordsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    model: str = Field(
        ...,
        description=(
            "Odoo model to search. Common models: sale.order, purchase.order, "
            "account.move, stock.picking, res.partner, product.product, "
            "product.template, stock.quant, hr.employee, account.payment"
        ),
        min_length=1,
    )
    domain: list = Field(
        default_factory=list,
        description='Odoo domain filter as list of tuples, e.g. [["state","=","sale"]]',
    )
    fields: list[str] = Field(
        default=["id", "name"],
        description="Fields to return, e.g. ['name','amount_total','state']",
    )
    limit: int = Field(default=20, description="Max records to return", ge=1, le=200)
    offset: int = Field(default=0, description="Records to skip for pagination", ge=0)
    order: str = Field(default="id desc", description="Sort order, e.g. 'date_order desc'")


class GetRecordInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    model: str = Field(..., description="Odoo model name", min_length=1)
    record_id: int = Field(..., description="Record ID to fetch", ge=1)
    fields: list[str] = Field(
        default_factory=list,
        description="Specific fields to return (empty = all fields)",
    )


class SalesSummaryInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    state: str = Field(
        default="sale",
        description="Order state filter: draft, sent, sale, done, cancel, or 'all'",
    )
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        allowed = {"draft", "sent", "sale", "done", "cancel", "all"}
        if v not in allowed:
            raise ValueError(f"state must be one of {allowed}")
        return v


class InventoryInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    product_name: str = Field(default="", description="Filter by product name (partial match)")
    low_stock_only: bool = Field(default=False, description="Only show products with qty < 10")
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)


class CustomerInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(default="", description="Filter by customer name (partial match)")
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class InvoiceInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    state: str = Field(default="posted", description="Invoice state: draft, posted, cancel")
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        allowed = {"draft", "posted", "cancel"}
        if v not in allowed:
            raise ValueError(f"state must be one of {allowed}")
        return v


class PurchaseOrderInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    state: str = Field(default="purchase", description="PO state: draft, purchase, done, cancel")
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        allowed = {"draft", "purchase", "done", "cancel"}
        if v not in allowed:
            raise ValueError(f"state must be one of {allowed}")
        return v


class EmployeeInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(default="", description="Filter by employee name (partial match)")
    limit: int = Field(default=30, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class StockMovementInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    picking_type: str = Field(
        default="outgoing",
        description="Movement type: outgoing (deliveries), incoming (receipts), internal (transfers)",
    )
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

    @field_validator("picking_type")
    @classmethod
    def validate_picking_type(cls, v: str) -> str:
        allowed = {"outgoing", "incoming", "internal"}
        if v not in allowed:
            raise ValueError(f"picking_type must be one of {allowed}")
        return v


class CreateRecordInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    model: str = Field(..., description="Odoo model to create record in", min_length=1)
    values: dict = Field(..., description="Field values for the new record, e.g. {'name': 'John', 'email': 'j@co.com'}")


class UpdateRecordInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    model: str = Field(..., description="Odoo model of the record to update", min_length=1)
    record_id: int = Field(..., description="ID of the record to update", ge=1)
    values: dict = Field(..., description="Field values to update, e.g. {'list_price': 29.99}")


class ReportInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    report_type: str = Field(
        ...,
        description="Report type: sales_by_branch, sales_by_product, top_customers",
    )
    limit: int = Field(default=20, ge=1, le=100)

    @field_validator("report_type")
    @classmethod
    def validate_report_type(cls, v: str) -> str:
        allowed = {"sales_by_branch", "sales_by_product", "top_customers"}
        if v not in allowed:
            raise ValueError(f"report_type must be one of {allowed}")
        return v


# ---------------------------------------------------------------------------
# Tools — Read-only
# ---------------------------------------------------------------------------

@mcp.tool(
    name="axanta_search_records",
    annotations={
        "title": "Search Axanta Records",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_search_records(params: SearchRecordsInput, ctx=None) -> str:
    """Search any Odoo model with domain filters, field selection, and pagination.

    Use this tool for flexible queries across all Axanta ERP models. Supports
    Odoo domain syntax for filtering (e.g. [["state","=","sale"]]).
    """
    try:
        total = _odoo(ctx, params.model, "search_count", [params.domain])
        records = _odoo(ctx, params.model, "search_read", [params.domain], {
            "fields": params.fields,
            "limit": params.limit,
            "offset": params.offset,
            "order": params.order,
        })
        return json.dumps({
            **_pagination_meta(total, params.offset, len(records)),
            "records": records,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_search_records")


@mcp.tool(
    name="axanta_get_record",
    annotations={
        "title": "Get Axanta Record by ID",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_record(params: GetRecordInput, ctx=None) -> str:
    """Get full details of a single record by its ID.

    Returns all fields (or specified fields) for the given record. Use
    axanta_search_records first to find the record ID.
    """
    try:
        result = _odoo(ctx, params.model, "read",
                       [[params.record_id]],
                       {"fields": params.fields} if params.fields else {})
        if not result:
            return (f"No record found: {params.model} ID {params.record_id}. "
                    "The record may have been deleted or archived.")
        return json.dumps(result[0], indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_record")


@mcp.tool(
    name="axanta_get_sales_summary",
    annotations={
        "title": "Sales Summary",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_sales_summary(params: SalesSummaryInput, ctx=None) -> str:
    """Get sales orders summary with totals, statuses, and top customers.

    Returns a list of sale orders with amount totals, partner info, and
    an aggregate summary. Filter by order state.
    """
    try:
        domain = [] if params.state == "all" else [["state", "=", params.state]]
        fields = ["name", "partner_id", "amount_total", "state",
                  "date_order", "user_id", "team_id"]

        total_count = _odoo(ctx, "sale.order", "search_count", [domain])
        orders = _odoo(ctx, "sale.order", "search_read", [domain], {
            "fields": fields,
            "limit": params.limit,
            "offset": params.offset,
            "order": "date_order desc",
        })
        total_amount = sum(o["amount_total"] for o in orders)

        return json.dumps({
            **_pagination_meta(total_count, params.offset, len(orders)),
            "total_amount": round(total_amount, 2),
            "currency": "KWD",
            "orders": orders,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_sales_summary")


@mcp.tool(
    name="axanta_get_inventory",
    annotations={
        "title": "Product Inventory Levels",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_inventory(params: InventoryInput, ctx=None) -> str:
    """Get product stock levels and availability across all locations.

    Returns on-hand quantity, forecasted quantity, price, and category for
    each product. Use product_name for partial-match filtering and
    low_stock_only to find items needing restocking.
    """
    try:
        domain: list = [["type", "in", ["product", "consu"]]]
        if params.product_name:
            domain.append(["name", "ilike", params.product_name])
        if params.low_stock_only:
            domain.append(["qty_available", "<", 10])

        fields = ["name", "default_code", "qty_available",
                  "virtual_available", "list_price", "categ_id"]

        total_count = _odoo(ctx, "product.product", "search_count", [domain])
        products = _odoo(ctx, "product.product", "search_read", [domain], {
            "fields": fields,
            "limit": params.limit,
            "offset": params.offset,
            "order": "qty_available asc",
        })

        return json.dumps({
            **_pagination_meta(total_count, params.offset, len(products)),
            "products": products,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_inventory")


@mcp.tool(
    name="axanta_get_customers",
    annotations={
        "title": "Search Customers",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_customers(params: CustomerInput, ctx=None) -> str:
    """Search and list customers with contact info and invoice totals.

    Filter by name (partial match). Returns name, email, phone, city,
    and total invoiced amount per customer.
    """
    try:
        domain: list = [["customer_rank", ">", 0]]
        if params.name:
            domain.append(["name", "ilike", params.name])

        fields = ["name", "email", "phone", "city",
                  "customer_rank", "total_invoiced"]

        total_count = _odoo(ctx, "res.partner", "search_count", [domain])
        customers = _odoo(ctx, "res.partner", "search_read", [domain], {
            "fields": fields,
            "limit": params.limit,
            "offset": params.offset,
        })

        return json.dumps({
            **_pagination_meta(total_count, params.offset, len(customers)),
            "customers": customers,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_customers")


@mcp.tool(
    name="axanta_get_invoices",
    annotations={
        "title": "Customer Invoices",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_invoices(params: InvoiceInput, ctx=None) -> str:
    """Get customer invoices with amounts, due dates, and payment status.

    Filter by invoice state (draft, posted, cancel). Shows amount total,
    residual balance, and due date for each invoice.
    """
    try:
        domain = [["move_type", "=", "out_invoice"],
                  ["state", "=", params.state]]
        fields = ["name", "partner_id", "amount_total", "amount_residual",
                  "state", "invoice_date", "invoice_date_due"]

        total_count = _odoo(ctx, "account.move", "search_count", [domain])
        invoices = _odoo(ctx, "account.move", "search_read", [domain], {
            "fields": fields,
            "limit": params.limit,
            "offset": params.offset,
            "order": "invoice_date desc",
        })

        return json.dumps({
            **_pagination_meta(total_count, params.offset, len(invoices)),
            "invoices": invoices,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_invoices")


@mcp.tool(
    name="axanta_get_purchase_orders",
    annotations={
        "title": "Purchase Orders",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_purchase_orders(params: PurchaseOrderInput, ctx=None) -> str:
    """Get purchase orders from vendors with amounts and delivery dates.

    Filter by PO state (draft, purchase, done, cancel). Shows vendor,
    amount, order date, and planned delivery date.
    """
    try:
        domain = [["state", "=", params.state]]
        fields = ["name", "partner_id", "amount_total", "state",
                  "date_order", "date_planned"]

        total_count = _odoo(ctx, "purchase.order", "search_count", [domain])
        orders = _odoo(ctx, "purchase.order", "search_read", [domain], {
            "fields": fields,
            "limit": params.limit,
            "offset": params.offset,
            "order": "date_order desc",
        })

        return json.dumps({
            **_pagination_meta(total_count, params.offset, len(orders)),
            "purchase_orders": orders,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_purchase_orders")


@mcp.tool(
    name="axanta_get_employees",
    annotations={
        "title": "List Employees",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_employees(params: EmployeeInput, ctx=None) -> str:
    """List employees with job titles, departments, and contact info.

    Filter by name (partial match). Only returns active employees.
    """
    try:
        domain: list = [["active", "=", True]]
        if params.name:
            domain.append(["name", "ilike", params.name])

        fields = ["name", "job_title", "department_id",
                  "work_email", "work_phone"]

        total_count = _odoo(ctx, "hr.employee", "search_count", [domain])
        employees = _odoo(ctx, "hr.employee", "search_read", [domain], {
            "fields": fields,
            "limit": params.limit,
            "offset": params.offset,
        })

        return json.dumps({
            **_pagination_meta(total_count, params.offset, len(employees)),
            "employees": employees,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_employees")


@mcp.tool(
    name="axanta_get_stock_movements",
    annotations={
        "title": "Stock Movements",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_stock_movements(params: StockMovementInput, ctx=None) -> str:
    """Get inventory transfers and movements (deliveries, receipts, internal).

    Filter by picking_type: outgoing (deliveries to customers),
    incoming (receipts from vendors), internal (warehouse transfers).
    """
    try:
        domain = [["picking_type_code", "=", params.picking_type],
                  ["state", "in", ["done", "assigned"]]]
        fields = ["name", "partner_id", "state", "scheduled_date",
                  "date_done", "picking_type_id", "origin"]

        total_count = _odoo(ctx, "stock.picking", "search_count", [domain])
        movements = _odoo(ctx, "stock.picking", "search_read", [domain], {
            "fields": fields,
            "limit": params.limit,
            "offset": params.offset,
            "order": "date_done desc",
        })

        return json.dumps({
            **_pagination_meta(total_count, params.offset, len(movements)),
            "movements": movements,
        }, indent=2, default=str)
    except Exception as e:
        return _handle_error(e, "axanta_get_stock_movements")


@mcp.tool(
    name="axanta_get_report",
    annotations={
        "title": "Aggregated Reports",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_get_report(params: ReportInput, ctx=None) -> str:
    """Get aggregated report data: sales by branch, by product, or top customers.

    Aggregates across confirmed/done sale orders. Use report_type to pick
    the dimension: sales_by_branch, sales_by_product, or top_customers.
    """
    try:
        if params.report_type == "sales_by_branch":
            orders = _odoo(ctx, "sale.order", "search_read",
                           [[["state", "in", ["sale", "done"]]]],
                           {"fields": ["name", "team_id", "amount_total"],
                            "limit": 500})
            branches: dict[str, float] = {}
            for o in orders:
                b = o["team_id"][1] if o["team_id"] else "Unknown"
                branches[b] = branches.get(b, 0) + o["amount_total"]
            sorted_branches = sorted(branches.items(),
                                     key=lambda x: x[1], reverse=True)[:params.limit]
            return json.dumps({
                "report_type": "sales_by_branch",
                "data": [{"branch": b, "total": round(t, 2)}
                         for b, t in sorted_branches],
            }, indent=2, default=str)

        elif params.report_type == "top_customers":
            customers = _odoo(ctx, "res.partner", "search_read",
                              [[["customer_rank", ">", 0]]],
                              {"fields": ["name", "total_invoiced"],
                               "limit": params.limit,
                               "order": "total_invoiced desc"})
            return json.dumps({
                "report_type": "top_customers",
                "data": customers,
            }, indent=2, default=str)

        elif params.report_type == "sales_by_product":
            lines = _odoo(ctx, "sale.order.line", "search_read",
                          [[["order_id.state", "in", ["sale", "done"]]]],
                          {"fields": ["product_id", "product_uom_qty",
                                      "price_subtotal"], "limit": 1000})
            products: dict[str, dict] = {}
            for ln in lines:
                p = ln["product_id"][1] if ln["product_id"] else "Unknown"
                if p not in products:
                    products[p] = {"qty": 0, "revenue": 0.0}
                products[p]["qty"] += ln["product_uom_qty"]
                products[p]["revenue"] += ln["price_subtotal"]
            sorted_products = sorted(products.items(),
                                     key=lambda x: x[1]["revenue"],
                                     reverse=True)[:params.limit]
            return json.dumps({
                "report_type": "sales_by_product",
                "data": [{"product": p, "qty_sold": d["qty"],
                          "revenue": round(d["revenue"], 2)}
                         for p, d in sorted_products],
            }, indent=2, default=str)

        return json.dumps({"error": f"Unknown report_type: {params.report_type}"})
    except Exception as e:
        return _handle_error(e, "axanta_get_report")


# ---------------------------------------------------------------------------
# Tools — Write operations
# ---------------------------------------------------------------------------

@mcp.tool(
    name="axanta_create_record",
    annotations={
        "title": "Create Record",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
async def axanta_create_record(params: CreateRecordInput, ctx=None) -> str:
    """Create a new record in any Odoo model (customer, product, sale order, etc.).

    Provide the model name and a dict of field values. Returns the new
    record ID on success. Check required fields with axanta_search_records first.
    """
    try:
        new_id = _odoo(ctx, params.model, "create", [params.values])
        return json.dumps({
            "success": True,
            "id": new_id,
            "model": params.model,
            "message": f"Created {params.model} record with ID {new_id}",
        }, indent=2)
    except Exception as e:
        return _handle_error(e, "axanta_create_record")


@mcp.tool(
    name="axanta_update_record",
    annotations={
        "title": "Update Record",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def axanta_update_record(params: UpdateRecordInput, ctx=None) -> str:
    """Update fields of an existing record in any Odoo model.

    Provide the model name, record ID, and a dict of field values to change.
    Only the specified fields are updated; other fields remain unchanged.
    """
    try:
        _odoo(ctx, params.model, "write",
              [[params.record_id], params.values])
        return json.dumps({
            "success": True,
            "model": params.model,
            "id": params.record_id,
            "message": f"Updated {params.model} ID {params.record_id}",
        }, indent=2)
    except Exception as e:
        return _handle_error(e, "axanta_update_record")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
