from selenium.webdriver.common.by import By

from pages.zillow_base_page import ZillowBasePage
from selenium_util.locator import Locator


class MortgageRatesPage(ZillowBasePage):
    """
    Class that represents the mortgage rates web page, inherits from ZillowBasePage
    TODO further define this class, only a simple stub for now

    ...

    Attributes
    ----------
    driver : webdriver
        webdriver that this page will use to interact with the web page, defined in parent class
    various locators : Locator
        Locator objects that define ways to find web elements on this page, see decelerations below

    Methods
    -------
    assert_intro_span(self)
        Assertion method to prove that something on the page actually loaded
    """

    '''
    ***** BEGIN LOCATORS *****
    '''

    _INTRO_SPAN = Locator(By.XPATH, "//span[text()=\"Compare Today's Mortgage Rates\"]")

    '''
    ***** END LOCATORS *****
    '''

    def __init__(self, driver):
        """
        Create a new MortgageRatesPage
        Assumes you have already navigated to this page, and will wait for the intro span element to be
        clickable before returning your new page object to you
        :param driver: webdriver that this page will use to interact with the web page
        """
        super().__init__(driver)
        self.wait_for_element_to_exist(self._INTRO_SPAN).wait_for_element_to_be_clickable()

    def assert_intro_span(self):
        """
        Assert that the main span at the top of the page has the expected text
        :return: self, this page object after any changes
        """
        span_text = self.get_element(self._INTRO_SPAN).get_text()

        assert span_text == "Compare Today's Mortgage Rates"

        return self
