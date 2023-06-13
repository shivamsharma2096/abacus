from abacus import Chart, Entry
from abacus.accounts import Asset, Capital, IncomeSummaryAccount, RetainedEarnings
from abacus.ledger import Ledger, safe_process_postings


def test_make_ledger():
    _chart = Chart(
        assets=["cash"],
        equity=["equity"],
        retained_earnings_account="re",
        income=[],
        expenses=[],
        liabilities=[],
    )
    assert _chart.ledger() == {
        "cash": Asset(debits=[], credits=[]),
        "equity": Capital(debits=[], credits=[]),
        "_profit": IncomeSummaryAccount(debits=[], credits=[]),
        "re": RetainedEarnings(debits=[], credits=[]),
    }


def test_safe_process_entries():
    _ledger = Ledger(
        {
            "cash": Asset(debits=[], credits=[]),
            "equity": Capital(debits=[], credits=[]),
        }
    )
    _, _failed = safe_process_postings(_ledger, [Entry("", "", 0)])
    assert _failed == [Entry("", "", 0)]
