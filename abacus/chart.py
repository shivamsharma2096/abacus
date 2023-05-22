"""Chart of accounts."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Type

from .accounting_types import AccountName
from .accounts import (
    Account,
    Asset,
    Capital,
    Expense,
    Income,
    IncomeSummaryAccount,
    Liability,
    Netting,
    RetainedEarnings,
    RegularAccount,
    get_contra_account_type,
)
from .ledger import Ledger

__all__ = ["Chart"]


@dataclass
class Chart:
    """Chart of accounts."""

    assets: List[str]
    expenses: List[str]
    equity: List[str]
    liabilities: List[str]
    income: List[str]
    contra_accounts: Dict[str, Tuple[List[str], str]] = field(default_factory=dict)
    income_summary_account: str = "_profit"
    retained_earnings_account: Optional[str] = None

    def __post_init__(self):
        if (
            self.retained_earnings_account
            and self.retained_earnings_account not in self.equity
        ):
            raise ValueError("Wrong name for retained earnings account")

    def set_retained_earnings_account(self, account_name: str):
        if account_name in self.equity:
            self.retained_earnings_account = account_name
            return self
        else:
            raise ValueError(f"{account_name} must be in {self.equity}")

    def _flat(self):
        """Stream regular account names (without contra accounts)."""
        equity_accounts = self.equity.copy()
        if self.retained_earnings_account:
            addon = [(RetainedEarnings, [self.retained_earnings_account])]
            equity_accounts.remove(self.retained_earnings_account)
        else:
            addon = []
        return [
            (Asset, self.assets),
            (Expense, self.expenses),
            (Capital, equity_accounts),
            (Liability, self.liabilities),
            (Income, self.income),
            (IncomeSummaryAccount, [self.income_summary_account]),
        ] + addon

    def get_type(self, account_name: AccountName) -> Type[RegularAccount]:
        return [
            Class
            for Class, account_names in self._flat()
            if account_name in account_names
        ][0]

    @property
    def account_names(self):
        return [
            account_name
            for _, account_names in self._flat()
            for account_name in account_names
        ]

        # TODO: must check for duplicatre account keys
        # list all accounts

    def make_ledger(self) -> Ledger:
        ledger = make_regular_accounts(self)
        return add_contra_accounts(self, ledger)


def make_regular_accounts(chart: Chart):
    return Ledger(
        (account_name, cls())
        for cls, account_names in chart._flat()
        for account_name in account_names
    )


def add_contra_accounts(chart: Chart, ledger: Ledger) -> Ledger:
    for refers_to, (
        contra_account_names,
        target_account,
    ) in chart.contra_accounts.items():
        ledger[refers_to].netting = Netting(contra_account_names, target_account)  # type: ignore
        cls = get_contra_account_type(chart.get_type(refers_to))
        for contra_account_name in contra_account_names:
            account: Account = cls()
            ledger[contra_account_name] = account
    return ledger
