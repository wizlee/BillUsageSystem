import itertools
import random
from decimal import Decimal
from datetime import datetime as Datetime, date as Date


class Customer:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Bill:
    def __init__(self, id, customer_id, bill_date, bill_amount,
                 paid_amount=Decimal(0), paid_date=None):
        self.id = id
        self.customer_id = customer_id
        self.bill_date = bill_date
        self.bill_amount = bill_amount
        self.paid_amount = paid_amount
        self.paid_date = paid_date

    def __eq__(self, other):
        if isinstance(other, Bill):
            return self.id == other.id and \
                self.customer_id == other.customer_id and \
                self.bill_date == other.bill_date and \
                self.bill_amount == other.bill_amount and \
                self.paid_amount == other.paid_amount and \
                self.paid_date == other.paid_date
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def pay_bill(self, paid_amount, paid_date=Datetime.now().date()):
        if self.bill_amount >= paid_amount:
            self.paid_amount = paid_amount
        else:
            # for simplicity, a more realistic handling will be to credit
            # the extra amount into the customer's account
            self.paid_amount = self.bill_amount

        if self.bill_amount == paid_amount:
            self.paid_date = paid_date

    def get_outstanding_amount(self):
        if self.paid_date:
            return None
        else:
            return self.bill_amount - self.paid_amount


class BillUsageSystem:
    '''
    Main function of this simplified Bill Usage System is get_possible_customer_ids_for_outstanding_amount
    that can return list of possible customers when an amount is keyed-in. 

    The rest of the code are helpers to illustrate the usage by providing the mock customers and bills data
    '''

    def __init__(self):
        self.customers = BillUsageSystem.create_customer_list()
        self.bills = BillUsageSystem.create_bills()

    @staticmethod
    def create_customer_list():
        return [
            Customer(0, "HealthMetrics"),
            Customer(1, "Petronas"),
            Customer(2, "TnG"),
            Customer(3, "swisslog"),
            Customer(4, "IHM"),
            Customer(5, "Docket")
        ]

    @staticmethod
    def create_bills():
        return [
            # HealthMetrics
            Bill(0, 0, Date(2020, 1, 18), Decimal(50000.00),
                 Decimal(50000.00), Date(2020, 5, 18)),  # fully paid

            # Petronas
            Bill(1, 1, Date(2020, 1, 18), Decimal(50000.00)),
            Bill(2, 1, Date(2020, 2, 18), Decimal(60000.00)),
            Bill(3, 1, Date(2020, 3, 18), Decimal(70000.00),
                 Decimal(20000.00)),
            Bill(4, 1, Date(2020, 4, 18), Decimal(80000.00),
                 Decimal(80000.00), Date(2020, 8, 18)),  # fully paid

            # TnG
            Bill(5, 2, Date(2020, 1, 18), Decimal(160000.00)),

            # swisslog
            Bill(6, 3, Date(2020, 1, 18), Decimal(50000.00)),
            Bill(7, 3, Date(2020, 2, 18), Decimal(60000.00)),
            Bill(8, 3, Date(2020, 3, 18), Decimal(70000.00)),

            # IHM
            Bill(9, 4, Date(2020, 1, 18), Decimal(50000.00),
                 Decimal(50000.00), Date(2020, 6, 18)),  # fully paid

            # Docket
            Bill(10, 5, Date(2020, 1, 18), Decimal(50000.00))
        ]

    def get_outstanding_bills(self):
        '''
        Returns a list of outstanding bills, fully paid bills will not
        be included in the returned list
        '''
        return [bill for bill in self.bills if bill.get_outstanding_amount()]

    @staticmethod
    def get_possible_customer_ids_for_outstanding_amount(outstanding_bills, amount_to_match):
        '''
        Returns zero, one or multiple customer IDs that may have one or more bills with sum of
        outstanding amount matching the value specified by amount_to_match.
        '''
        customer_ids = []

        # build outstanding_amounts_dict to temporarily contains only the
        # outstanding amount without the sums
        outstanding_amounts_dict = BillUsageSystem.sort_outstanding_amount_by_customer(
            outstanding_bills)

        for customer_id in outstanding_amounts_dict:
            # override value with its original items and all combinations of their sum
            outstanding_amounts_dict[customer_id] = BillUsageSystem.create_list_with_combination_sum_of_all_items(
                outstanding_amounts_dict[customer_id])

            if amount_to_match in outstanding_amounts_dict[customer_id]:
                customer_ids.append(customer_id)

        return customer_ids

    @staticmethod
    def sort_outstanding_amount_by_customer(outstanding_bills):
        outstanding_amount_by_customer = {}
        for bill in outstanding_bills:
            outstanding_amount = bill.get_outstanding_amount()
            if bill.customer_id in outstanding_amount_by_customer:
                outstanding_amount_by_customer[bill.customer_id].append(
                    outstanding_amount)
            else:
                outstanding_amount_by_customer[bill.customer_id] = [
                    outstanding_amount]
        return outstanding_amount_by_customer

    @staticmethod
    def create_list_with_combination_sum_of_all_items(input_list):
        '''
        Return a list with its original items and the combination sum of all items

        Example:
        Given a list of [1, 2, 3]
        this function will return [1, 2, 3, 4, 5, 6]
        '''
        output_list = []
        for L in range(1, len(input_list)+1):
            for subset in itertools.combinations(input_list, L):
                if sum(list(subset)) not in output_list:
                    output_list.append(sum(list(subset)))
        return output_list

    def get_customer_name(self, id):
        return [customer.name for customer in self.customers if customer.id == id]
