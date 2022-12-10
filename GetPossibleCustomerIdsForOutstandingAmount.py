import itertools
from BillUsageSystem import Bill


def get_possible_customer_ids_for_outstanding_amount(outstanding_bills, amount_to_match):
    '''
    Returns zero, one or multiple customer IDs that may have one or more bills with sum of
    outstanding amount matching the value specified by amount_to_match.
    '''
    customer_ids = []

    # build outstanding_amounts_dict to temporarily contains only the
    # outstanding amount without the sums
    outstanding_amounts_dict = sort_outstanding_amount_by_customer(
        outstanding_bills)

    for customer_id in outstanding_amounts_dict:
        # override value with its original items and all combinations of their sum
        outstanding_amounts_dict[customer_id] = create_list_with_combination_sum_of_all_items(
            outstanding_amounts_dict[customer_id])

        if amount_to_match in outstanding_amounts_dict[customer_id]:
            customer_ids.append(customer_id)

    return customer_ids


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


def create_list_with_combination_sum_of_all_items(input_list):
    """
    Return a list with its original items and the combination sum of all items

    Example:
    Given a list of [1, 2, 3]
    this function will return [1, 2, 3, 4, 5, 6]
    """
    output_list = []
    for L in range(1, len(input_list)+1):
        for subset in itertools.combinations(input_list, L):
            if sum(list(subset)) not in output_list:
                output_list.append(sum(list(subset)))
    return output_list
