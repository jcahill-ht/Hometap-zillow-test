# Hometap-zillow-test

This project serves as the start of a test suite for Zillow's website https://www.zillow.com.

Currently the suite is focused around testing the mortgage calculator located at https://www.zillow.com/mortgage-calculator/ but was designed with expansion in mind so that it eventually could test all of Zillow.

There are numerous TODO's throughout the project that indicate were expansion would occur, and where bugs/issues with the web page are causing issues in the test suite

## Installation
*Note I created, and ran this project in a Windows Environment. These necessary install steps, and the act of running the project should work in a Linux based environment as well, but I was not able to test that*

1. Install Python, this project was developed with Python 3.8.2 but newer versions should work fine. If in Windows, I strongly suggest putting python on your path.
2. Upgrade pip to the latest version with:
```bash
python -m pip install --upgrade pip
```
Not having the most up to date pip can cause issues installing the next packages
3. Install the pytest package
```bash
python -m pip install -U pytest
```
4. Install the selenium package
```bash
python -m pip install selenium
```
5. Install or Update Chrome. The included Chromedriver was written for Chrome version 100+.
It is possible that a new version of Chrome could exist when you go to run this project, please check your computers chrome version and replace the chromedriver in this project with the correct driver from https://chromedriver.chromium.org/downloads

## Running The Tests

1. Open a terminal at the root level of the project and run:
```bash
pytest -s
```
The -s is not required, but it will put system out prints in chronological order with the tests instead of all at the end in the test results

## Current Status and Future Work

At the time of upload, all of the 10 test cases were passing. However due to the nature of web testing, it is possible that Zillow could change some html or javascript that would break 1 or more of these tests. Please let me know if any of the test
cases begin to fail.

As for the future of this code base, here is what I would want to do:

- Screenshots - It can be very hard to debug test failures at times, and screenshots play a pivotal role in diagnosing test failures
- Logging, at various levels, INFO, DEBUG, WARN, ERROR etc. - As it stands now this test suite is small and simple, but at large scale failures would be difficult to debug without logging, especially for new users to the system or code base
- Make test suite concurrent - At only 10 tests, this suite runs in less than two minutes, but as more are added concurrent testing would be needed to be able to run the tests in a timely manner. This could be done with `pytest-xdist`
- Drive test cases with Data, example from JSON file, testing tool or database - Code bases can be smaller and simpler if they are generically designed to be fed data for test cases from an outside source.
If running lots of pre-made test cases through the calculator was desired, having a data file/tool/database to drive a test method would simplify the test code, and make adding new test cases much easier (and possible to those not familiar with the code base)
- Interface with reporting tool - Starting a new framework and running it on your machine is perfectly fine, but you will quickly need a way to automate running those test cases, collecting and distributing the results, and looking at the history of the test results for analysis
- Different browsers - I started this project with the chromedriver because I have chrome on my PC, however it is certainly not the only browser and any serious test suite needs to use Edge, Firefox, Chrome and Safari at minimum (unless requirements of the system dictate otherwise).
This is not a difficult task as the Selenium project has a goal to make it easy. I would need to download the different drivers, and modify testcase.py to be fed a desired driver, or prompt for the tester for their browser choice, the page objects and test them-selves should not change.

Problems that could arise using this code base:
- If more test cases are added to test_mortgage_calc.py it may need to be split up into multiple python files. In my professional opinion tests should be kept under 5 minutes of execution time whenever possible, one reason being it will save the QA developers hours of debugging time every year
- In a Page Object Model framework like I have started, the Page objects can become very large files if they represent complicated web pages. This is a difficult problem to solve due to the chain nature of the framework, but can be helped by using as much inheritance as possible and creating static classes with supporting methods