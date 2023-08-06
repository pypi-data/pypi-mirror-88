from enum import Enum

import selenium
from appium.webdriver.common.touch_action import TouchAction
import time
TIME_OUT_PERIOD_TAP = 15.0
TIME_OUT_PERIOD_SWIPE = 20.0


feature_names = ['Add / Drop Classes', 'AED Locator', 'Alumni Connect', 'BYU Homepage', 'BYU Speeches', 'Calendars', 'Campus Buildings', 'Campus Cameras', 'Campus Maps', 'Campus Operators', 'Campus Shuttles', 'Class Rolls', 'Copyright', 'Cougar Cash', 'Counseling Services', 'Dining Account', 'Dining Locations', 'Dining Mobile Ordering', 'Enrollment Services', 'Galleries', 'ID Card', 'IT Tech Support', 'Job Openings', 'Lab Computers', 'Learning Suite', 'Locker Rental', 'My Book List', 'My Classes', 'My Finals Schedule', 'My Financial Center', 'myBYU', 'Off Campus Housing', 'Parking', 'Person Directory', 'Printers', 'Reg Permission-To-Add', 'Restrooms', 'ROC Pass', 'SafeWalk', 'Salt Lake Center', 'Sick/Vacation Balances', 'TA Lab Check In', 'Testing Center', 'Transcripts', 'University Class Schedule', 'Vending', 'Y-Message', 'Y-Serve', 'Y-Time']

class TimeOutException(Exception):
    def __init__(self, elem_id, time_elapsed=float(TIME_OUT_PERIOD_TAP)):
        self.id = elem_id
        self.time_elapsed = time_elapsed
        self.message = f"TIME_OUT_ERROR || Unable to locate '{elem_id}'," \
                       f" {time_elapsed} seconds passed without finding it."
        super().__init__(self.message)


class LocatingError(Exception):
    def __init__(self, selector, name):
        self.selector = selector
        self.name = name
        self.message = f"LOCATING ERROR || Could not locate {name} with the {selector} selector."
        super().__init__(self.message)


class LogInError(Exception):
    def __init__(self):
        self.message = f"LOG_IN : Error trying to login. Check logs."
        super().__init__(self.message)


class Direction(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4


def wait(seconds):
    time.sleep(seconds)


def shorten_name(name, char_limit=30):
    temp_name = name
    if len(name) > char_limit:
        temp_name = name[0:char_limit] + '...'
    return temp_name

#
#
# Helper functions, do not use outside


def _find_the_identifier(elements, identifier):
    desired_button = None
    print(f'Looking for {identifier} among the elements...')
    for elem in elements:
        # This is just to debug  when selecting multiple elements
        # print(f'\tFound \'{elem.text}\'')
        if elem.text == identifier:
            desired_button = elem
            break
    else:
        return 1
    # print(f'Found {identifier}.')
    return desired_button


def _find_element(app_driver, selector, name, multiple_elements):
    element = 1
    if selector == 'access':
        if multiple_elements:
            element = app_driver.find_elements_by_accessibility_id(name)
        else:
            element = app_driver.find_element_by_accessibility_id(name)
    elif selector == 'class':
        if multiple_elements:
            element = app_driver.find_elements_by_class_name(name)
        else:
            element = app_driver.find_element_by_class_name(name)
    elif selector == 'id':
        if multiple_elements:
            element = app_driver.find_elements_by_id(name)
        else:
            element = app_driver.find_element_by_id(name)
    else:
        element = None
    return element


def _driver_element_locator(app_driver, selector, name, identifier):
    multiple_elements = False
    if identifier is not None:
        multiple_elements = True
    element = _find_element(app_driver, selector, name, multiple_elements)
    if element is None:
        print('***Specify a selector!')
        return 1
    if multiple_elements:
        element = _find_the_identifier(element, identifier)
    return element


# Helper functions
#
#

def locate_element(app_driver, selector, name, identifier=None, err_if_not_found=False):
    element = 1
    try:
        temp_name = shorten_name(name)
        if identifier is not None:
            temp_name = shorten_name(identifier)
        print('Locating ' + temp_name + '.')
        element = _driver_element_locator(app_driver, selector, name, identifier)
        if element != 1:
            print(f'Element {temp_name} found!\n')
        elif err_if_not_found:
            print(f'Couldn\'t find the <{temp_name}><{identifier}> element, raising error.')
            raise LocatingError(selector, name)
    except selenium.common.exceptions.NoSuchElementException:
        print(f'Could not find the element {temp_name} using a {selector} selector.')
    return element  # should return a 1 if no element found, otherwise returns the element


def time_out_tracker(time_start, time_elapsed, name, for_swipe=False):
    time_out = TIME_OUT_PERIOD_TAP
    if for_swipe:
        time_out = TIME_OUT_PERIOD_SWIPE
    if time_start + time_out < time_elapsed:
        raise TimeOutException(name, round((time_elapsed - time_start), 1))
    return time.time()


def touch_by_access_id(app_driver, accessibility_id, conditional=False, swipe_dir=False, for_ios=False):
    button = wait_by_selector(app_driver, accessibility_id, "access", None, swipe_dir, for_ios, conditional)
    if button != 1:
        button.click()


def touch_by_id(app_driver, elem_id, name=None, conditional=False, swipe_dir=False, for_ios=False):
    button = wait_by_selector(app_driver, elem_id, 'id', name, swipe_dir, for_ios, conditional)
    if button != 1:
        button.click()


def touch_by_class(app_driver, class_name, name=None, conditional=False, swipe_dir=False, for_ios=False):
    button = wait_by_selector(app_driver, class_name, 'class', name, swipe_dir, for_ios, conditional)
    if button != 1:
        button.click()


def touch_xy(app_driver, x_pos, y_pos):
    TouchAction(app_driver).tap(x=x_pos, y=y_pos).perform()


# a scale of 1.5 will yield a powerful scroll, where 1 will scroll the screen slightly
# avoid going higher than 1.5 to avoid the scroll not registering, as the coordinates
# may run off screen or into headers. Best to scale from 1 - 1.5
def swipe(app_driver, scroll_direction, with_stop=False, scale=1):
    window_dimensions = app_driver.get_window_size()
    x_pos1 = window_dimensions['width'] / 2
    y_pos1 = window_dimensions['height'] / 2
    x_pos2 = 0
    y_pos2 = 0
    actions = TouchAction(app_driver)
    if scroll_direction == Direction.DOWN:
        y_pos1 = y_pos1 * scale
        x_pos2 = x_pos1
        y_pos2 = y_pos1 / (2 * scale)
    elif scroll_direction == Direction.UP:
        y_pos1 = y_pos1 / scale
        x_pos2 = x_pos1
        y_pos2 = y_pos1 * (1.5 * scale)
    elif scroll_direction == Direction.LEFT:
        x_pos1 = x_pos1 / scale
        y_pos2 = y_pos1
        x_pos2 = x_pos1 * (1.5 * scale)
    elif scroll_direction == Direction.RIGHT:
        x_pos1 = x_pos1 * scale
        y_pos2 = y_pos1
        x_pos2 = x_pos1 / (2 * scale)
    if x_pos2 != 0:
        if with_stop:
            actions.press(x=x_pos1, y=y_pos1).wait(int(200 / scale)).move_to(x=x_pos2, y=y_pos2)\
                .release().perform().wait(600).press(x=x_pos1, y=y_pos1)
            # Possibly adding a release  after press?         ^^HERE  - '.wait(10).release()'
        else:
            actions.press(x=x_pos1, y=y_pos1).wait(int(350 / scale)).move_to(x=x_pos2, y=y_pos2)\
                .release().perform()
    else:
        print('**** passed in invalid argument to scroll function.\n' + scroll_direction + ' is not a valid input.')


# Will wait until the given ID is found. If nothing is found according #
# to the given params, it will timeout after TIME_OUT_PERIOD_TAP #
def wait_by_selector(app_driver, element_id, selector, name=None, swipe_dir=False, swipe_ios=False, conditional=False):
    iteration = 0
    log_per_iteration = 70
    if swipe_dir:
        log_per_iteration = 2
    button_visible = False
    time_start = time.time()
    time_elapsed = time.time()
    temp_name = shorten_name(element_id)
    element = 1
    while not button_visible:
        try:
            time_elapsed = time_out_tracker(time_start, time_elapsed, temp_name, swipe_dir)
            # if no element is found, returns a 1
            element = locate_element(app_driver, selector, element_id, name, False)
            if element == 1:
                raise selenium.common.exceptions.StaleElementReferenceException
            button_visible = True
        except selenium.common.exceptions.StaleElementReferenceException:
            iteration += 1
            if (time.time() - time_start >= 5) and conditional:
                print(f'\nLooked for {temp_name} unsuccessful, but conditional. Continuing test...')
                return element
            if iteration == log_per_iteration:
                iteration = 0
                print(f'Locating {temp_name} element. {round((time_elapsed - time_start), 1)} '
                      f'/ {TIME_OUT_PERIOD_TAP} seconds until timeout.')
                if swipe_dir:
                    print('Swiping ' + swipe_dir)
            if swipe_dir:
                swipe(app_driver, swipe_dir, swipe_ios)
            wait(.1)
        except TimeOutException as e:
            # Should not need this line of code because of first if in first except block
            # if conditional:
            #     print(f'||Time out reached, skipping command <{element_id}>, <{selector}>, <{name}>')
            #     button_visible = True
            raise e
    return element


def explore_swipe(driver, feature_name):
    button_displayed = False
    time_start = time.time()
    time_elapsed = time.time()
    feature_button = 1
    while not button_displayed:
        feature_button = locate_element(driver, 'access', feature_name)
        time_elapsed = time_out_tracker(time_start, time_elapsed, feature_name, True)
        if feature_button == 1:
            print('\tBut not visible\tSwiping...\n')
            swipe(driver, Direction.DOWN, True)
        elif not feature_button.is_displayed():
            print('\tBut not visible\tSwiping...\n')
            swipe(driver, Direction.DOWN, True)
        else:
            button_displayed = True
    print('Clicking on feature.')
    feature_button.click()


def ios_wait_for_successful_login(driver):
    button_visible = False
    time_start = time.time()
    time_elapsed = time.time()
    while not button_visible:
        try:
            time_elapsed = time_out_tracker(time_start, time_elapsed, "Logged in...")
            # if no element is found, returns a 1
            elements = driver.find_elements_by_class_name("XCUIElementTypeStaticText")
            for elem in elements:
                if elem.text[0:9] == "Logged in":
                    button_visible = True
                    return True
            else:
                raise selenium.common.exceptions.StaleElementReferenceException
        except selenium.common.exceptions.StaleElementReferenceException:
            pass
