"""Vehicle optimization for daily inbound shipments."""

from typing import List

try:
    import pulp
except Exception:  # pragma: no cover - pulp may not be installed
    pulp = None


def optimize_trucks(order_qty: List[int], capacity: int = 1000) -> List[List[int]]:
    """Assign product quantities to trucks to minimize the number of trucks.

    Parameters
    ----------
    order_qty : List[int]
        Quantities for each product.
    capacity : int
        Maximum capacity of a single truck.
    Returns
    -------
    List of lists. Each sublist contains indexes of products assigned to a truck.
    """
    if pulp is None:
        raise RuntimeError("PuLP is required for optimization")

    n = len(order_qty)
    max_trucks = n

    prob = pulp.LpProblem("truck_load", pulp.LpMinimize)
    y = pulp.LpVariable.dicts("truck", range(max_trucks), 0, 1, cat="Binary")
    x = pulp.LpVariable.dicts(
        "assign", (range(n), range(max_trucks)), 0, 1, cat="Binary"
    )

    # objective: minimize the number of trucks used
    prob += pulp.lpSum(y[j] for j in range(max_trucks))

    # each product assigned to one truck
    for i in range(n):
        prob += pulp.lpSum(x[i][j] for j in range(max_trucks)) == 1

    # capacity constraints
    for j in range(max_trucks):
        prob += (
            pulp.lpSum(order_qty[i] * x[i][j] for i in range(n)) <= capacity * y[j]
        )

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    trucks: List[List[int]] = []
    for j in range(max_trucks):
        if y[j].varValue > 0.5:
            assigned = [i for i in range(n) if x[i][j].varValue > 0.5]
            trucks.append(assigned)
    return trucks
