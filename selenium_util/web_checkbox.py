from selenium_util.web_element import WebElement


class WebCheckbox(WebElement):
    """
    Helper class for checkbox web elements

    ...

    Attributes
    ----------
    driver : webdriver
        webdriver that this page will use to interact with the web page, defined in parent class
    locator : Locator
        Locator object that defines how to find this element
    element : element
        Selenium element object for the element that was found

    Methods
    -------
    check(self, check)
        Check or uncheck this checkbox
    """

    def __init__(self, driver, locator, element=None):
        """
        Create a web checkbox
        :param driver: web driver that will be used to interact with this element
        :param locator: how to find this element in the DOM
        :param element: If you have already found a selenium element object for this web element, specify it to prevent
        searching for it again
        """
        super().__init__(driver, locator, element)

    def check(self, check):
        """
        Check or uncheck this checkbox, does nothing if the checkbox is already in the desired state
        :param check: True to check the checkbox, False to un-check
        """
        current_state = self.element.is_selected()
        if current_state != check:
            self.element.click()
