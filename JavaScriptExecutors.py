"""
A module designed to circumvent some of the
shortcomings of the basic Python implementation of Selenium driver.
This module passes reusable JavaScript
snippets to the JavaScript engine powering Selenium.


Written for Python 3.6, 3.x and above
is required for type and return annotations.
-JoJo
"""

from selenium import webdriver  # Needed for type annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *  # we'll be using most of them
from selenium.webdriver.support.ui import Select
from time import sleep


def wait_for_element_clickable(
        driver: webdriver, identifier: str,
        element_type: By, time: int = 10) -> None:
    """
    Wraps the verbose syntax for SeleniumWebdriverWait... for Python bindings.
    :param driver: A webdriver object.
    :param identifier: The identifier for your element.
    :param element_type: ID, NAME, XPATH, etc.
    :param time: Time in seconds to wait before timeout.
    :return: None.
    """
    try:
        # waits for n seconds for element to be
        # clickable, raises timeout if exceeded
        WebDriverWait(driver, time).until(
            ec.element_to_be_clickable((element_type, identifier)))
    except TimeoutException:
        pass
        # Define additional errors and catch behavior here


def send_keys_to(
        driver: webdriver, identifier: str,
        element_type: By, keystrokes: str = '') -> None:
    """

    :param driver: A webdriver object.
    :param identifier: element unique identifier.
    :param element_type: NAME, ID, XPATH, etc.
    :param keystrokes: String value to send to field.
    :return: None.
    """
    # Checks to make sure we have something to send before executing
    if keystrokes != '' and keystrokes != 'None' and\
            type(keystrokes) is not None:
        # Something needs to be sent, so we will try to send it
        try:
            # clear the field first
            # Warning: If your element contains an onblur, this can trigger it
            driver.find_element(element_type, identifier).clear()
            driver.find_element(element_type, identifier)\
                .send_keys(keystrokes)

        except NoSuchElementException:
            pass
            # define errors and catch behavior here
    else:
        pass
        # define pass behavior here


def check_box_helper(
        driver: webdriver, identifier: str,
        element_type: By, check: str) -> None:
    """
    Helper method to check a checkbox. This is useful as shorthand,
    and if a box is obscured as JavaScript
    will click under the obscuring element;
    Python binding would not.
    :param driver: webdriver object.
    :param identifier: unique identifier for your element.
    :param element_type: XPATH, NAME, ID, etc
    :param check: string that decides to either check or not check element.
    :return:
    """
    if check.lower() == 'check':
        try:
            # Find checkbox
            # expose Selenium object reference to JavaScript engine
            checkbox = driver.find_element(element_type, identifier)
            driver.execute_script('arguments[0].click()', checkbox)
        except NoSuchElementException:
            pass
            # Define errors, catch behavior here
    else:
        pass
        # Define pass behavior, elif behavior here


def generic_click_helper(
        driver: webdriver, identifier: str, element_type: By) -> None:
    """
    A generic click on a desired element.
    Useful for onblurs or selecting elements.
    :param driver: webdriver object.
    :param identifier: unique element id.
    :param element_type: XPATH, NAME, ID, etc.
    :return: None.
    """

    try:
        element = driver.find_element(element_type, identifier)
        driver.execute_script('arguments[0].click()', element)
    except NoSuchElementException:
        pass
        # Define errors and catch behavior here


def radio_button_helper(
        driver: webdriver, common_id: str, unique_id: str) -> None:
    """
    Helper to deal with radio buttons which share NAME, ID attributes.
    :param driver: webdriver object.
    :param common_id: example: "@name='my_radio_button'"
    :param unique_id: example: "@value='01'"
    :return: None.
    """

    # build an xpath to locate element on page, execute through JS engine
    try:
        # Builds and executes the xpath we need.
        # Who said they were inflexible?
        driver.execute_script('arguments[0].click()', driver.find_element(
            By.XPATH, ''.join(
                ['//*[', common_id, ' and ', unique_id, ']'])))
    except NoSuchElementException:
        pass
        # Define errors and catch behaviors here


def dropdown_select_helper(
        driver: webdriver, by: By, identifier: str, value: str) -> None:
    """

    :param driver: webdriver object.
    :param by: By type.
    :param identifier: identifier for element.
    :param value: text value to search dropdown for.
    :return: None.
    """

    # make sure we're looking for something
    if value != '':
        try:
            Select(driver.find_element(by, identifier))\
                .select_by_visible_text(value)
        except NoSuchElementException:
            pass
            # Define errors and behavior here
    else:
        pass
        # Define pass behavior here


def indexed_dropdown_select_helper(
        driver: webdriver, by: By, identifier: str,
        value: str, index: int) -> None:
    """
    Looks for a given element in a dropdown menu where
    the dropdown menu id is not unique.
    This happens on JavaScript built pages
    or in bootstrap pages occasionally.
    :param driver: webdriver object.
    :param by: By type.
    :param identifier: element identifier.
    :param value: value to search for.
    :param index: index of list of non unique id dropdown list to search.
    :return:
    """
    if value != '':
        try:
            Select(
                driver.find_elements(by, identifier)[index])\
                .select_by_visible_text(value)
        except NoSuchElementException:
            pass
    else:
        pass


def wait_for_new_window(
        driver: webdriver, seconds: int = 5,
        current_win_num: int = 1) -> bool:
    """
    Waits for a new window to spawn.
    :param driver: webdriver object.
    :param seconds: max seconds before timeout, defaults to 5.
    :param current_win_num: current number of windows, defaults to 1.
    :return: None.
    """
    wait_counter = 0
    while len(driver.window_handles) == current_win_num and\
            wait_counter < seconds:
        # wait for the new window
        sleep(1)
        wait_counter += 1
        print("waiting for new window")
        if wait_counter == seconds:
            return False  # window not found
        # if not at timeout, exits loop, returns true
    return True


def switch_to_new_window(driver: webdriver, current_handle: str) -> None:
    """
    Switches driver focus to the most recently opened window.
    Assumes only one window exists before.
    :param driver: webdriver object.
    :param current_handle: current window handle
    :return:
    """
    # look through handles for the one we're not on
    desired_handle = ''
    for window in driver.window_handles:
        if window != current_handle:
            desired_handle = window

    # only one window exists
    if desired_handle == '':
        print('Only main window existed, cannot switch.')
        raise NoSuchWindowException

    # if we're here, we can switch to the new window
    driver.switch_to.window(desired_handle)


def wait_for_javascript_load(
        driver: webdriver, action, element_type: By,
        identifier: str, wait: int = 10) -> None:
    """
    Takes in an element ref to check for staleness to
    determine DOM modification or reload.
    :param driver: webdriver.
    :param action: action that causes reload of DOM or firing of JS script.
    :param element_type: By type.
    :param identifier: element id.
    :param wait: time before timeout exception.
    :return: None.
    """

    old_ref = driver.find_element(element_type, identifier)
    action  # any drivver call such
    # as driver.find_element(By.ID, 'saveButton').click()
    sleep(.5)  # hopefully avoid race condition
    print('beginning wait for page reload')
    try:
        # wait until old Selenium Object Reference is invalid
        WebDriverWait(driver, wait).until(ec.staleness_of(old_ref))
    except NoSuchElementException:
        pass
    print('Page has completed reload')
