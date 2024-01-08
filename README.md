# abacus

[![pytest](https://github.com/epogrebnyak/abacus/actions/workflows/.pytest.yml/badge.svg)](https://github.com/epogrebnyak/abacus/actions/workflows/.pytest.yml)
[![PyPI](https://img.shields.io/pypi/v/abacus-py?color=blue)](https://pypi.org/project/abacus-py/)

A minimal, yet valid double-entry accounting system in Python.

## Documentation

See project documentation at <https://epogrebnyak.github.io/abacus/>.

## Installation

```
pip install abacus-py
```

For latest version install from github:

```
pip install git+https://github.com/epogrebnyak/abacus.git
```

`abacus-py` requires Python 3.10 or higher.

## Quick example

Let's do Sample Transaction #1 from [accountingcoach.com](https://www.accountingcoach.com/accounting-basics/explanation/5) (a great learning resource, highly recommended).

```python 
from abacus import Chart, Report

chart = Chart(assets=["cash"], capital=["common_stock"])
ledger = chart.ledger()
ledger.post(debit="cash", credit="common_stock", amount=20000)
report = Report(chart, ledger)
print(report.balance_sheet.viewer)
```
The result is:

```
Balance sheet
ASSETS  20000  CAPITAL              20000
  Cash  20000    Common stock       20000
                 Retained earnings      0
               LIABILITIES              0
TOTAL   20000  TOTAL                20000
```
