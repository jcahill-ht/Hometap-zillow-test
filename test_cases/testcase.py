"""
Static Test Case python file, used to setup, and teardown test cases

Author: Nick Coriale
"""

import platform
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pages.zillow_home_page import ZillowHomePage

'''
The following 3 lines of code are to figure out the current directory, move up a level and path to the 
chromedriver executable at the root of the project. This allows us to run the tests from the root directory or use the 
IDE to run 1 test at a time from the test case directory. This is at the global scope so that it is only run once, no
need to determine this multiple times
'''
this_dir = os.path.dirname(os.path.abspath(__file__))

# TODO support more browsers
executable = "chromedriver.exe"
non_windows_os = platform.system() != "Windows"
if non_windows_os:
    executable = "chromedriver"

chrome_driver_path = os.path.join(this_dir, "..", executable)
chrome_service = Service(executable_path=chrome_driver_path)


@pytest.fixture
def create_driver():
    """
    Fixture to create a driver for a test method.
    Creates it, yields it, and then closes it when the test method ends (clean run or not)
    """
    driver = webdriver.Chrome(service=chrome_service)
    yield driver
    driver.quit()


def start(driver):
    """
    Entry point to a test case, gives you the first page in the Stack
    :param driver: the driver you have created to use to interact with web pages
    :return: a new ZillowHomePage
    """
    # No point in navigating to the root url, there is a human check so we cannot interact with the page. See comment
    # in zillow_base_page.py for more detail
    # driver.get(ROOT_ZILLOW_URL)
    return ZillowHomePage(driver)
