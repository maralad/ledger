# ledger
### A simple python program for processing a currency transaction ledger

### In order to query the ledger for balances on a certain date or current balance you need to first run load_transactions
### then run get_balances

### This is the order...
* load transactions
    * ### transaction, parties = load_transactions(os.path.join('fixtures', '1000_rows.csv'))
* Get balances
    * ### balances = get_balances(parties, transaction)
  
* Get latest balance for a party :
    * ### print(query_get_latest_party_balance(balances, 'Roxine'))
* Get closing balance for a particular date for a party:
    * ### print(query_get_party_balance_by_date(balances, 'Roxine','2016-10-31'))
* Get all changing balances for a party
    * ### print(query_get_party_balances(balances, 'Roxine'))    
 
