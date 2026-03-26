from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from warehouse_optimization.wms.adapters.base import WMSAdapter
from warehouse_optimization.wms.models import (
    DemandSnapshot,
    InventoryBalance,
    Product,
    SalesOrder,
    SalesOrderLine,
    StockMovement,
    WarehouseSite,
)


@dataclass(slots=True)
class ERPNextConfig:
    base_url: str
    api_key: str | None = None
    api_secret: str | None = None
    username: str | None = None
    password: str | None = None
    verify_ssl: bool = True
    timeout_seconds: int = 30


@dataclass(slots=True)
class ERPNextAdapter(WMSAdapter):
    """ERPNext-backed WMS adapter.

    This starts as a normalization layer and contract stub.
    Real HTTP calls can be added once the internal canonical models stabilize.
    """

    config: ERPNextConfig
    fixture_products: list[Product] = field(default_factory=list)
    fixture_warehouses: list[WarehouseSite] = field(default_factory=list)
    fixture_sales_orders: list[SalesOrder] = field(default_factory=list)
    fixture_sales_order_lines: list[SalesOrderLine] = field(default_factory=list)
    fixture_inventory_balances: list[InventoryBalance] = field(default_factory=list)
    fixture_stock_movements: list[StockMovement] = field(default_factory=list)

    def list_products(self) -> list[Product]:
        return list(self.fixture_products)

    def list_warehouses(self) -> list[WarehouseSite]:
        return list(self.fixture_warehouses)

    def list_sales_orders(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[SalesOrder]:
        orders = self.fixture_sales_orders
        if start is not None:
            orders = [order for order in orders if order.order_date >= start]
        if end is not None:
            orders = [order for order in orders if order.order_date <= end]
        return list(orders)

    def list_sales_order_lines(
        self,
        order_ids: list[str] | None = None,
    ) -> list[SalesOrderLine]:
        lines = self.fixture_sales_order_lines
        if order_ids is not None:
            allowed = set(order_ids)
            lines = [line for line in lines if line.order_id in allowed]
        return list(lines)

    def list_inventory_balances(self) -> list[InventoryBalance]:
        return list(self.fixture_inventory_balances)

    def list_stock_movements(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[StockMovement]:
        movements = self.fixture_stock_movements
        if start is not None:
            movements = [m for m in movements if m.occurred_at >= start]
        if end is not None:
            movements = [m for m in movements if m.occurred_at <= end]
        return list(movements)

    def build_demand_snapshot(
        self,
        warehouse_id: str,
        start: datetime,
        end: datetime,
    ) -> DemandSnapshot:
        orders = [
            order
            for order in self.list_sales_orders(start=start, end=end)
            if order.warehouse_id == warehouse_id or order.warehouse_id is None
        ]
        lines = self.list_sales_order_lines(order_ids=[order.order_id for order in orders])

        total_units = 0.0
        product_quantities: dict[str, float] = {}
        for line in lines:
            total_units += line.quantity
            product_quantities[line.product_id] = (
                product_quantities.get(line.product_id, 0.0) + line.quantity
            )

        return DemandSnapshot(
            warehouse_id=warehouse_id,
            period_start=start,
            period_end=end,
            total_order_count=len(orders),
            total_units=total_units,
            product_quantities=product_quantities,
        )

    def auth_headers(self) -> dict[str, str]:
        if self.config.api_key and self.config.api_secret:
            return {
                "Authorization": f"token {self.config.api_key}:{self.config.api_secret}",
            }
        return {}

    def endpoint(self, path: str) -> str:
        return f"{self.config.base_url.rstrip('/')}/{path.lstrip('/')}"

    def _normalize_item(self, payload: dict[str, Any]) -> Product:
        return Product(
            product_id=str(payload.get("name") or payload.get("item_code")),
            sku=str(payload.get("item_code") or payload.get("name")),
            name=str(payload.get("item_name") or payload.get("item_code") or payload.get("name")),
            item_group=payload.get("item_group"),
            stock_uom=payload.get("stock_uom"),
        )

    def _normalize_warehouse(self, payload: dict[str, Any]) -> WarehouseSite:
        return WarehouseSite(
            warehouse_id=str(payload.get("name")),
            name=str(payload.get("warehouse_name") or payload.get("name")),
            company=payload.get("company"),
            parent_warehouse_id=payload.get("parent_warehouse"),
        )
