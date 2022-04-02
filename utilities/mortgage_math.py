"""
Static python file, contains math functions around mortgages
"""


def calculate_down_payment(price, percent):
    """
    Calculate the down payment given a total price and percentage you want to put down
    :param price: price of the home
    :param percent: percentage you want to put down
    :return: amount that equates to that percentage
    """
    return price * (percent / 100)


def calculate_payment(home_price, down_payment, interest_rate, term):
    """
    Calculate a mortgage payment given the necessary info
    :param home_price: total home price
    :param down_payment: down payment amount
    :param interest_rate: interest rate of the loan
    :param term: LoanProgram object indicating what kind of mortgage this is
    :return: the monthly payment for this loan, given the parameters
    """
    principal = home_price - down_payment
    # Enum value of index 1 is the amount of years, so we multiply by 12 for the total number of payments over the life
    # of the loan
    payment_count = term.value[1] * 12

    # we have a test case with an interest rate of 0, so we need this conditional, easier to handle here
    if interest_rate == 0:
        return principal/payment_count

    # convert interest rate from a percent to a decimal, and then divide by 12 months in a year
    monthly_rate = (interest_rate / 100) / 12

    # Formula for a mortgage payment, has delicate order of operations
    return (principal * (monthly_rate * ((1 + monthly_rate) ** payment_count))) / \
           (((1 + monthly_rate) ** payment_count) - 1)


