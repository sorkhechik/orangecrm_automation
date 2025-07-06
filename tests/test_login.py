import pytest
from pages.login_page import LoginPage
from tests.base_test import BaseTest

class TestLogin(BaseTest):
    # def _handle_exception(self, test_name, exception):
    #     """متد مشترک برای مدیریت استثناها و ذخیره اسکرین‌شات/منبع صفحه."""
    #     self.logger.error(f"Test failed: {str(exception)}")
    #     self.save_page_source(f"{test_name}_error")
    #     self.take_screenshot(f"{test_name}_error")
    #     raise

    # @pytest.mark.parametrize("login_module", ["Admin", "TestUser"], indirect=True)
    # def test_successful_login_module(self, login_module):
    #     test_name = "test_successful_login_module"
    #     try:
    #         self.assert_element_present("h6.oxd-text.oxd-text--h6", timeout=30)
    #         self.take_screenshot(test_name)
    #     except Exception as e:
    #         self._handle_exception(test_name, e)

    # @pytest.mark.parametrize("login_function", ["Admin", "TestUser"], indirect=True)
    # def test_successful_login_function(self, login_function):
    #     test_name = "test_successful_login_function"
    #     try:
    #         self.assert_element_present("h6.oxd-text.oxd-text--h6", timeout=30)
    #         self.take_screenshot(test_name)
    #     except Exception as e:
    #         self._handle_exception(test_name, e)


    def test_failed_login(self, login_function):
        test_name = "test_failed_login"
        login_page = LoginPage(self)
        try:
            login_page.login("InvalidUser", "wrongpass", test_name=test_name)
            error_message = login_page.get_error_message(test_name=test_name)
            assert error_message == "Invalid credentials", f"Expected 'Invalid credentials', got {error_message}"
            self.take_screenshot(test_name)
        except Exception as e:
            self._handle_exception(test_name, e)


    def test_open_login_page(self):
        test_name = "test_open_login_page"
        try:
            self.logger.info("Opening login page")
            self.open("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
            self.wait_for_element_visible("input[name='username']", timeout=30)
            self.save_page_source(test_name)
            self.take_screenshot(test_name)
            assert self.is_element_visible("input[name='username']")
            login_page = LoginPage(self)
            self.logger.info("Attempting login with Admin/admin123")
            login_page.login("Admin", "admin123", test_name=test_name)
            self.wait_for_element_present("h6.oxd-text.oxd-text--h6", timeout=30)
            self.save_page_source(f"{test_name}_attempt")
            self.take_screenshot(f"{test_name}_attempt")
            assert self.is_element_visible("h6.oxd-text.oxd-text--h6")
        except Exception as e:
            self._handle_exception(test_name, e)