import collections
from main import *
import os
import unittest


class TestLedgerFunctions(unittest.TestCase):
    def setUp(self):

        Transactions = collections.namedtuple('Transactions', [
            'index', 'date', 'outgoing_party', 'incoming_party', 'amount_sent'
        ])

        self.transactions = (Transactions(index=0,
                                          date='2015-01-16',
                                          outgoing_party='john',
                                          incoming_party='mary',
                                          amount_sent=125.0),
                             Transactions(index=1,
                                          date='2015-01-18',
                                          outgoing_party='supermarket',
                                          incoming_party='john',
                                          amount_sent=20.0))

        self.parties = ['john', 'mary', 'supermarket']

        Balances = collections.namedtuple(
            'Balances', ['index', 'party', 'date', 'balance'])

        self.balances = (Balances(index=0,
                                  party='john',
                                  date='2015-01-16',
                                  balance=-125.0),
                         Balances(index=1,
                                  party='mary',
                                  date='2015-01-16',
                                  balance=125.0),
                         Balances(index=2,
                                  party='supermarket',
                                  date='2015-01-18',
                                  balance=-20.0),
                         Balances(index=3,
                                  party='john',
                                  date='2015-01-18',
                                  balance=-105.0))

        self.party_balances = (Balances(index=0,
                                        party='john',
                                        date='2015-01-16',
                                        balance=-125.0),
                               Balances(index=3,
                                        party='john',
                                        date='2015-01-18',
                                        balance=-105.0))

    def test_load_transactions(self):

        transactions, parties_list = load_transactions(
            os.path.join('fixtures', 'test_data.dat'))

        assert self.parties == parties_list
        assert self.transactions == transactions

    def test_load_transactions_File_Not_Found_Error(self):

        self.assertRaises(FileNotFoundError, load_transactions,
                          os.path.join('fixtures', 'rockford_file.dat'))

    def test_get_balances(self):

        balances_tup = get_balances(self.parties, self.transactions)

        assert self.balances == balances_tup

    def test_query_get_party_balances(self):

        party_balances_tup = query_get_party_balances(self.balances, 'john')

        assert self.party_balances == party_balances_tup

    def test_query_get_party_balances_with_non_existent_name(self):

        response_str = query_get_party_balances(self.balances, 'Ron Burgundy')

        assert 'No record found for party Ron Burgundy' == response_str

    def test_query_get_latest_party_balance(self):

        latest_balance_float = query_get_latest_party_balance(
            self.balances, 'john')
        assert latest_balance_float == -105.0

    def test_query_get_latest_party_balance_with_non_existent_name(self):
        response_str = query_get_latest_party_balance(self.balances,
                                                      'Ron Burgundy')

        assert 'No record found for party Ron Burgundy' == response_str

    def test_query_get_party_balance_by_date_before_any_transaction(self):

        balance_on_15 = query_get_party_balance_by_date(
            self.balances, 'john', '2015-01-15')
        assert balance_on_15 == 0.0

    def test_query_get_party_balance_by_date_first_transaction(self):

        balance_on_16 = query_get_party_balance_by_date(
            self.balances, 'john', '2015-01-16')
        assert balance_on_16 == -125.0

    def test_query_get_party_balance_by_date_between_transactions(self):

        balance_on_17 = query_get_party_balance_by_date(
            self.balances, 'john', '2015-01-17')
        assert balance_on_17 == -125.0

    def test_query_get_party_balance_by_date_on_last_day_of_transactions(self):

        balance_on_18 = query_get_party_balance_by_date(
            self.balances, 'john', '2015-01-18')
        assert balance_on_18 == -105.0

    def test_query_get_party_balance_by_date_on_day_after_transactions(self):

        balance_on_19 = query_get_party_balance_by_date(
            self.balances, 'john', '2015-01-19')
        assert balance_on_19 == -105.0

    def test_query_get_party_balance_by_date_with_non_existent_name(self):

        response_str = query_get_party_balance_by_date(self.balances,
                                                       'Ron Burgundy',
                                                       '2015-01-19')
        assert 'No record found for party Ron Burgundy' == response_str

    def test_query_get_party_balance_by_date_Value_Error(self):

        self.assertRaises(ValueError, query_get_party_balance_by_date,
                          self.balances, 'john', '20155-01-19')


if __name__ == '__main__':
    unittest.main()
