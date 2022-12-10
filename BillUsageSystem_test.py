import unittest
from decimal import Decimal
from datetime import datetime as Datetime, date as Date
from BillUsageSystem import BillUsageSystem, Bill, Customer


class BillTest(unittest.TestCase):
    def setUp(self):
        self.bill = Bill(0, 0, Date(2020, 10, 18), Decimal(50000.00))

    def tearDown(self):
        self.bill = None

    def test_when_billCreated_then_paidAmountAndPaidDateInitialStateSetCorrectly(self):
        '''
        Test when a bill is created, the PaidAmount is 0 and PaidDate is undefined (null)
        '''
        self.assertEqual(self.bill.paid_amount, Decimal(0))
        self.assertEqual(self.bill.paid_date, None)

    def test_given_billFullyPaid_when_payBill_then_paidAmountAndPaidDateSetCorrectly(self):
        '''
        Test when a bill is fully paid for, the PaidDate is set, and the PaidAmount shall be the 
        same as BillAmount.
        '''
        paid_amount = Decimal(50000.00)
        self.bill.pay_bill(paid_amount)

        self.assertEqual(self.bill.paid_amount, paid_amount)
        self.assertEqual(self.bill.paid_amount, self.bill.bill_amount)
        self.assertEqual(self.bill.paid_date, Datetime.now().date())

    def test_given_billPartiallyPaid_when_payBill_then_paidAmountAndPaidDateSetCorrectly(self):
        '''
        Test when a bill is partially paid, the PaidAmount shall
        indicate the partially paid amount, but the PaidDate shall remain undefined.
        '''
        paid_amount = Decimal(30000.00)
        self.bill.pay_bill(paid_amount)

        self.assertEqual(self.bill.paid_amount, paid_amount)
        self.assertEqual(self.bill.paid_date, None)

    def test_given_billPartiallyPaid_when_payBill_then_returnTheCorrectOutstandingAmount(self):
        '''
        Test when a bill is partially paid, the outstanding amount equals to
        BillAmount - PaidAmount.
        '''
        paid_amount = Decimal(30000.00)
        self.bill.pay_bill(paid_amount)

        self.assertEqual(self.bill.get_outstanding_amount(), Decimal(20000.00))

    def test_when_comparingTwoBillsWithIdenticalValues_then_returnTrue(self):
        first_bill = Bill(0, 0, Date(2020, 1, 18), Decimal(50000.00),
                          Decimal(50000.00), Date(2020, 5, 18))
        second_bill = Bill(0, 0, Date(2020, 1, 18), Decimal(50000.00),
                           Decimal(50000.00), Date(2020, 5, 18))

        self.assertTrue(first_bill == second_bill)

    def test_when_comparingTwoBillsWithDifferentlValues_then_returnFalse(self):
        first_bill = Bill(0, 0, Date(2020, 1, 18), Decimal(50000.00),
                          Decimal(50000.00), Date(2020, 5, 18))
        second_bill = Bill(0, 0, Date(2020, 1, 18), Decimal(50000.00),
                           Decimal(50000.00))

        self.assertTrue(first_bill != second_bill)


class BillUsageSystemTest(unittest.TestCase):
    def setUp(self):
        self.bill_usage_system = BillUsageSystem()

    def tearDown(self):
        self.bill_usage_system = None

    def test_given_mixtureOfPartialAndFullyPaidBills_when_getOutstandingBills_then_returnOnlyNotFullyPaidBills(self):
        '''
        Test fully paid for bills will not be included in outstandingBills
        '''
        outstanding_bills = self.bill_usage_system.get_outstanding_bills()
        self.assertEqual(
            outstanding_bills, [
                # Petronas
                Bill(1, 1, Date(2020, 1, 18), Decimal(50000.00)),
                Bill(2, 1, Date(2020, 2, 18), Decimal(60000.00)),
                Bill(3, 1, Date(2020, 3, 18), Decimal(70000.00),
                     Decimal(20000.00)),

                # TnG
                Bill(5, 2, Date(2020, 1, 18), Decimal(160000.00)),

                # swisslog
                Bill(6, 3, Date(2020, 1, 18), Decimal(50000.00)),
                Bill(7, 3, Date(2020, 2, 18), Decimal(60000.00)),
                Bill(8, 3, Date(2020, 3, 18), Decimal(70000.00)),

                # Docket
                Bill(10, 5, Date(2020, 1, 18), Decimal(50000.00))
            ])

    def test_given_amountNotMatchAnyBill_when_getPossibleCustomerIdsForOutstandingAmount_then_returnZeroCustomerId(self):
        '''
        Test get_possible_customer_ids_for_outstanding_amount function return zero customer ID (empty list) 
        when outstanding amount in all bills does not match the value specified by amountToMatch.
        '''
        outstanding_bills = self.bill_usage_system.get_outstanding_bills()
        possible_customer_ids = BillUsageSystem.get_possible_customer_ids_for_outstanding_amount(
            outstanding_bills, Decimal(123456.00))

        self.assertEqual(possible_customer_ids, [])

    def test_given_amountMatchSingleBill_when_getPossibleCustomerIdsForOutstandingAmount_then_returnOneCustomerId(self):
        '''
        Test get_possible_customer_ids_for_outstanding_amount function return 1 customer ID
        when value specified by amountToMatch matches a single bill
        '''
        outstanding_bills = self.bill_usage_system.get_outstanding_bills()
        possible_customer_ids = BillUsageSystem.get_possible_customer_ids_for_outstanding_amount(
            outstanding_bills, Decimal(70000.00))

        self.assertEqual(possible_customer_ids, [3])

    def test_given_amountMatchSumOfTwoBills_when_getPossibleCustomerIdsForOutstandingAmount_then_returnOneCustomerId(self):
        '''
        Test get_possible_customer_ids_for_outstanding_amount function return 1 customer ID
        when value specified by amountToMatch matches a single bill
        '''
        outstanding_bills = self.bill_usage_system.get_outstanding_bills()
        possible_customer_ids = BillUsageSystem.get_possible_customer_ids_for_outstanding_amount(
            outstanding_bills, Decimal(130000.00))

        self.assertEqual(possible_customer_ids, [3])

    def test_given_amountMatchFourBillsWithTwoBillsFromTheSameCustomer_when_getPossibleCustomerIdsForOutstandingAmount_then_returnThreeUniqueCustomerIds(self):
        '''
        Test get_possible_customer_ids_for_outstanding_amount function return 3 unique customer IDs
        when value specified by amountToMatch matches four bills where two of the bills are from the
        same company

        Petronas(id=1) has two bills with the same outstanding amount of RM 50,000, no duplication of id 1
        '''
        outstanding_bills = self.bill_usage_system.get_outstanding_bills()
        possible_customer_ids = BillUsageSystem.get_possible_customer_ids_for_outstanding_amount(
            outstanding_bills, Decimal(50000.00))

        self.assertEqual(possible_customer_ids, [1, 3, 5])

    def test_given_amountMatchOneIndividualAndOneSumOfBills_when_getPossibleCustomerIdsForOutstandingAmount_then_returnTwoCustomerIds(self):
        '''
        Test get_possible_customer_ids_for_outstanding_amount function return 2 customer IDs
        when value specified by amountToMatch matches one individual bill from 1 customer 
        AND sum of two bills from another customer 

        Petronas(id=1) has two bills with the sum of RM 160,000. The sum is the same with the amount 
        of a single bill from TnG(id=2)
        '''
        outstanding_bills = self.bill_usage_system.get_outstanding_bills()
        possible_customer_ids = BillUsageSystem.get_possible_customer_ids_for_outstanding_amount(
            outstanding_bills, Decimal(160000.00))

        self.assertEqual(possible_customer_ids, [1, 2])

    
if __name__ == '__main__':
    unittest.main()
