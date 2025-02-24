# iphone_actions.py
# Moving the code related to "MacBook" and "iPhone" into separate functions or modules
# and then call those functions in your pytest test file.
# This will make the code cleaner and more modular.

import logging

logger = logging.getLogger()


def handle_iphone(page):
    """Handle actions related to iPhone 16 Pro."""
    logger.info("Handling iPhone 16 Pro Max actions.")
    """Click iphone buy button"""
    page.wait_for_timeout(10000)
    page.get_by_role('link', name='Buy iPhone 16 Pro').nth(2).click(timeout=120000)

    # page.locator("section").filter(has_text="iPhone 16 Pro Hello, Apple").get_by_label("Buy iPhone 16 Pro").click()
    # page.locator("section:has-text('iPhone 16 Pro Hello, Apple')").locator('a[aria-label="Buy iPhone 16 Pro"]')\
    #    .nth(0).click(timeout=60000)

    page.get_by_text('iPhone 16 Pro 6.3-inch').click()
    page.get_by_role('listitem').filter(has_text='Desert Titanium').locator('img').click()
    page.locator('#root span').filter(has_text='256GB Footnote ²').nth(1).click()
    page.get_by_role('radio', name='No trade-in').check()
    page.get_by_role('radio', name='Buy $1,099.00 Pay with Apple').check()
    page.get_by_role('radio', name='Buy $1,099.00 Pay with Apple').check()
    page.get_by_role('radio', name='Connect to any carrier later $').check()
    page.get_by_role('radio', name='No AppleCare+ coverage').check()

    page.get_by_role("button", name="Add to Bag").click()
    page.wait_for_timeout(5000)
    page.screenshot(path='screenshots/iPhone 16 Pro Max.png')
    logger.info("Screenshot of iPhone 16 Pro Max taken.")
