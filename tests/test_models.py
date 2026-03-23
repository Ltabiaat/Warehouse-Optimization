import unittest

from warehouse_optimization.config.models import WarehouseConfiguration, WarehouseDimensions


class WarehouseConfigurationTests(unittest.TestCase):
    def test_warehouse_configuration_minimal(self) -> None:
        config = WarehouseConfiguration(
            warehouse_id="wh-1",
            name="Demo Warehouse",
            dimensions=WarehouseDimensions(width_m=20.0, length_m=50.0),
        )

        self.assertEqual(config.name, "Demo Warehouse")
        self.assertEqual(config.dimensions.width_m, 20.0)
        self.assertEqual(config.zones, [])


if __name__ == "__main__":
    unittest.main()
