import unittest
from datetime import datetime

from warehouse_optimization.wms.adapters.erpnext import ERPNextAdapter, ERPNextConfig
from warehouse_optimization.wms.models import Product, SalesOrder, SalesOrderLine, WarehouseSite


class ERPNextAdapterTests(unittest.TestCase):
    def test_build_demand_snapshot_aggregates_quantities(self) -> None:
        adapter = ERPNextAdapter(
            config=ERPNextConfig(base_url="https://erp.example.com"),
            fixture_products=[
                Product(product_id="ITEM-001", sku="ITEM-001", name="Widget A"),
                Product(product_id="ITEM-002", sku="ITEM-002", name="Widget B"),
            ],
            fixture_warehouses=[
                WarehouseSite(warehouse_id="Main Warehouse", name="Main Warehouse"),
            ],
            fixture_sales_orders=[
                SalesOrder(
                    order_id="SO-001",
                    customer_id="CUST-001",
                    order_date=datetime(2024, 9, 9, 9, 0, 0),
                    warehouse_id="Main Warehouse",
                ),
                SalesOrder(
                    order_id="SO-002",
                    customer_id="CUST-002",
                    order_date=datetime(2024, 9, 9, 10, 0, 0),
                    warehouse_id="Main Warehouse",
                ),
            ],
            fixture_sales_order_lines=[
                SalesOrderLine(
                    line_id="SO-001-1",
                    order_id="SO-001",
                    product_id="ITEM-001",
                    quantity=3,
                    warehouse_id="Main Warehouse",
                ),
                SalesOrderLine(
                    line_id="SO-002-1",
                    order_id="SO-002",
                    product_id="ITEM-001",
                    quantity=2,
                    warehouse_id="Main Warehouse",
                ),
                SalesOrderLine(
                    line_id="SO-002-2",
                    order_id="SO-002",
                    product_id="ITEM-002",
                    quantity=5,
                    warehouse_id="Main Warehouse",
                ),
            ],
        )

        snapshot = adapter.build_demand_snapshot(
            warehouse_id="Main Warehouse",
            start=datetime(2024, 9, 9, 0, 0, 0),
            end=datetime(2024, 9, 9, 23, 59, 59),
        )

        self.assertEqual(snapshot.total_order_count, 2)
        self.assertEqual(snapshot.total_units, 10)
        self.assertEqual(snapshot.product_quantities["ITEM-001"], 5)
        self.assertEqual(snapshot.product_quantities["ITEM-002"], 5)


if __name__ == "__main__":
    unittest.main()
