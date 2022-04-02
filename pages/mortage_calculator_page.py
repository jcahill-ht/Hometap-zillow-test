from enum import Enum

from selenium_util.locator import Locator
from selenium.webdriver.common.by import By

from pages.mortgage_rates_page import MortgageRatesPage
from pages.zillow_base_page import ZillowBasePage
from utilities.mortgage_math import calculate_payment


class LoanPrograms(Enum):
    """
    A class to represent the loan programs that are available in the web select element

    Note to developer, if you change the structure of this enum, make sure you fix all references to it, there are some
    references to the 0th and 1st indexes of the tuple values
    """
    FIXED_30 = ("Fixed30Year", 30)
    FIXED_15 = ("Fixed15Year", 15)
    ARM_5 = ("ARM5", 5)

    @staticmethod
    def lookup(html_value):
        """
        If you have an html value and you need the corresponding enum, use this static helper method
        :param html_value: the html "value" attribute on a <option> that you would like the enum for
        :return: The enum that represents that value
        """
        for program in LoanPrograms:
            if program.value[0] == html_value:
                return program
        assert False, "Failed to find [" + html_value + "] in LoanPrograms enum, please add a new enum value"


class MortgageCalcPage(ZillowBasePage):
    """
    Class that represents the mortgage calculator web page, inherits from ZillowBasePage

    ...

    Attributes
    ----------
    driver : webdriver
        webdriver that this page will use to interact with the web page, defined in parent class
    various locators : Locator
        Locator objects that define ways to find web elements on this page, see decelerations below

    Methods
    -------
    See below - numerous methods for setting, and asserting different web elements on this page
    """

    '''
    ***** BEGIN LOCATORS *****
    '''

    _HOME_PRICE_INPUT = Locator(By.ID, "homePrice")

    _DOWN_PAYMENT_PERCENT_INPUT = Locator(By.ID, "form-1_downPaymentPercent")
    _DOWN_PAYMENT_AMOUNT_INPUT = Locator(By.ID, "form-1_downPayment")

    _TERM_SELECT = Locator(By.ID, "form-1_term")

    _RATE_INPUT = Locator(By.ID, 'rate')
    _RATE_HELP_BUTTON = Locator(By.XPATH, "//span[text()=\"More info on Interest rate\"]/ancestor::button")
    # TODO ask dev for an ID on this element, this is the best way to locate the element currently and it is decently
    #  fragile to future changes
    _SEE_CURRENT_RATES_LINK = Locator(By.XPATH, "//a[text()=\"See current rates\"]")
    _RATE_ERROR_MESSAGE = Locator(By.CSS_SELECTOR, "[class*=StyledFormHelp]")

    # TODO ask dev for an ID on this element, this is the best way to locate the element currently and it is very
    #  fragile to future changes
    _ADVANCED_BUTTON = Locator(By.XPATH, "//button[text() = \"Advanced\"]")

    _PMI_CHECKBOX = Locator(By.ID, "form-1_includePMI")
    _TAXES_INSURANCE_CHECKBOX = Locator(By.ID, "form-1_includeTaxesInsurance")

    _TAXES_INPUT = Locator(By.ID, "form-1_propertyTaxRateAnnualAmount")
    _INSURANCE_INPUT = Locator(By.ID, "annualHomeownersInsurance")

    # TODO ask dev for an ID on this element, this is the best way to locate the element currently and it is very
    #  fragile to future changes
    _PAYMENT_TEXT = Locator(By.CSS_SELECTOR, "[y=\"20\"]")

    '''
    ***** END LOCATORS *****
    '''

    def __init__(self, driver):
        """
        Create a new MortgageCalcPage
        Assumes you have already navigated to this page, and will wait for the mortgage rate input element to be
        clickable before returning your new page object to you
        :param driver: webdriver that this page will use to interact with the web page
        """
        super().__init__(driver)
        self.wait_for_element_to_exist(self._RATE_INPUT).wait_for_element_to_be_clickable()

    def set_interest_rate(self, rate):
        """
        Set the interest rate to the given value
        :param rate: rate to set, can be any type, eventually it will be casted to string for entry
        :return: self, this page object after any changes
        """
        # TODO if pressing enter bug on Interest rate input is fixed, we could make this method send the enter key
        #  and then we could remove the click of payment
        self.get_element(self._RATE_INPUT).set_text(rate)
        # click on something else to make the input field lose focus and cause a re-calculation
        self.get_element(self._PAYMENT_TEXT).click()
        return self

    def assert_interest_rate(self, expected_rate):
        """
        assert that the interest rate input has an expected value
        :param expected_rate: the rate you expect
        :return: self, this page object after any changes
        """
        actual_value = self.get_element(self._RATE_INPUT).get_value()

        assert actual_value == expected_rate, \
            "Expected interest rate to be [" + expected_rate + "] but it was [" + actual_value + "]"
        return self

    def assert_interest_rate_has_value(self):
        """
        Simple assertion, just verifies that the interest rate input has a value
        :return: self, this page object after any changes
        """
        actual_value = self.get_element(self._RATE_INPUT).get_value()

        assert float(actual_value) > 0, \
            "Expected interest rate to be a non empty value greater than 0 but it was [" + actual_value + "]"
        return self

    def assert_payment(self, expected_payment):
        """
        Assert the calculated payment on the web page is the expected value
        :param expected_payment: numeric value of what you expect the payment to be
        :return: self, this page object after any changes
        """

        # add a $ and strip off an decimal places in the expected
        expected_payment = "${:,.0f}".format(expected_payment)

        payment_element = self.get_element(self._PAYMENT_TEXT)
        # We might have just changed an input,
        # give the payment element a chance to update if it hasn't yet (race condition)
        payment_element.wait_for_element_to_have_text(expected_payment)
        actual_value = payment_element.get_text()

        print("Asserting payment is [" + expected_payment + "]")

        # note we are comparing strings here
        assert actual_value == expected_payment, \
            "Expected payment to be [" + expected_payment + "] but it was [" + actual_value + "]"
        return self

    def assert_payment_given_input_values(self):
        """
        Assertion method to assert that based on what value all of the inputs have, the displayed calculation is correct
        This method was created to specifically test that when the page loads, it loads with all of the inputs having
        a value, and that the displayed calculation is correct based on those values.

        This method should NOT be used in place of assert_payment to prevent false positives. It's better practice to
        fully calculate the payment yourself, based on what you inputted

        :return: self, this page object after any changes
        """
        price = float(self.get_element(self._HOME_PRICE_INPUT).get_value().replace(",", ""))
        down_payment = float(self.get_element(self._DOWN_PAYMENT_AMOUNT_INPUT).get_value().replace(",", ""))

        term_selected = self.get_select_element(self._TERM_SELECT).get_selected_value()
        loan_program = LoanPrograms.lookup(term_selected)

        rate = float(self.get_element(self._RATE_INPUT).get_value())

        calculated_payment = calculate_payment(price, down_payment, rate, loan_program)

        monthly_taxes = float(self.get_element(self._TAXES_INPUT).get_value().replace(",", "")) / 12
        monthly_insurance = float(self.get_element(self._INSURANCE_INPUT).get_value().replace(",", "")) / 12

        # our calculation above does not consider taxes and insurance, so now that we have scraped them off the page,
        # add them into to our expected total
        total_payment = calculated_payment + monthly_taxes + monthly_insurance

        self.assert_payment(total_payment)

        return self

    def set_home_price(self, home_price):
        """
        Set the home price input to the desired value
        :param home_price: value to enter into the input, will be casted to string
        :return: self, this page object after any changes
        """
        self.get_element(self._HOME_PRICE_INPUT).set_text(home_price)
        return self

    def set_down_payment_percent(self, percent):
        """
        Set the down payment percent input to the desired value (numeric or string accepted)
        Note your percent should not include a % if you choose to pass a string
        :param percent: desired percent (numeric or string accepted)
        :return: self, this page object after any changes
        """
        self.get_element(self._DOWN_PAYMENT_PERCENT_INPUT).set_text(percent, True)
        return self

    def assert_down_payment_percent(self, expected_percent):
        """
        Assert the down payment percent input is the expected value
        :param expected_percent: value to assert against the input, should be numeric
        :return: self, this page object after any changes
        """
        percent_element = self.get_element(self._DOWN_PAYMENT_PERCENT_INPUT)
        percent_element.wait_for_element_to_have_value(expected_percent, True)
        actual_value = percent_element.get_value()
        assert float(actual_value) == float(expected_percent), \
            "Expected down payment percent to be [" + str(expected_percent) + "] but it was [" + str(actual_value) + "]"
        return self

    def set_down_payment_amount(self, amount):
        """
        Set the down payment amount input to the desired value
        :param amount: desired value, will be casted to string before entered
        :return: self, this page object after any changes
        """
        self.get_element(self._DOWN_PAYMENT_AMOUNT_INPUT).set_text(amount, True)
        return self

    def assert_down_payment_amount(self, expected_amount):
        """
        Assert that the down payment amount has an expected value
        :param expected_amount: numeric value that you expect the input to have
        :return: self, this page object after any changes
        """

        # Add in commas to your expected amount and remove any decimal places
        expected_amount = "{:,.0f}".format(expected_amount)

        actual_value = self.get_element(self._DOWN_PAYMENT_AMOUNT_INPUT).get_value()

        # note comparing strings here
        assert actual_value == expected_amount, \
            "Expected down payment to be [" + str(expected_amount) + "] but it was [" + str(actual_value) + "]"
        return self

    def select_loan_program(self, loan_program: LoanPrograms):
        """
        Select the desired loan program in the drop-down
        :param loan_program: Enum for the value you would like selected
        :return: self, this page object after any changes
        """
        # 0th index of the loan program value is the html value attribute for that choice
        self.get_select_element(self._TERM_SELECT).select_by_value(loan_program.value[0])
        return self

    def _open_advanced(self):
        """
        Open the advanced drop down to expose the advanced options, smart enough to first determine if it is already
        open and do nothing
        """
        optional_element = self.get_element_if_exists(self._ADVANCED_BUTTON)

        if optional_element is not None:
            optional_element.click()
            self.wait_for_element_to_exist(self._TAXES_INSURANCE_CHECKBOX)

        # private method that does not refresh the page, does not need to return self

    def check_taxes_insurance(self, check):
        """
        Check or uncheck the taxes/insurance checkbox based on your desired value
        :param check: true to check the box, false to uncheck it
        :return: self, this page object after any changes
        """
        self._open_advanced()
        self.get_checkbox_element(self._TAXES_INSURANCE_CHECKBOX).check(check)
        return self

    def check_pmi(self, check):
        """
        Check or uncheck the PMI checkbox based on your desired value
        :param check: true to check the box, false to uncheck it
        :return: self, this page object after any changes
        """
        self._open_advanced()
        self.get_checkbox_element(self._PMI_CHECKBOX).check(check)
        return self

    def assert_interest_help_modal_opens_and_closes(self, click_x):
        """
        Assert that the interest help modal will open, be click-able and then assert that it closes if someone clicks
        off the modal, or clicks the close x button
        :param click_x: do you want to click the x button (True) or do you want to click off the modal (FALSE)
        :return: self, this page object after any changes
        """

        # create locator inline because it is very unlikely that any other method in this class will ever need it. If
        # that changes, move this to a class deceleration
        modal_p_loc = Locator(By.XPATH, "//p[contains(text(), \"Representative interest rates\")]")

        # Assert that the modal is not open, needed to prove we can tell it's not open
        assert len(self.driver.find_elements(*modal_p_loc.as_args())) == 0, \
            "Found modal in DOM before trying to open it, this means our next assertion cannot prove " \
            "that the modal is actually open"

        self.get_element(self._RATE_HELP_BUTTON).click()

        # Wait for the modal to open and be click-able, if either of these fail this test will fail before the assertion
        modal_p_element = self.wait_for_element_to_exist(modal_p_loc)
        modal_p_element.wait_for_element_to_be_clickable()

        # Technically covered by the conditions above, but a good sanity check
        assert len(self.driver.find_elements(*modal_p_loc.as_args())) == 1, \
            "Interest rate help modal did not open"

        if click_x:
            # create locator inline because it is very unlikely that any other method in this class will ever need it.
            # If that changes, move this to a class deceleration
            self.get_element(Locator(By.CSS_SELECTOR, "[class*=CloseButton]")).click()
        else:
            # click somewhere else to close the modal
            self.get_element(self._PAYMENT_TEXT).click()

        # Wait until the modal is no longer in the DOM
        modal_p_element.wait_for_element_to_be_stale()

        # Technically covered by the condition above, but a good sanity check to make sure it's actually gone
        assert len(self.driver.find_elements(*modal_p_loc.as_args())) == 0, \
            "Found modal after it was supposedly closed"

        return self

    def click_see_current_rates(self):
        """
        Click the see current rates link and navigate to that page
        :return: a new MortgageRatesPage as a result of navigation
        """
        # Note! opens in a new tab
        self.get_element(self._SEE_CURRENT_RATES_LINK).click()
        # close the current window
        self.driver.close()
        # switch to the new tab we opened
        self.driver.switch_to.window(self.driver.window_handles[0])
        return MortgageRatesPage(self.driver)

    def assert_interest_rate_error_message(self, expected_message):
        """
        Assert the interest rate error message
        :param expected_message: error message that you expect to be showing
        :return: self, this page object after any changes
        """
        message_p_element = self.wait_for_element_to_exist(self._RATE_ERROR_MESSAGE)
        actual_message = message_p_element.get_text()

        assert actual_message == expected_message, \
            "Expected down payment percent to be [" + expected_message + "] but it was [" + actual_message + "]"
        return self

    def assert_no_interest_rate_error_message(self):
        """
        Assert that the interest rate input does NOT have any error messages
        :return: self, this page object after any changes
        """
        potential_message_elements = self.get_elements(self._RATE_ERROR_MESSAGE)

        assert len(potential_message_elements) == 0, \
            "Unexpected error message found: " + potential_message_elements[0].get_text()
        return self

