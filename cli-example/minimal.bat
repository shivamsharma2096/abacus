call jaba chart chart.json unlink
call jaba chart chart.json touch
call jaba chart chart.json set --assets cash ar goods ppe
call jaba chart chart.json set --capital equity
call jaba chart chart.json set --retained-earnings re
call jaba chart chart.json set --liabilities ap dividend_due
call jaba chart chart.json set --income sales
call jaba chart chart.json set --expenses cogs sga
call jaba chart chart.json offset ppe depreciation
call jaba chart chart.json offset sales discounts cashback
call jaba chart chart.json list --validate

call jaba store store.json init chart.json
call jaba store store.json post --dr cash --cr equity --amount 1000
call jaba store store.json post goods cash 300
call jaba store store.json post cogs goods 250
call jaba store store.json post ar sales 440
call jaba store store.json post discounts ar 41
call jaba store store.json post cash ar 150
call jaba store store.json post sga cash 69
call jaba store store.json close
call jaba store store.json list

call jaba report store.json --balance-sheet
call jaba report store.json --income-statement
call jaba report store.json --trial-balance

call jaba balances store.json list --json

call jaba balances store.json list cash

call jaba balances store.json assert re 80

