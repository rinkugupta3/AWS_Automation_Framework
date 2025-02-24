import pytest
from playwright.sync_api import sync_playwright

# Fixture to set up Playwright and browser context
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for headless mode
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

# Optional: You can add more fixtures or configuration here if needed
