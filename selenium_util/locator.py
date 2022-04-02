from selenium.webdriver.common.by import By


class Locator(object):
    """
    Helper class for developers to quickly define ways to locate elements, and then having a common object allows
    methods to use locators in a common way

    ...

    Attributes
    ----------
    by : By
        Selenium By locator object, the method to use to find an element
    find_with : str
        A string defining what to run with the provided By

    Methods
    -------
    as_args(self)
        Selenium methods use by, string parameters, so you can use this method with * for shorthand
    """

    def __init__(self, by: By, find_with: str):
        """
        Create a Locator
        :param by: Selenium By locator object, the method to use to find an element
        :param find_with: A string defining what to run with the provided By
        """
        self.by = by
        self.find_with = find_with

    def as_args(self):
        """
        If you want to use * shorthand to selenium methods, call *<locator>.as_args
        :return: by and find with attributes
        """
        return self.by, self.find_with
