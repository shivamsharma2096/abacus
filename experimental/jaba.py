"""
`jaba` is a minimal accounting manager.

Usage:
jaba create chart <file>
jaba chart <chart_file> add --assets <account_names>
jaba chart <chart_file> add --expenses <account_names>  
jaba chart <chart_file> add --capital <account_names>  
jaba chart <chart_file> add --liabilities <account_names>   
jaba chart <chart_file> add --income <account_names>   
jaba chart <chart_file> offset <contra_account_names> --refer <existing_account_name> --create <account_name_after_netting>   
jaba create names <name_file>
jaba names <name_file> add <var> <title> 
jaba names <name_file> list
jaba names <name_file> rename
jaba create store <store_file> [--start-balances start_balances.json] [--use-chart chart.json]
jaba store <store_file> add entry --dr dr_account --cr cr_account --amount amount
jaba store <store_file> list --all
jaba store <store_file> list [--start-balances] [--entry] [--rename-account] [--mark-event] [--income-statement-ready]
jaba store <store_file> <chart_file> trial > trial_balance.json
jaba store <store_file> <chart_file> close --contra-income --contra-expenses
jaba store <store_file> mark ready --income-statement
jaba store <store_file> <chart_file> close --income --expenses 
jaba store <store_file> mark ready --income-summary
jaba store <store_file> <chart_file> close --isa 
jaba store <store_file> mark ready --retained-earnings
jaba store <store_file> mark ready --balance-sheet
jaba store <store_file> mark ready --end-balances
jaba store <store_file> <chart_file> close --contra-asset --contra-liability --contra-capital
jaba store <store_file> mark ready --balance-sheet
jaba store <store_file> list --income-statement | jaba process <chart_file> | jaba names <name_file> rename | jaba report <chart_file> --income-statement
jaba store <store_file> list --balance-sheet | jaba process <chart_file> | jaba names <name_file> rename | jaba report <chart_file> --balance-sheet
jaba store <store_file> list --end-balances | jaba process <chart_file>  
jaba store <store_file> <chart_file> report -i > income_statement.json [--names <name_file>] 
jaba store <store_file> <chart_file> report -b > balance_sheet.json [--names <name_file>] 
jaba store <store_file> <chart_file> report -e > end_balances.json 
jaba store <store_file> <chart_file> balance <account_names>
jaba store <store_file> <chart_file> balances --all
jaba store <store_file> <chart_file> balances [(--credit | --debit)]

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
"""
jaba chart <chart_file> list [--assets] [--expenses] [--capital] [--liabilities] [--income] [--contra-accounts]
jaba store <store_file> add multiple --dr account,amount [--dr account,amount] --cr account,amount [--cr account,amount]
jaba store <store_file> list | head <n>
jaba store <store_file> list | tail <n>
"""

from docopt import docopt

if __name__ == "__main__":
    arguments = docopt(__doc__, version="pre_alpha")
    print(arguments)
