from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions


class WebElement(object):
    """
    Helper class for Selenium web elements. Using Selenium has it's drawbacks, and one is a lot of code duplication to
    do things safely, or to do things not part of the basic Selenium object.

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
    get_underling_web_element_obj
        Return the selenium element for direct use
    click
        Click on this element
    get_text
        Get the text from this element
    set_text
        Clear the text from this element and then enter new text
    get_value
        Get the value attribute from this element
    wait_for_element_to_have_text
        Wait for an element's text value to exactly match your desired value, useful to prevent race conditions
        around asserting too quickly
    wait_for_element_to_have_value
        Wait for an element's value attribute to exactly match your desired value, useful to prevent race conditions
        around asserting too quickly
    wait_for_element_to_be_clickable
        Wait for the element to be clickable (uses Selenium's expected conditions)
    wait_for_element_to_be_stale
        Wait for the element to be stale, aka no longer in to DOM (uses Selenium's expected conditions)
    """

    def __init__(self, driver, locator, element=None):
        """
        Create a WebElement object
        :param driver: the driver to use to find, and interact with this element
        :param locator: Locator object detailing how to find this element in the DOM
        :param element: If you have already found this element with a driver, pass it in to wrap it with this class. If
        you have already located it, be sure to use this parameter to not waste resources re-locating it
        """
        self.driver = driver

        if element is None:
            self.element = self.driver.find_element(locator.by, locator.find_with)
        else:
            self.element = element

    def get_underling_web_element_obj(self):
        """
        Return the selenium element for direct use
        :return: selenium web element
        """
        return self.element

    def click(self):
        """
        Click on this element
        """
        self.element.click()

    def get_text(self) -> str:
        """
        Get the text from this element
        :return: a string containing the text this element has
        """
        return self.element.text

    def set_text(self, text, press_enter=False):
        """
        Clear the text from this element and then enter new text
        :param text: the value to input into this element, will be cased to a string
        :param press_enter: after we are done entering text, do you want this method to press enter? This can trigger
        events on the web page, similar to clicking on something else (but pressing enter is more efficient)
        """
        # Selenium's element.clear() was not working on some of the elements on Zillows page, this is a common
        # problem that is solved by doing ctrl a delete yourself
        self.element.send_keys(Keys.CONTROL + "a")
        self.element.send_keys(Keys.DELETE)
        self.element.send_keys(text)

        if press_enter:
            self.element.send_keys(Keys.RETURN)

    def get_value(self) -> str:
        """
        Get the value attribute from this element
        :return: a string, holding the value that was found in the value html attribute for this element
        """
        return self.element.get_attribute("value")

    def wait_for_element_to_have_text(self, desired_text: str, timeout_in_seconds=10):
        """
        Wait for an element's text value to exactly match your desired value, useful to prevent
        race conditions around asserting too quickly
        :param desired_text: string that you want this elements text to be
        :param timeout_in_seconds: how long you are willing to wait for this element to have your desired text
        """
        try:
            WebDriverWait(self.driver, timeout_in_seconds).until(lambda the_driver: self.get_text() == desired_text)
        except TimeoutException:
            print("ELEMENT FAILED TO HAVE TEXT VALUE [" + str(desired_text) + "] within 10 seconds")

    def wait_for_element_to_have_value(self, desired_value, compare_as_floats=False, timeout_in_seconds=10):
        """
        Wait for an element's value attribute to exactly match your desired value, useful to prevent
        race conditions around asserting too quickly
        :param compare_as_floats: Pass True to compare equality AFTER casting both actual and expected to floats
        :param desired_value: string that you want this elements value attribute to be
        :param timeout_in_seconds: how long you are willing to wait for this element to have your desired value
        """
        try:
            if compare_as_floats:
                WebDriverWait(self.driver, timeout_in_seconds).until(
                    lambda the_driver: float(self.get_value()) == float(desired_value))
            else:
                WebDriverWait(self.driver, timeout_in_seconds).until(
                    lambda the_driver: self.get_value() == desired_value)
        except TimeoutException:
            print("ELEMENT FAILED TO HAVE VALUE [" + str(desired_value) + "] within 10 seconds")

    def wait_for_element_to_be_clickable(self, timeout_in_seconds=10):
        """
        Wait for the element to be clickable (uses Selenium's expected conditions)
        :param timeout_in_seconds: how long you are willing to wait
        """
        WebDriverWait(self.driver, timeout_in_seconds).until(expected_conditions.element_to_be_clickable(self.element))

    def wait_for_element_to_be_stale(self, timeout_in_seconds=10):
        """
        Wait for the element to be stale, aka no longer in to DOM (uses Selenium's expected conditions)
        :param timeout_in_seconds: how long you are willing to wait
        """
        WebDriverWait(self.driver, timeout_in_seconds).until(expected_conditions.staleness_of(self.element))
