"""Order quantity calculation utilities."""

from dataclasses import dataclass
from typing import Iterable, List

try:
    import pandas as pd
except Exception:  # pragma: no cover - pandas may not be installed during tests
    pd = None


@dataclass
class ProductInfo:
    product_id: str
    safety_stock: int
    pallet_qty: int


@dataclass
class InventoryStatus:
    product_id: str
    quantity: int


def calculate_orders(
    forecast: Iterable[dict],
    inventory: Iterable[InventoryStatus],
    products: Iterable[ProductInfo],
    lead_time_days: int,
    target_days: int,
) -> List[dict]:
    """Return recommended order quantities per product."""
    if pd is None:
        raise RuntimeError("pandas is required for order calculations")

    forecast_df = pd.DataFrame(forecast)
    inv_map = {i.product_id: i.quantity for i in inventory}
    prod_map = {p.product_id: p for p in products}

    results = []
    for product_id, group in forecast_df.groupby("product_id"):
        info = prod_map.get(product_id)
        if info is None:
            continue
        demand = (
            group.sort_values("date")
            .head(lead_time_days + target_days)["qty"]
            .sum()
        )
        current = inv_map.get(product_id, 0)
        reorder_point = demand + info.safety_stock
        order_qty = max(reorder_point - current, 0)
        if info.pallet_qty:
            # round up to pallet quantity
            pallets = -(-order_qty // info.pallet_qty)
            order_qty = pallets * info.pallet_qty
        results.append({"product_id": product_id, "order_qty": int(order_qty)})
    return results
