"""Demonstration of order calculation and vehicle optimization."""

from datetime import date, timedelta

from sendcal.order_calc import ProductInfo, InventoryStatus, calculate_orders
from sendcal.vehicle_opt import optimize_trucks


def main() -> None:
    # sample forecast for 3 products, 7 days each
    forecast = []
    for pid in ["A", "B", "C"]:
        for d in range(7):
            forecast.append({"product_id": pid, "date": date.today() + timedelta(days=d), "qty": 10 + d})

    inventory = [
        InventoryStatus("A", 20),
        InventoryStatus("B", 5),
        InventoryStatus("C", 8),
    ]
    products = [
        ProductInfo("A", safety_stock=5, pallet_qty=10),
        ProductInfo("B", safety_stock=3, pallet_qty=20),
        ProductInfo("C", safety_stock=2, pallet_qty=15),
    ]

    orders = calculate_orders(forecast, inventory, products, lead_time_days=2, target_days=3)
    print("Order suggestions:")
    for row in orders:
        print(row)

    qty_list = [row["order_qty"] for row in orders]
    trucks = optimize_trucks(qty_list, capacity=40)
    print("\nTruck allocation:")
    for idx, t in enumerate(trucks, 1):
        print(f"Truck {idx}: products {t}")


if __name__ == "__main__":
    main()
