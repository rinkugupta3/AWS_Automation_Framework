# Moving the code related to "MacBook" and "iPhone" into separate functions or modules
# and then call those functions in your pytest test file.
# This will make the code cleaner and more modular.
# Head mode is set to True and (Headless=false) test will run only at Chromium.
# Head mode will open Chrome browser and run test

# pytest -s -v interactive_tests/test_head_user_input_apple_search_module.py
# pytest -s -v interactive_tests/test_head_user_input_apple_search_module.py --html=report.html
# For report install pip install pytest-html

import logging
import os
import sys

import pytest
from playwright.sync_api import Page, Playwright
from pytest_bdd import scenarios, given, then, when
from config.config import Config
from modules.macbook_actions import handle_macbook  # Import MacBook actions
from modules.iphone_actions import handle_iphone  # Import iPhone actions

# Set up logging
log_file = '../test_results.txt'
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

scenarios('../features/apple_search.feature')

# Ensure the screenshots directory exists
if not os.path.exists('../screenshots'):
    os.makedirs('../screenshots')


@pytest.fixture(scope="session")
def browser_setup(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    # Headless mode is set to True and test will run across multiple browsers (Chromium, Firefox, WebKit)
    # browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    yield page
    context.close()
    browser.close()


# Global variable to track attempts
attempts_remaining = 3
@pytest.fixture(scope="session")
def product_to_search():
    global attempts_remaining  # Use the global attempts variable

    while attempts_remaining > 0:
        user_input = input(
            "Enter the product name you want to search (e.g., 'MacBook Pro' or 'iPhone 16 Pro Max'): ").strip()
        matching_products = [product for product in Config.PRODUCT_NAME if user_input.lower() in product.lower()]

        if matching_products:
            return matching_products[0]
        else:
            attempts_remaining -= 1  # Decrease attempts remaining
            print(f"Product '{user_input}' not found in the config. Please try again.")
            print(f"Attempts remaining: {attempts_remaining}")

    # If the user fails after the allowed attempts
    print("Too many invalid attempts. Exiting the test.")
    sys.exit(1)  # Exit the program with a non-zero status


@given("I am on the Apple homepage")
def visit_apple_com(browser_setup: Page):
    page = browser_setup
    page.goto("https://www.apple.com/")
    page.wait_for_load_state("networkidle")
    page.screenshot(path='../screenshots/homepage.png')
    logger.info("Visited Apple homepage")


@when("I search for the product")
def search_for_product(browser_setup: Page, product_to_search):
    product = product_to_search
    logger.info(f"Searching for {product}")

    page = browser_setup
    page.wait_for_load_state("networkidle")
    search_button = page.get_by_role("button", name="Search apple.com")
    search_button.click()
    search_input = page.get_by_placeholder("Search apple.com")
    search_input.fill(product)
    search_input.press("Enter")
    page.wait_for_selector('text="Search Results"', timeout=10000)
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f'screenshots/search_results_for_{product}.png')

    if "MacBook Pro" in product:
        product_name = "MacBook Pro - Apple"
    elif "iPhone" in product:
        product_name = "iPhone 16 Pro and iPhone 16 Pro Max - Apple"
    else:
        raise ValueError(f"Product '{product}' is not handled in the script.")

    page.get_by_role("link", name=product_name, exact=True).click()
    page.wait_for_timeout(5000)


@when("I add the first product result to the bag")
def add_product_to_bag(browser_setup: Page, product_to_search):
    page = browser_setup
    product = product_to_search

    if "MacBook Pro" in product:
        handle_macbook(page)  # Call the function for MacBook
    elif "iPhone 16 Pro Max" in product:
        handle_iphone(page)  # Call the function for iPhone
    else:
        raise ValueError(f"Product '{product}' not handled by the script.")


@then("I should be able to proceed to the review bag")
def proceed_to_review_bag(browser_setup: Page):
    page = browser_setup
    review_bag_button = page.get_by_role("button", name="Review Bag")
    review_bag_button.wait_for(state="visible", timeout=5000)
    review_bag_button.click()
    page.wait_for_load_state("networkidle")


@then("a screenshot of the reviewed product should be taken")
def take_screenshot_of_review(browser_setup: Page):
    page = browser_setup
    page.wait_for_load_state("networkidle")
    page.screenshot(path='../screenshots/reviewed_product.png')
    logger.info("Screenshot of the reviewed product taken.")


# Scenario: Delete product or item from the bag
@then("the product should be removed or deleted from the bag")
def remove_product_from_bag(browser_setup: Page):
    page = browser_setup
    # remove_button = page.get_by_role("button", name="Remove iPhone 16 Pro 128GB")
    remove_button = page.locator('[data-autom="bag-item-remove-button"]')
    remove_button.wait_for(state="visible", timeout=5000)
    remove_button.click()


@then("I close the browser")
def close_browser(browser_setup: Page):
    logger.info("Closing the browser.")
    # The browser will be closed automatically by the fixture
