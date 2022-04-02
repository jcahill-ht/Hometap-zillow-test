from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from selenium_util.locator import Locator

# ROOT url of zillow, used to open driver to page
ROOT_ZILLOW_URL = "https://www.zillow.com/"


class ZillowBasePage(Page):
    """
    Class that represents the base page for Zillow. Any page that has the common header can extend this class to
    prevent duplication of code. Inherits from Page, and like page, should not be instantiated directly
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
    click_mortgage_calculator_link(self)
        Click the mortgage calculator link
    """

    '''
    ***** BEGIN LOCATORS *****
    '''

    _HOME_LOANS_ANCHOR = Locator(By.XPATH, "//a/span[text()=\"Home Loans\"]")
    _MORTGAGE_CALCULATOR_LINK = Locator(By.XPATH, "//a/span[text()=\"Mortgage calculator\"]")

    '''
    ***** END LOCATORS *****
    '''

    def __init__(self, driver):
        """
        Create a ZillowBasePage, a common page for other Zillow pages with the Zillow header
        :param driver: the web driver to use to interact with this page
        """
        super().__init__(driver)

    def click_mortgage_calculator_link(self):
        """
        Open the anchor for home loans and click the mortgage calculator
        :return: a new MortgageCalcPage
        """
        # TODO I wanted to load the main page and then validate that the Home Loans -> Mortgage Calculator link is
        #  functional but there is a human check to enter the first page. Talk to dev about QA's options. Instead we
        #  will directly navigate to the url. NOTE IF THIS IS CHANGED, YOU NEED TO CHANGE test case's start method to
        #  navigate to the root url again (currently commented out)
        # home_loans_anchor = self.driver.find_element(self._HOME_LOANS_ANCHOR.by, self._HOME_LOANS_ANCHOR.find_with)
        # mortgage_calculator_link = self.driver.find_element(*self._MORTGAGE_CALCULATOR_LINK.as_args())
        #
        # ActionChains(self.driver).move_to_element(home_loans_anchor).click(mortgage_calculator_link).perform()

        # work around because the main page has human detection
        self.driver.get(ROOT_ZILLOW_URL + "mortgage-calculator/")

        # import here because if we import at the top of the class we have a circular dependency. Let the two python
        # files be interpreted first, then when this method is called we are safe to do this import at run time
        from pages.mortage_calculator_page import MortgageCalcPage
        return MortgageCalcPage(self.driver)
