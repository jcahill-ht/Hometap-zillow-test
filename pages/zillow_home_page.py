from pages.zillow_base_page import ZillowBasePage


class ZillowHomePage(ZillowBasePage):
    """
    Class that represents the home page for Zillow, inherits from ZillowBasePage
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
    """

    '''
    ***** BEGIN LOCATORS *****
    '''

    '''
    ***** END LOCATORS *****
    '''

    def __init__(self, driver):
        """
        Create a new ZillowHomePage
        Assumes you have already navigated to this page
        :param driver: webdriver that this page will use to interact with the web page
        """
        super().__init__(driver)
