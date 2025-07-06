from pages.base_page import BasePage

class AdminPage(BasePage):
    ADMIN_HEADER = "div.oxd-topbar-header"

    def verify_admin_page_loaded(self):
        self.assert_element_present(self.ADMIN_HEADER)