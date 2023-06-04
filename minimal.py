from abacus import Chart, BalanceSheet, IncomeStatement

chart = Chart(
    assets=["cash", "ar", "goods"],
    expenses=["cogs", "sga"],
    equity=["equity"],
    retained_earnings_account="re",
    income=["sales"],
    contra_accounts={"sales": ["cashback"]},
)
journal = (
    chart.journal(cash=1200, goods=300, equity=1500)
    .post(dr="ar", cr="sales", amount=440)
    .post(dr="cashback", cr="cash", amount=41)
    .post(dr="cash", cr="ar", amount=250)
    .post(dr="cogs", cr="goods", amount=250)
    .post(dr="sga", cr="cash", amount=59)
    .close()
)
print(journal.balance_sheet())
# BalanceSheet(
#     assets={"cash": 1540, "goods": 50},
#     capital={"equity": 1500, "re": 90},
#     liabilities={},
# )
print(journal.income_statement())
# IncomeStatement(income={"sales": 399},
#                 expenses={"cogs": 250, "sga": 59})

from abacus import Chart, Entry


chart = Chart(
    assets=["cash", "receivables", "goods_for_sale"],
    expenses=["cogs", "sga"],
    equity=["equity"],
    retained_earnings_account="re",
    liabilities=["divp", "payables"],
    income=["sales"],
)

journal = chart.journal()

e1 = Entry(dr="cash", cr="equity", amount=1000)  # pay in capital
e2 = Entry(dr="goods_for_sale", cr="cash", amount=250)  # acquire goods worth 250
e3 = Entry(cr="goods_for_sale", dr="cogs", amount=200)  # sell goods worth 200
e4 = Entry(cr="sales", dr="cash", amount=400)  # for 400 in cash
e5 = Entry(cr="cash", dr="sga", amount=50)  # administrative expenses
journal = journal.post_many([e1, e2, e3, e4, e5]).close()

from abacus import IncomeStatement

income_statement = journal.income_statement()
assert income_statement == IncomeStatement(
    income={"sales": 400}, expenses={"cogs": 200, "sga": 50}
)

from abacus import BalanceSheet

balance_sheet = journal.balance_sheet()
assert balance_sheet == BalanceSheet(
    assets={"cash": 1100, "receivables": 0, "goods_for_sale": 50},
    capital={"equity": 1000, "re": 150},
    liabilities={"divp": 0, "payables": 0},
)

from abacus import RichViewer


rename_dict = {
    "re": "Retained earnings",
    "divp": "Dividend due",
    "cogs": "Cost of goods sold",
    "sga": "Selling, general and adm. expenses",
}
rv = RichViewer(rename_dict, width=60)
rv.print(balance_sheet)
rv.print(income_statement)
