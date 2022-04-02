"""
Test cases for the Mortgage Calculator

This file contains the test cases for the Mortgage Calculator. There are acceptance tests, end to end tests negative
tests.

Author: Nick Coriale
"""


from pages.mortage_calculator_page import LoanPrograms

# Not directly invoked so the IDE thinks this import is unused which is not true, pytest is using it
# noinspection PyUnresolvedReferences
from test_cases.testcase import create_driver, start
from utilities.mortgage_math import calculate_payment, calculate_down_payment

# $300,000 with 20% down for 30 years are the default values in the inputs when the page loads
default_home_price = 300000
default_down_payment_percent = 20
default_down_payment = calculate_down_payment(default_home_price, default_down_payment_percent)


def test_default_interest_rate(create_driver):
    """
    Test that on page load there is a interest rate in the input, and a correct calculation is made given the values of
    all of the inputs on the page
    :param create_driver: fixture to create a web driver, found in testcase.py
    """
    start(create_driver)\
        .click_mortgage_calculator_link()\
        .assert_interest_rate_has_value()\
        .assert_payment_given_input_values()


def test_five_percent_interest_rate(create_driver):
    """
    Test that a 5% interest rate gives the correct calculation (with the default values on the page and
    taxes/insurance disabled)
    :param create_driver: fixture to create a web driver, found in testcase.py
    """

    price = default_home_price
    down_payment = default_down_payment
    rate = 5
    calculated_payment = calculate_payment(price, down_payment, rate, LoanPrograms.FIXED_30)

    start(create_driver) \
        .click_mortgage_calculator_link() \
        .set_interest_rate(rate)\
        .check_taxes_insurance(False)\
        .assert_payment(calculated_payment)


def test_million_dollar_home(create_driver):
    """
    Test that a million dollar home with 40% down at 2.44% interest gives the correct calculation.
    Does disable taxes and insurance
    :param create_driver: fixture to create a web driver, found in testcase.py
    """

    price = 1000000
    down_pay_percent = 40
    calculated_down_payment = calculate_down_payment(price, down_pay_percent)
    rate = 2.44
    calculated_payment = calculate_payment(price, calculated_down_payment, rate, LoanPrograms.FIXED_30)

    start(create_driver) \
        .click_mortgage_calculator_link() \
        .set_home_price(price)\
        .set_down_payment_percent(down_pay_percent)\
        .assert_down_payment_amount(calculated_down_payment)\
        .set_interest_rate(rate)\
        .check_taxes_insurance(False)\
        .assert_payment(calculated_payment)


def test_15_year_fixed(create_driver):
    """
    Test that a 150,000 dollar home with 2000 down for 15 years at 0% interest gives the correct calculation.
    Does disable taxes and insurance, and PMI (because down payment is less than 20%)
    :param create_driver: fixture to create a web driver, found in testcase.py
    """

    price = 150000
    down_payment = 2000
    down_pay_percent = (down_payment/price) * 100
    term = LoanPrograms.FIXED_15
    rate = 0
    calculated_payment = calculate_payment(price, down_payment, rate, term)

    start(create_driver) \
        .click_mortgage_calculator_link() \
        .set_home_price(price)\
        .set_down_payment_amount(down_payment)\
        .assert_down_payment_percent(down_pay_percent)\
        .select_loan_program(term)\
        .set_interest_rate(rate) \
        .check_taxes_insurance(False)\
        .check_pmi(False)\
        .assert_payment(calculated_payment)


def test_interest_rate_help(create_driver):
    """
    Test that the help modal can be opened and closed
    :param create_driver: fixture to create a web driver, found in testcase.py
    """
    start(create_driver) \
        .click_mortgage_calculator_link() \
        .assert_interest_help_modal_opens_and_closes(False) \
        .assert_interest_help_modal_opens_and_closes(True)


def test_see_current_rates_link(create_driver):
    """
    Test that the current rates link goes to a page that loads
    :param create_driver: fixture to create a web driver, found in testcase.py
    """
    start(create_driver) \
        .click_mortgage_calculator_link() \
        .click_see_current_rates()\
        .assert_intro_span()


def test_greater_than_equal_to_100(create_driver):
    """
    Test that 100 is a valid interest rate with a correct calculation, and then test that 101 gives an error on the
    input
    Uses default page values and disables taxes/insurance
    :param create_driver: fixture to create a web driver, found in testcase.py
    """
    price = default_home_price
    down_payment = default_down_payment
    rate = 100
    calculated_payment = calculate_payment(price, down_payment, rate, LoanPrograms.FIXED_30)

    start(create_driver) \
        .click_mortgage_calculator_link() \
        .set_interest_rate(rate) \
        .check_taxes_insurance(False) \
        .assert_payment(calculated_payment)\
        .assert_no_interest_rate_error_message()\
        .set_interest_rate(rate + 1)\
        .assert_interest_rate_error_message("Rate must be less than or equal to 100")


def test_less_than_equal_to_0(create_driver):
    """
    Test that 0 is a valid interest rate with a a correct calculation, and then test that -1 gives an error on the input
    Uses default page values and disables taxes/insurance
    :param create_driver: fixture to create a web driver, found in testcase.py
    """
    price = default_home_price
    down_payment = default_down_payment
    rate = 0
    calculated_payment = calculate_payment(price, down_payment, rate, LoanPrograms.FIXED_30)

    start(create_driver) \
        .click_mortgage_calculator_link() \
        .set_interest_rate(rate) \
        .check_taxes_insurance(False) \
        .assert_payment(calculated_payment)\
        .assert_no_interest_rate_error_message()\
        .set_interest_rate(rate - 1)\
        .assert_interest_rate_error_message("Rate must be greater than or equal to 0")


def test_empty_input_message(create_driver):
    """
    Test that leaving the interest rate empty shows an error on the input
    :param create_driver: fixture to create a web driver, found in testcase.py
    """
    start(create_driver) \
        .click_mortgage_calculator_link() \
        .set_interest_rate("") \
        .assert_interest_rate_error_message("Invalid value")


def test_non_numeric_error_message(create_driver):
    """
    Test that entering a non numeric value for the interest rate shows an error on the input
    :param create_driver: fixture to create a web driver, found in testcase.py
    """
    start(create_driver) \
        .click_mortgage_calculator_link() \
        .set_interest_rate("ABC") \
        .assert_interest_rate_error_message("'ABC' is not a valid number")
