# SendCal

Sample implementation of the order calculation and vehicle optimization system.

## Structure

- `src/sendcal/etl.py` – basic ETL helpers using SQLAlchemy and pandas
- `src/sendcal/order_calc.py` – functions to compute recommended order quantities
- `src/sendcal/vehicle_opt.py` – PuLP based truck allocation solver
- `scripts/demo.py` – runnable example combining the modules

## Usage

The demo script generates sample forecast and inventory data, calculates the
required order quantities, and assigns them to trucks.

```bash
python scripts/demo.py
```

The code relies on `pandas` and `pulp`. These modules must be installed in your
environment to run the example.
