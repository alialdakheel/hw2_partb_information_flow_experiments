import os
import sys
import time
import logging
from automation import CommandSequence, TaskManager
from automation.Commands.utils.webdriver_utils import wait_until_loaded
from selenium.webdriver.common.keys import Keys

from pprint import pprint

NUM_BROWSERS = 1
site = "https://www.google.com"
query = "pie"
number_of_clicks = 6

# Loads the default manager params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

for i in range(NUM_BROWSERS):
    # Record Navigations
    browser_params[i]['navigation_instrument'] = True
    # Launch headless
    browser_params[i]['display_mode'] = 'headless'

cwd = os.getcwd() + "/temp"
manager_params['data_directory'] = cwd
manager_params['log_directory'] = cwd

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
logger_params = {
        "log_level_console": logging.CRITICAL
        }
manager = TaskManager.TaskManager(
        manager_params,
        browser_params,
        logger_kwargs=logger_params
        )

# Define command sequence
command_sequence = CommandSequence.CommandSequence(
    site, reset=True,
    callback=lambda success, val=site:
    print("CommandSequence {} done".format(val))
    )

command_sequence.get(sleep=3, timeout=60)

def search_and_visit(query, n, **kwargs):
    driver = kwargs['driver']
    input_elem = driver.find_element_by_name("q")
    print(f"searching: {query}  ...")
    input_elem.send_keys(query)
    input_elem.submit();
    time.sleep(1)
    wait_until_loaded(driver, 300)

    if n > 10: raise Exception("Choose samller n")
    for i in range(1, n+1):
        h_elem = driver.find_element_by_xpath(
                f"//div[@class='g'][{i}]/div[@class='rc']/div[@class='r']//h3"
                )
        a_elem = driver.find_element_by_xpath(
                f"//div[@class='g'][{i}]/div[@class='rc']/div[@class='r']//a"
                )
        print(f"Click on {h_elem.get_attribute('innerHTML')}")
        print(a_elem.get_attribute("href"))
        try:
            a_elem.send_keys(Keys.CONTROL + Keys.RETURN)
        except Exception as e:
            print("click fail... skip to next")
            print(e)
            continue
        time.sleep(1)
        wait_until_loaded(driver, 300)

    print("=" * 60)

command_sequence.run_custom_function(search_and_visit, (query, number_of_clicks))

# Run commands across the browsers
for i in range(len(manager.browsers)):
    manager.execute_command_sequence(command_sequence, i)

manager.close()
