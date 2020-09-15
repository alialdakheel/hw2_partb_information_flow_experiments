import os
import sys
from automation import CommandSequence, TaskManager
from automation.Commands.utils.webdriver_utils import wait_until_loaded

import time
import logging
from pprint import pprint

NUM_BROWSERS = 1
site = "https://www.google.com"
query = "whos fas"
number_of_results = 6

# Loads the default manager params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

for i in range(NUM_BROWSERS):
    # Record Navigations
    browser_params[i]['navigation_instrument'] = True
    # Launch headless
    # browser_params[i]['display_mode'] = 'headless'

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

def search(query, n, **kwargs):
    driver = kwargs['driver']
    input_elem = driver.find_element_by_name("q")
    print(f"searching: {query}  ...")
    input_elem.send_keys(query)
    input_elem.submit();
    time.sleep(1)
    wait_until_loaded(driver, 300)
    g_elems = driver.find_elements_by_xpath("//div[@class='r']//h3")

    results = [g_elem.get_attribute("innerHTML") for g_elem in g_elems]
    pprint(results[:n])
    print("=" * 60)

command_sequence.run_custom_function(search, (query, number_of_results))

# Run commands across the browsers
for i in range(len(manager.browsers)):
    manager.execute_command_sequence(command_sequence, i)

manager.close()
