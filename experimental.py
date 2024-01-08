from dataclasses import dataclass, field
from enum import Enum

from pydantic import BaseModel

from abacus.base import Amount
from abacus.core import (
    Ledger,
    BalanceSheet,
    CompoundEntry,
    Entry,
    IncomeStatement,
    Pipeline,
    TrialBalance,
)
from abacus.user_chart import UserChart, make_user_chart


class Author(Enum):
    User = "from_user"
    Machine = "generated"


class Transaction(BaseModel):
    title: str
    entries: list[Entry]
    author: Author
    # may include date and UUID


def prefix(p, strings):
    return [p + ":" + s for s in strings]


@dataclass
class Book:
    company: str
    user_chart: UserChart = field(default_factory=make_user_chart)
    transactions: list[Transaction] = field(default_factory=list)
    starting_balances: dict[str, Amount] = field(default_factory=dict)

    @property
    def entries(self):
        return [e for t in self.transactions for e in t.entries]

    @property
    def entries_not_touching_isa(self):
        isa = self.user_chart.income_summary_account

        def not_isa(entry):
            return (entry.debit != isa) and (entry.credit != isa)

        return list(filter(not_isa, self.entries))

    def add_asset_accounts(self, *strings):
        self.user_chart.use(*prefix("asset", strings))

    def add_capital_accounts(self, *strings, retained_earnings_account=None):
        if retained_earnings_account:
            self.user_chart.set_re(retained_earnings_account)
        self.user_chart.use(*prefix("capital", strings))

    def add_liability_accounts(self, *strings):
        self.user_chart.use(*prefix("liability", strings))

    def add_income_accounts(self, *strings):
        self.user_chart.use(*prefix("income", strings))

    def add_expense_accounts(self, *strings):
        self.user_chart.use(*prefix("expense", strings))

    def offset(self, account_name, account_contra_name):
        self.user_chart.offset(account_name, account_contra_name)

    def name(self, account_name, title):
        self.user_chart.rename(account_name, title)

    def post(self, title, amount, debit, credit):
        entry = Entry(debit, credit, amount)
        self._transact_user(title, [entry])

    def post_compound(self, title, debits, credits):
        entry = CompoundEntry(debits, credits)
        self._transact_user(title, entry.to_entries(self.user_chart.null_account))

    @property
    def _chart(self):
        return self.user_chart.chart()

    @property
    def _ledger0(self) -> Ledger:
        chart = self.user_chart.chart()
        return chart.ledger(self.starting_balances)

    @property
    def ledger(self):
        """Current state of the ledger unmodified."""
        return self._ledger0.post_many(self.entries)

    @property
    def ledger_for_income_statement(self):
        ledger = self._ledger0.post_many(self.entries_not_touching_isa)
        p = Pipeline(self._chart, ledger).close_first()
        return ledger.post_many(p.closing_entries)

    def close_period(self):
        """Add closing entries at the end of accounting period."""
        p = Pipeline(self._chart, self.ledger).close()
        self._transact("Closing entries", p.closing_entries, Author.Machine)

    def _transact_user(self, title, entries):
        self._transact(title, entries, Author.User)

    def _transact(self, title, entries, author):
        t = Transaction(title=title, entries=entries, author=author)
        self.transactions.append(t)

    def is_closed(self):
        return "Closing entries" in [
            t.title for t in self.transactions if t.author == Author.Machine
        ]

    @property
    def balance_sheet(self):
        from abacus.viewers import BalanceSheetViewer

        return BalanceSheetViewer(
            statement=BalanceSheet.new(self.ledger),
            title="Balance sheet: " + self.company,
            rename_dict=self.user_chart.rename_dict,
        )

    @property
    def income_statement(self):
        from abacus.viewers import IncomeStatementViewer

        return IncomeStatementViewer(
            statement=IncomeStatement.new(self.ledger_for_income_statement),
            title="Income statement: " + self.company,
            rename_dict=self.user_chart.rename_dict,
        )

    @property
    def trial_balance(self):
        from abacus.viewers import TrialBalanceViewer

        return TrialBalanceViewer(
            TrialBalance.new(self.ledger),
            title="Trial balance: " + self.company,
            rename_dict=self.user_chart.rename_dict,
        )

    @property
    def account_balances(self):
        return self.ledger.balances

    def print_all(self):
        from abacus.viewers import print_viewers

        print_viewers(
            self.user_chart.rename_dict,
            self.trial_balance,
            self.balance_sheet,
            self.income_statement,
        )

    def save(self, chart_path, entries_path):
        ...


book = Book(company="Dragon Trading Company")

# Register valid account names and indicate account type
book.add_asset_accounts("cash", "ar", "inventory")
book.add_capital_accounts("equity", retained_earnings_account="retained_earnings")
book.add_liability_accounts("vat", "ap")
book.add_income_accounts("sales")
book.add_expense_accounts("salaries")
book.offset("sales", "refunds")
book.name("vat", "VAT payable")
book.name("ap", "Other accounts payable")
book.name("ar", "Accounts receivable")

# Regular syntax - post double entry
book.post("Shareholder investment", amount=1500, debit="cash", credit="equity")
# Post multiple entry
book.post_compound(
    "Invoice with VAT", debits=[("ar", 120)], credits=[("sales", 100), ("vat", 20)]
)

# Close, print to screen and save
book.close_period()
print(book.entries)
print(book.transactions)
print(book.user_chart)
print(book.trial_balance)
print(book.balance_sheet)
print(book.income_statement)
print(book.account_balances)
book.print_all()
book.save(chart_path="./chart.json", entries_path="./entries.linejson")
