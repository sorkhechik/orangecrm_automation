from pages.base_page import BasePage

class DashboardPage(BasePage):
    DASHBOARD_HEADER = "h6.oxd-text--h6"
    USER_DROPDOWN = "span.oxd-userdropdown"

    def verify_dashboard_loaded(self):
        self.wait_for_element(self.DASHBOARD_HEADER)
        self.assert_element_present(self.DASHBOARD_HEADER)