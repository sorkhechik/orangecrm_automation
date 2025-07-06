import os
import pytest
from pytest_html import extras
from markupsafe import Markup
import logging
from seleniumbase import BaseCase
from pages.login_page import LoginPage
import yaml

# بارگذاری داده‌ها از فایل YAML
def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# خواندن رمز عبور از فایل YAML
class DataReader:
    @staticmethod
    def get_password_by_username(file_path, username):
        data = load_yaml(file_path)
        for user in data.get('users', []):
            if user.get('username') == username:
                return user.get('password', 'admin123')
        return 'admin123'

# تنظیم لاگینگ یکپارچه
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s',  # فرمت یکسان
    handlers=[logging.StreamHandler()]  # خروجی به کنسول
)
logger = logging.getLogger(__name__)

def pytest_configure(config):
    logger.debug("pytest_configure called")
    os.makedirs("screenshots", exist_ok=True)

@pytest.fixture(scope="function")
def login_function(browser, request):
    username = getattr(request, "param", "Admin")
    password = DataReader.get_password_by_username("data/login_data.yaml", username)
    logger.info(f"Logging in with username: {username}")
    login_page = LoginPage(browser)
    try:
        login_page.login(username, password)
        logger.info("Waiting for dashboard to load")
        login_page.wait_for_element("h6.oxd-text.oxd-text--h6", timeout=30)
        test_name = request.node.name
        browser.save_screenshot(f"screenshots/{test_name}_dashboard_loaded.png")
        login_page.save_page_source(f"{test_name}_dashboard_loaded")
        logger.info("Login successful")
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        test_name = request.node.name
        browser.save_screenshot(f"screenshots/{test_name}_login_failed.png")
        login_page.save_page_source(f"{test_name}_login_failed")
        raise
    return browser

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    logger.debug("pytest_runtest_makereport called")
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and hasattr(report, 'extra'):
        test_name = item.name
        screenshot_path = None
        if report.outcome == "failed":
            screenshot_path = f"screenshots/{test_name}_login_failed.png"
        elif report.outcome == "passed":
            screenshot_path = f"screenshots/{test_name}_dashboard_loaded.png"
        if screenshot_path and os.path.exists(screenshot_path):
            try:
                with open(screenshot_path, "rb") as f:
                    report.extra.append(extras.image(f.read(), mime_type="image/png"))
                logger.info(f"Image added to extra: {screenshot_path}")
            except Exception as e:
                report.extra.append(extras.text(f"خطا در بارگذاری تصویر: {str(e)}", name="خطا"))
                logger.error(f"Error loading image: {str(e)}")
        elif screenshot_path:
            report.extra.append(extras.text(f"اسکرین‌شات {screenshot_path} یافت نشد.", name="خطا"))
            logger.warning(f"Screenshot not found: {screenshot_path}")

def pytest_html_results_table_header(cells):
    logger.debug("pytest_html_results_table_header called")
    cells.insert(2, Markup("<th>اسکرین‌شات</th>"))

def pytest_html_results_table_row(report, cells):
    logger.debug("pytest_html_results_table_row called")
    if report.when == "call":
        test_name = report.nodeid.split("::")[-1]
        screenshot_path = f"screenshots/{test_name}_login_failed.png" if report.outcome == "failed" else f"screenshots/{test_name}_dashboard_loaded.png"
        if os.path.exists(screenshot_path):
            cells.insert(2, Markup(f'<td><a href="file:///{os.path.abspath(screenshot_path)}">مشاهده تصویر</a></td>'))
        else:
            cells.insert(2, Markup("<td>تصویر موجود نیست</td>"))