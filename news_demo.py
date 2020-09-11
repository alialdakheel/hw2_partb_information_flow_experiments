
from automation import CommandSequence, TaskManager
import tempfile
import time
import os
import copy
import json
import logging
from pprint import pprint

NUM_BROWSERS = 1
news_site = "https://news.google.com"

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    # browser_params[i]['http_instrument'] = True
    # Record cookie changes
    # browser_params[i]['cookie_instrument'] = True
    # Record Navigations
    browser_params[i]['navigation_instrument'] = True
    # Record JS Web API calls
    # browser_params[i]['js_instrument'] = True
    # Record the callstack of all WebRequests made
    # browser_params[i]['callstack_instrument'] = True
    # Launch headless
    browser_params[i]['display_mode'] = 'headless'

# Update TaskManager configuration (use this for crawl-wide settings)
cwd = os.getcwd()
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

# Parallelize sites over all number of browsers set above.
command_sequence = CommandSequence.CommandSequence(
    news_site, reset=True,
    callback=lambda success, val=news_site:
    print("CommandSequence {} done".format(val)))

command_sequence.get(sleep=3, timeout=60)
command_sequence.dump_page_source("_".join(news_site.split('.')[-2:]))

def get_news_headline(**kwargs):
    driver = kwargs['driver']
    a_elem_news = driver.find_elements_by_xpath("//article[1]//h3//a")
    headlines = [a_elem.get_attribute("innerHTML") for a_elem in a_elem_news]
    pprint(headlines)

command_sequence.run_custom_function(get_news_headline)

# Run commands across the three browsers (simple parallelization)
manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
