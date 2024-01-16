import os
import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from demo_shop_tests.utils import attach


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture
def base_url():
    return 'https://demowebshop.tricentis.com'


@pytest.fixture(scope='function')
def browser_setup(request):
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')
    remote_driver_url = os.getenv('REMOTE_DRIVER_URL')
    driver = webdriver.Remote(command_executor=f"https://{login}:{password}@{remote_driver_url}",
                              options=options)
    browser.config.driver = driver
    browser.config.base_url = 'https://demowebshop.tricentis.com'
    browser.config.window_height = 1920
    browser.config.window_width = 1080

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()

