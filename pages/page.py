from selenium.webdriver.support.wait import WebDriverWait

from selenium_util.web_checkbox import WebCheckbox
from selenium_util.web_element import WebElement
from selenium_util.web_select import WebSelect


class Page(object):
    """
    Class that represents ALL pages. Methods defined in this class will be common to every child, and thus should
    be written very generically. This class should not be instantiated directly

    ...

    Attributes
    ----------
    driver : webdriver
        webdriver that this page will use to interact with the web page

    Methods
    -------
    get_element
    get_elements
    get_element_if_exists
    get_select_element
    get_checkbox_element
    wait_for_element_to_exist
    """

    def __init__(self, driver):
        """
        Create a Page object
        :param driver: the web driver to use to interact with the web page
        """
        self.driver = driver

    def get_element(self, locator):
        """
        Get our custom web element object given a locator
        :param locator: how to find the element in the DOM
        :return: a new WebElement object
        """
        return WebElement(self.driver, locator)

    def get_element_if_exists(self, locator):
        """
        Get an element if it exists in the DOM, otherwise return None
        :param locator: how to find the element in the DOM
        :return: a new WebElement object if we found the element, otherwise None
        """
        elements = self.get_elements(locator)

        if len(elements) > 0:
            return elements[0]
        else:
            return None

    def get_elements(self, locator):
        """
        Get all elements (as our custom object) that are found using the given locator
        :param locator: how to find the element(s) in the DOM
        :return: a list of WebElements that were found
        """

        # For every element found with driver.find_elements, use map to convert them to web_element objects,
        # and then return as a list
        return list(map(lambda e: WebElement(self.driver, locator, e), self.driver.find_elements(*locator.as_args())))

    def get_select_element(self, locator):
        """
        Get an element, as our WebSelect class for additional select-specific functionality
        :param locator: how to find the element in the DOM
        :return: a new WebSelect object
        """
        return WebSelect(self.driver, locator)

    def get_checkbox_element(self, locator):
        """
        Get an element, as our WebCheckbox class for additional select-specific functionality
        :param locator: how to find the element in the DOM
        :return: a new WebCheckbox object
        """
        return WebCheckbox(self.driver, locator)

    def wait_for_element_to_exist(self, locator, timeout_in_seconds=10):
        """
        Have an element that might not exist in the DOM right when you search for it? Use this method. It is tolerant
        and will wait up until the specified timeout before throwing an exception indicating it failed to find the
        element
        :param locator: how to find the element in the DOM
        :param timeout_in_seconds: how many seconds to search for the element
        :return: a new WebElement object if we find the element, otherwise this will throw a timeout exception
        """
        return WebElement(self,
                          locator,
                          WebDriverWait(self.driver, timeout_in_seconds).until(
                              lambda the_driver: the_driver.find_element(locator.by, locator.find_with)))



