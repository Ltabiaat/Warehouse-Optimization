from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from warehouse_optimization.wms.models import (
    DemandSnapshot,
    InventoryBalance,
    Product,
    SalesOrder,
    SalesOrderLine,
    StockMovement,
    WarehouseSite,
)


class WMSAdapter(ABC):
    """Abstract interface for upstream WMS / ERP integrations."""

    @abstractmethod
    def list_products(self) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    def list_warehouses(self) -> list[WarehouseSite]:
        raise NotImplementedError

    @abstractmethod
    def list_sales_orders(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[SalesOrder]:
        raise NotImplementedError

    @abstractmethod
    def list_sales_order_lines(
        self,
        order_ids: list[str] | None = None,
    ) -> list[SalesOrderLine]:
        raise NotImplementedError

    @abstractmethod
    def list_inventory_balances(self) -> list[InventoryBalance]:
        raise NotImplementedError

    @abstractmethod
    def list_stock_movements(
        self,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> list[StockMovement]:
        raise NotImplementedError

    @abstractmethod
    def build_demand_snapshot(
        self,
        warehouse_id: str,
        start: datetime,
        end: datetime,
    ) -> DemandSnapshot:
        raise NotImplementedError
