import collections
import os
from datetime import datetime
from pprint import pprint


def load_transactions(path_to_file):
    """
    Returns
           1. a tuple of named tuples with all the transactions from the passed file.
           2. a list of all the parties in the ledger
    :param path_to_file: the path to the ledger file to be processed
    """

    Transaction = collections.namedtuple(
        'Transactions',
        ['index', 'date', 'outgoing_party', 'incoming_party', 'amount_sent'])

    transactions = tuple()
    index = 0
    party_list = list()

    # Open the file and populate the named tuple: Transactions
    with open(path_to_file, 'r') as file_obj:
        for line in file_obj:
            list_items = line.split(',')
            ledger_transaction = Transaction(
                index=index,
                date=list_items[0].strip(),
                outgoing_party=list_items[1].strip(),
                incoming_party=list_items[2].strip(),
                amount_sent=float(list_items[3].strip())),
            # add the parties to a list so we can return them to make further processing easy
            if list_items[1].strip() not in party_list:
                party_list.append(list_items[1].strip())
            if list_items[2].strip() not in party_list:
                party_list.append(list_items[2].strip())

            index += 1
            transactions += ledger_transaction

    return transactions, party_list


def get_balances(party_list, transaction_tup):
    """

    Returns a tuple of named tuples containing the balance for every party
    each time their account is debited or credited
    :param transaction_tup: transaction: all the transactions loaded from file
    :param party_list: list of all parties in the ledger
    """

    Balance = collections.namedtuple('Balances',
                                     ['index', 'party', 'date', 'balance'])

    balances_tup = tuple()
    index = 0

    party_dict = {party: 0 for party in party_list}
    # Create a record for each party every time their account is debited or credited
    for record in transaction_tup:
        # here we debit by amount_sent (outgoing party)
        party_dict[record.outgoing_party] -= record.amount_sent
        party_dict[record.outgoing_party] = round(
            party_dict[record.outgoing_party], 2)
        outgoing_balance = Balance(
            index=index,
            party=record.outgoing_party,
            date=record.date,
            balance=party_dict[record.outgoing_party],
        )
        index += 1
        balances_tup += outgoing_balance,
        # here we credit by amount_sent (incoming party)
        party_dict[record.incoming_party] += record.amount_sent
        party_dict[record.incoming_party] = round(
            party_dict[record.incoming_party], 2)
        incoming_balance = Balance(index=index,
                                   party=record.incoming_party,
                                   date=record.date,
                                   balance=party_dict[record.incoming_party])
        index += 1
        balances_tup += incoming_balance,

    return balances_tup


def query_get_party_balances(balances_tup, party_str):
    """

    :return: Returns all the balances of the given party for each time their account is credited and debited
    :param balances_tup: tuple of named tuples containing the complete record of balances in the ledger
    :param party_str: name of a party to search for
    """

    party_balances_tup = tuple(
        (bal for bal in balances_tup if bal.party == party_str))

    if not party_balances_tup:
        return f'No record found for party {party_str}'

    return party_balances_tup


def query_get_latest_party_balance(balances_tup, party_str):
    """

    :param balances_tup: Balances processed from ledger file
    :param party_str: party who's balances you are searching for
    :return: The latest or current balance
    """

    party_balances_tup = tuple(
        (bal for bal in balances_tup if bal.party == party_str))

    if not party_balances_tup:
        return f'No record found for party {party_str}'

    return party_balances_tup[-1:][0][3]


def query_get_party_balance_by_date(balances_tup, party_str, date_str):
    """

    :return: The closing balance of a party on the date specified in the parameter
    :param balances_tup:
    :param party_str:
    :param date_str:
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    party_balances_dict = {
        bal.index: [datetime.strptime(bal.date, '%Y-%m-%d'), bal.balance]
        for bal in sorted(balances_tup) if bal.party == party_str
    }

    if not party_balances_dict:
        return f'No record found for party {party_str}'

    first_bal_key = min(party_balances_dict.keys())
    last_bal_key = max(party_balances_dict.keys())

    if date_obj < party_balances_dict[first_bal_key][0]:
        return 0.0
    if date_obj >= party_balances_dict[last_bal_key][0]:
        return party_balances_dict[last_bal_key][1]

    previous_date = party_balances_dict[first_bal_key][0]
    previous_val = party_balances_dict[first_bal_key][1]
    is_match = False

    for key, val in party_balances_dict.items():
        if previous_date != val[0] and is_match is True:
            return previous_val
        if date_obj == val[0]:
            is_match = True
        if val[0] > date_obj:
            return previous_val

        previous_date = val[0]
        previous_val = val[1]


if __name__ == '__main__':
    transaction, parties = load_transactions(
        os.path.join('fixtures', '1000_rows.csv'))
    balances = get_balances(parties, transaction)
    pprint(balances)
    pprint(query_get_party_balances(balances, 'Roxine'))
    latest_balance = query_get_latest_party_balance(balances, 'Roxine')
    pprint(latest_balance)
    balance_on_date = query_get_party_balance_by_date(balances, 'Roxine',
                                                      '2016-10-31')
    pprint(balance_on_date)
