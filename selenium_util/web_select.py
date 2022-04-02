from selenium.webdriver.support.ui import Select

from selenium_util.web_element import WebElement


class WebSelect(WebElement):
    """
    Helper class for select (drop-down) web elements

    ...

    Attributes
    ----------
    driver : webdriver
        webdriver that this page will use to interact with the web page, defined in parent class
    locator : Locator
        Locator object that defines how to find this element
    element : element
        Selenium element object for the element that was found
    select : Select
        Selenium Select object for this web element, giving us extended functionality

    Methods
    -------
    select_by_value(self, check)
        Make a selection in this select element based on html value attributes
    get_selected_value
        Return the selected <option>'s value attribute
    """

    def __init__(self, driver, locator, element=None):
        """
        Create a web select
        :param driver: web driver that will be used to interact with this element
        :param locator: how to find this element in the DOM
        :param element: If you have already found a selenium element object for this web element, specify it to prevent
        searching for it again
        """
        super().__init__(driver, locator, element)
        self.select = Select(self.element)

    def select_by_value(self, value: str):
        """
        Make a selection in this select element based on html value attributes
        :param value: html value attribute to find on an <option> and select it
        """
        self.select.select_by_value(value)

    def get_selected_value(self) -> str:
        """
        Return the selected <option>'s value attribute
        :return: a string containing the value
        """
        return self.select.first_selected_option.get_attribute("value")
