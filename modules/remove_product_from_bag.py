from playwright.sync_api import Page, Playwright


def handle_remove_product(browser_setup: Page, product_name: str):
    page = browser_setup

    # remove_button = page.locator('[data-autom="bag-item-remove-button"]')

    # bag or cart item that matches the product name with variable "{product_name}"
    remove_button = page.locator(f'[data-autom="bag-item-remove-button"]:has-text("{product_name}")')

    remove_button.wait_for(state="visible", timeout=5000)
    remove_button.click()